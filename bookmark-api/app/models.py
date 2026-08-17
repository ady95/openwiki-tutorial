# -*- coding: utf-8 -*-
"""SQLAlchemy 모델 — Bookmark와 Tag는 다대다 관계다."""
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Table, Text
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

# 북마크-태그 다대다 연결 테이블
bookmark_tags = Table(
    "bookmark_tags",
    Base.metadata,
    Column("bookmark_id", ForeignKey("bookmarks.id"), primary_key=True),
    Column("tag_id", ForeignKey("tags.id"), primary_key=True),
)


class Bookmark(Base):
    __tablename__ = "bookmarks"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String(2048), nullable=False, unique=True, index=True)
    title = Column(String(512), nullable=False)
    memo = Column(Text, default="")
    archived_at = Column(DateTime, nullable=True)  # None이면 활성 북마크
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    tags = relationship("Tag", secondary=bookmark_tags, back_populates="bookmarks")


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(64), nullable=False, unique=True, index=True)

    bookmarks = relationship("Bookmark", secondary=bookmark_tags, back_populates="tags")
