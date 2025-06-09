"""Модуль для настройки движка и создания сессий для работы с БД."""

from app.db.session import async_engine
from sqlmodel import SQLModel


async def create_db_and_tables():
    """Асинхронное создание всех таблиц в БД."""
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
