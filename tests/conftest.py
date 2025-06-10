"""Модуль для настройки конфигурации тестов."""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import (
    AsyncSession, async_sessionmaker, create_async_engine
)
from sqlmodel import SQLModel

from app.core.config import settings
from app.db.session import get_async_session
from app.main import app


@pytest.fixture
def client():
    """Фикстура для тестового клиента."""
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
async def session():
    """Фикстура для тестового движка и инициализации сессии для тестовой БД."""
    test_engine = create_async_engine(
        settings.TEST_DATABASE_URL,
        echo=True
    )
    async with test_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    async_session = async_sessionmaker(
        test_engine, expire_on_commit=False
    )
    async with async_session() as session:
        yield session
    await test_engine.dispose()


@pytest.fixture(autouse=True)
async def override_get_session(session: AsyncSession):
    """Переопределение зависимостей для тестов."""
    app.dependency_overrides[get_async_session] = lambda: session
    yield
    app.dependency_overrides.clear()
