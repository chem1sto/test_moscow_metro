"""Модуль для настройки Pydantic-схем моделей данных Post."""

from pydantic import Field
from sqlmodel import SQLModel


class PostCreate(SQLModel):
    """Схема для создания данных поста пользователя."""

    user_id: int = Field(..., description="Пользователь", examples=[1])
    title: str | None = Field(
        None,
        min_length=1,
        description="Первое название поста",
        examples=["Заголовок 1"],
    )
    content: str | None = Field(
        None,
        min_length=1,
        description="Содержание поста 1",
        examples=["Топовый контент"],
    )


class PostRead(SQLModel):
    """Схема для чтения данных поста пользователя."""

    id: int = Field(..., description="ID", examples=[2])
    user_id: int = Field(..., description="Автор поста", examples=[2])
    title: str | None = Field(
        None,
        min_length=1,
        description="Второе название поста",
        examples=["Заголовок 2"],
    )
    content: str | None = Field(
        None,
        min_length=1,
        description="Содержание поста 2",
        examples=["Ещё один топовый контент"],
    )


class PostUpdate(SQLModel):
    """Схема для обновления данных поста пользователя (PUT)."""

    user_id: int = Field(..., description="Другой автор поста", examples=[2])
    title: str | None = Field(
        ...,
        min_length=1,
        description="Третье название поста",
        examples=["Заголовок 3"],
    )
    content: str | None = Field(
        ...,
        min_length=1,
        description="Содержание поста 3",
        examples=["Ещё один топовый контент для обновления"],
    )


class PostPartialUpdate(SQLModel):
    """Схема для частичного обновления данных поста пользователя (PATCH)."""

    user_id: int = Field(..., description="Лучший автор поста", examples=[2])
    content: str | None = Field(
        ...,
        min_length=1,
        description="Содержание поста 4",
        examples=["Best of the best"],
    )
