"""Модуль для тестирования API-эндпоинтов для User."""

import pytest
from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import User


@pytest.mark.asyncio
async def test_get_users(client):
    """Тест получения данных всех пользователей."""
    response = client.get("/users/")
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_get_user(
        client: TestClient, session: AsyncSession, test_user: User
):
    """Тест получения данных одного пользователя."""
    response = client.get(f"/users/{test_user.id}/")
    assert response.status_code == status.HTTP_200_OK
    user_data = response.json()
    assert user_data["id"] == test_user.id
    assert user_data["first_name"] == test_user.first_name
    assert user_data["second_name"] == test_user.second_name
    assert user_data["email"] == test_user.email
    response = client.get("/users/100/")
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_create_user(client: TestClient, session: AsyncSession):
    """Тест создания пользователя."""
    user_data = {
        "first_name": "Иван",
        "second_name": "Иванов",
        "email": "ivan@example.com"
    }
    response = client.post(
        "/users/",
        json=user_data
    )
    assert response.status_code == status.HTTP_201_CREATED
    response_data = response.json()
    assert response_data["first_name"] == user_data["first_name"]
    assert response_data["email"] == user_data["email"]
    assert "id" in response_data
    db_user = await session.get(User, response_data["id"])
    assert db_user is not None
    assert db_user.email == user_data["email"]


@pytest.mark.asyncio
async def test_create_user_validation_error(client: TestClient):
    """Тест валидации данных при создании пользователя."""
    invalid_data = {
        "email": "invalid-email"
    }
    response = client.post(
        "/users/",
        json=invalid_data
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_create_user_duplicate_email(client: TestClient):
    """Тест дублирования email при создании пользователя."""
    user_data = {
        "first_name": "Петр",
        "email": "peter@example.com"
    }
    response1 = client.post("/users/", json=user_data)
    assert response1.status_code == status.HTTP_201_CREATED
    response2 = client.post("/users/", json=user_data)
    assert response2.status_code == status.HTTP_400_BAD_REQUEST
    assert (
        "Электронная почта уже используется для другого пользователя"
        in response2.json()["detail"]
    )


@pytest.mark.asyncio
async def test_update_user(
        client: TestClient, session: AsyncSession, test_user: User
):
    """Тест обновления данных пользователя."""
    updated_user_data = {
        "first_name": "Василий",
        "second_name": "Васильев",
        "patronymic": "Васильевич",
        "email": "vasiliy@example.ru",
        "address": "ул. Гоголя, д.30",
        "photo_url": None
    }
    response = client.put(
        f"/users/{test_user.id}/",
        json=updated_user_data
    )
    assert response.status_code == status.HTTP_200_OK
    user_data = response.json()
    assert user_data["id"] == test_user.id
    assert user_data["first_name"] == updated_user_data["first_name"]
    assert user_data["second_name"] == updated_user_data["second_name"]
    assert user_data["patronymic"] == updated_user_data["patronymic"]
    assert user_data["email"] == updated_user_data["email"]
    assert user_data["address"] == updated_user_data["address"]
    assert user_data["photo_url"] == updated_user_data["photo_url"]
    await session.refresh(test_user)
    assert test_user.first_name == updated_user_data["first_name"]
    assert test_user.second_name == updated_user_data["second_name"]
    assert test_user.patronymic == updated_user_data["patronymic"]
    assert test_user.email == updated_user_data["email"]
    assert test_user.address == updated_user_data["address"]
    assert test_user.photo_url == updated_user_data["photo_url"]


@pytest.mark.asyncio
async def test_partial_update_user(
        client: TestClient, session: AsyncSession, test_user: User
):
    """Тест частичного обновления данных пользователя."""
    updated_user_data = {
        "first_name": "Дмитрий",
        "second_name": "Дмитриев",
        "patronymic": "Дмитриевич",
        "email": "dmitriy@example.ru",
    }
    response = client.patch(
        f"/users/{test_user.id}/",
        json=updated_user_data
    )
    assert response.status_code == status.HTTP_200_OK
    user_data = response.json()
    assert user_data["id"] == test_user.id
    assert user_data["first_name"] == updated_user_data["first_name"]
    assert user_data["second_name"] == updated_user_data["second_name"]
    assert user_data["patronymic"] == updated_user_data["patronymic"]
    assert user_data["email"] == updated_user_data["email"]
    await session.refresh(test_user)
    assert test_user.first_name == updated_user_data["first_name"]
    assert test_user.second_name == updated_user_data["second_name"]
    assert test_user.patronymic == updated_user_data["patronymic"]
    assert test_user.email == updated_user_data["email"]


@pytest.mark.asyncio
async def test_delete_user(
        client: TestClient, session: AsyncSession, test_user: User
):
    """Тест удаления пользователя."""
    response = client.delete(f"/users/{test_user.id}/")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not response.content
    deleted_user = await session.get(User, test_user.id)
    assert deleted_user is None
    response_for_nonexistent = client.delete(f"/users/{test_user.id}/")
    assert response_for_nonexistent.status_code == status.HTTP_404_NOT_FOUND
