"""Модуль для настройки Pydantic-схем моделей данных User."""

from pydantic import EmailStr, Field
from sqlmodel import SQLModel


class UserCreate(SQLModel):
    """Схема для создания пользователя."""

    first_name: str | None = Field(
        None, min_length=1, description="Имя", examples=["Иван"]
    )
    second_name: str | None = Field(
        None, min_length=1, description="Фамилия", examples=["Иванов"]
    )
    patronymic: str | None = Field(
        None, min_length=1, description="Отчество", examples=["Иванович"]
    )
    email: EmailStr | None = Field(
        None, description="Электронная почта", examples=["ivan@example.ru"]
    )
    address: str | None = Field(
        None, description="Адрес", examples=["ул. Пушкина, д.10"]
    )
    photo_url: str | None = Field(
        None, examples=["http://127.0.0.1:8000/static/photo_user_1.jpg"]
    )


class UserRead(SQLModel):
    """Схема для чтения данных пользователя."""

    id: int = Field(..., description="ID", examples=[1])
    first_name: str | None = Field(
        None, min_length=1, description="Имя", examples=["Пётр"]
    )
    second_name: str | None = Field(
        None, min_length=1, description="Фамилия", examples=["Петров"]
    )
    patronymic: str | None = Field(
        None, min_length=1, description="Отчество", examples=["Петрович"]
    )
    email: EmailStr | None = Field(
        None, description="Электронная почта", examples=["peter@example.ru"]
    )
    address: str | None = Field(
        None, description="Адрес", examples=["ул. Лермонтова, д.20"]
    )
    photo_url: str | None = Field(
        None, examples=["http://127.0.0.1:8000/static/photo_user_2.jpg"]
    )


class UserUpdate(SQLModel):
    """Схема для обновления данных пользователя (PUT)."""

    first_name: str = Field(
        ..., min_length=1, description="Имя", examples=["Василий"]
    )
    second_name: str = Field(
        ..., min_length=1, description="Фамилия", examples=["Васильев"]
    )
    patronymic: str = Field(
        ..., min_length=1, description="Отчество", examples=["Васильевич"]
    )
    email: EmailStr = Field(
        ..., description="Электронная почта", examples=["vasiliy@example.ru"]
    )
    address: str = Field(
        ..., description="Адрес", examples=["ул. Гоголя, д.30"]
    )


class UserPartialUpdate(SQLModel):
    """Схема для частичного обновления данных пользователя (PATCH)."""

    first_name: str | None = Field(
        None, min_length=1, description="Имя", examples=["Дмитрий"]
    )
    second_name: str | None = Field(
        None, min_length=1, description="Фамилия", examples=["Дмитриев"]
    )
    patronymic: str | None = Field(
        None, min_length=1, description="Отчество", examples=["Дмитриевич"]
    )
    email: EmailStr | None = Field(
        None, description="Электронная почта", examples=["dmitriy@example.ru"]
    )
