---
name: rvlab-ppt
description: RVLAB 연구실 양식의 발표를 만들거나 수정할 때 slides.md와 PPTX를 제작한다. 주장과 근거에서 시각 자료의 필요성·표현·배치를 설계하고, 필요한 그래프·도식·애니메이션 스킬을 연결해 실제 슬라이드를 검수한다. 새 task와 표지 정보도 다룬다.
---

# RVLAB PPT

`slides.md`를 원본으로 유지하며 RVLAB 고정 양식의 PPTX와 검토 자료를 생성한다. 프로젝트는 Overleaf처럼 원본·그림·자료·결과가 한 폴더에 보인다. 공통 규칙은 저장소의 `AGENTS.md`, 승인과 단계 보고는 `docs/workflow.md`를 따른다. 발견 경로가 symlink이면 실제 `skills/` 위치를 기준으로 저장소 루트를 찾는다.

## 시작

- 사용자가 준 task 폴더와 원자료를 재사용하고 `uv run rvppt status tasks/<task>`로 재개 위치를 확인한다. Stage 1~3이 남았으면 [rvlab-interview](../rvlab-interview/SKILL.md)부터 진행한다.
- 새 발표는 `uv run rvppt new <slug> --title <제목> [--subtitle ..] [--date YYYY-MM-DD]`로 만든다. `profile.yaml`이 없으면 `profile.example.yaml`을 복사하고 이름·영문 이름·소속 두 줄을 사용자에게 받아 채운다.
- 연구자가 `sources/`에 넣은 초안 PPT·논문·데이터를 먼저 읽는다. 초안 PPT는 `docs/workflow.md`의 기존 도구(markitdown·LibreOffice·unzip)로 읽는다.

## 슬라이드 문법과 이름 규칙

문법은 `docs/rendering.md`, 이름 규칙은 `DESIGN.md`의 "슬라이드 문법과 이름 규칙" 절을 따른다. 표지·목차·감사합니다는 빌드가 만든다.

- `# 섹션 | 부제`: 섹션 슬라이드이자 목차의 Chapter.
- `## 토픽`: 상단 바 제목이자 목차 항목. 한 줄짜리 **짧은 이름**(한글 10자·영문 20자 이내)이며 문장이 아니다. 같은 토픽의 여러 장은 이 이름을 반복한다.
- `### 핵심 문장`: 슬라이드 한 장의 결론. 본문 첫 줄 ▪ 24pt, 두 줄까지 들어간다.
- 좌표·폰트·색·레이아웃을 입력하지 않고 결과·수치·인용을 만들지 않는다. 불릿 깊이 2·표 8행 6열은 양식 제약이다. 불릿 개수와 길이는 권고이며 lint가 경고만 한다. 실제 넘침은 build가 막는다.
- 한국어 문장은 발표자가 말하는 문장으로 쓴다. 모든 핵심 문장을 `~한다`로 끝내면 기계적으로 읽히므로 발표자의 말투(보통 합니다체)를 따른다. 불릿은 짧은 구나 명사형, 노트는 말하듯 쓴다.

발표 유형별 구성과 좋은 슬라이드의 조건은 [랩미팅 가이드](references/lab-meeting.md)에 있다.

## 그림

그림이 필요한 슬라이드는 [시각 설계 절차](references/visual-planning.md)로 역할과 표현을 정한다. 글이나 표로 충분하면 그림을 만들지 않는다.

- **찾아 넣기:** 기존 자료, 웹 사진, 공개 논문 figure를 먼저 확보한다([외부 시각 자료 절차](references/external-visuals.md)). 논문 PDF는 `uv run rvppt extract-paper TASK <pdf>`로 Markdown·media를 분리해 캡션과 본문을 읽는다.
- **직접 만들기:** 순서·구조·분류·대안 비교를 불릿이나 표로만 나열하게 되면 흐름도·타임라인·매트릭스·카드([rvlab-charts](../rvlab-charts/SKILL.md))를 요청 없이 만든다. 새 값을 담지 않기 때문이다. 수치 차트(도넛·깔때기), 새 연구 결과 그래프, 교육용 GIF([rvlab-animation](../rvlab-animation/SKILL.md))는 사용자가 요청했을 때 만든다. 그 범위 안에서 그림마다 다시 허락받지 않는다.
- **요청하기:** 연구자가 만들어야 하는 그림은 `![캡션](figures/이름.png "요청 내용")`으로 자리를 잡는다. 빌드는 그 자리에 요청 상자를 그리고 `missing_figures`에 남긴다.

## 승인

- 같이 만들기면 섹션을 쓰면서 자료로 확인할 수 없는 사실, 표·그림의 범위, 연구자 경험으로 바꿀 수 있는 부분을 모아서 묻는다.
- `uv run rvppt lint tasks/<task>`로 문법·경로·그림 요청과 경고(`findings`)를 확인한다. 빈 표지 부제·섹션 부제는 후보를 제안해 묻는다.
- 한국어 발표는 요청이 없어도 승인 요청 전에 [윤문 절차](references/polish.md)를 실행한다. 사용자가 원하지 않으면 생략한다.
- 핵심 문장은 쓰면서 다듬어도 된다. `status`의 `warnings`에 목차와 달라진 문장이 나오므로 Stage 4 보고에 포함한다. 슬라이드 수·토픽·순서가 바뀌면 `plan/outline.md`를 고쳐 Stage 3부터 다시 승인받는다.
- [단계 보고](../../docs/workflow.md#단계-보고와-승인)를 쓰고 명시적 승인 뒤에만 `uv run rvppt approve tasks/<task> --stage 4 --expected-hash <검토한-review_hash>`를 실행한다.

## 제작과 QA

`uv run rvppt build tasks/<task>`는 Overleaf의 Recompile처럼 언제든 실행된다. 내용 승인 전 결과는 초안이며, 사용자가 요청할 때만 보여 준다.

빌드 뒤 `uv run rvppt preview tasks/<task>`가 가리키는 PNG를 직접 보고 랩미팅 가이드와 시각 설계 절차의 확인 목록을 점검한다. 자동 검사 통과를 전달력 검증으로 보지 않는다. 문제는 `slides.md`나 자료를 고쳐 다시 빌드한다. 산출 PPTX를 사람이 고쳤으면 빌드가 멈추므로 덮어쓰지 말고 파일을 옮길지 묻는다.

## 전달

task 루트의 `YYYYMMDD_제목.pptx`·`.pdf`와 `.build/output/`의 PNG·리포트를 전달한다. 남은 그림 요청, 실제 폰트, 수식 처리, 내용 승인 여부(`content_approved`)를 요약하고 PowerPoint에서 확인한 범위를 밝힌다. 수식이 있는 발표는 편집형과 `_수식호환.pptx`를 함께 전달하고 용도를 [수식](../../docs/rendering.md#수식)에 따라 설명한다.

도구·폰트·외부 스킬 해시 문제는 `uv run rvppt doctor`로 확인한다.
