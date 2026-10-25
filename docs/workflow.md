# 발표 제작 워크플로우

발표의 Stage 1~4 흐름, 승인 규칙, 단계 보고 형식을 정의하는 단일 문서다. 기획은 [ppt-interview](../skills/ppt-interview/SKILL.md), 본문·제작은 [ppt-maker](../skills/ppt-maker/SKILL.md)가 이 문서를 따른다. 문서 필드는 [schemas.md](schemas.md)에 있다.

## 시작과 재개

기존 task가 있으면 폴더·원자료·답변을 재사용한다. 새 발표는 `uv run pptgen new <slug> --title <제목> [--subtitle <부제>] [--date YYYY-MM-DD] [--preset <id>] [--budget quick|standard|thorough]`로 만든다. 표지 인적사항은 저장소 루트의 `profile.yaml`에서 `slides.md`의 `deck`으로 복사된다. 이 파일이 없으면 `profile.example.yaml`을 복사하고 사용자에게 채워 달라고 요청한다.

| 위치 | 누가 쓰나 | 내용 |
| --- | --- | --- |
| `slides.md` | 연구자·에이전트 | 발표 원본(Overleaf의 main.tex) |
| `figures/` | 연구자·에이전트 | 연구자 그림, 에이전트가 찾은 사진·논문 figure(`figures/external/`), 만든 도식·차트와 출처 기록 |
| `sources/` | 연구자 | 논문·데이터·메모·초안 PPT. 읽기 전용이며 Git에서 제외한다 |
| `plan/` | 에이전트·명령 | interview·brief·outline 승인 문서, contracts 승인 관계도, revisions 수정 기록, PROGRESS 작업 기록 |
| `YYYYMMDD_제목.pptx/.pdf` | 빌드 | 최신 성공 결과 |
| `.build/` | 빌드·에이전트 | 슬라이드 PNG·리포트·윤문과 논문 추출의 중간 파일 |

연구자가 넣은 초안 PPTX/PDF는 기존 도구로 읽는다. 텍스트·노트·표는 `uvx --from 'markitdown[pptx]' markitdown sources/<초안>.pptx`로, 슬라이드 모양은 LibreOffice로 PDF를 만들어 확인한다. 그림은 `unzip -j sources/<초안>.pptx 'ppt/media/*' -d figures/draft/`처럼 꺼내 재사용을 제안한다. 초안의 구성·표현은 연구자 요구로 기록하고, 수치는 원자료로 확인한 뒤에만 사실로 기록한다.

`uv run pptgen status tasks/<task>`는 읽기 전용이다. 처음으로 승인되지 않은 단계(`next_stage`·`next_document`)와 단계별 `issues`(승인을 막는 문제), `warnings`(보고할 권고), 가정·미해결 항목을 JSON으로 보여 준다. 이미 유효한 승인은 다시 받지 않는다.

## 기존 발표 수정과 승인 관계도

수정·되돌리기는 [수정 절차](revisions.md)를 따른다. 사용자는 페이지·토픽·문장과 원하는 변경을 자연어로 말하면 된다. 에이전트가 대상 ID·변경 원본·재검토 범위를 찾아 `plan/revisions.md`에 기록하고 반영한다. 수정 요청은 착수 지시이며 단계별 내용 승인과 구분한다.

`uv run pptgen plan tasks/<task>`는 `plan/contracts.md`에 단계별 합의 대상·문서 위치·승인 상태·의존 관계도·다음 검토 위치를 생성한다. 기존 수정 기록은 덮어쓰지 않는다. 재개·수정 후·승인 후·단계 보고 전에 갱신하며, `status` 자체는 계속 읽기 전용이다. 새 task에서는 `contracts.md`·`revisions.md`와 작업 기록 `PROGRESS.md`(Truth Model·규모)가 자동 생성된다. `PROGRESS.md`는 처음 한 번만 만들고 이후에는 에이전트가 고친다.

## 질문 방식

자료에서 먼저 답을 찾고 모르는 것만 묶어 묻는다. 새 task의 첫 질문 묶음에서 진행 방식을 묻는다.

- **같이 만들기:** Stage 2~4에서도 사용자만 아는 것(시간 배분, 사례의 깊이, 가진 그림·결과)이 나오면 모아서 묻는다.
- **핵심만:** Stage 1 질문 뒤에는 추천안으로 진행하고 단계 승인 때만 확인한다.
- **바로 초안:** Stage 1~3을 추천안으로 채워 한 번에 보고하고 초안을 빌드한다.

확인되지 않은 전제를 사용자 합의로 기록하지 않는다. 질문 예와 답변에 따른 분기는 [질문 가이드](../skills/ppt-interview/references/interview-guide.md)에 있다.

## Stage 1: 상황·의도·전제

자료를 읽고 파일 위치와 실제 관찰을 기록한다. 청중·목적·핵심 결과·성공 기준·제약 중 확인하지 못한 것을 묻는다. 웹 사진과 공개 논문은 이 단계부터 찾아도 된다. 내려받은 논문 PDF는 `figures/external/`에 두고 `uv run pptgen extract-paper TASK figures/external/PAPER.pdf`로 읽는다([외부 시각 자료](../skills/ppt-maker/references/external-visuals.md)).

`interview.md`의 `review`에는 audience·purpose·key_evidence·success_criteria·constraints를 담는다. 본문에는 확인한 상황, 사실/요구/추정/미해결의 구분, 주요 질문과 답, 합의한 전제를 남긴다. 핵심 근거가 없으면 주장을 좁히거나 해당 항목을 blocking으로 남긴다.

