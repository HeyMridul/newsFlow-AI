from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.news import NewsCreate, NewsRead
from app.services.news_service import create_news_item

router = APIRouter()


@router.post("/news", response_model=NewsRead, status_code=201)
def create_news(data: NewsCreate, db: Session = Depends(get_db)):
    return create_news_item(db, data)