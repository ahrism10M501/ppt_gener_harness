# RVLAB PPT 공통 지침

이 파일이 Claude Code·Codex·Gemini·Antigravity 등 모든 에이전트의 공통 지침이다. 에이전트별 진입 문서(`CLAUDE.md`, `GEMINI.md`)는 이 파일을 가리키며 규칙을 복제하지 않는다.

## 무엇을 읽을까

처음부터 모든 문서를 읽지 않는다. 하려는 일에 맞는 스킬 하나에서 시작하고, 스킬이 가리키는 문서는 필요할 때 연다. 문서와 명령의 동작은 실제 코드를 기준으로 확인한다.

| 하려는 일 | 시작점 |
| --- | --- |
| 발표 기획(청중·메시지·목차, Stage 1~3) | [rvlab-interview](skills/rvlab-interview/SKILL.md) |
| 본문 작성·빌드·QA·전달(Stage 4) | [rvlab-ppt](skills/rvlab-ppt/SKILL.md) |
| 그림 선택·제작 경로 | [시각 설계 절차](skills/rvlab-ppt/references/visual-planning.md) |
| 도넛·흐름도·타임라인 등 꾸밈 차트 | [rvlab-charts](skills/rvlab-charts/SKILL.md) |
| 개념 설명용 GIF | [rvlab-animation](skills/rvlab-animation/SKILL.md) |
| 웹 사진·논문 figure | [외부 시각 자료 절차](skills/rvlab-ppt/references/external-visuals.md) |
| 설치·도구 문제 | [setup](docs/setup.md), `uv run rvppt doctor` |
| 코드·양식 유지보수 | [구조](docs/architecture.md), [DESIGN.md](DESIGN.md) |

[구조](docs/architecture.md)와 `graphify-out/`는 프로젝트 구조 참고 자료다. 실제 코드와 입력이 우선이며 task 자료를 그래프에 넣지 않는다.

## 제작 흐름과 승인

`slides.md`가 원본이고 PPTX는 재생성 가능한 산출물이다. task는 Overleaf 프로젝트처럼 `slides.md`·`figures/`(연구자 그림·외부 사진·논문 figure)·`sources/`(연구자가 준 논문·데이터·초안 PPT)·`plan/`(승인 문서)와 그 옆의 `YYYYMMDD_제목.pptx/.pdf`로 구성된다. 사용자가 자료를 넣은 task가 있으면 그 폴더를 재사용한다. 새 task는 `uv run rvppt new <slug> --title <제목>`으로 만들고 표지 인적사항은 `profile.yaml`에서 가져온다. task 간 파일을 공유하거나 덮어쓰지 않는다. `sources/`의 원자료를 수정하지 않는다.

| 단계 | 문서 | 확인할 내용 |
| --- | --- | --- |
| 1 | `plan/interview.md` | 청중·목적·근거·성공 기준·제약·전제 |
| 2 | `plan/brief.md` | 핵심 메시지와 스토리라인(후보와 추천, 또는 사용자가 정한 하나) |
| 3 | `plan/outline.md` | 슬라이드별 섹션·토픽·핵심 문장·근거·시간·그림 |
| 4 | `slides.md` | 본문·그림·표·수식·출처·발표자 노트, 윤문·QA |

자료에서 먼저 답을 찾고 모르는 것만 묻는다. 사실·사용자 요구·에이전트 추정·미해결 항목을 구분하고, 근거 없는 주장과 숨은 전제를 짚는다. 단계가 끝나면 사용자가 파일을 열지 않고도 판단할 수 있게 채팅에 보고하고 명시적 승인을 받는다. 승인 절차와 보고 형식은 [워크플로우](docs/workflow.md), 문서 필드는 [스키마](docs/schemas.md)가 정한다.

승인은 사용자가 명시적으로 승인한 뒤 `uv run rvppt approve tasks/<task> --stage N --expected-hash <검토한-review_hash>`로만 기록한다. 승인 필드를 직접 고치지 않는다. 내용 승인(`content_approved`)은 디자인·렌더 QA 결과와 별개다. `rvppt build`는 언제든 실행할 수 있지만, 내용 승인 전 렌더링 결과를 최종본으로 전달하지 않는다.

## 양식은 강제, 내용은 판단

