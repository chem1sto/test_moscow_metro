"""Модуль для настройки подключения к БД и создание сессий для работы с ней."""

from typing import Annotated

from fastapi import Depends
from sqlalchemy import Column, Integer
from sqlalchemy.ext.asyncio import (
    create_async_engine, async_sessionmaker, AsyncSession
)
from sqlalchemy.orm import declarative_base, declared_attr
from sqlmodel import SQLModel

from app.core.config import settings


class PreBase:
    @declared_attr
    def __tablename__(cls):
        """Присваивание названия таблицы в БД от имени класса."""
        return cls.__name__.lower()
    id = Column(Integer, primary_key=True)


Base = declarative_base(cls=PreBase)
async_engine = create_async_engine(
    settings.database_url, connect_args={"check_same_thread": False}
)


async def create_db_and_tables():
    """Асинхронное создание всех таблиц в БД."""
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_async_session():
    """Асинхронный генератор сессий."""
    async_session = async_sessionmaker(
        async_engine, autoflush=False, expire_on_commit=False
    )
    async with async_session() as session:
        yield session

SessionDep = Annotated[AsyncSession, Depends(get_async_session)]
