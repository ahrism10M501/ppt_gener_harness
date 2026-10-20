---
name: ppt-charts
description: 발표의 흐름도·분기·그룹·피드백·상호작용 도식과 도넛·타임라인·매트릭스·퍼널·비교 카드를 현재 발표 프리셋(rvlab, modern-16x9, academic-16x9, executive-16x9, minimal-4x3 등) 팔레트에 맞춰 PNG·SVG로 제작한다. 기구·시스템 해부 도해는 anatomy, 실험 그래프는 scientific-visualization을 쓴다.
---

# 범용 프레젠테이션 차트 & 다이어그램 (`ppt-charts`)

선택된 프리셋(`deck.preset`)의 컬러 팔레트와 타이포그래피 규칙을 자동으로 적용해 깔끔한 벡터(SVG) 및 300-DPI 래스터(PNG) 도식을 생성한다.
세부 레시피와 스크립트는 [skills/rvlab-charts](../rvlab-charts/SKILL.md)의 `diagrams.py` 및 `charts.py`를 공유하며, 멀티 프리셋 옵션을 지원한다.

## 1. 로컬 자동 배치 다이어그램 (`diagrams.py`)

분기·그룹·피드백·순차 흐름도는 `beautiful-mermaid` + ELK 기반의 `diagrams.py`에 `--preset <preset_id>`를 넘겨 실행한다:

```bash
uv run python skills/rvlab-charts/diagrams.py render tasks/<task>/figures/pipeline.mmd tasks/<task>/figures/pipeline --preset modern-16x9
```

- 스타일·색상·좌표를 `.mmd`에 직접 적지 않고 의미 역할(`:::focus`)만 표시하면 프리셋의 `accent_blue`, `band_blue`, `table_tint` 팔레트가 자동 적용된다.
- 슬라이드 내 최소 글자 크기(18pt) 미달 시 에러를 발생시켜 가독성을 강제한다.

## 2. 고정 팔레트 차트 레시피 (`charts.py`)

도넛(`donut`), 가로 흐름(`flow`), 타임라인(`timeline`), 2x2 매트릭스(`matrix2x2`), 퍼널(`funnel`), 비교 카드(`cards`)를 만들 때는 `charts.set_preset("<preset_id>")`를 먼저 호출한다:

```python
import sys
from pathlib import Path
here = Path(__file__).resolve().parent
sys.path.insert(0, str(here.parents[2] / "skills/rvlab-charts"))
import charts

charts.set_preset("modern-16x9")  # 또는 rvlab, academic-16x9, executive-16x9, minimal-4x3
charts.flow(here / "pipeline", ["데이터 수집", "특징 추출", "정책 학습", "실시간 제어"], highlight=2)
```

## 3. 복합 구조·하드웨어·메커니즘 도해는 `anatomy`로 연결

단순 박스-화살표 흐름도를 넘어 센서/기구 구조, 계층적 시스템 아키텍처, 단면도/분해도가 필요할 때는 [anatomy](../anatomy/SKILL.md) 스킬과 `uv run pptgen anatomy tasks/<task> --name <fig>` 명령을 사용한다.
