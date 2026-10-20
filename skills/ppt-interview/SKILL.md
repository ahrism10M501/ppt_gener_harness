---
name: ppt-interview
description: 범용 연구·기술·비즈니스 발표를 기획할 때 자료와 질문으로 청중·목적·디자인 프리셋(16:9/4:3/RVLAB/커스텀)·예산(quick/standard/thorough)·근거를 확인하고 plan/의 interview.md, brief.md, outline.md, PROGRESS.md를 작성한다. 저장소 구축 작업에는 적용하지 않는다.
---

# 범용 PPT 인터뷰 & 하네스 기획 (`ppt-interview`)

발표 의도와 디자인 프리셋·작업 예산을 확인하고 Stage 1~3 문서를 사용자가 검토·승인할 수 있는 상태로 만든다.
`anatomy` 스킬의 하네스 철학(**Up-front Sizing/Budget**, **Truth-first Model**, **PROGRESS.md 상태 지속성**)을 발표 기획 단계에 통합한다.
승인 규칙과 단계 보고 형식은 저장소의 [docs/workflow.md](../../docs/workflow.md), 문서 필드는 [docs/schemas.md](../../docs/schemas.md)를 따른다.

## 시작 및 프리셋·예산 선정

사용자가 지정한 task와 원자료를 재사용하고 `sources/`는 수정하지 않는다.
새 task는 `uv run pptgen new <slug> --title <제목> [--preset <preset_id>] [--budget <quick|standard|thorough>]`로 만든다.
사용 가능한 프리셋은 `uv run pptgen presets`로 확인할 수 있으며, 사용자가 별도 `.pptx` 양식을 제공하면 `uv run pptgen register-template <path.pptx> --id <id>`로 등록해 사용한다:

- `rvlab` (기본값, 4:3): 경기대학교 RVLAB 연구실 표준 양식
- `modern-16x9` (16:9): 컨퍼런스·세미나·테크 발표용 모던 인디고/슬레이트 와이드 양식
- `academic-16x9` (16:9): 학술 대회·논문 디펜스용 네이비 와이드 양식
- `executive-16x9` (16:9): 프로젝트 제안·경영진 보고·피치덱용 틸/슬레이트 와이드 양식
- `minimal-4x3` (4:3): 기관 로고 없는 깔끔한 범용 4:3 양식

새 task의 첫 질문 묶음에서는 다음을 함께 확인한다:
1. **진행 방식**: 같이 만들기(단계별 협의) / 핵심만 빠르게
2. **디자인 프리셋 (`preset`) 및 화면 비율**: 기본 `rvlab`(4:3) 또는 `modern-16x9`, `academic-16x9`, `executive-16x9`, `minimal-4x3`, 혹은 사용자 커스텀 `.pptx`
3. **작업 규모·예산 (`budget`)**:
   - `quick` (Figure급): 핵심 슬라이드 위주 빠른 구성, 기본 도식·표 중심
   - `standard` (Hero급): 표준 연구/기술 발표, 핵심 아키텍처·데이터 시각화 포함
   - `thorough` (Epic급): 심층 발표, `anatomy` 기반 고정밀 아이소메트릭 기구/아키텍처 도해 또는 수식·상태 전이 애니메이션 포함

## Truth-First 모델 기록 (`plan/PROGRESS.md`)

자료를 읽은 직후, 슬라이드나 그림을 기획하기 전에 `plan/PROGRESS.md`의 **Truth Model** 섹션을 먼저 채운다:
- 원자료(`sources/`)에서 확인된 핵심 수식, 물리·논리적 관계, 좌표계/단위 규약
- 검증된 실험 수치·표본 수·비교 조건
- 발표 전체에서 일관되게 유지해야 할 불변 조건(Invariants)

## 자료와 질문 (`plan/interview.md`)

자료에서 먼저 답을 찾고 `interview.md`에 다음을 구분한다:
- **자료 사실:** 실제 관찰·수치·설정, 근거 파일과 위치.
- **사용자 요구:** 직접 밝힌 목적·취향·프리셋·예산·제약.
- **에이전트 추정:** 자료로 추론한 청중 지식·우선순위·스토리. 사용자가 동의하기 전에는 요구로 기록하지 않는다.
- **미해결:** 모르는 사실·부족한 근거·상충하는 요구. 핵심 주장을 바꾸는 항목은 `open_items`에 `blocking: true`로 남긴다.

질문 예와 모호한 답변을 다루는 방법은 [질문 가이드](../rvlab-interview/references/interview-guide.md)를 참고한다.

## 단계별 결과물

1. **`plan/interview.md` (Stage 1):** 청중·목적·핵심 근거·성공 기준·제약·전제 및 선택된 `preset`/`budget`.
2. **`plan/brief.md` (Stage 2):** 메시지·스토리라인 후보(1~3개)와 근거·장단점, 추천안.
3. **`plan/outline.md` (Stage 3):** 슬라이드 ID·섹션·토픽·핵심 문장·근거·예상 시간·그림 계획.
   - 그림 계획(`figure`)에는 단순 차트(`[ppt-charts]`), 정량 실험 그래프(`[scientific-visualization]`), 기구/하드웨어/시스템 해부 도해(`[anatomy]`), 상태 전이/최적화 움직임(`[ppt-animation]`) 중 어떤 도구를 쓸지 명시한다.

Stage 3 승인 뒤 본문·제작·4x 크리틱 QA는 [ppt-maker](../ppt-maker/SKILL.md)를 따른다.

## 승인

각 단계가 끝나면 `uv run pptgen plan tasks/<task>`로 `plan/contracts.md`를 갱신하고, `review_hash`를 붙여 명시적 승인을 받은 뒤에만 `uv run pptgen approve tasks/<task> --stage N --expected-hash <검토한-review_hash>`를 실행한다.
