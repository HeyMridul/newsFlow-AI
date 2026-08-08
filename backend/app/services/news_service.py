from pathlib import Path
import uuid
from sqlalchemy.orm import Session

from app.repositories.news_repository import create_news, get_news_list, get_news_by_id
from app.schemas.news import NewsCreate, NewsRead

from app.services.scraper_service import scrape_article
from app.services.ai_service import rewrite_article

from app.services.ocr_service import extract_text_from_image

from app.services.media_service import download_image, attach_media_to_news, save_uploaded_image
from app.services.wordpress_service import upload_media, create_post




def create_news_item(db: Session, data: NewsCreate) -> NewsRead:
    news_item = create_news(db, data)
    return NewsRead.model_validate(news_item)


def list_news_items(db: Session, skip: int = 0, limit: int = 20) -> list[NewsRead]:
    items = get_news_list(db, skip, limit)
    return [NewsRead.model_validate(item) for item in items]


def get_news_item(db: Session, news_id: uuid.UUID) -> NewsRead | None:
    item = get_news_by_id(db, news_id)
    if item is None:
        return None
    return NewsRead.model_validate(item)


def generate_news_from_url(db: Session, url: str) -> NewsRead:
    scraped = scrape_article(url)
    ai_result = rewrite_article(scraped["title"], scraped["text"])

    data = NewsCreate(
        headline=ai_result["headline"],
        summary=ai_result["summary"],
        article=ai_result["article"],
        category=ai_result["category"],
        tags=ai_result.get("tags"),
        source=url,
        language="en",
    )
    news_item = create_news(db, data)

    # Download and attach images found on the source page
    for i, image_url in enumerate(scraped.get("image_urls", [])):
        local_path = download_image(image_url)
        if local_path:
            attach_media_to_news(
                db, news_item.id, local_path,
                original_url=image_url,
                is_featured=(i == 0),  # first successfully-downloaded image becomes featured
            )

    db.refresh(news_item)
    return NewsRead.model_validate(news_item)

def generate_news_from_image(db: Session, image_bytes: bytes, filename: str) -> NewsRead:
    extracted_text = extract_text_from_image(image_bytes)

    # OCR doesn't give us a clean "title" like a webpage does — let AI infer one
    ai_result = rewrite_article(title="(extracted from image)", content=extracted_text)

    data = NewsCreate(
        headline=ai_result["headline"],
        summary=ai_result["summary"],
        article=ai_result["article"],
        category=ai_result["category"],
        tags=ai_result.get("tags"),
        source=f"uploaded image: {filename}",
        language="en",
    )
    news_item = create_news(db, data)

    # The uploaded image itself becomes the featured image for this article
    local_path = save_uploaded_image(image_bytes, filename)
    attach_media_to_news(db, news_item.id, local_path, is_featured=True)

    db.refresh(news_item)
    return NewsRead.model_validate(news_item)


def publish_news_to_wordpress(db: Session, news_id) -> NewsRead:
    from app.repositories.news_repository import get_news_by_id

    news_item = get_news_by_id(db, news_id)
    if news_item is None:
        raise ValueError("News item not found")

    featured_media_id = None
    for media in news_item.media:
        wp_media_id = upload_media(media.file_path, Path(media.file_path).name)
        if wp_media_id and media.is_featured:
            featured_media_id = wp_media_id

    wp_post = create_post(
        title=news_item.headline,
        content=news_item.article or "",
        status="draft",
        featured_media_id=featured_media_id,
        excerpt=news_item.summary,
    )

    news_item.wordpress_post_id = wp_post["id"]
    news_item.wordpress_url = wp_post.get("link")
    db.commit()
    db.refresh(news_item)

    return NewsRead.model_validate(news_item)