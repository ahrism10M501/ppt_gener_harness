---
name: ppt-maker
description: 이 저장소(tasks/)의 발표 본문(slides.md)을 쓰고 PPTX로 빌드·검수·전달하거나 기존 발표를 수정할 때 쓴다(Stage 4). 작업 전에 템플릿의 templates/<id>/DESIGN.md를 읽고 내용·그림·강조가 어울리는지 판단하며, 그림은 ppt-charts·ppt-animation·anatomy·scientific-visualization으로 연결한다.
---

# 발표 제작 (`ppt-maker`)

`slides.md`가 원본이고 PPTX·PDF는 빌드 산출물이다. 단계와 승인은 [워크플로우](../../docs/workflow.md), 작성 문법은 [rendering](../../docs/rendering.md)을 따른다.

## 시작

**먼저 읽기:** task `slides.md`의 `deck.preset`(없으면 `rvlab`)에 해당하는 `templates/<deck.preset>/DESIGN.md`를 읽어 컨텍스트에 올린다. 그 템플릿의 색 사용·도식 모양·그래프 스타일·빌드 후 점검은 이 문서가 정하며, 이 스킬에는 템플릿에 따라 달라지는 규약을 두지 않는다.

- `uv run pptgen status tasks/<task>`와 `plan/PROGRESS.md`로 이어 갈 위치를 확인한다. Stage 1~3이 비어 있으면 [ppt-interview](../ppt-interview/SKILL.md)로 기획한다. 사용자가 바로 만들기를 원하면 기획 문서를 추천안으로 채워 한 번에 보고한다.
- 수정·되돌리기 요청은 [수정 절차](../../docs/revisions.md)로 대상과 재검토 범위를 정한 뒤 바로 반영한다.
- `plan/interview.md`에 `review.tutorial`이 있으면 [ppt-tutorial](../ppt-tutorial/SKILL.md)의 실습 슬라이드 규약과 승인 전 크리틱을 따른다.

## 어울림 판단

프리셋은 레이아웃·폰트·색만 정한다. 무엇을 얼마나 어떻게 보여 줄지는 에이전트가 판단한다. 판단 순서는 다음과 같다.

1. **청중과 목적:** `plan/interview.md`. 누가 무엇을 판단하는 자리인지가 가장 앞선다.
2. **템플릿의 규약:** 위에서 읽은 `templates/<deck.preset>/DESIGN.md`. 성격·어울리는 구성과 밀도·그림 인상·빌드 후 볼 것이 적혀 있다.
3. **덱 안의 일관성:** 같은 의미에는 같은 표현과 색을 쓴다. 강조는 드물수록 효과가 있다.

1과 2가 부딪히면 청중을 따르고 Stage 4 보고에 그 판단을 적는다. DESIGN.md에 없는 상황은 비슷한 성격의 다른 템플릿 DESIGN.md를 참고해 판단한다. lint 경고(불릿 수·깊이, 표 크기, 길이)는 권고이고, 실제 넘침은 build가 막는다.

## 쓰기

- `# 섹션 | 부제`, `## 토픽`(상단 바·목차의 짧은 이름, 생략하면 섹션 제목), `### 핵심 문장`(슬라이드의 결론). 표지·목차·감사합니다는 빌드가 만든다.
- 한국어 핵심 문장은 발표자가 말하는 문장으로 쓴다. 모든 문장을 `~한다`로 끝내면 기계적으로 읽힌다. 불릿은 짧은 구, 노트는 말하듯 쓴다.
- 결과·수치·인용은 자료에서 확인한 것만 쓴다. 발표 유형별 구성은 [발표 유형 가이드](references/talk-types.md)를 참고한다.
- 같은 모양이 이어지면 청중이 지친다. 섹션을 여는 결론, 기억시킬 숫자 하나, 짧은 인용처럼 한 문장이 주인공인 곳에는 `{.statement}`·`{.number}`·`{.quote}` 슬라이드([문법](../../docs/rendering.md#슬라이드-종류))를 섞어 리듬을 만든다. 몇 장마다 쓸지는 정해져 있지 않으며 내용이 그 모양을 원할 때만 쓴다. 표는 비교할 값이 있을 때만 쓰고, 열이 많거나 셀이 문장이면 표 대신 불릿이나 카드(`ppt-charts`)를 검토한다.
- 같이 만들기라면 섹션을 쓰면서 자료로 확인할 수 없는 사실과 연구자 경험으로 바꿀 부분을 모아서 묻는다.

## 그림

그림이 필요한지, 어떤 표현이 맞는지, 누가 만드는지는 [시각 설계](references/visual-planning.md)를 따른다. 웹 사진·논문 figure는 [외부 시각 자료](references/external-visuals.md), 도식·차트는 [ppt-charts](../ppt-charts/SKILL.md), 움직임은 [ppt-animation](../ppt-animation/SKILL.md), 기구·시스템 해부도는 `uv run pptgen anatomy`([anatomy](../anatomy/SKILL.md)), 정량 그래프는 [scientific-visualization](../scientific-visualization/SKILL.md)을 쓴다.

## 승인 전

1. `uv run pptgen lint tasks/<task>`로 문법·경로·그림 요청·경고를 확인한다. 비어 있는 표지·섹션 부제는 후보를 제안한다.
2. 한국어 발표는 [윤문](references/polish.md)을 거친다. 사용자가 원하지 않으면 생략한다.
3. `status`의 `warnings`(목차와 달라진 핵심 문장·구조)를 Stage 4 보고에 넣고, [워크플로우](../../docs/workflow.md#단계-보고와-승인)대로 승인을 받는다.

## 빌드와 검수

`uv run pptgen build tasks/<task>`는 언제든 실행할 수 있다. 내용 승인 전 결과는 초안이다. 결과 PPTX를 사람이 고쳤으면 빌드가 멈춘다. 이때는 덮어쓰지 말고 파일을 옮길지 묻는다.

1. `uv run pptgen preview tasks/<task>`의 슬라이드 PNG를 직접 본다. 자동 검사 통과가 전달력을 보장하지는 않는다.
2. `uv run pptgen audit tasks/<task> --zoom 4`의 확대 크롭(`critic-crops-sheet.png`)과 여백·대비(`critic-audit.json`)로 잘림·겹침·작은 글씨를 확인한다. 썸네일만으로는 놓치기 쉽다. 검수 깊이는 규모에 맞춘다.
3. 템플릿 DESIGN.md의 "빌드 후 볼 것"을 확인하고, 발견한 문제와 수정은 `plan/PROGRESS.md`에 남긴다. 문제는 `slides.md`나 그림 원본을 고쳐 다시 빌드한다.

## 전달

task 루트의 `YYYYMMDD_제목.pptx`·`.pdf`와 `.build/output/`의 PNG·리포트를 전달한다. 남은 그림 요청, 실제 사용 폰트, 내용 승인 여부(`content_approved`), PowerPoint에서 확인한 범위를 요약한다. 수식이 있으면 편집형과 `_수식호환.pptx`의 용도를 [수식](../../docs/rendering.md#수식)대로 설명한다. 도구 문제는 `uv run pptgen doctor`로 확인한다.
