# openwiki-tutorial

위키독스 책 「OpenWiki & OKF 따라하기」의 공개 예제코드 저장소입니다.

- 책: [https://wikidocs.net/book/20996](https://wikidocs.net/book/20996)

## 구성

| 폴더 | 내용 | 관련 장 |
|---|---|---|
| [bookmark-api/](bookmark-api/) | FastAPI + SQLite 북마크 관리 API — 코드 위키 실습 대상 | 2~5장 |

## 빠른 시작

```bash
git clone https://github.com/ady95/openwiki-tutorial.git
cd openwiki-tutorial/bookmark-api

# 이 폴더를 독립 저장소로 만든 뒤 위키를 생성합니다 (책 2장 참조)
git init
git add .
git commit -m "init"
openwiki --init
```

## 요구사항

- Node.js 22 이상, `npm install -g openwiki`
- LLM 프로바이더 1개 (OpenAI / Anthropic / Gemini / Copilot / OpenRouter / Ollama 등 — 책 02-1 참조)
