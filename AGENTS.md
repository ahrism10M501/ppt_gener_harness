# RVLAB PPT 공통 지침

이 파일이 Claude Code·Codex·Gemini·Antigravity 등 모든 에이전트의 공통 지침이다.
에이전트별 진입 문서는 이 파일을 가리키며 규칙을 복제하지 않는다.

## 읽는 순서

1. 이 파일과 [README](README.md)의 문서 안내를 확인한다.
2. PPT 작업이면 [rvlab-ppt 스킬](skills/rvlab-ppt/SKILL.md)과 [DESIGN.md](DESIGN.md)를 읽는다.
   목차·본문의 시각 자료는 [시각 설계 절차](skills/rvlab-ppt/references/visual-planning.md)로 필요성·표현·제작 경로·검수를 연결한다.
   도넛·흐름도·타임라인 같은 꾸밈 차트는 [차트 스킬](skills/rvlab-charts/SKILL.md)을 쓴다.
   개념 설명용 GIF를 만들거나 배치할 때는 [교육 애니메이션 스킬](skills/rvlab-animation/SKILL.md)도 읽는다.
3. 발표 기획은 [인터뷰 스킬](skills/rvlab-interview/SKILL.md), [워크플로우](docs/workflow.md), [문서 스키마](docs/schemas.md)를 따른다. 윤문은 [윤문 절차](skills/rvlab-ppt/references/polish.md)를 따른다. 문서와 명령의 동작은 실제 코드를 기준으로 확인한다.
4. 설치·도구 문제는 [setup](docs/setup.md)과 [toolchain](docs/toolchain.md)을 확인한다.
5. [구조](docs/architecture.md)와 `graphify-out/`는 프로젝트 구조 참고 자료다. 실제 코드와 입력이 우선이며 task 자료를 그래프에 넣지 않는다.

## 제작 흐름과 승인

`slides.md`가 원본이고 PPTX는 재생성 가능한 산출물이다. task는 Overleaf 프로젝트처럼 `slides.md`(원본)·`figures/`(연구자 그림·외부 사진·논문 figure)·`sources/`(논문·데이터·초안 PPT)·`plan/`(승인 문서)와 그 옆의 `YYYYMMDD_제목.pptx/.pdf`로 구성된다. 사용자가 자료를 넣은 task가 있으면 그 폴더를 재사용한다. 새 task는 `uv run rvppt new <slug> --title <제목>`으로 만들고 표지 인적사항은 `profile.yaml`에서 가져온다. task 간 파일을 공유하거나 덮어쓰지 않는다. `sources/` 원자료를 수정하지 않는다.

| 단계 | 문서 | 확인할 내용 |
| --- | --- | --- |
| 1 | `plan/interview.md` | 청중·목적·결과·근거·성공/실패 기준·제약·전제 |
| 2 | `plan/brief.md` | 핵심 메시지와 스토리라인 후보 2~3개, 추천·선택 |
| 3 | `plan/outline.md` | 슬라이드 ID·섹션·토픽·핵심 문장·근거·시간·그림 제안 |
| 4 | `slides.md` | 본문·그림 요청·표·수식·출처·발표자 노트, 윤문·QA |

먼저 자료에서 답을 찾고 아직 모르는 항목만 **3~5개 질문 묶음**으로 묻는다. 질문마다 선택지와 자유 입력을 제공한다. 사실·사용자 요구·에이전트 추정·미해결 항목을 구분한다. 근거 없는 주장, 숨은 전제, 상충하는 요구와 피해야 할 오해를 확인한다. 같은 모호함을 두 차례 확인해도 해결되지 않으면 근거 있는 후보와 추천안을 제시한다. 주제가 미정이면 TBD로 두고 결과·자료부터 탐색한다.

각 단계 종료 시 파일 링크만 주지 않고 채팅에 단계 보고(목차라면 분량·Chapter·슬라이드별 내용·그림 요청)를 쓰고, 중요한 가정·미해결 항목과 함께 승인받는다. 새 task는 첫 질문에서 진행 방식(같이 만들기/핵심만)을 묻고, 같이 만들기면 Stage 2~4에서도 연구자만 아는 것을 질문한다. 이미 승인된 의도나 선택을 다시 묻지 않는다. 질문을 줄여 달라는 요청에는 확인한 자료를 재사용하고 추천안과 남은 추정을 명시한다. 내용 승인 전 렌더링 결과를 최종본으로 전달하지 않는다. `rvppt build`는 연구자가 언제든 실행할 수 있으며, 에이전트는 사용자가 요청한 경우에만 초안 빌드를 보여 준다.

단계 문서는 [스키마](docs/schemas.md)에 따라 버전·task ID·단계·draft/approved·승인 대상 해시·상위 입력 해시와 review·가정·미해결 항목을 기록한다. `uv run rvppt status tasks/<task>`로 실제 유효 상태와 재개 위치를 확인한다. 원자료가 바뀌면 Stage 1부터, 그림 자산만 바뀌면 Stage 4부터 재확인한다.

명시적인 사용자 승인 후 `uv run rvppt approve tasks/<task> --stage N --expected-hash <검토한-review_hash>`로 기록한다. review_hash는 문서와 상위 입력을 함께 묶으므로 검토 뒤 원자료만 바뀌어도 승인하지 않는다. 단계 승인 필드를 직접 수정하지 않는다. 상위 입력이 바뀌면 이후 승인도 무효다. content_approved는 내용 승인 상태이며 디자인/렌더 QA 결과를 뜻하지 않는다. [제작 문법과 QA](docs/rendering.md)에 따라 lint·build·preview를 사용하고 PNG를 직접 확인한다.

