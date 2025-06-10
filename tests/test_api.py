"""Модуль для тестирования API-эндпоинтов."""

import pytest
from fastapi import status

from app.db.models import User


@pytest.mark.asyncio
async def test_create_user_success(client, session):
    """Тест успешного создания пользователя."""
    user_data = {
        "first_name": "Иван",
        "last_name": "Иванов",
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
async def test_create_user_validation_error(client):
    """Тест валидации данных."""
    invalid_data = {
        "email": "invalid-email"
    }
    response = client.post(
        "/users/",
        json=invalid_data
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_create_user_duplicate_email(client):
    """Тест дублирования email при создании пользователя."""
    user_data = {
        "first_name": "Петр",
        "email": "petr@example.com"
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
async def test_get_users_endpoint(client):
    response = client.get("/users/")
    assert response.status_code == status.HTTP_200_OK


# @pytest.mark.asyncio
# async def test_get_user_endpoint(client):
#     response = client.get("/user/")
#     assert response.status_code == status.HTTP_200_OK
