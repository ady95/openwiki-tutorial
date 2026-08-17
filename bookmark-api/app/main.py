# -*- coding: utf-8 -*-
"""Bookmark API 엔트리포인트.

라우터를 조립하고 시작 시 테이블을 생성한다.
"""
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import engine
from app.models import Base
from app.routers import bookmarks, tags


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 개발 편의용 — 운영에서는 마이그레이션 도구(alembic) 사용을 권장
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Bookmark API",
    description="OpenWiki 실습용 북마크 관리 API",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(bookmarks.router, prefix="/bookmarks", tags=["bookmarks"])
app.include_router(tags.router, prefix="/tags", tags=["tags"])


@app.get("/")
def health_check():
    return {"status": "ok", "service": "bookmark-api"}