## 양식과 자료 규칙

- 원본 `templates/RVLAB_PPT양식.pptx`는 수정하지 않는다. 파생 `templates/RVLAB_reference.pptx`를 사용한다.
- 에이전트는 내용과 정해진 레이아웃 이름만 선택한다. 입력에서 좌표·폰트·색·크기·장식을 지정하지 않는다. 고정 토큰은 DESIGN.md의 YAML이 정의한다.
- 표지·목차·섹션·상단 바는 DESIGN.md의 RVLAB 이름 규칙을 따른다. `## 토픽`은 상단 바·목차에 실릴 짧은 한 줄 이름이고, 결론은 `### 핵심 문장`에 쓴다. 표지·목차·감사합니다는 빌드가 만든다.
- 한 슬라이드에 메시지 1개, 불릿 최대 5개·깊이 2단계, 표 최대 8행(헤더 포함)·6열을 지킨다.
- 에이전트는 연구실 내부 발표에 필요한 웹 사진과 공개 논문 figure를 검색·다운로드·추출해 `figures/`에 넣을 수 있다. 캡션·본문 설명과 슬라이드 주장을 대조해 선택하고 원본 이미지·PDF와 눈으로 확인한다. 출처·figure 번호·페이지·변형 내역은 [외부 시각 자료 절차](skills/rvlab-ppt/references/external-visuals.md)를 따른다. 연구 결과 그래프를 새로 만드는 것은 사용자가 요청한 경우에만 한다. 적합한 기존 자료가 없으면 그림을 제안하고 요청 상자로 남긴다.
- 사용자가 교육 애니메이션 제작을 요청하면 GIF와 같은 이름의 대표 PNG를 `figures/`에 함께 만든다. PPTX에는 원본 GIF, PDF·미리보기에는 대표 PNG를 사용한다. 정적 QA를 PowerPoint 재생 검증으로 기록하지 않는다.
- 수치·자료·인용·실험 결과를 만들지 않는다. 예시 데이터는 합성임을 명시한다. 한글이 기본이며 영어 발표도 지원한다.
- Arial·맑은 고딕을 우선 사용한다. 누락 시 Liberation Sans·Noto Sans CJK KR 대체를 허용하고 실제 폰트 프로필을 task에 기록한다.
- 수식은 `slides.md`에 LaTeX로 작성하고 [수식 제작·검수](docs/rendering.md#수식)를 따른다.
- 빌드 실패 시 이전 성공 산출물을 보존한다. QA 수정은 Markdown/자료를 고친 뒤 재생성한다.

## 스킬·외부 도구

프로젝트 스킬은 `skills/`가 본체이며 `.agents/skills/`와 `.claude/skills/`가 발견 진입점이다. 외부 스킬 원문·라이선스·고정 버전을 보존하고 RVLAB 규칙은 프로젝트 스킬에 둔다. 외부 스킬은 고정 버전을 저장소에 포함하며 출처·라이선스·파일 해시는 `skills/dependencies.yaml`, 사용 범위는 `docs/skills.md`에 기록한다. 자동 다운로드·동기화는 하지 않는다. 한국어 윤문은 `skills/rvlab-ppt/references/polish.md` 절차로 `humanize-korean`을 쓰고 `polish-check`로 보존을 검사한다. 외부 스킬의 자체 작업 폴더는 task의 `.build/editorial/` 안에 격리한다. 수식·PDF·일반 문서 처리의 후보·라이선스·실행 의존성은 `docs/document-tools.md`를 따른다. 포함한 외부 설치·갱신 스크립트는 자동 실행하지 않으며 일반 PPTX 스킬로 RVLAB 고정 양식·승인 절차를 우회하지 않는다.


현재 명령: `uv run rvppt new SLUG --title TITLE`, `uv run rvppt status TASK`, `uv run rvppt approve TASK --stage 1|2|3|4 [--expected-hash HASH]`, `uv run rvppt lint TASK`, `uv run rvppt build TASK`, `uv run rvppt preview TASK`, `uv run rvppt polish-check TASK --before BEFORE.md`, `uv run rvppt extract-paper TASK sources/PAPER.pdf`, `uv run rvppt doctor`, `uv run rvppt graph-check`. 성공 결과는 `TASK/YYYYMMDD_제목.pptx/.pdf`, 미리보기 PNG·리포트는 `TASK/.build/output/`에 있다. 사람이 고친 산출 PPTX는 덮어쓰지 않는다. `doctor`는 도구·폰트·양식·외부 스킬 해시를 읽기 전용으로 점검한다. 완성 예제는 `tasks/261011-example-il-progress/`다. `graph-check`는 프로젝트 구조 스냅샷의 변경과 제외 규칙을 점검한다.

sudo·시스템 설치가 필요한 조치는 구체적인 명령과 이유를 제시해 확인받는다.

## 금지사항

원본 양식 변경, 승인 해시 조작, 에이전트가 PPTX만 직접 고치기, 인적사항 추측, task 원자료 덮어쓰기, 임의 스타일 입력, 외부 스킬 원문에 RVLAB 규칙 삽입, 실제 task 내용의 Graphify 게시, 수행하지 않은 OS·PowerPoint 검증을 완료했다고 기록하는 행위를 금한다.
