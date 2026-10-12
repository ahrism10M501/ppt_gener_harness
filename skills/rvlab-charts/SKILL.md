---
name: rvlab-charts
description: RVLAB 발표에서 도넛·파이, 흐름도, 타임라인, 2×2 매트릭스, 깔때기, 비교 카드처럼 표·불릿보다 한눈에 읽히는 꾸밈 차트가 필요할 때 고정 팔레트 레시피로 PNG·SVG를 만든다. 정밀한 실험 그래프(축·오차막대)는 scientific-visualization, 움직임은 rvlab-animation을 쓴다.
---

# RVLAB 꾸밈 차트

[시각 설계 절차](../rvlab-ppt/references/visual-planning.md)에서 "표·불릿보다 구조·비율·순서가 먼저 보여야 한다"고 판단한 슬라이드에 쓴다. 처음부터 그리지 않고 `charts.py`의 레시피를 복사해 데이터만 바꾼다. 색은 `DESIGN.md` 팔레트(파랑 계열)와 그 옅은 단계·회색만 쓴다. 그 밖의 색·좌표·장식을 입력하지 않는다.

## 표현 고르기

| 전하려는 것 | 레시피 | 제한 |
| --- | --- | --- |
| 전체 대비 비율(합이 100%) | `donut` | 3~5조각, 직접 라벨, 3D·폭발 금지. 값이 5개를 넘거나 비교가 목적이면 막대 |
| 입력→처리→출력 절차, 되돌림 | `flow(loop_back=)` | 3~5칸 직선. 분기가 있는 단순 흐름은 Mermaid, 그보다 복잡하면 슬라이드를 나눈다 |
| 시간·단계 순서 | `timeline` | 3~6개. 간격은 균등이며 비례 시간축이 아님 |
| 두 기준으로 분류·우선순위 | `matrix2x2` | 점 위치는 개념 배치임을 캡션에 밝힘 |
| 단계별 감소·전환 | `funnel` | 실제 값 필요, 큰 값부터 3~5단 |
| 2~4개 대안의 한 줄 비교 | `cards` | 설명은 25자 안팎. 수치 비교가 많으면 표 |

차트는 한 슬라이드에 하나만 두고 헤드라인이 그 차트의 결론이 되게 한다. 구체적인 값·비율·순서는 자료에서 확인한 것만 쓴다. 근거 없이 값을 만들지 않으며, 설명용 값은 캡션에 "합성 예시"라고 쓴다.

## 만드는 법

1. `uv sync --frozen --extra visual` 후 `uv run python skills/rvlab-charts/charts.py demo /tmp/charts`로 모양을 본다.
2. 생성 스크립트는 task의 `figures/make_charts.py`에 보존하고 값의 출처를 주석으로 남긴다. 실행은 `uv run python tasks/<task>/figures/make_charts.py`.

   ```python
   import sys
   from pathlib import Path
   here = Path(__file__).resolve().parent
   sys.path.insert(0, str(here.parents[2] / "skills/rvlab-charts"))
   import charts
   charts.flow(here / "pipeline", ["입력", "인코더", "정책", "행동"], highlight=2)
   print("chart fonts:", charts.FONTS)  # 실제 폰트 프로필을 노트·리포트에 기록
   ```
3. `slides.md`에 `![짧은 설명](figures/이름.png)`를 독립 문단으로 넣는다. 레시피는 본문 폭(약 9.3in)에 맞춰 18pt로 그린다. **2단(`columns`)이나 그림 그리드에 가로로 긴 차트(flow·timeline·funnel·cards)를 넣지 않는다.** 글자가 절반 아래로 줄어든다. 2단에는 도넛·매트릭스만 쓰거나 차트를 단독 슬라이드로 뺀다.
4. 라벨이 상자에 들어가지 않으면 레시피가 `ValueError`를 낸다. 글자를 줄이지 말고 라벨을 줄인다.
5. `uv run rvppt lint`·`build` 후 PNG를 직접 확인한다. 빌드의 넘침 검사는 그림 내부 글자를 보지 못한다.

레시피에 없는 모양은 `charts.py`의 `_box`·`_arrow`·`_canvas`로 조합하되 새 레시피가 반복해 필요하면 이 파일에 추가한다. 연구 결과 그래프(점·선·막대·오차)는 [scientific-visualization](../scientific-visualization/SKILL.md)을 쓴다.
