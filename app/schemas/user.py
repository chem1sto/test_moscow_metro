"""Модуль для настройки Pydantic-схем для модели User."""

from pydantic import EmailStr, Field
from sqlmodel import SQLModel


class UserCreate(SQLModel):
    first_name: str = Field(
        ..., min_length=1, example="Иван", description="Имя"
    )
    second_name: str = Field(
        ..., min_length=1, example="Петров", description="Фамилия"
    )
    email: EmailStr = Field(
        ..., example="user@example.com", description="Электронная почта"
    )
    photo_url: str | None = Field(
        None, example="https://example.com/photo.jpg"
    )


class UserRead(SQLModel):
    id: int
    first_name: str
    second_name: str
    email: EmailStr
    photo_url: str | None
