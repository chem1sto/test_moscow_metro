"""Модуль для работы с эндпоинтами пользователей."""

from typing import Annotated

from fastapi import APIRouter, HTTPException, Query, status
from sqlmodel import select

from app.db.models import User
from app.db.session import SessionDep
from app.schemas.user import UserCreate, UserRead

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
    stmt = await session.execute(select(User).offset(offset).limit(limit))
    return stmt.scalars().all()


@user_router.get(
    "/{user_id}/",
    summary="Получить пользователя",
    response_model=UserRead,
    response_description="Выбранный пользователь",
    status_code=status.HTTP_200_OK,
)
async def get_user(user_id: int, session: SessionDep) -> User:
    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return user


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
