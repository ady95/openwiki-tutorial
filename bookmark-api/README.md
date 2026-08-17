# Bookmark API — OpenWiki 실습용 예제 프로젝트

「OpenWiki & OKF 따라하기」 책의 실습 대상 프로젝트입니다.
FastAPI + SQLite로 만든 작은 북마크 관리 API로, OpenWiki가 코드 위키를 생성하기에 적당한 구조(라우터/서비스/모델 분리)를 갖추고 있습니다.

## 실행 방법

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

- API 문서: http://localhost:8000/docs

## 구조

```
bookmark-api/
├── app/
│   ├── main.py                  # FastAPI 앱 엔트리포인트
│   ├── database.py              # SQLite 연결·세션 관리
│   ├── models.py                # SQLAlchemy 모델 (Bookmark, Tag)
│   ├── schemas.py               # Pydantic 스키마
│   ├── routers/
│   │   ├── bookmarks.py         # 북마크 CRUD·검색 라우터
│   │   └── tags.py              # 태그 라우터
│   └── services/
│       └── bookmark_service.py  # 비즈니스 로직 (중복 검사, 아카이브)
├── tests/
│   └── test_bookmarks.py
└── requirements.txt
```

## OpenWiki 실습

책 2장의 실습은 이 폴더를 독립 git 저장소로 만든 뒤 진행합니다.

```bash
cd bookmark-api
git init
git add .
git commit -m "init"
openwiki --init
```
