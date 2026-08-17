# -*- coding: utf-8 -*-
"""예제 3 — 위키 품질 감사 에이전트 (LEDGER-lite).

위키의 사실 주장을 추출해 소스 코드·테스트와 대조하고,
supported / stale / hallucinated / unverified 로 판정한 표를 만든다.

사용법:
  python 03_wiki_audit_agent.py <저장소경로> [감사할 위키 문서 경로...]
  (문서 경로 생략 시 quickstart.md와 domain/ 문서를 감사)
"""
import sys
from pathlib import Path

from deepagents import create_deep_agent
from deepagents.backends import FilesystemBackend

from common import make_model, print_tool_trace, setup_stdout

SYSTEM_PROMPT = """당신은 이 저장소 위키의 품질 감사관입니다.
위키가 코드의 현재 상태를 정확히 반영하는지 검증합니다.

절차 (write_todos로 계획을 세우고 진행하세요):
1. 지정된 위키 문서를 읽고, 검증 가능한 사실 주장을 추출합니다.
   부정문("~하지 않는다")과 한정어("~만", "기본적으로")를 우선 추출하세요.
2. 각 주장을 소스 코드와 테스트에서 확인합니다. 위키를 근거로 위키를
   판정하지 마세요 — 코드만이 근거입니다.
3. 주장마다 판정합니다:
   - supported: 코드가 주장을 뒷받침한다
   - stale: 코드가 바뀌어 주장이 낡았다
   - hallucinated: 코드에 근거가 없다
   - unverified: 코드로 확인 불가능한 서술이다
4. 다음 형식의 마크다운 표로 보고합니다.

| # | 주장 (요약) | 판정 | 근거 (파일:심벌·줄) |

마지막에 판정별 개수 요약과, stale/hallucinated 항목에 대한 조치
제안(--update 실행 등)을 덧붙입니다. 답변은 한국어로 작성합니다."""


def main():
    setup_stdout()
    repo = Path(sys.argv[1] if len(sys.argv) > 1 else "../bookmark-api").resolve()
    targets = sys.argv[2:] or ["openwiki/quickstart.md", "openwiki/domain/bookmark-service.md"]

    agent = create_deep_agent(
        model=make_model(),
        system_prompt=SYSTEM_PROMPT,
        backend=FilesystemBackend(root_dir=repo, virtual_mode=True),
    )

    print(f"[대상 저장소] {repo}")
    print(f"[감사 대상] {', '.join(targets)}\n")
    result = agent.invoke({
        "messages": [{"role": "user", "content": "다음 위키 문서를 감사해 주세요: " + ", ".join(targets)}]
    })
    print(result["messages"][-1].content)
    print_tool_trace(result)


if __name__ == "__main__":
    main()
