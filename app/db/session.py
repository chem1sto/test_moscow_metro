"""Модуль для настройки движка и создания сессий для работы с БД."""

from typing import Annotated

from fastapi import Depends
from sqlalchemy import Column, Integer
from sqlalchemy.ext.asyncio import (
    AsyncSession, async_sessionmaker, create_async_engine
)
from sqlalchemy.orm import declarative_base, declared_attr

from app.core.config import settings


class PreBase:
    @declared_attr
    def __tablename__(cls):
        """Присваивание названия таблицы в БД от имени класса."""
        return cls.__name__.lower()
    id = Column(Integer, primary_key=True)


Base = declarative_base(cls=PreBase)
async_engine = create_async_engine(
    settings.DATABASE_URL, connect_args={"check_same_thread": False}
)


async def get_async_session():
    """Асинхронный генератор сессий."""
    async_session = async_sessionmaker(
        async_engine, autoflush=False, expire_on_commit=False
    )
    async with async_session() as session:
        yield session

SessionDep = Annotated[AsyncSession, Depends(get_async_session)]
