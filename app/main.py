"""Создание и запуск веб-приложения."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api.routing import main_router
from app.core.config import settings
from app.core.constants import UPLOAD_DIR
from app.db.init_db import create_db_and_tables


@asynccontextmanager
async def lifespan(current_app: FastAPI):
    await create_db_and_tables()
    yield


app = FastAPI(
    title=settings.APP_TITLE,
    description=settings.APP_DESCRIPTION,
    lifespan=lifespan
)
app.include_router(main_router)
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
app.mount("/static", StaticFiles(directory=UPLOAD_DIR), name="static")
