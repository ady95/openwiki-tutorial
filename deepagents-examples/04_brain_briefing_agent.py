# -*- coding: utf-8 -*-
"""예제 4 — OKF 번들 브리핑 에이전트.

어떤 OKF 번들이든(개인 브레인 ~/.openwiki/wiki, 저장소 위키 openwiki/ ...)
읽고 상태 브리핑을 만든다. 같은 코드가 번들만 바꿔 재사용된다는 것이
OKF 이식성의 실증이다.

사용법:
  python 04_brain_briefing_agent.py [번들경로]
  (경로 생략 시 개인 브레인 ~/.openwiki/wiki)
"""
import sys
from pathlib import Path

from deepagents import create_deep_agent
from deepagents.backends import FilesystemBackend

from common import make_model, print_tool_trace, setup_stdout

SYSTEM_PROMPT = """당신은 OKF 지식 번들의 브리핑 담당자입니다.
번들 루트가 작업 디렉터리입니다.

절차:
1. index.md와 .last-update.json을 읽어 번들의 정체와 최신 상태(마지막
   갱신 시각·언어)를 파악합니다.
2. 인덱스가 안내하는 주요 문서를 읽습니다. 전부 읽지 말고, 브리핑에
   필요한 만큼만 읽으세요.
3. 다음 구성으로 브리핑을 작성합니다.
   - 번들 개요: 무엇에 대한 지식 베이스인지 한 문단
   - 지금 알아둘 것: 약속·마감·미해결 질문 등 행동이 필요한 항목
     (코드 위키라면: 백로그·알려진 한계)
   - 지식 상태: 마지막 갱신, 비어 있거나 얇은 영역
4. 증거가 없는 영역은 지어내지 말고 "정보 없음"으로 정직하게 보고합니다.

답변은 한국어로 작성합니다."""


def main():
    setup_stdout()
    default = Path.home() / ".openwiki" / "wiki"
    bundle = Path(sys.argv[1] if len(sys.argv) > 1 else default).resolve()
    if not bundle.exists():
        print(f"번들이 없습니다: {bundle}")
        print("openwiki personal --init 을 먼저 실행하거나, 번들 경로를 인자로 주세요.")
        sys.exit(1)

    agent = create_deep_agent(
        model=make_model(),
        system_prompt=SYSTEM_PROMPT,
        backend=FilesystemBackend(root_dir=bundle, virtual_mode=True),
    )

    print(f"[번들] {bundle}\n")
    result = agent.invoke({
        "messages": [{"role": "user", "content": "이 지식 번들의 오늘자 브리핑을 만들어 주세요."}]
    })
    print(result["messages"][-1].content)
    print_tool_trace(result)


if __name__ == "__main__":
    main()
