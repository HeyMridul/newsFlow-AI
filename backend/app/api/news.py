import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.news import NewsCreate, NewsRead
from app.services.news_service import create_news_item, list_news_items, get_news_item
from pydantic import BaseModel

router = APIRouter()


@router.post("/news", response_model=NewsRead, status_code=201)
def create_news(data: NewsCreate, db: Session = Depends(get_db)):
    return create_news_item(db, data)


@router.get("/news", response_model=list[NewsRead])
def list_news(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    return list_news_items(db, skip, limit)


@router.get("/news/{news_id}", response_model=NewsRead)
def get_news(news_id: uuid.UUID, db: Session = Depends(get_db)):
    item = get_news_item(db, news_id)
    if item is None:
        raise HTTPException(status_code=404, detail="News item not found")
    return item

class GenerateFromUrlRequest(BaseModel):
    url: str


@router.post("/news/generate-from-url", response_model=NewsRead, status_code=201)
def generate_from_url(payload: GenerateFromUrlRequest, db: Session = Depends(get_db)):
    from app.services.news_service import generate_news_from_url
    return generate_news_from_url(db, payload.url)

@router.post("/news/generate-from-url", response_model=NewsRead, status_code=201)
def generate_from_url(payload: GenerateFromUrlRequest, db: Session = Depends(get_db)):
    from app.services.news_service import generate_news_from_url
    try:
        return generate_news_from_url(db, payload.url)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")