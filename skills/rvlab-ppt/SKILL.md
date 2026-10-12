---
name: rvlab-ppt
description: RVLAB 연구실 양식의 발표를 만들거나 수정할 때 slides.md와 PPTX를 제작한다. 주장과 근거에서 시각 자료의 필요성·표현·배치를 설계하고, 필요한 그래프·도식·애니메이션 스킬을 연결해 실제 슬라이드를 검수한다. 새 task와 표지 정보도 다룬다.
---

# RVLAB PPT

`slides.md`를 원본으로 유지하며 RVLAB 고정 양식의 PPTX와 검토 자료를 생성한다. 프로젝트는 Overleaf처럼 원본·그림·자료·결과가 한 폴더에 보인다.

## 시작

저장소 루트의 `AGENTS.md`, `DESIGN.md`를 읽는다. 발견 경로가 symlink이면 실제 `skills/` 위치를 기준으로 저장소 루트를 찾는다. 현재 구현된 명령만 실행한다.

- 사용자가 준 task 폴더와 원자료를 재사용하고 `uv run rvppt status tasks/<task>`로 재개 위치를 확인한다.
- 새 발표는 `uv run rvppt new <slug> --title <제목> [--subtitle ..] [--date YYYY-MM-DD]`로 만든다. `profile.yaml`이 없으면 `profile.example.yaml`을 복사하고 이름·영문 이름·소속 두 줄을 사용자에게 받아 채운다. 인적사항을 추측하지 않는다.
- 연구자가 `sources/`에 넣은 초안 PPT·논문·데이터를 먼저 읽는다. 초안 PPT는 `docs/workflow.md`의 기존 도구(markitdown·LibreOffice·unzip)로 읽는다. 외부 사진과 논문 figure는 [외부 시각 자료 절차](references/external-visuals.md)에 따라 직접 검색·추출·선정하고 출처와 함께 넣는다. PDF는 `uv run rvppt extract-paper TASK sources/논문.pdf`로 Markdown·media를 분리해 캡션과 본문 설명을 읽는다.
- Stage 1~3 탐색·기획은 [rvlab-interview](../rvlab-interview/SKILL.md), 단계 문서 형식은 `docs/schemas.md`를 따른다. 유효한 승인은 다시 받지 않는다.

## 시각 자료 계획과 제작

목차를 정할 때와 본문·그림을 만들거나 수정할 때 [시각 설계 절차](references/visual-planning.md)를 읽는다. 주장·근거·청중에서 그림의 역할을 정하고, 기존 자료 재사용과 표현 선택 → 설명·배치 설계 → 필요한 제작 스킬·도구 → 실제 슬라이드 검수로 연결한다. 글이나 표로 충분하면 새 그림을 만들지 않는다.

제작 전 결정은 기존 outline의 `figure`와 본문·발표자 노트에 남긴다. 선택한 경로의 지침만 읽고, 외부 스킬에서 이미 확인한 청중·목적·스타일·제작 허가를 다시 묻지 않는다. 별도 승인 단계는 추가하지 않는다.

## 슬라이드 문법과 이름 규칙

`docs/rendering.md` 문법으로 쓴다. 표지·목차·감사합니다는 빌드가 만든다.

- `# 섹션 | 부제`: 섹션 슬라이드이자 목차의 Chapter.
- `## 토픽`: 상단 바 제목이자 목차 항목. **짧은 이름**(한글 10자·영문 20자 이내 한 줄)이며 문장이 아니다. 같은 토픽의 여러 장은 이 이름을 반복한다.
- `### 핵심 문장`: 슬라이드 한 장의 결론. 본문 첫 줄 ▪ 24pt, 최대 두 줄.
- 본문은 메시지 하나, 불릿 5개·깊이 2, 표 8행·6열. 좌표·폰트·색·레이아웃을 입력하지 않고 결과·수치·인용을 만들지 않는다.
- 한국어 문장 끝: 핵심 문장을 모두 `~한다`로 맞추지 않는다. 발표에서 말하는 문장이므로 `~입니다`·`~합니다`·`~하겠습니다`·`~해야 합니다`를 섞는다. 불릿은 짧은 구나 명사형으로 끝내고, 노트는 말하듯 합니다체로 쓴다.

