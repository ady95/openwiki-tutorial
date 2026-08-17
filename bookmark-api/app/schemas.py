# -*- coding: utf-8 -*-
"""Pydantic 요청·응답 스키마."""
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class TagOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str


class BookmarkCreate(BaseModel):
    url: str = Field(..., max_length=2048)
    title: str = Field(..., max_length=512)
    memo: str = ""
    tags: list[str] = []  # 태그 이름 목록 — 없으면 자동 생성된다


class BookmarkUpdate(BaseModel):
    title: str | None = None
    memo: str | None = None
    tags: list[str] | None = None


class BookmarkOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    url: str
    title: str
    memo: str
    archived_at: datetime | None
    created_at: datetime
    tags: list[TagOut]
