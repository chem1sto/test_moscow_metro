"""Модуль для работы с эндпоинтами по загрузке фото пользователей."""

import shutil
from pathlib import Path

from fastapi import APIRouter, File, HTTPException, Request, UploadFile, status
from sqlalchemy.exc import SQLAlchemyError

from app.core.constants import ALLOWED_IMAGE_TYPES
from app.core.constants import UPLOAD_DIR
from app.db.models import User
from app.db.session import SessionDep
from app.schemas.user import UserRead

user_photo_router = APIRouter()


@user_photo_router.post(
    "/{user_id}/",
    summary="Загрузить новое фото пользователя",
    response_model=UserRead,
    response_description="Обновленный пользователь с фото",
    status_code=status.HTTP_201_CREATED,
)
async def upload_user_photo(
        request: Request,
        user_id: int,
        session: SessionDep,
        file: UploadFile = File(...)
) -> User:
    if file.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Разрешены только файлы изображений JPEG, PNG, GIF, WEBP"
        )
    try:
        db_user = await session.get(User, user_id)
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Пользователь для загрузки фото не найден"
            )
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка при запросе к базе данных"
        )
    file_extension = Path(file.filename).suffix
    filename = f"photo_user_{user_id}{file_extension}"
    file_location = UPLOAD_DIR / filename
    try:
        with file_location.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        photo_url = str(request.url_for("static", path=filename))
        db_user.photo_url = photo_url
        session.add(db_user)
        await session.commit()
        await session.refresh(db_user)
        return db_user
    except IOError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при сохранении файла: {str(e)}"
        )
    finally:
        await file.close()
