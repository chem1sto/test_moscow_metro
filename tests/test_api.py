"""Модуль для тестирования API-эндпоинтов."""

import pytest
from fastapi import status


@pytest.mark.asyncio
async def test_example_endpoint(client):
    response = client.get("/users/")
    assert response.status_code == status.HTTP_200_OK
