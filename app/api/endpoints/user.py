"""Модуль для работы с эндпоинтами пользователей."""

from typing import Annotated

from fastapi import APIRouter, HTTPException, Query, status
from sqlmodel import select

from app.db.models import User
from app.db.session import SessionDep
from app.schemas.user import (
    UserCreate,
    UserPartialUpdate,
    UserRead,
    UserUpdate,
)

user_router = APIRouter()


@user_router.get(
    "/",
    summary="Получить всех пользователей",
    response_model=list[UserRead],
    response_description="Список всех пользователей",
    status_code=status.HTTP_200_OK,
)
async def get_users(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[User]:
    db_users = await session.execute(select(User).offset(offset).limit(limit))
    return db_users.scalars().all()


@user_router.post(
    "/",
    summary="Создать нового пользователя",
    response_model=UserRead,
    response_description="Созданный пользователь",
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    user: UserCreate,
    session: SessionDep,
) -> User:
    """Создаёт нового пользователя."""
    stmt = await session.execute(select(User).where(User.email == user.email))
    existing_user = stmt.scalars().first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Электронная почта уже используется для другого пользователя"
            ),
        )
    user = User.model_validate(user)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


@user_router.get(
    "/{user_id}/",
    summary="Получить пользователя",
    response_model=UserRead,
    response_description="Выбранный пользователь",
    status_code=status.HTTP_200_OK,
)
async def get_user(user_id: int, session: SessionDep) -> User:
    db_user = await session.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return db_user


@user_router.put(
    "/{user_id}/",
    summary="Обновить данные пользователя",
    response_model=UserRead,
    response_description="Обновленный пользователь",
    status_code=status.HTTP_200_OK,
)
async def update_user(
    user_id: int,
    user: UserUpdate,
    session: SessionDep,
) -> User:
    """Полностью обновляет данные пользователя."""
    db_user = await session.get(User, user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь для обновления не найден",
        )
    update_user_data = user.model_dump()
    user.sqlmodel_update(update_user_data)
    for key, value in update_user_data.items():
        setattr(db_user, key, value)
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)
    return db_user


@user_router.patch(
    "/{user_id}/",
    summary="Частично обновить данные пользователя",
    response_model=UserRead,
    response_description="Частично обновленный пользователь",
    status_code=status.HTTP_200_OK,
)
async def partial_update_user(
    user_id: int,
    user: UserPartialUpdate,
    session: SessionDep,
) -> User:
    """Частично обновляет данные пользователя."""
    db_user = await session.get(User, user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь для обновления не найден",
        )
    update_data = user.model_dump(exclude_unset=True)
    if "email" in update_data:
        existing = await session.execute(
            select(User).where(User.email == update_data["email"])
        )
        if existing.scalars().first():
            raise HTTPException(
                status_code=400,
                detail="Email уже используется другим пользователем",
            )
    db_user.sqlmodel_update(update_data)
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)
    return db_user


@user_router.delete(
    "/{user_id}/",
    summary="Удалить пользователя",
    response_description="Пользователь удалён",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_user(user_id: int, session: SessionDep):
    """Удаляет пользователя."""
    db_user = await session.get(User, user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь для удаления не был найден",
        )
    await session.delete(db_user)
    await session.commit()
    return {"ok": True}
