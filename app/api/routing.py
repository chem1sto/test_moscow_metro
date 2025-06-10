"""Модуль для настройки маршрутов веб-приложения."""

from fastapi import APIRouter

from app.api.endpoints.post import post_router
from app.api.endpoints.user import user_router
from app.api.endpoints.upload_photo import user_photo_router


main_router = APIRouter()

main_router.include_router(
    post_router,
    prefix="/posts",
    tags=["Посты"],
)
main_router.include_router(
    user_router,
    prefix="/users",
    tags=["Пользователи"],
)
main_router.include_router(
    user_photo_router,
    prefix="/users_photo",
    tags=["Фото пользователей"],
)
