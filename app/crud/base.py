from typing import Optional, TypeVar

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import Base

PydanticSchema = TypeVar('PydanticSchema', bound=BaseModel)
SQLAlchemyModel = TypeVar('SQLAlchemyModel', bound=Base)  # type: ignore


class CRUDBase:

    def __init__(self, model):
        self.model = model

    async def get(
        self,
        obj_id: int,
        async_session: AsyncSession,
    ):
        db_obj = await async_session.execute(
            select(self.model).where(self.model.id == obj_id)
        )
        return db_obj.scalars().first()

    async def get_multi(
        self,
        async_session: AsyncSession,
        order_by=None,
        **filter_by,
    ):
        query = select(self.model).filter_by(**filter_by)
        if order_by:
            query = query.order_by(order_by)
        db_objs = await async_session.execute(query)
        return db_objs.scalars().unique().all()

    async def create(
        self,
        obj_in: PydanticSchema,
        async_session: AsyncSession,
        user_id: Optional[int] = None,
    ):
        obj_in_data = obj_in.model_dump()
        if user_id is not None:
            obj_in_data['user_id'] = user_id
        db_obj = self.model(**obj_in_data)
        async_session.add(db_obj)
        await async_session.commit()
        await async_session.refresh(db_obj)
        return db_obj

    async def update(
        self,
        db_obj: SQLAlchemyModel,
        obj_in: PydanticSchema,
        async_session: AsyncSession,
    ):
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.model_dump(exclude_unset=True)

        for field in update_data:
            if field in obj_data:
                setattr(db_obj, field, update_data[field])
        async_session.add(db_obj)
        await async_session.commit()
        await async_session.refresh(db_obj)
        return db_obj

    async def delete(
        self,
        db_obj: SQLAlchemyModel,
        async_session: AsyncSession,
    ):
        await async_session.delete(db_obj)
        await async_session.commit()
        return db_obj

    async def get_by_attribute(
        self,
        attr_name: str,
        attr_value: str,
        async_session: AsyncSession,
    ):
        if not hasattr(self.model, attr_name):
            raise AttributeError(
                f"Атрибут '{attr_name}' не существует в модели {self.model.__name__}"
            )

        try:
            attr = getattr(self.model, attr_name)
            db_obj = await async_session.execute(
                select(self.model).where(attr == attr_value)
            )
            return db_obj.scalars().first()
        except InvalidRequestError as e:
            raise ValueError(
                f"Невозможно выполнить запрос с атрибутом '{attr_name}': {str(e)}"
            )
