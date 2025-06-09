"""Модуль для работы с эндпоинтами пользователей."""

from fastapi import APIRouter, HTTPException, status
from sqlmodel import select

from app.db.models import User
from app.db.session import SessionDep
from app.schemas.user import UserCreate, UserRead

user_router = APIRouter()


@user_router.post(
    "/",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
    summary="Создать нового пользователя",
    response_description="Созданный пользователь"
)
async def create_new_user(
    session: SessionDep,
    user: UserCreate,
):
    """Создаёт нового пользователя."""
    existing_user = await session.exec(
        select(User).where(User.email == user.email)
    ).first()
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail=(
                "Электронная почта уже используется для другого пользователя"
            )
        )
    user = User(**user.dict())
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user
