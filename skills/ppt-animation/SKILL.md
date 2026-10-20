---
name: ppt-animation
description: 발표에서 최적화·상태 변화·기하 변환 등 움직임이 이해에 필요한 개념을 GIF와 대표 정적 그림(PNG)으로 설명한다. Truth-first 수치 검증·storyboard·프리셋 팔레트 일관성·정적 대안을 검수한다.
---

# 범용 교육·연구 애니메이션 (`ppt-animation`)

정적 그림이나 [anatomy](../anatomy/SKILL.md) 도해만으로는 전달할 수 없는 **연속적 상태 변화, 수렴 과정, 좌표 변환, 시간차 상호작용**을 GIF와 대표 정적 프레임(PNG)으로 제작한다.
상세 스토리보드 규격과 검수 절차는 [rvlab-animation](../rvlab-animation/SKILL.md)과 공유하며, 다음 하네스 원칙을 추가로 준수한다:

1. **Truth-First 수치 모델**:
   - 임의의 가짜 궤적이나 수렴 곡선을 그리지 않는다. `plan/PROGRESS.md`의 Truth Model에 기록된 실제 수식·미분·갱신식·시뮬레이션 데이터에서 궤적을 생성한다.
2. **프리셋 팔레트 동기화**:
   - `rvppt.template.semantic_palette(preset=...)`에서 현재 발표 프리셋(`rvlab`, `modern-16x9`, `academic-16x9`, `executive-16x9`, `minimal-4x3`)의 강조색(`accent`, `band`)과 보조색(`neutral`)을 읽어 슬라이드 본문과 시각적 통일성을 유지한다.
   - 팔레트 키: `accent`, `band`, `secondary`, `tint`, `neutral`, `ink`, `section_accent`, `background`. 값은 #RRGGBB 형식이다.
3. **Dual Artifact 계약 (`foo.gif` + `foo.png`)**:
   - PPTX에는 애니메이션 `figures/foo.gif`가 삽입되고, PDF 및 정적 인쇄본·크리틱 시트에는 동일 해상도의 핵심 상태 포스터 `figures/foo.png`가 자동 사용된다.
   - 생성 후 반드시 `uv run pptgen build tasks/<task>` 및 `uv run pptgen audit tasks/<task> --zoom 4`로 포스터 프레임의 라벨 잘림·여백·대비를 검수한다.
