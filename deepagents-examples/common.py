# -*- coding: utf-8 -*-
"""예제 공통 유틸 — 모델 준비와 도구 호출 추적 출력.

모델은 환경변수로 설정한다 (독자 프로바이더에 맞게):
  OPENAI_API_KEY   : API 키 (OpenAI 호환 게이트웨이면 그 키)
  OPENAI_BASE_URL  : (선택) OpenAI 호환 엔드포인트 URL
  BOOK_MODEL_ID    : (선택) 모델 ID, 기본 gpt-5.5
"""
import io
import os
import sys

from langchain_openai import ChatOpenAI


def setup_stdout():
    """Windows 콘솔에서 한글 깨짐 방지."""
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    else:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")


def make_model():
    return ChatOpenAI(model=os.getenv("BOOK_MODEL_ID", "gpt-5.5"))


def print_tool_trace(result):
    """에이전트가 사용한 도구 호출을 순서대로 출력한다 (관찰용)."""
    print("\n--- 도구 호출 추적 ---")
    n = 0
    for msg in result["messages"]:
        for call in getattr(msg, "tool_calls", None) or []:
            n += 1
            args = call.get("args", {})
            target = args.get("file_path") or args.get("path") or args.get("pattern") or ""
            print(f"{n:2d}. {call['name']}  {target}")
    print(f"총 {n}회 도구 호출")
