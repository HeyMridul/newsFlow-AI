from sqlalchemy.orm import Session

from app.models.news import News
from app.schemas.news import NewsCreate


def create_news(db: Session, data: NewsCreate) -> News:
    news_item = News(**data.model_dump())
    db.add(news_item)
    db.commit()
    db.refresh(news_item)
    return news_item