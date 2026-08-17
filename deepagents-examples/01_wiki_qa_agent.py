# -*- coding: utf-8 -*-
"""예제 1 — 위키 Q&A 에이전트.

openwiki/ 번들을 search → read → follow links 방식으로 탐색해 질문에 답하고,
실제로 참고한 문서 경로를 출처로 밝힌다.

사용법:
  python 01_wiki_qa_agent.py <저장소경로> ["질문"]
"""
import sys
from pathlib import Path

from deepagents import create_deep_agent
from deepagents.backends import FilesystemBackend

from common import make_model, print_tool_trace, setup_stdout

SYSTEM_PROMPT = """당신은 이 저장소의 지식 베이스를 활용해 질문에 답하는 어시스턴트입니다.

규칙:
1. 먼저 openwiki/quickstart.md(없으면 openwiki/index.md)를 읽고,
   어느 문서에 답이 있을지 판단하세요.
2. 관련 위키 문서를 읽고, 본문 링크가 가리키는 이웃 문서가 필요하면 따라가세요.
3. 세부 사항이 중요한 질문은 소스 코드로 교차 확인하세요.
   코드와 테스트가 위키보다 우선하는 최종 근거입니다.
4. 답변 마지막에 "출처:" 목록으로 실제로 참고한 문서·코드 경로를 밝히세요.

전체 파일을 무작정 훑지 말고, 인덱스가 안내하는 최단 경로로 이동하세요.
답변은 한국어로 작성합니다."""


def main():
    setup_stdout()
    repo = Path(sys.argv[1] if len(sys.argv) > 1 else "../bookmark-api").resolve()
    question = sys.argv[2] if len(sys.argv) > 2 else (
        "북마크 아카이브와 복원은 어떻게 동작하나요? 복원하면 목록에 어떻게 반영되나요?"
    )

    agent = create_deep_agent(
        model=make_model(),
        system_prompt=SYSTEM_PROMPT,
        backend=FilesystemBackend(root_dir=repo, virtual_mode=True),
    )

    print(f"[대상 저장소] {repo}")
    print(f"[질문] {question}\n")
    result = agent.invoke({"messages": [{"role": "user", "content": question}]})
    print(result["messages"][-1].content)
    print_tool_trace(result)


if __name__ == "__main__":
    main()
