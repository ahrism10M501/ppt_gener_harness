---
name: ppt-charts
description: 이 저장소(tasks/) 발표의 흐름도·분기·그룹·피드백·상호작용 도식과 도넛·타임라인·매트릭스·퍼널·비교 카드를 발표 프리셋 팔레트에 맞춰 PNG·SVG로 만든다. 기구·시스템 해부도는 anatomy, 실험 그래프는 scientific-visualization을 쓴다.
---

# 도식·꾸밈 차트 (`ppt-charts`)

[시각 설계](../ppt-maker/references/visual-planning.md)에서 "구조·비율·순서가 먼저 보여야 한다"고 판단한 슬라이드에 쓴다. 누가 언제 만드는지도 그 문서가 정한다. 모서리·색 사용량·밀도처럼 어떤 인상이 어울리는지는 그 DESIGN.md로 판단한다.

**먼저 읽기:** task `slides.md`의 `deck.preset`(없으면 `rvlab`)에 해당하는 `templates/<deck.preset>/DESIGN.md`를 읽어 컨텍스트에 올린다. 그 템플릿의 색 사용·도식 모양·그래프 스타일·빌드 후 점검은 이 문서가 정하며, 이 스킬에는 템플릿에 따라 달라지는 규약을 두지 않는다.

**프리셋:** 두 도구는 출력 경로나 실행 스크립트가 속한 task의 `deck.preset`을 자동으로 쓴다(task 밖이면 `rvlab`). 다른 프리셋으로 그릴 때만 `--preset <id>`나 `charts.set_preset("<id>")`를 쓴다. 색은 `rvppt.template.semantic_palette(<id>)`에서 온다.

팔레트 키: `accent`, `band`, `secondary`, `tint`, `neutral`, `ink`, `section_accent`, `background`.

## 흐름·구조 도식 (`diagrams.py`)

분기·그룹·피드백·순차·상태 도식은 [로컬 자동 도식](references/local-diagrams.md)을 읽고 만든다. `beautiful-mermaid`와 ELK가 로컬에서 배치한다(설치는 저장소 루트의 `npm ci`).

```bash
uv run python skills/ppt-charts/diagrams.py render tasks/<task>/figures/pipeline.mmd tasks/<task>/figures/pipeline
```

- 모든 내용을 같은 가로 상자 행으로 만들지 않는다. 순서·판단·병렬 입력·그룹·상호작용 중 설명할 관계를 고른다. 자료에서 확인되지 않은 화살표는 추가하지 않는다.
- 노드에는 짧은 개념, 화살표에는 필요한 관계를 쓴다. 핵심 처리 하나만 `:::focus`로 강조한다.
- `.mmd` 원본과 PNG·SVG·가독성 JSON을 같은 task의 `figures/`에 둔다.

## 꾸밈 차트 (`charts.py`)

| 전하려는 것 | 레시피 | 참고 |
| --- | --- | --- |
| 전체 대비 비율(합 100%) | `donut` | 조각이 많거나 비교가 목적이면 막대가 낫다 |
| 단순 직선 흐름 | `flow` | 분기·그룹이 있으면 `diagrams.py` |
| 시간·단계 순서 | `timeline` | 간격이 균등하며 비례 시간축이 아님 |
| 두 기준의 분류·우선순위 | `matrix2x2` | 점 위치가 개념 배치임을 캡션에 밝힘 |
| 단계별 감소·전환 | `funnel` | 실제 값이 필요 |
| 2~4개 대안의 짧은 비교 | `cards` | 수치 비교가 많으면 표 |

생성 스크립트는 task의 `figures/make_charts.py`에 두고 값의 출처를 주석으로 남긴다. 실행은 `uv run python tasks/<task>/figures/make_charts.py`이고, 전체 모양은 `uv run python skills/ppt-charts/charts.py demo /tmp/charts`로 볼 수 있다(`uv sync --extra visual` 필요).

```python
import sys
from pathlib import Path
here = Path(__file__).resolve().parent
sys.path.insert(0, str(here.parents[2] / "skills/ppt-charts"))
import charts

charts.flow(here / "pipeline", ["입력", "인코더", "정책", "행동"], highlight=2)
print("chart fonts:", charts.FONTS)  # 실제 폰트를 노트·리포트에 기록
```

차트는 한 슬라이드에 하나만 두고 핵심 문장이 그 차트의 결론이 되게 한다. 값·비율·순서는 자료에서 확인한 것만 쓴다. 설명용 값은 캡션에 "합성 예시"라고 적는다. 레시피에 없는 차트는 `_box`·`_arrow`·`_canvas`로 조합하고, 반복해서 필요하면 레시피로 추가한다.

## 크기와 검수

`diagrams.py`는 프리셋 본문 폭에 단독으로 넣는다고 보고 실제 글자 크기를 검사한다. `charts.py`는 캔버스 안에서 18pt로 그리고, 전체 폭에 넣었을 때 프리셋 최소 글자보다 작아지면 경고만 출력한다. 빌드가 그림을 슬롯에 맞춰 줄이므로 가로로 긴 차트(5단계 flow, timeline, cards)나 2단·그리드에 넣은 그림은 실제 글자가 더 작아진다. 빌드의 넘침 검사와 `audit` 크롭은 그림 안의 글자를 보지 않으므로 `uv run pptgen preview tasks/<task>`의 슬라이드 PNG를 확대해 확인한다. 작으면 라벨을 줄이거나 방향을 바꾸거나 그림을 단독 슬라이드로 옮긴다. 라벨이 상자에 들어가지 않으면 레시피가 `ValueError`를 낸다. 이때도 글자를 줄이지 말고 라벨을 줄인다.
