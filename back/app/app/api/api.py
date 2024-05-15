from fastapi import APIRouter

from app.api.endpoints.auth import router as auth_router
from app.api.endpoints.register import router as register_router

api_router = APIRouter()
api_router.include_router(
    register_router,
    prefix="",
    tags=["Регистрация"],
)

api_router.include_router(
    auth_router,
    prefix="/jwt",
    tags=["Авторизация"],
)
