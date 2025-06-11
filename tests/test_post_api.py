"""Модуль для тестирования API-эндпоинтов для Post."""

import pytest
from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Post, User


@pytest.mark.asyncio
async def test_get_posts(client):
    """Тест получения всех постов пользователей."""
    response = client.get("/posts/")
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_create_post(
        client: TestClient, session: AsyncSession, test_user: User
):
    """Тест создания поста пользователя."""
    post_data = {
        "user_id": test_user.id,
        "title": "Новый пост",
        "content": "Новый топовый контент"
    }
    response = client.post(
        "/posts/",
        json=post_data
    )
    assert response.status_code == status.HTTP_201_CREATED
    response_data = response.json()
    assert response_data["user_id"] == post_data["user_id"]
    assert response_data["title"] == post_data["title"]
    assert response_data["content"] == post_data["content"]
    assert "id" in response_data
    db_post = await session.get(Post, response_data["id"])
    assert db_post is not None
    assert db_post.user_id == post_data["user_id"]
    assert db_post.title == post_data["title"]
    assert db_post.content == post_data["content"]
