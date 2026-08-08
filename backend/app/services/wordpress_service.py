import base64
from pathlib import Path

import httpx

from app.core.config import settings


def _auth_header() -> dict:
    credentials = f"{settings.wordpress_username}:{settings.wordpress_application_password}"
    token = base64.b64encode(credentials.encode()).decode()
    return {"Authorization": f"Basic {token}"}


def upload_media(file_path: str, filename: str) -> int | None:
    """Uploads a local image file to WordPress Media Library. Returns the WP media ID."""
    full_path = Path(file_path)
    if not full_path.exists():
        return None

    content_type = "image/jpeg"
    if filename.lower().endswith(".png"):
        content_type = "image/png"
    elif filename.lower().endswith(".webp"):
        content_type = "image/webp"

    headers = {
        **_auth_header(),
        "Content-Disposition": f'attachment; filename="{filename}"',
        "Content-Type": content_type,
    }

    with open(full_path, "rb") as f:
        response = httpx.post(
            f"{settings.wordpress_url}/wp-json/wp/v2/media",
            headers=headers,
            content=f.read(),
            timeout=30,
        )

    if response.status_code not in (200, 201):
        raise ValueError(f"WordPress media upload failed: {response.status_code} — {response.text[:300]}")

    return response.json()["id"]


def create_post(
    title: str,
    content: str,
    status: str = "draft",
    featured_media_id: int | None = None,
    excerpt: str | None = None,
) -> dict:
    """Creates a post on WordPress. Returns the created post's data (id, link, etc)."""
    payload = {
        "title": title,
        "content": content,
        "status": status,  # "draft" or "publish"
    }
    if featured_media_id:
        payload["featured_media"] = featured_media_id
    if excerpt:
        payload["excerpt"] = excerpt

    response = httpx.post(
        f"{settings.wordpress_url}/wp-json/wp/v2/posts",
        headers=_auth_header(),
        json=payload,
        timeout=30,
    )

    if response.status_code not in (200, 201):
        raise ValueError(f"WordPress post creation failed: {response.status_code} — {response.text[:300]}")

    return response.json()
