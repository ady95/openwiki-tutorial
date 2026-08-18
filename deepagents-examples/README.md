# deepagents-examples — 9장 예제 코드

「OpenWiki & OKF 따라하기」 9장(전자책)의 예제입니다.
Deep Agents 프레임워크로 OpenWiki 위키를 소비하는 에이전트 4종을 만듭니다.

| 파일 | 예제 | 관련 절 |
|---|---|---|
| 01_wiki_qa_agent.py | 위키 Q&A 에이전트 (search→read→follow + 출처 인용) | 09-2 |
| 02_review_guard_agent.py | 코드 리뷰 가드레일 에이전트 (서브에이전트 위임) | 09-3 |
| 03_wiki_audit_agent.py | 위키 품질 감사 에이전트 (LEDGER-lite) | 09-4 |
| 04_brain_briefing_agent.py | OKF 번들 브리핑 에이전트 (이식성 실증) | 09-5 |

## 준비

Python 3.11 이상이 필요합니다 (deepagents 요구사항).

```bash
python -m venv .venv

# 가상환경 활성화 (셸에 맞게 택일)
#  - Windows PowerShell : .\.venv\Scripts\Activate.ps1
#  - Windows cmd        : .venv\Scripts\activate.bat
#  - macOS / Linux      : source .venv/bin/activate

pip install -r requirements.txt
```

모델 설정 (자기 프로바이더에 맞게 환경변수로):

```powershell
# Windows PowerShell
$env:OPENAI_API_KEY = "sk-..."
# OpenAI 호환 게이트웨이·로컬 모델을 쓰는 경우 추가:
$env:OPENAI_BASE_URL = "https://your-gateway.example.com/v1"
$env:BOOK_MODEL_ID = "your-model-id"
```

```bash
# macOS / Linux
export OPENAI_API_KEY=sk-...
# OpenAI 호환 게이트웨이·로컬 모델을 쓰는 경우 추가:
export OPENAI_BASE_URL=https://your-gateway.example.com/v1
export BOOK_MODEL_ID=your-model-id
```

## 실행

실습 대상은 위키가 생성된 bookmark-api입니다 (책 2장에서 생성).

```bash
python 01_wiki_qa_agent.py ../bookmark-api
python 02_review_guard_agent.py ../bookmark-api
python 03_wiki_audit_agent.py ../bookmark-api
python 04_brain_briefing_agent.py            # 개인 브레인 (~/.openwiki/wiki)
python 04_brain_briefing_agent.py ../bookmark-api/openwiki   # 저장소 위키로도
```

자세한 해설은 책 9장을 참조하세요.
