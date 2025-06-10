"""Модуль для основных настроек веб-приложения."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Настройки веб-приложения."""
    APP_TITLE: str = "test_moscow_metro"
    APP_DESCRIPTION: str = (
        "Тестовое задание на позицию 'Python разработчик' для 'Московского "
        "метрополитена'"
    )
    DATABASE_URL: str = "sqlite+aiosqlite:///test_moscow_metro.db"
    TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


settings = Settings()
