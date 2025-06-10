"""Модуль для работы с эндпоинтами постов пользователей."""

from typing import Annotated

from fastapi import APIRouter, HTTPException, Query, status
from sqlmodel import select

from app.db.models import Post, User
from app.db.session import SessionDep
from app.schemas.post import (
    PostCreate, PostRead, PostUpdate, PostPartialUpdate
)

post_router = APIRouter()


@post_router.get(
    "/",
    summary="Получить все посты пользователей",
    response_model=list[PostRead],
    response_description="Список всех постов пользователей",
    status_code=status.HTTP_200_OK,
)
async def get_posts(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[Post]:
    db_posts = await session.execute(select(Post).offset(offset).limit(limit))
    return db_posts.scalars().all()


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


@post_router.put(
    "/{post_id}/",
    summary="Обновить данные поста пользователя",
    response_model=PostRead,
    response_description="Обновленный пост пользователя",
    status_code=status.HTTP_200_OK,
)
async def update_post(
    post_id: int,
    post: PostUpdate,
    session: SessionDep,
) -> Post:
    """Полностью обновляет данные поста пользователя."""
    db_post = await session.get(Post, post_id)
    if not db_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пост пользователя для обновления не найден",
        )
    post_data = post.model_dump()
    post.sqlmodel_update(post_data)
    session.add(db_post)
    await session.commit()
    await session.refresh(db_post)
    return db_post


@post_router.patch(
    "/{post_id}/",
    summary="Частично обновить данные поста пользователя",
    response_model=PostRead,
    response_description="Частично обновленный пост пользователя",
    status_code=status.HTTP_200_OK,
)
async def partial_update_post(
    post_id: int,
    post: PostPartialUpdate,
    session: SessionDep,
) -> Post:
    """Частично обновляет данные пользователя."""
    db_post = await session.get(Post, post_id)
    if not db_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пост пользователя для обновления не найден",
        )
    update_post_data = post.model_dump(exclude_unset=True)
    db_post.sqlmodel_update(update_post_data)
    session.add(db_post)
    await session.commit()
    await session.refresh(db_post)
    return db_post


@post_router.delete(
    "/{post_id}/",
    summary="Удалить пост пользователя",
    response_description="Пост пользователя удалён",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_post(post_id: int, session: SessionDep):
    """Удаляет пост пользователя."""
    db_post = await session.get(Post, post_id)
    if not db_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пост пользователя для обновления не найден",
        )
    await session.delete(db_post)
    await session.commit()
    return {"ok": True}
