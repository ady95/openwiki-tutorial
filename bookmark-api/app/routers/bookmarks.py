# -*- coding: utf-8 -*-
"""북마크 CRUD·검색 라우터."""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Bookmark
from app.schemas import BookmarkCreate, BookmarkOut, BookmarkUpdate
from app.services import bookmark_service

router = APIRouter()


@router.post("", response_model=BookmarkOut, status_code=201)
def create_bookmark(payload: BookmarkCreate, db: Session = Depends(get_db)):
    try:
        return bookmark_service.create_bookmark(
            db, payload.url, payload.title, payload.memo, payload.tags
        )
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.get("", response_model=list[BookmarkOut])
def list_bookmarks(
    include_archived: bool = Query(False, description="아카이브 포함 여부"),
    db: Session = Depends(get_db),
):
    query = db.query(Bookmark)
    if not include_archived:
        query = query.filter(Bookmark.archived_at.is_(None))
    return query.order_by(Bookmark.created_at.desc()).all()


@router.get("/search", response_model=list[BookmarkOut])
def search(q: str = Query(..., min_length=1), db: Session = Depends(get_db)):
    return bookmark_service.search_bookmarks(db, q)


@router.get("/{bookmark_id}", response_model=BookmarkOut)
def get_bookmark(bookmark_id: int, db: Session = Depends(get_db)):
    bookmark = db.get(Bookmark, bookmark_id)
    if bookmark is None:
        raise HTTPException(status_code=404, detail="북마크가 없습니다")
    return bookmark


@router.patch("/{bookmark_id}", response_model=BookmarkOut)
def update_bookmark(bookmark_id: int, payload: BookmarkUpdate, db: Session = Depends(get_db)):
    bookmark = db.get(Bookmark, bookmark_id)
    if bookmark is None:
        raise HTTPException(status_code=404, detail="북마크가 없습니다")
    if payload.title is not None:
        bookmark.title = payload.title.strip()
    if payload.memo is not None:
        bookmark.memo = payload.memo
    if payload.tags is not None:
        bookmark.tags = bookmark_service.get_or_create_tags(db, payload.tags)
    db.commit()
    db.refresh(bookmark)
    return bookmark


@router.post("/{bookmark_id}/archive", response_model=BookmarkOut)
def archive(bookmark_id: int, db: Session = Depends(get_db)):
    bookmark = db.get(Bookmark, bookmark_id)
    if bookmark is None:
        raise HTTPException(status_code=404, detail="북마크가 없습니다")
    return bookmark_service.archive_bookmark(db, bookmark)
