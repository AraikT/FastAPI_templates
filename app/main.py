from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from app.api.routers import main_router
from app.core.docs.docs import get_custom_docs
from app.core.middleware.cors import add_cors_middleware

app = FastAPI(
    default_response_class=ORJSONResponse,
    docs_url=None,
    redoc_url=None,
)

add_cors_middleware(app)
app.include_router(main_router)
get_custom_docs(app, docs_url='/docs')
