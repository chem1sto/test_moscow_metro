"""Модуль для работы с эндпоинтами постов пользователей."""

from fastapi import APIRouter, HTTPException, status

from app.db.models import Post, User
from app.db.session import SessionDep
from app.schemas.post import PostCreate, PostRead

post_router = APIRouter()


@post_router.post(
    "/",
    summary="Создать новый пост",
    response_model=PostRead,
    response_description="Созданный пост",
    status_code=status.HTTP_201_CREATED,
)
async def create_post(
    post: PostCreate,
    session: SessionDep,
):
    """Создаёт новый пост от имени пользователя."""
    user = await session.get(User, post.user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден",
        )
    post = Post.model_validate(post)
    session.add(post)
    await session.commit()
    await session.refresh(post)
    return post
