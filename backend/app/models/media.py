import uuid
from datetime import datetime

from sqlalchemy import String, DateTime, Boolean, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from app.database.base import Base


class Media(Base):
    __tablename__ = "media"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    news_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("news.id", ondelete="CASCADE")
    )
    type: Mapped[str] = mapped_column(String(20), default="image")  # image, video (later)
    file_path: Mapped[str] = mapped_column(String(1000))  # local path or storage URL
    original_url: Mapped[str | None] = mapped_column(String(2000), nullable=True)
    caption: Mapped[str | None] = mapped_column(String(500), nullable=True)
    is_featured: Mapped[bool] = mapped_column(Boolean, default=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    news = relationship("News", back_populates="media")