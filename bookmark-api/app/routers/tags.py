# -*- coding: utf-8 -*-
"""태그 라우터 — 태그 목록과 태그별 북마크 조회."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Tag
from app.schemas import BookmarkOut, TagOut

router = APIRouter()


@router.get("", response_model=list[TagOut])
def list_tags(db: Session = Depends(get_db)):
    return db.query(Tag).order_by(Tag.name).all()


@router.get("/{tag_name}/bookmarks", response_model=list[BookmarkOut])
def bookmarks_by_tag(tag_name: str, db: Session = Depends(get_db)):
    tag = db.query(Tag).filter(Tag.name == tag_name.lower()).first()
    if tag is None:
        raise HTTPException(status_code=404, detail="태그가 없습니다")
    return [b for b in tag.bookmarks if b.archived_at is None]
