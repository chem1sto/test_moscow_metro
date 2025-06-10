"""Модуль для констант, используемых в веб-приложении."""

from pathlib import Path

ALLOWED_IMAGE_TYPES = [
    "image/jpeg",
    "image/png",
    "image/gif",
    "image/webp",
]
UPLOAD_DIR = Path(__file__).parent.parent / "uploads"
