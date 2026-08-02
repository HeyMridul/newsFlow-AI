import uuid
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class NewsCreate(BaseModel):
    headline: str
    summary: str | None = None
    article: str | None = None
    language: str = "en"
    source: str | None = None
    category: str | None = None


class NewsRead(BaseModel):
    id: uuid.UUID
    headline: str
    summary: str | None
    article: str | None
    status: str
    language: str
    source: str | None
    category: str | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)