**양식(코드가 강제):** 원본 `templates/RVLAB_PPT양식.pptx`는 수정하지 않고 파생 `templates/RVLAB_reference.pptx`를 쓴다. 입력에서 좌표·폰트·색·크기·장식을 지정하지 않으며 고정 토큰은 DESIGN.md의 YAML이 정의한다. 표지·목차·섹션·감사합니다는 빌드가 만든다. `## 토픽`은 상단 바·목차에 실릴 한 줄 이름이고 결론은 `### 핵심 문장`에 쓴다. 불릿 깊이는 2단계, 표는 헤더 포함 8행·6열까지다. 빌드가 측정한 넘침은 슬라이드를 나누거나 줄여서 고친다.

**내용(에이전트 판단):** 한 슬라이드에 메시지 하나, 불릿 5개 안팎, 짧은 핵심 문장을 기본으로 하되 lint 경고는 권고다. 문장·어조·구성·분량은 청중과 발표 목적에 맞춘다. 목차 승인 뒤에도 핵심 문장의 문구는 다듬을 수 있다. 바뀐 문장은 `status`의 `warnings`에 나오므로 Stage 4 보고에 포함한다. 슬라이드 수·토픽·순서가 바뀌면 목차를 고쳐 다시 승인받는다.

## 자료와 그림

- 수치·자료·인용·실험 결과를 만들지 않는다. 설명용 예시 데이터는 합성임을 명시한다. 인적사항을 추측하지 않는다.
- 웹 사진과 공개 논문 figure는 에이전트가 직접 찾아 `figures/`에 넣는다. 내려받은 논문 PDF는 `figures/external/`에 둔다. 승인된 내용의 순서·구조·분류·비교를 다시 그리는 도식(흐름도·타임라인·매트릭스·카드)은 요청 없이 만든다. 수치를 담는 차트(도넛·깔때기)와 연구 결과 그래프, 교육용 GIF는 사용자가 요청했을 때 만든다. 적합한 자료가 없으면 그림 요청 상자로 남긴다.
- GIF는 같은 이름의 대표 PNG와 함께 `figures/`에 둔다. PPTX에는 GIF, PDF·미리보기에는 PNG가 들어간다.
- 수식은 `slides.md`에 LaTeX로 쓴다([수식](docs/rendering.md#수식)).
- 한글이 기본이며 영어 발표도 지원한다. 한국어 발표는 요청이 없어도 Stage 4 승인 요청 전에 [윤문 절차](skills/rvlab-ppt/references/polish.md)를 실행한다. 사용자가 원하지 않으면 생략한다.
- Arial·맑은 고딕을 우선하고 없으면 Liberation Sans·Noto Sans CJK KR로 대체한다. 실제 폰트는 빌드 리포트에 기록된다.

## 스킬·외부 도구

프로젝트 스킬은 `skills/`가 본체이며 `.agents/skills/`와 `.claude/skills/`가 발견 진입점(symlink)이다. 외부 스킬은 고정 버전을 저장소에 포함하며 원문을 수정하지 않는다. 출처·라이선스·해시는 `skills/dependencies.yaml`, 사용 범위는 [docs/skills.md](docs/skills.md), 수식·PDF·Office 도구는 [docs/document-tools.md](docs/document-tools.md)를 따른다. 외부 스킬의 작업 폴더는 task의 `.build/editorial/` 안에 둔다. 포함한 설치·갱신 스크립트를 자동 실행하지 않고, 일반 PPTX 스킬로 RVLAB 양식·승인 절차를 우회하지 않는다.

명령 목록은 `uv run rvppt --help`가 기준이다. 자주 쓰는 명령은 `new`, `status`, `approve`, `lint`, `build`, `preview`, `extract-paper`, `polish-check`, `doctor`다. 빌드 결과는 `TASK/YYYYMMDD_제목.pptx/.pdf`, 미리보기 PNG와 리포트는 `TASK/.build/output/`에 있다. 빌드가 실패하면 이전 성공 산출물이 보존되고, 사람이 고친 산출 PPTX는 덮어쓰지 않는다. 완성 예제는 `tasks/261011-example-il-progress/`다.

sudo·시스템 설치가 필요하면 구체적인 명령과 이유를 제시해 확인받는다.

## 금지사항

원본 양식 변경, 승인 해시 조작, 에이전트가 PPTX만 직접 고치기, 인적사항 추측, task 원자료 덮어쓰기, 입력에 임의 스타일 지정, 외부 스킬 원문에 RVLAB 규칙 삽입, 실제 task 내용의 Graphify 게시를 금한다. 수행하지 않은 검증(PowerPoint 편집·GIF 재생·OS별 실행 등)을 완료했다고 기록하지 않는다.