## Stage 2: 핵심 메시지 선택

`brief.md`에 근거 있는 메시지·스토리라인 후보를 비교하고 추천안을 표시한다. 사용자가 이미 메시지를 정했다면 그 하나만 적어도 된다. 사용자가 고르거나 수정하면 해당 후보를 갱신하고 selected_candidate·key_message·storyline을 일치시킨다. 최종 주제는 TBD로 승인할 수 없다. 메시지를 고르면 표지 제목·부제 후보를 함께 제안하고, 고른 값을 `slides.md`의 `deck`에 반영한다.

## Stage 3: 목차와 주장–근거 연결

`plan/outline.md`의 review에 ID·섹션·토픽·핵심 문장(headline)·근거·예상 seconds와 그림 계획(figure)을 순서대로 적는다. 본문에는 순서의 이유, 필요한 배경, 한계·반론을 적는다. 예상 시간이 발표 시간을 넘으면 `status`가 경고하므로 줄이거나 나누는 안을 보고에 넣는다. 발표 유형별 구성은 [발표 유형 가이드](../skills/ppt-maker/references/talk-types.md), 그림 계획은 [시각 설계](../skills/ppt-maker/references/visual-planning.md)를 참고한다.

## Stage 4: 내용·윤문·제작 QA

`slides.md`는 `# 섹션`, `## 토픽`, `### 핵심 문장`으로 쓰며 [rendering](rendering.md) 문법을 따른다. 쓰면서 핵심 문장·슬라이드 수·토픽·순서를 바꿔도 된다. 승인된 목차와 달라진 점은 `status`의 `warnings`에 나오므로 Stage 4 보고에 포함한다. 메시지나 스토리라인 자체가 바뀌면 해당 단계 문서를 고친다.

한국어 발표는 요청이 없어도 승인 요청 전에 [윤문](../skills/ppt-maker/references/polish.md)을 거친다. 사용자가 원하지 않으면 생략한다.

build는 언제든 실행할 수 있으며 내용 승인 전 결과는 초안이다. 검수는 [ppt-maker](../skills/ppt-maker/SKILL.md#빌드와-검수)를 따른다.

## 단계 보고와 승인

단계가 끝나면 **파일 링크만 주지 말고 채팅에 보고한다.** 사용자가 파일을 열지 않고도 판단할 수 있어야 한다.

- **Stage 1:** 누구에게·무엇을·어떤 판단을 받으려는지 세 줄 재진술, 자료로 확인한 것과 추정한 것, 남은 질문.
- **Stage 2:** 후보마다 한 줄 메시지와 흐름(섹션 순서), 추천과 이유, 표지 제목·부제 후보.
- **Stage 3:**
  1. 분량: 본문 N장 + 자동 M장(표지·목차·섹션 K장·감사합니다) = 총 T장, 예상 시간.
  2. 표지(제목·부제·날짜·발표자)와 목차: Chapter마다 섹션 부제, 토픽, 장수·시간.
  3. 슬라이드별 표: `ID | 상단 바 | 핵심 문장 | 들어갈 내용(불릿 요지·그림·표·수식)`.
  4. 연구자에게 요청할 그림과 준비 부담이 큰 부분.
  5. 추정·미해결, 결정이 필요한 질문.
- **Stage 4:** 표지 정보, 장별로 바뀐 점(목차 대비 바뀐 핵심 문장 포함), 윤문 결과 요약, 남은 그림 요청, 미리보기 PNG.

보고 끝에 문서 링크, `status`의 `review_hash`, 중요한 가정·미해결 항목을 붙여 명시적으로 승인받는다. 다른 질문에 대한 "예", 추천안 선택, 시간 경과를 단계 승인으로 해석하지 않는다. blocking 항목이 있으면 해결하거나 범위를 좁힌다.

```bash
uv run pptgen status tasks/<task>
uv run pptgen approve tasks/<task> --stage 1 --expected-hash <검토한-review_hash>
```

approve는 검토한 문서와 상위 입력이 지금과 같은지 확인한 뒤 승인 메타데이터를 기록한다. 원자료가 바뀌었으면 본문이 같아도 승인하지 않는다. 상위 단계가 승인된 상태여야 하며, 한 단계를 다시 승인하면 뒤 단계의 이전 승인은 draft로 돌아간다. 실패한 승인 명령은 본문을 덮어쓰지 않는다.

`sources/`가 바뀌면 Stage 1부터, `figures/`만 바뀌면 Stage 4부터 다시 확인한다. 네 단계가 모두 유효하게 승인되면 `content_approved`가 true다. 이 값은 내용 승인 상태이며 디자인·렌더 QA 결과와 별개다.

## 참고한 의도 탐색 방식

gstack [Office Hours](https://github.com/garrytan/gstack/blob/20eb6202fa8ea83a882e7c0463b722cd8a31af1e/office-hours/SKILL.md)의 구체적 증거·전제 검증·대안 비교와 superpowers [brainstorming](https://github.com/obra/superpowers/blob/bb92a77741419a4ab5f06e711a283343f1ada0c3/skills/brainstorming/SKILL.md)의 실제 상황 탐색·재진술·요구/추정 분리를 연구 발표에 맞게 적용했다. 원문은 한 번에 한 질문을 선호하지만 여기서는 질문 묶음을 쓴다. 원문은 위 고정 커밋 링크로만 참조한다.
