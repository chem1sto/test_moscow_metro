"""Модуль для настройки Pydantic-схем моделей данных Post."""

from pydantic import Field
from sqlmodel import SQLModel


class PostCreate(SQLModel):
    user_id: int = Field(..., description="Автор поста", examples=[1])
    title: str | None = Field(
        ...,
        min_length=1,
        description="Название поста",
        examples=["Заголовок 1"],
    )
    content: str | None = Field(
        ...,
        min_length=1,
        description="Содержание поста",
        examples=["Топовый контент"],
    )


class PostRead(SQLModel):
    id: int
    user_id: int
    title: str | None
    content: str | None
