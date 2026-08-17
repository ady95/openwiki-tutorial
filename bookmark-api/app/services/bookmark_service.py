# -*- coding: utf-8 -*-
"""북마크 비즈니스 로직.

라우터는 HTTP 입출력만 다루고, 규칙(URL 정규화·중복 검사·아카이브)은
이 서비스 계층에 모은다.
"""
from datetime import datetime, timezone
from urllib.parse import urlparse, urlunparse

from sqlalchemy.orm import Session

from app.models import Bookmark, Tag


def normalize_url(url: str) -> str:
    """URL을 저장 전 정규화한다.

    - 스킴·호스트는 소문자로
    - 프래그먼트(#...)는 제거
    - 끝의 슬래시는 제거
    """
    parsed = urlparse(url.strip())
    if not parsed.scheme:
        parsed = urlparse("https://" + url.strip())
    normalized = parsed._replace(
        scheme=parsed.scheme.lower(),
        netloc=parsed.netloc.lower(),
        fragment="",
    )
    return urlunparse(normalized).rstrip("/")


def get_or_create_tags(db: Session, names: list[str]) -> list[Tag]:
    """태그 이름 목록을 Tag 객체 목록으로 바꾼다. 없는 태그는 만든다."""
    tags = []
    for raw in names:
        name = raw.strip().lower()
        if not name:
            continue
        tag = db.query(Tag).filter(Tag.name == name).first()
        if tag is None:
            tag = Tag(name=name)
            db.add(tag)
        tags.append(tag)
    return tags


def create_bookmark(db: Session, url: str, title: str, memo: str, tag_names: list[str]) -> Bookmark:
    """북마크를 생성한다. 정규화된 URL 기준으로 중복이면 ValueError."""
    normalized = normalize_url(url)
    exists = db.query(Bookmark).filter(Bookmark.url == normalized).first()
    if exists is not None:
        raise ValueError(f"이미 등록된 URL입니다: {normalized}")

    bookmark = Bookmark(
        url=normalized,
        title=title.strip(),
        memo=memo,
        tags=get_or_create_tags(db, tag_names),
    )
    db.add(bookmark)
    db.commit()
    db.refresh(bookmark)
    return bookmark


def archive_bookmark(db: Session, bookmark: Bookmark) -> Bookmark:
    """북마크를 아카이브한다 — 삭제 대신 보관 시각을 기록한다."""
    bookmark.archived_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(bookmark)
    return bookmark


def search_bookmarks(db: Session, keyword: str, include_archived: bool = False):
    """제목·메모에서 키워드를 검색한다."""
    query = db.query(Bookmark)
    if not include_archived:
        query = query.filter(Bookmark.archived_at.is_(None))
    like = f"%{keyword}%"
    return query.filter((Bookmark.title.like(like)) | (Bookmark.memo.like(like))).all()