랩미팅 유형별 구성·좋은 슬라이드의 조건은 [랩미팅 가이드](references/lab-meeting.md)를 따른다. 기존 자료·웹 사진·논문 figure에서 적합한 시각 자료를 먼저 확보한다. 연구자가 새로 만들어야 하는 그림은 `![캡션](figures/이름.png "요청 내용")`으로 자리를 잡아 요청한다. 연구 결과 그래프의 신규 제작은 사용자 요청이 있을 때만 한다.

표·불릿보다 비율·순서·분류가 먼저 보여야 하는 슬라이드는 [rvlab-charts](../rvlab-charts/SKILL.md)의 도넛·흐름도·타임라인·매트릭스·깔때기·카드 레시피로 그림을 만든다.
사용자가 그림·교육 애니메이션 제작을 요청한 경우에는 그 범위에서 직접 만든다. 움직임의 설명 목적·장면 순서·배치는 [rvlab-animation](../rvlab-animation/SKILL.md)을 따른다. `figures/이름.gif`에는 같은 크기의 `figures/이름.png` 대표 상태가 필요하며, 정적 미리보기는 GIF 재생을 검증하지 않는다.

## 승인

- 진행 방식이 같이 만들기면 섹션 하나를 쓸 때마다 자료로 확인할 수 없는 사실, 표·그림의 범위, 연구자 경험으로 바꿀 수 있는 부분을 모아 3~5개씩 묻는다. 추측으로 채우지 않는다([질문 가이드](../rvlab-interview/references/interview-guide.md)).
- `uv run rvppt lint tasks/<task>`로 문법·제한·경로·그림 요청을 확인한다. `findings`의 빈 표지 부제·섹션 부제는 후보를 제안해 사용자에게 묻는다.
- 한국어 발표는 승인 요청 전에 [윤문 절차](references/polish.md)로 `humanize-korean`을 적용하고 `uv run rvppt polish-check`로 숫자·구조·수식·경로 보존을 확인한다. 사용자가 원하지 않으면 생략한다.
- 채팅에 Stage 4 단계 보고(표지 제목·부제·날짜·발표자, 장별로 바뀐 점, 남은 그림 요청, 미리보기 PNG)를 쓰고 `review_hash`, 중요한 가정·미해결 항목을 붙여 승인받는다. 형식은 [rvlab-interview](../rvlab-interview/SKILL.md)의 단계 보고를 따른다. 명시적인 승인 뒤에만 `uv run rvppt approve tasks/<task> --stage 4 --expected-hash <검토한-review_hash>`를 실행한다. 승인 필드를 직접 고치지 않는다.
- 연구자가 `slides.md`를 직접 고쳐 목차와 달라지면 무엇이 바뀌었는지 보여 주고 `plan/outline.md`를 맞춘 뒤 다시 승인받는다.

## 제작과 QA

`uv run rvppt build tasks/<task>`는 Overleaf의 Recompile처럼 언제든 실행된다. 에이전트는 내용 승인 전 빌드 결과를 최종본으로 전달하지 않으며, 사용자가 요청한 경우에만 초안 빌드를 보여 준다.

빌드 뒤 `uv run rvppt preview tasks/<task>`가 가리키는 PNG를 직접 보고 랩미팅 가이드와 시각 설계 절차의 확인 목록을 점검한다. 수식은 편집용 PPTX의 OMML과 별도 preview copy를 구분한다. 자동 검사 통과를 전달력 검증으로 간주하지 않는다. 검사 실패는 `slides.md`/자료를 고쳐 다시 빌드한다. 산출 PPTX를 사람이 고쳤으면 빌드가 멈추므로 덮어쓰지 말고 사용자에게 파일을 옮길지 묻는다.

## 전달

task 루트의 `YYYYMMDD_제목.pptx`·`.pdf`와 `.build/output/`의 PNG·리포트를 전달한다. 남은 그림 요청(`missing_figures`), 실제 폰트 프로필, 수식 fallback, 내용 승인 여부(`content_approved`)를 요약하고 PowerPoint에서 확인한 범위를 밝힌다. 수행하지 않은 실제 편집 확인을 완료했다고 말하지 않는다.

수식이 있는 발표는 편집형과 `_수식호환.pptx`를 함께 전달하고, 용도와 LaTeX 원본 편집 방법을 [제작 문법](../../docs/rendering.md#수식)에 따라 설명한다.

도구·폰트·외부 스킬 해시 문제는 `uv run rvppt doctor`로 확인한다. 이 명령은 읽기만 하며 무엇을 설치·복구할지 알려 준다. sudo·시스템 설치가 필요하면 명령과 이유를 제시해 확인받는다.
