"""Модуль для работы с эндпоинтами по загрузке фото пользователей."""

from fastapi import UploadFile, File, APIRouter
import shutil
from app.core.constants import UPLOAD_DIR

router = APIRouter()


@router.post("/users/{user_id}/photo")
async def upload_user_photo(
        user_id: int,
        file: UploadFile = File(...),
):
    file_location = UPLOAD_DIR / f"user_{user_id}_{file.filename}"
    with file_location.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    photo_url = f"/static/{file_location.name}"

    # Обновляем пользователя в БД (это нужно реализовать)
    # update_user_photo_url(user_id, photo_url)

    return {"photo_url": photo_url}
