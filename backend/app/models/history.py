import uuid
import json
from datetime import datetime, timezone
from typing import Optional, Dict, Any
from sqlalchemy import String, Integer, Text, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class HistoryItem(Base):
    __tablename__ = "history_items"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    topic: Mapped[str] = mapped_column(Text, nullable=False)
    post_type: Mapped[str] = mapped_column(String(50), default="Story", nullable=False)
    tone: Mapped[str] = mapped_column(String(50), default="Conversational", nullable=False)
    target_audience: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    language: Mapped[str] = mapped_column(String(20), default="English", nullable=False)
    writing_style: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    personal_context: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    key_points: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    length: Mapped[str] = mapped_column(String(20), default="Medium", nullable=False)

    post: Mapped[str] = mapped_column(Text, nullable=False)
    word_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    reading_time: Mapped[str] = mapped_column(String(30), default="1 min read", nullable=False)
    emoji_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    hashtag_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    action: Mapped[str] = mapped_column(String(50), default="generate", nullable=False)
    parent_id: Mapped[Optional[str]] = mapped_column(String(36), nullable=True)

    metadata_json: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, nullable=False)

    def to_dict(self) -> Dict[str, Any]:
        meta = {}
        if self.metadata_json:
            try:
                meta = json.loads(self.metadata_json)
            except Exception:
                meta = {}

        return {
            "id": self.id,
            "topic": self.topic,
            "post_type": self.post_type,
            "tone": self.tone,
            "target_audience": self.target_audience or "",
            "language": self.language,
            "writing_style": self.writing_style or "",
            "personal_context": self.personal_context or "",
            "key_points": self.key_points or "",
            "length": self.length,
            "post": self.post,
            "word_count": self.word_count,
            "reading_time": self.reading_time,
            "emoji_count": self.emoji_count,
            "hashtag_count": self.hashtag_count,
            "action": self.action,
            "parent_id": self.parent_id,
            "metadata": meta,
            "created_at": self.created_at.isoformat() if self.created_at else utc_now().isoformat()
        }
