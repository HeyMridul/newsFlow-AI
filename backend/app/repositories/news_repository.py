import uuid
from sqlalchemy.orm import Session
from app.models.news import News
from app.schemas.news import NewsCreate


def create_news(db: Session, data: NewsCreate) -> News:
    news_item = News(**data.model_dump())
    db.add(news_item)
    db.commit()
    db.refresh(news_item)
    return news_item

def get_news_list(db: Session, skip: int = 0, limit: int = 20) -> list[News]:
    return (
        db.query(News)
        .order_by(News.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_news_by_id(db: Session, news_id: uuid.UUID) -> News | None:
    return db.query(News).filter(News.id == news_id).first()