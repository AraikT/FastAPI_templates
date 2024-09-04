from fastapi import APIRouter

router = APIRouter(prefix='', tags=['root'])


@router.get('/')
def read_root() -> bool:
    return True
