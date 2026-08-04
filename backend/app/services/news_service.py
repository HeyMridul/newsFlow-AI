import uuid
from sqlalchemy.orm import Session

from app.repositories.news_repository import create_news, get_news_list, get_news_by_id
from app.schemas.news import NewsCreate, NewsRead

from app.services.scraper_service import scrape_article
from app.services.ai_service import rewrite_article



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
    return NewsRead.model_validate(news_item)