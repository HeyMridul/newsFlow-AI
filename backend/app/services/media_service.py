import uuid
import os
from pathlib import Path

import httpx
from sqlalchemy.orm import Session

from app.models.media import Media

MEDIA_DIR = Path("media/uploads")
MEDIA_DIR.mkdir(parents=True, exist_ok=True)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    )
}


def download_image(url: str) -> str | None:
    try:
        response = httpx.get(url, timeout=10, follow_redirects=True, headers=HEADERS)
        response.raise_for_status()

        content_type = response.headers.get("content-type", "")
        if not content_type.startswith("image/"):
            return None

        # Skip tiny images — likely icons/tracking pixels, not real photos
        if len(response.content) < 5000:  # under ~5KB
            return None

        ext = content_type.split("/")[-1].split(";")[0]
        if ext not in ("jpeg", "jpg", "png", "webp", "gif"):
            ext = "jpg"

        filename = f"{uuid.uuid4()}.{ext}"
        filepath = MEDIA_DIR / filename
        filepath.write_bytes(response.content)

        return f"media/uploads/{filename}"
    except Exception:
        return None


def save_uploaded_image(image_bytes: bytes, original_filename: str) -> str:
    """Saves a directly-uploaded image (from the OCR flow) to local storage."""
    ext = Path(original_filename).suffix.lstrip(".") or "jpg"
    filename = f"{uuid.uuid4()}.{ext}"
    filepath = MEDIA_DIR / filename
    filepath.write_bytes(image_bytes)
    return f"media/uploads/{filename}"


def attach_media_to_news(
    db: Session, news_id, file_path: str, original_url: str | None = None,
    is_featured: bool = False,
) -> Media:
    media = Media(
        news_id=news_id,
        file_path=file_path,
        original_url=original_url,
        is_featured=is_featured,
    )
    db.add(media)
    db.commit()
    db.refresh(media)
    return media