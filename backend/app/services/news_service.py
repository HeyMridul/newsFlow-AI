from sqlalchemy.orm import Session

from app.repositories.news_repository import create_news
from app.schemas.news import NewsCreate, NewsRead


def create_news_item(db: Session, data: NewsCreate) -> NewsRead:
    news_item = create_news(db, data)
    return NewsRead.model_validate(news_item)