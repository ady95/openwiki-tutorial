# -*- coding: utf-8 -*-
"""북마크 API 테스트 — 인메모리 SQLite 사용."""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import get_db
from app.main import app
from app.models import Base

engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSession()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def test_create_and_get():
    res = client.post(
        "/bookmarks",
        json={"url": "https://Example.com/Docs#intro", "title": "예제 문서", "tags": ["Docs"]},
    )
    assert res.status_code == 201
    body = res.json()
    # URL 정규화: 호스트 소문자화, 프래그먼트 제거
    assert body["url"] == "https://example.com/Docs"
    assert body["tags"][0]["name"] == "docs"


def test_duplicate_url_conflict():
    payload = {"url": "https://example.com/a", "title": "A"}
    assert client.post("/bookmarks", json=payload).status_code == 201
    assert client.post("/bookmarks", json=payload).status_code == 409


def test_archive_excluded_from_list():
    res = client.post("/bookmarks", json={"url": "https://example.com/b", "title": "B"})
    bookmark_id = res.json()["id"]
    client.post(f"/bookmarks/{bookmark_id}/archive")
    assert res.json()["id"] not in [b["id"] for b in client.get("/bookmarks").json()]
    assert bookmark_id in [
        b["id"] for b in client.get("/bookmarks", params={"include_archived": True}).json()
    ]


def test_search():
    client.post("/bookmarks", json={"url": "https://example.com/fastapi", "title": "FastAPI 배우기"})
    client.post("/bookmarks", json={"url": "https://example.com/django", "title": "Django 배우기"})
    hits = client.get("/bookmarks/search", params={"q": "FastAPI"}).json()
    assert len(hits) == 1
    assert hits[0]["title"] == "FastAPI 배우기"
