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
    assert db_post.user_id == test_user.id
    assert db_post.title == post_data["title"]
    assert db_post.content == post_data["content"]


@pytest.mark.asyncio
async def test_create_post_missing_required_fields(client: TestClient):
    # Тест без user_id
    response = client.post("/posts/", json={
        "title": "Пост без пользователя",
        "content": "Контент"
    })
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.parametrize("user_id,expected_status", [
    (100, status.HTTP_404_NOT_FOUND),
    (-1, status.HTTP_404_NOT_FOUND),
])
@pytest.mark.asyncio
async def test_create_post_invalid_user_ids(
        client: TestClient, user_id: int, expected_status: status
):
    """Тест валидации данных с неправильным user_id при создании поста
    пользователя."""
    response = client.post(
        "/posts/",
        json={
            "user_id": user_id,
            "title": "Тестовый заголовок",
            "content": "Тестовый контент"
        }
    )
    assert response.status_code == expected_status
    assert "Пользователь не найден" in response.json()["detail"]


@pytest.mark.parametrize("user_id,expected_status", [
    (None, status.HTTP_422_UNPROCESSABLE_ENTITY),
    ("a", status.HTTP_422_UNPROCESSABLE_ENTITY)
])
@pytest.mark.asyncio
async def test_create_post_invalid_user_ids_type(
        client: TestClient, user_id: str | None, expected_status: status
):
    """Тест валидации данных с неправильным типом user_id при создании поста
    пользователя."""
    response = client.post(
        "/posts/",
        json={
            "user_id": user_id,
            "title": "Тестовый заголовок",
            "content": "Тестовый контент"
        }
    )
    assert response.status_code == expected_status


@pytest.mark.asyncio
async def test_update_post(
        client: TestClient,
        session: AsyncSession,
        test_user_post: Post,
):
    """Тест обновления данных поста пользователя."""
    updated_post_data = {
        "user_id": 1,
        "title": "Обновленный заголовок",
        "content": "Обновленный контент",
    }
    response = client.put(
        f"/posts/{test_user_post.id}/",
        json=updated_post_data
    )
    assert response.status_code == status.HTTP_200_OK
    user_post_data = response.json()
    assert user_post_data["id"] == test_user_post.id
    assert user_post_data["user_id"] == updated_post_data["user_id"]
    assert user_post_data["title"] == updated_post_data["title"]
    assert user_post_data["content"] == updated_post_data["content"]
    await session.refresh(test_user_post)
    assert test_user_post.user_id == updated_post_data["user_id"]
    assert test_user_post.title == updated_post_data["title"]
    assert test_user_post.content == updated_post_data["content"]


@pytest.mark.asyncio
async def test_partial_update_post(
        client: TestClient,
        session: AsyncSession,
        test_user_post: Post,
):
    """Тест частичного обновления данных поста пользователя."""
    updated_post_data = {
        "user_id": 1,
        "content": "Супер контент",
    }
    response = client.patch(
        f"/posts/{test_user_post.id}/",
        json=updated_post_data
    )
    assert response.status_code == status.HTTP_200_OK
    user_post_data = response.json()
    assert user_post_data["id"] == test_user_post.id
    assert user_post_data["user_id"] == updated_post_data["user_id"]
    assert user_post_data["content"] == updated_post_data["content"]
    await session.refresh(test_user_post)
    assert test_user_post.user_id == updated_post_data["user_id"]
    assert test_user_post.content == updated_post_data["content"]


@pytest.mark.asyncio
async def test_delete_post(
        client: TestClient, session: AsyncSession, test_user_post: Post
):
    """Тест удаления поста пользователя."""
    response = client.delete(f"/posts/{test_user_post.id}/")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not response.content
    deleted_user_post = await session.get(Post, test_user_post.id)
    assert deleted_user_post is None
    response_for_nonexistent = client.delete(f"/posts/{test_user_post.id}/")
    assert response_for_nonexistent.status_code == status.HTTP_404_NOT_FOUND
