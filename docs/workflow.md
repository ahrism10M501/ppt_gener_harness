# 연구 발표 제작 워크플로우

이 문서는 발표의 Stage 1~4 의도 탐색과 승인 흐름을 정의한다. 에이전트는 [rvlab-interview 스킬](../skills/rvlab-interview/SKILL.md)을 사용한다.

## 시작과 재개

기존 task가 있으면 폴더·원자료·답변을 재사용한다. 새 발표는 `uv run rvppt new <slug> --title <제목> [--date YYYY-MM-DD]`로 만든다. 표지 인적사항은 저장소 루트의 `profile.yaml`(없으면 `profile.example.yaml`을 복사해 사용자에게 채워 달라고 요청)에서 `slides.md`의 `deck`으로 복사된다. 폴더 구조는 Overleaf 프로젝트를 따른다.

| 위치 | 누가 쓰나 | 내용 |
| --- | --- | --- |
| `slides.md` | 연구자·에이전트 | 발표 원본(Overleaf의 main.tex) |
| `figures/` | 연구자·에이전트 | 연구자 그림·외부 사진·논문 figure와 출처 기록. 새 연구 그림은 제안한다 |
| `sources/` | 연구자·에이전트 | 논문·데이터·메모·초안 PPT. 에이전트는 새 공개 자료만 추가하며 기존 원자료는 읽기 전용. Git에서 제외(완성 예제만 추적) |
| `plan/` | 에이전트 | interview·brief·outline 승인 문서 |
| `YYYYMMDD_제목.pptx/.pdf` | 빌드 | 최신 성공 결과. 바로 열어 본다 |
| `.build/` | 빌드 | 슬라이드 PNG·리포트·중간 파일 |

`sources/`의 내용은 수정하지 않는다. 폴더 간 파일을 공유하거나 덮어쓰지 않는다. 연구자가 넣은 초안 PPTX/PDF는 바퀴를 새로 만들지 않고 기존 도구로 읽는다. 텍스트·노트·표는 `uvx --from 'markitdown[pptx]' markitdown sources/<초안>.pptx`, 슬라이드 모양은 LibreOffice로 PDF를 만들어 확인하고, 연구자의 그림은 `unzip -j sources/<초안>.pptx 'ppt/media/*' -d figures/draft/`처럼 꺼내 재사용을 제안한다. 초안의 구성·표현은 연구자 요구로, 수치는 원자료로 확인한 뒤에만 사실로 기록한다.

`uv run rvppt status tasks/<task>`는 읽기 전용이다. 최초 미승인/변경/누락 단계인 `next_stage`와 `next_document`, 단계별 문제·가정·미해결 항목을 JSON으로 보여준다. 사용자가 자료만 넣고 “이걸로 만들어줘”라고 해도 Stage 1부터 시작한다. 유효한 승인은 다시 받지 않는다.

## Stage 1: 상황·의도·전제

자료 확보 때 웹 사진과 공개 논문 figure를 에이전트가 직접 검색·다운로드·추출할 수 있다. PDF는 `uv run rvppt extract-paper TASK sources/PAPER.pdf`로 읽으며 [외부 시각 자료 절차](../skills/rvlab-ppt/references/external-visuals.md)에 따라 캡션·본문과 핵심 문장을 대조해 선택한다. 변환 중간 파일은 `.build/editorial/papers/`, 선택한 자산과 출처 기록은 `figures/`에 둔다. 새로운 PDF를 `sources/`에 추가하면 Stage 1부터, 그림과 출처 기록만 바꾸면 Stage 4부터 재검토한다.

자료를 먼저 읽고 파일/위치와 실제 관찰을 기록한다. 새 task의 첫 질문 묶음에서 진행 방식(같이 만들기/핵심만)을 묻는다. 같이 만들기면 Stage 2~4에서도 연구자만 아는 것을 계속 묻는다. 사용자 발언과 에이전트 추정을 구분한다. 아직 확인하지 못한 청중·목적·핵심 결과·성공/실패 기준·제약 중 3~5개를 묶어 묻는다. 질문마다 선택지와 자유 입력을 제공한다.

