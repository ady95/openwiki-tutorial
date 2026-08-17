# -*- coding: utf-8 -*-
"""예제 2 — 코드 리뷰 가드레일 에이전트.

PR diff를 받아, 위키에 문서화된 규칙(도메인 규칙·수정 가드레일·HTTP 계약)과
대조해 위반을 지적한다. 위키 조사는 서브에이전트에게 위임한다.

사용법:
  python 02_review_guard_agent.py <저장소경로> [diff파일]
  (diff파일 생략 시 내장 샘플 diff — 규칙 위반 2건 포함 — 사용)
"""
import sys
from pathlib import Path

from deepagents import create_deep_agent
from deepagents.backends import FilesystemBackend

from common import make_model, print_tool_trace, setup_stdout

# 일부러 위키의 문서화된 규칙을 어기는 샘플 diff (실습용)
SAMPLE_DIFF = """\
--- a/app/routers/bookmarks.py
+++ b/app/routers/bookmarks.py
@@ -18,7 +18,7 @@ def create_bookmark(payload: BookmarkCreate, db: Session = Depends(get_db)):
     except ValueError as e:
-        raise HTTPException(status_code=409, detail=str(e))
+        raise HTTPException(status_code=400, detail=str(e))

--- a/app/services/bookmark_service.py
+++ b/app/services/bookmark_service.py
@@ -29,7 +29,7 @@ def normalize_url(url: str) -> str:
-    return urlunparse(normalized).rstrip("/")
+    return urlunparse(normalized).rstrip("/").lower()
"""

WIKI_RESEARCHER = {
    "name": "wiki-researcher",
    "description": (
        "위키(openwiki/)에서 특정 주제의 문서화된 규칙·계약·가드레일을 찾아 "
        "원문 그대로 인용해 온다. 리뷰 판단은 하지 않는다."
    ),
    "system_prompt": (
        "당신은 openwiki/ 지식 베이스 조사원입니다. 요청받은 주제에 대해 "
        "quickstart의 작업 라우팅 표를 시작점으로 관련 문서를 찾아, 규칙·계약에 "
        "해당하는 문장을 문서 경로와 함께 원문 그대로 인용해 보고하세요. "
        "해석이나 판단은 덧붙이지 마세요."
    ),
}

SYSTEM_PROMPT = """당신은 이 저장소의 코드 리뷰어입니다. 주어진 diff를
위키에 문서화된 규칙과 대조해 심사합니다.

절차:
1. diff가 손대는 영역을 파악합니다.
2. wiki-researcher 서브에이전트에게 해당 영역의 문서화된 규칙·계약·
   가드레일 조사를 맡깁니다 (task 도구 사용).
3. 돌아온 규칙 인용과 diff를 대조해, 위반이 있으면 다음 표로 보고합니다.

| 위반 | diff 위치 | 근거 (위키 문서와 인용) | 심각도 |

위반이 없으면 "위반 없음"과 확인한 규칙 목록을 보고합니다.
필요하면 소스 코드·테스트를 직접 읽어 diff의 영향을 확인해도 됩니다.
답변은 한국어로 작성합니다."""


def main():
    setup_stdout()
    repo = Path(sys.argv[1] if len(sys.argv) > 1 else "../bookmark-api").resolve()
    diff = Path(sys.argv[2]).read_text(encoding="utf-8") if len(sys.argv) > 2 else SAMPLE_DIFF

    agent = create_deep_agent(
        model=make_model(),
        system_prompt=SYSTEM_PROMPT,
        backend=FilesystemBackend(root_dir=repo, virtual_mode=True),
        subagents=[WIKI_RESEARCHER],
    )

    print(f"[대상 저장소] {repo}\n[심사할 diff]\n{diff}")
    result = agent.invoke({
        "messages": [{"role": "user", "content": f"다음 diff를 심사해 주세요.\n\n```diff\n{diff}\n```"}]
    })
    print(result["messages"][-1].content)
    print_tool_trace(result)


if __name__ == "__main__":
    main()
