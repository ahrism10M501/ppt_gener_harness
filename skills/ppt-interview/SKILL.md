---
name: ppt-interview
description: 이 저장소(tasks/)의 발표를 기획할 때 자료와 질문으로 청중·목적·근거·디자인 프리셋·작업 규모를 확인하고 plan/의 interview.md, brief.md, outline.md, PROGRESS.md(Stage 1~3)를 작성한다. 저장소 자체를 고치는 작업에는 쓰지 않는다.
---

# 발표 기획 (`ppt-interview`)

발표 의도를 확인하고 Stage 1~3 문서를 사용자가 판단할 수 있는 상태로 만든다. 단계·승인·보고 형식은 [워크플로우](../../docs/workflow.md), 문서 필드는 [스키마](../../docs/schemas.md)가 정한다. 본문 작성부터는 [ppt-maker](../ppt-maker/SKILL.md)로 넘어간다.

## 시작

- 기존 task면 `uv run pptgen status tasks/<task>`의 `next_stage`부터 이어 가고 기존 답변·유효한 승인을 재사용한다. 상위 합의를 바꾸는 요청은 [수정 절차](../../docs/revisions.md)를 따른다.
- 새 task는 [워크플로우의 시작](../../docs/workflow.md#시작과-재개)대로 만든다.
- `sources/`의 논문·데이터·초안 PPT를 먼저 읽는다. `sources/`는 수정하지 않는다.
- 초보자가 혼자 따라 하는 튜토리얼을 요청받았거나 `interview.md`에 `review.tutorial`이 있으면 [ppt-tutorial](../ppt-tutorial/SKILL.md)을 함께 읽는다.

## 첫 질문 묶음

자료로 답할 수 없는 것만 [질문 가이드](references/interview-guide.md)대로 묶어 묻는다. 새 task라면 다음을 함께 확인한다.

1. **진행 방식:** 같이 만들기(단계마다 협의) / 핵심만(추천안으로 진행하고 승인 때만 확인) / 바로 초안.
2. **프리셋:** `uv run pptgen presets`가 목록과 각 템플릿의 `design`(DESIGN.md 경로)을 보여 준다. 후보의 DESIGN.md에서 성격을 읽고 청중·장소·화면 비율에 맞는 것을 추천하며 이유를 한 줄로 댄다. 정한 뒤에는 그 DESIGN.md를 컨텍스트에 두고 기획한다. 사용자 `.pptx`가 있으면 `uv run pptgen register-template <file> --id <id>`로 등록한다.
3. **규모(`budget`):** `quick` 핵심 슬라이드와 기본 도식 / `standard` 일반 발표, 구조 도식·데이터 그래프 / `thorough` anatomy 도해·애니메이션까지.

정한 프리셋·규모가 `pptgen new` 때와 다르면 `slides.md`의 `deck.preset`·`deck.budget`과 `plan/PROGRESS.md`의 해당 줄을 고치고 `uv run pptgen plan tasks/<task>`를 실행한다. 빌드는 `deck.preset`만 읽는다.

## 기록

**Truth Model (`plan/PROGRESS.md`):** 그림이나 슬라이드를 기획하기 전에 자료에서 확인한 수식·수치·비교 조건·단위·불변 조건을 적는다. 이후 그림과 애니메이션은 여기에 적힌 값만 쓴다.

**`interview.md`:** 다음 네 가지를 구분해 적는다. 사용자가 동의하기 전의 추정을 요구로 기록하지 않는다.
- 자료 사실: 관찰·수치·설정과 근거 파일 위치
- 사용자 요구: 직접 밝힌 목적·취향·프리셋·규모·제약
- 에이전트 추정: 자료로 추론한 청중 지식·우선순위·스토리
- 미해결: 모르는 사실·부족한 근거. 핵심 주장을 바꾸는 항목은 `open_items`에 `blocking: true`

끝에 누구에게, 어떤 결과로, 어떤 판단을 받으려는지 세 줄로 재진술한다.

**`brief.md`:** 근거 있는 메시지·스토리라인 후보와 추천안. 사용자가 정한 메시지가 있으면 그 하나로 충분하다. 메시지가 정해지면 표지 제목·부제 후보를 함께 제안한다.

**`outline.md`:** 슬라이드별 ID·섹션·토픽·핵심 문장·근거·시간·그림 계획. 토픽은 상단 바와 목차에 실릴 짧은 이름, 핵심 문장은 그 슬라이드의 결론이다. 구성은 [발표 유형 가이드](../ppt-maker/references/talk-types.md), 그림 계획은 [시각 설계](../ppt-maker/references/visual-planning.md)를 참고하고, 어떤 표현이 어울리는지는 그 템플릿의 DESIGN.md로 판단한다.

## 보고와 승인

단계마다 [단계 보고](../../docs/workflow.md#단계-보고와-승인) 형식으로 채팅에 보고하고 승인을 받는다. 승인이 입력 변경으로 실패하면 무엇이 바뀌었는지 보여 주고 다시 검토받는다. 문서 검증·해시·무효화는 코드가 맡고, 질문 선택과 근거의 타당성 판단은 에이전트와 사용자가 맡는다.