| 사용자 답변 또는 관찰 | 다음 행동 |
| --- | --- |
| “교수님께 진행 보고” | 실제로 받고 싶은 피드백/결정과 교수님의 사전 지식을 확인 |
| “loss가 내려가니 성공률이 오른다” | 학습 지표와 독립 평가 결과를 분리하고 메시지의 범위를 확인 |
| “결과가 좋다” | 같은 조건의 비교·표본 수·보여 줄 실제 결과 파일 확인 |
| “5분, 결과/방법/모든 ablation 포함” | 핵심 목적에 맞는 우선순위를 추천하고 본문/보조 자료 구분 |
| “주제는 아직 모르겠다” | TBD로 두고 결과·자료·판단 목적부터 탐색 |
| “질문을 줄여 달라” | 기존 근거 재사용, 추천안·가정·미해결을 제시하고 승인 경계 유지 |

같은 항목은 추가 확인 두 차례까지 진행한다. 해결되지 않으면 후보와 추천안을 제시한다. 중요한 근거를 얻지 못했다면 주장을 좁히거나 해당 항목을 blocking으로 남긴다. 확인되지 않은 전제를 사용자 합의로 기록하지 않는다.

`interview.md` 본문에는 확인한 상황, 사실/요구/추정/미해결 장부, 질문/답변/추가 확인 횟수, 합의한 전제, 승인 요약을 둔다. `review`에는 audience·purpose·key_evidence·success_criteria·constraints를 담는다. schema 예시는 [schemas.md](schemas.md)를 따른다.

## Stage 2: 핵심 메시지 선택

`brief.md`에 근거가 있는 메시지·스토리라인 후보 2~3개를 비교한다. 각 후보의 핵심 메시지·순서·근거·장단점/추가 자료를 설명하고 추천안을 표시한다. 청중과 발표 후 필요한 판단을 기준으로 추천한다.

사용자가 선택/수정하면 해당 후보 자체를 갱신하고 selected_candidate·key_message·storyline을 일치시킨다. 최종 주제는 TBD로 승인할 수 없다. 본문에는 목적·선택 이유·범위·제외 항목·전제·승인 요약을 적는다.

## Stage 3: 목차와 주장–근거 연결

`plan/outline.md`의 review에 ID·섹션·토픽·핵심 문장(headline)·근거·예상 seconds와 필요한 그림 제안(figure)을 순서대로 적는다. duration_minutes는 실제 발표 시간을 따른다. 본문에는 순서의 이유, 청중에게 필요한 배경, 한계·반론, 보조 자료 계획, 승인 요약을 적는다.

[시각 설계 절차](../skills/rvlab-ppt/references/visual-planning.md)로 각 주장에 필요한 표현과 제작 경로를 정한다. 기존 `figure`와 목차 본문에 자료·필수 시각 요소·설명과의 대응·배치 관계·검수 기준을 남기고 Stage 4에서 재사용한다. 새로운 스키마 필드나 승인 단계는 추가하지 않는다.

토픽은 상단 바와 목차에 실릴 짧은 이름이고, 핵심 문장은 그 슬라이드가 전할 결론이다([DESIGN.md](../DESIGN.md)의 이름 규칙). 같은 토픽을 여러 장에 이어 쓸 수 있다. 모든 핵심 문장이 메시지를 전달하고 근거가 해당 주장 범위를 뒷받침하는지 확인한다. 총 시간이 예산을 넘으면 내용을 줄이거나 나눈다. 랩미팅 구성과 그림 제안은 [rvlab-ppt의 랩미팅 가이드](../skills/rvlab-ppt/references/lab-meeting.md)를 따른다. 좌표·폰트·색·레이아웃 필드는 허용하지 않는다.

## Stage 4: 내용·윤문·제작 QA

`slides.md`는 `# 섹션`, `## 토픽`, `### 핵심 문장`으로 승인된 목차의 순서를 유지한다. 본문은 메시지 하나, 불릿 5개/깊이 2, 표 8행/6열, 출처와 노트를 따른다. 아직 없는 그림은 `![요청 내용](figures/이름.png)`으로 자리를 잡고 연구자에게 목록을 전달한다. [rendering](rendering.md) 문법으로 작성하고 lint로 구조와 그림 요청을 확인한다.

