"""Модуль для создания и настройки моделей таблиц."""

from typing import List, Optional

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
    posts: List["Post"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"cascade": "all, delete"}
    )


class Post(SQLModel, table=True):
    """Модель поста пользователя."""

    id: Optional[int] = Field(default=None, primary_key=True)
    title: Optional[str] = Field(nullable=True)
    content: Optional[str] = Field(nullable=True)
    user_id: Optional[int] = Field(
        default=None, foreign_key="user.id", nullable=True
    )
    user: Optional[User] = Relationship(back_populates="posts")
