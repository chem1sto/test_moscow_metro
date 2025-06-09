"""Модуль для создания и настройки моделей."""

from typing import Optional

from sqlmodel import Field, Relationship, SQLModel


class User(SQLModel, table=True):
    """Модель пользователя."""
    id: Optional[int] = Field(default=None, primary_key=True)
    first_name: Optional[str] = Field(nullable=True)
    second_name: Optional[str] = Field(nullable=True)
    patronymic: Optional[str] = Field(nullable=True)
    email: Optional[str] = Field(nullable=True)
    address: Optional[str] = Field(nullable=True)
    photo_url: Optional[str] = Field(nullable=True)
    posts: list["Post"] = Relationship(back_populates="user")


class Post(SQLModel, table=True):
    """Модель поста."""
    id: Optional[int] = Field(default=None, primary_key=True)
    title: Optional[str] = Field(nullable=True)
    description: Optional[str] = Field(nullable=True)
    user_id: Optional[int] = Field(
        default=None,
        foreign_key="user.id",
        nullable=True
    )
    user: Optional[User] = Relationship(back_populates="posts")
