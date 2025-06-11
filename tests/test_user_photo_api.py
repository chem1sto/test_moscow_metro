"""Модуль для тестирования API-эндпоинта для загрузки фото пользователей."""

import io
import os

import pytest
from fastapi import status
from fastapi.testclient import TestClient
from PIL import Image

from app.core.constants import UPLOAD_DIR
from app.db.models import User


@pytest.mark.asyncio
async def test_upload_user_photo(client: TestClient, test_user: User):
    """Тест загрузки фото для пользователя."""
    image = Image.new("RGB", (100, 100), color="red")
    image_bytes = io.BytesIO()
    image.save(image_bytes, format="JPEG")
    image_bytes.seek(0)
    photo_file = {"file": ("photo_test.jpg", image_bytes, "image/jpeg")}
    response = client.post(f"/users_photo/{test_user.id}/", files=photo_file)
    assert response.status_code == status.HTTP_201_CREATED
    response_data = response.json()
    assert "photo_url" in response_data
    assert response_data["photo_url"] is not None
    uploaded_files = list(UPLOAD_DIR.glob(f"photo_user_{test_user.id}*"))
    assert len(uploaded_files) == 1
    for file in uploaded_files:
        os.remove(file)


@pytest.mark.asyncio
async def test_upload_user_photo_invalid_user(client: TestClient):
    """Тест загрузки фото для несуществующего пользователя."""
    image = Image.new("RGB", (100, 100), color="red")
    image_bytes = io.BytesIO()
    image.save(image_bytes, format="PNG")
    image_bytes.seek(0)
    files = {"file": ("photo_test.jpg", image_bytes, "image/png")}
    response = client.post("/users_photo/100/", files=files)
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_upload_user_photo_invalid_file_type(
    client: TestClient, test_user: User
):
    """Тест загрузки файла недопустимого типа."""
    text_file = io.BytesIO(b"Text")
    photo_file = {"file": ("test.txt", text_file, "text/plain")}
    response = client.post(f"/users_photo/{test_user.id}/", files=photo_file)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Разрешены только файлы изображений" in response.json()["detail"]
