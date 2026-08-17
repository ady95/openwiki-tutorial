# -*- coding: utf-8 -*-
"""SQLite 연결과 세션 관리."""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./bookmarks.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},  # SQLite + FastAPI 조합 필수 옵션
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """요청 단위 DB 세션 의존성."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