한국어 발표는 승인 요청 전에 [윤문 절차](../skills/rvlab-ppt/references/polish.md)로 다듬고 `uv run rvppt polish-check`로 숫자·구조·수식·경로 보존을 확인한다. 윤문은 핵심 문장(`###`)과 제목을 바꾸지 않는다.

build는 Overleaf처럼 언제든 실행할 수 있다. 연구자가 직접 고친 `slides.md`나 초안을 미리 보려 할 때 사용한다. 에이전트는 내용 승인 전 빌드 결과를 최종본으로 전달하지 않고, 사용자가 요청한 경우에만 초안 빌드를 보여 준다. 내용 승인 뒤 build로 제작·렌더 QA를 실행하고 preview의 PNG를 직접 확인한다. 수정은 입력에 반영하고 필요한 단계부터 재승인한다. 수식 미리보기·폰트 대체와 실제 PowerPoint 확인 여부를 최종 리포트에 구분한다.

## 단계 종료와 변경

각 단계 종료 때 채팅에 단계 보고를 쓴다(형식은 [rvlab-interview](../skills/rvlab-interview/SKILL.md)의 승인과 재개). 목차 단계라면 분량·Chapter·슬라이드별 내용·그림 요청을 파일을 열지 않아도 알 수 있게 쓴다. 결과 문서·검토 해시·중요한 가정·미해결 항목을 보여 명시적 승인을 받는다. blocking 항목이 있으면 해결하거나 발표 범위를 좁힌다. nonblocking 항목은 사용자에게 남은 불확실성을 밝힌 뒤 승인 대상에 포함할 수 있다.

```bash
uv run rvppt status tasks/<task>
uv run rvppt approve tasks/<task> --stage 1 --expected-hash <검토한-review_hash>
```

approve는 승인 메타데이터를 자동으로 기록한다. hash 옵션에는 status의 review_hash를 전달한다. 검토한 문서뿐 아니라 상위 자료가 같은지도 확인하므로 본문이 그대로여도 원자료가 바뀌면 승인하지 않는다. 상위 단계가 현재 승인 상태여야 하며 문서를 승인할 때 뒤 단계의 이전 승인은 draft로 바뀐다. 파일을 외부 편집한 경우 status는 저장된 상태를 바꾸지 않고 stale/invalid를 보여준다. 실패한 승인 명령은 사용자의 본문을 덮어쓰지 않는다.

자료 변경은 Stage 1부터, `figures/` 변경은 Stage 4부터 재확인한다. 아직 stage 문서가 없으면 status는 해당 문서를 만들도록 안내한다. 네 단계가 유효하게 승인되면 content_approved가 true다. 이 값은 내용 승인 상태이며 디자인/렌더 QA 결과는 별도다.

## 참고한 의도 탐색 방식

gstack [Office Hours](https://github.com/garrytan/gstack/blob/20eb6202fa8ea83a882e7c0463b722cd8a31af1e/office-hours/SKILL.md)의 구체적 증거·전제 검증·대안 비교와 superpowers [brainstorming](https://github.com/obra/superpowers/blob/bb92a77741419a4ab5f06e711a283343f1ada0c3/skills/brainstorming/SKILL.md)의 실제 상황 탐색·재진술·요구/추정 분리를 연구 발표에 맞게 적용했다. 참고 버전은 위 링크의 commit으로 고정했다.

원문은 한 번에 한 질문을 선호하지만 여기서는 사용자가 선택한 3~5개 질문 묶음을 사용한다. 전체 프레임워크를 설치하거나 자체 telemetry/외부 검토 프로세스를 실행하지 않는다.

참고 원문은 `skills/office-hours/`와 `skills/brainstorming/`에도 고정 버전으로 보관한다. 두 자료는 전체 프레임워크를 실행하는 진입점으로 등록하지 않는다. 라이선스와 사용 범위는 [외부 스킬 안내](skills.md)를 따른다.
