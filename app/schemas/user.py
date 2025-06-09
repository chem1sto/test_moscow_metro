"""Модуль для настройки Pydantic-схем моделей данных User."""

from pydantic import EmailStr, Field
from sqlmodel import SQLModel


class UserCreate(SQLModel):
    first_name: str | None = Field(
        ..., min_length=1, description="Имя", examples=["Иван"]
    )
    second_name: str | None = Field(
        ..., min_length=1, description="Фамилия", examples=["Иванов"]
    )
    patronymic: str | None = Field(
        ..., min_length=1, description="Отчество", examples=["Иванович"]
    )
    email: EmailStr | None = Field(
        ..., description="Электронная почта", examples=["ivan@example.ru"]
    )
    address: str | None = Field(
        ..., description="Адрес", examples=["ул. Пушкина, д.10"]
    )
    photo_url: str | None = Field(
        None, examples=["http://127.0.0.1:8000/uploads/photo.jpg"]
    )


class UserRead(SQLModel):
    id: int
    first_name: str | None
    second_name: str | None
    patronymic: str | None
    email: EmailStr
    address: str | None
    photo_url: str | None
