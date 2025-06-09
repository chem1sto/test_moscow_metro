"""Модуль для основных настроек веб-приложения."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Настройки веб-приложения."""
    app_title: str = "test_moscow_metro"
    app_description: str = (
        "Тестовое задание на позицию 'Python разработчик' для 'Московского "
        "метрополитена'"
    )
    database_url: str = "sqlite+aiosqlite:///../test_moscow_metro.db"


settings = Settings()
