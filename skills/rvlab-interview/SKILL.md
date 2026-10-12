---
name: rvlab-interview
description: RVLAB 연구 발표를 기획할 때 자료와 질문으로 청중·목적·근거·전제를 확인하고 plan/의 interview.md, brief.md, outline.md를 작성한다. 저장소 구축 작업에는 적용하지 않는다.
---

# RVLAB 발표 인터뷰

발표 의도를 확인하고 Stage 1~3 문서를 사용자가 검토·승인할 수 있는 상태로 만든다. 승인 규칙과 단계 보고 형식은 저장소의 [docs/workflow.md](../../docs/workflow.md), 문서 필드는 [docs/schemas.md](../../docs/schemas.md)를 따른다. 발견 경로가 symlink이면 실제 `skills/` 위치를 기준으로 저장소 루트를 찾는다.

## 시작

사용자가 지정한 task와 원자료를 재사용하고 `sources/`는 수정하지 않는다. 연구자의 초안 PPT도 `sources/`의 자료로 읽는다. 새 task는 `uv run rvppt new <slug> --title <제목>`으로 만든다. `uv run rvppt status tasks/<task>`의 `next_stage`부터 재개하며 기존 답변과 유효한 승인을 보존한다.

## 자료와 질문

자료에서 먼저 답을 찾고 `interview.md`에 다음을 구분한다.

- **자료 사실:** 실제 관찰·수치·설정, 근거 파일과 위치.
- **사용자 요구:** 직접 밝힌 목적·취향·제약.
- **에이전트 추정:** 자료로 추론한 청중 지식·우선순위·스토리. 사용자가 동의하기 전에는 요구로 기록하지 않는다.
- **미해결:** 모르는 사실·부족한 근거·상충하는 요구. 핵심 주장을 바꾸는 항목은 `open_items`에 `blocking: true`로 남긴다.

모르는 것만 몇 개씩 묶어 묻고 질문마다 짧은 선택지와 자유 입력을 준다. 질문 수를 채우려고 묻지 않고, 자료로 확인되는 사실이나 사소한 표현 선택은 묻지 않는다. 새 task의 첫 질문 묶음에서는 진행 방식(같이 만들기/핵심만)을 함께 묻는다. 질문 예와 모호한 답변을 다루는 방법은 [질문 가이드](references/interview-guide.md)에 있다.

## 단계별 결과물

1. **`plan/interview.md`:** 청중·목적·핵심 근거·성공 기준·제약·전제. 끝에 누구에게, 어떤 결과로, 어떤 판단을 받으려는지 재진술한다.
2. **`plan/brief.md`:** 메시지·스토리라인 후보와 근거·장단점, 추천안. 사용자가 이미 정한 메시지가 있으면 그 하나로 충분하다. 메시지가 정해지면 표지 제목·부제(RVLAB 표지의 노란 한 줄) 후보를 함께 묻는다.
3. **`plan/outline.md`:** 슬라이드 ID·섹션·토픽·핵심 문장·근거·예상 시간·그림 계획. 토픽은 상단 바·목차에 실릴 짧은 이름이고 핵심 문장은 그 슬라이드의 결론이다. 구성은 [랩미팅 가이드](../rvlab-ppt/references/lab-meeting.md), 그림은 [시각 설계 절차](../rvlab-ppt/references/visual-planning.md)를 참고한다. 좌표·색·폰트·레이아웃은 묻지 않는다.

Stage 3 승인 뒤 본문·제작·QA는 [rvlab-ppt](../rvlab-ppt/SKILL.md)를 따른다.

## 승인

각 단계가 끝나면 [워크플로우의 단계 보고](../../docs/workflow.md#단계-보고와-승인) 형식으로 채팅에 보고하고 `review_hash`를 붙여 명시적 승인을 받는다. 승인 뒤에만 `uv run rvppt approve tasks/<task> --stage N --expected-hash <검토한-review_hash>`를 실행한다. 입력이 바뀌어 실패하면 변경점을 보여 주고 다시 검토받는다.

문서 검증·해시·승인 무효화는 `tools/rvppt/state.py`가 맡는다. 질문을 고르고 답을 해석하는 일과 근거의 타당성 판단은 에이전트와 사용자의 몫이다.
