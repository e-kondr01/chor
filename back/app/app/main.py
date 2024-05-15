from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination

from app.api.api import api_router
from app.config import settings
from app.exceptions import (
    APIException,
    api_exception_handler,
    request_validation_exception_handler,
)

if settings.SENTRY_DSN:
    import sentry_sdk

    sentry_sdk.init(
        dsn=settings.SENTRY_DSN,
        traces_sample_rate=0,
    )


app = FastAPI(
    title="chor_app",
    openapi_url="/api/openapi.json",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

add_pagination(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")


app.add_exception_handler(APIException, api_exception_handler)
app.add_exception_handler(RequestValidationError, request_validation_exception_handler)
