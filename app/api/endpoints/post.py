"""Модуль для работы с эндпоинтами постов пользователей."""

from fastapi import APIRouter

from app.db.models import Post
from app.db.session import SessionDep

post_router = APIRouter()


# @post_router.post("/", response_model=Post)
# async def create_new_post(
#     post: CharityProjectCreate,
#     session: SessionDep,
# ):
#     """Создаёт новый пост от имени пользователя."""
#     new_post = Post.model_validate(post)
#     session.add(new_post)
#     session.commit()
#     session.refresh(new_post)
#     return new_post
