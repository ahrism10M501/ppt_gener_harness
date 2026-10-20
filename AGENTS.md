# PPT-Gener (범용 & RVLAB PPT 하네스) 공통 지침

이 파일이 Claude Code·Codex·Gemini·Antigravity 등 모든 에이전트의 공통 지침이다. 에이전트별 진입 문서(`CLAUDE.md`, `GEMINI.md`)는 이 파일을 가리키며 규칙을 복제하지 않는다.

## 무엇을 읽을까

처음부터 모든 문서를 읽지 않는다. 하려는 일에 맞는 스킬 하나에서 시작하고, 스킬이 가리키는 문서는 필요할 때 연다. 문서와 명령의 동작은 실제 코드를 기준으로 확인한다.

| 하려는 일 | 시작점 (범용 / RVLAB 호환) |
| --- | --- |
| 발표 기획(청중·프리셋·예산·메시지·목차, Stage 1~3) | [ppt-interview](skills/ppt-interview/SKILL.md) / [rvlab-interview](skills/rvlab-interview/SKILL.md) |
| 본문 작성·빌드·4x 크리틱 QA·전달(Stage 4) | [ppt-maker](skills/ppt-maker/SKILL.md) / [rvlab-ppt](skills/rvlab-ppt/SKILL.md) |
| 기존 발표 수정·되돌리기·승인 영향 확인 | [수정 절차](docs/revisions.md), [ppt-maker](skills/ppt-maker/SKILL.md) |
| 그림 선택·제작 경로 | [시각 설계 절차](skills/rvlab-ppt/references/visual-planning.md) |
| 아이소메트릭 기구·센서·시스템 아키텍처 도해 | [anatomy](skills/anatomy/SKILL.md) (`uv run pptgen anatomy`) |
| 도넛·흐름도·타임라인 등 꾸밈 차트 (멀티 프리셋) | [ppt-charts](skills/ppt-charts/SKILL.md) / [rvlab-charts](skills/rvlab-charts/SKILL.md) |
| 개념 설명용 GIF | [ppt-animation](skills/ppt-animation/SKILL.md) / [rvlab-animation](skills/rvlab-animation/SKILL.md) |
| 웹 사진·논문 figure | [외부 시각 자료 절차](skills/rvlab-ppt/references/external-visuals.md) |
| 설치·도구 문제 | [setup](docs/setup.md), `uv run pptgen doctor` |
| 코드·양식 유지보수 | [구조](docs/architecture.md), [DESIGN.md](DESIGN.md) |

[구조](docs/architecture.md)와 `graphify-out/`는 프로젝트 구조 참고 자료다. 실제 코드와 입력이 우선이며 task 자료를 그래프에 넣지 않는다.

## 제작 흐름과 승인 (Anatomy 하네스 통합)

`slides.md`가 원본이고 PPTX는 재생성 가능한 산출물이다. task는 Overleaf 프로젝트처럼 `slides.md`·`figures/`·`sources/`·`plan/`(`interview.md`, `brief.md`, `outline.md`, `contracts.md`, `revisions.md`, `PROGRESS.md`)과 그 옆의 `YYYYMMDD_제목.pptx/.pdf`로 구성된다.
새 task는 `uv run pptgen new <slug> --title <제목> [--preset <preset_id>] [--budget <quick|standard|thorough>]`로 만들고 표지 인적사항은 `profile.yaml`에서 가져온다(`rvppt` 명령도 동일하게 동작한다).

| 단계 | 문서 | 확인할 내용 |
| --- | --- | --- |
| 0 | `plan/PROGRESS.md` | 규모/예산(`quick`/`standard`/`thorough`), 프리셋(`rvlab`/`modern-16x9` 등), Truth Model(검증된 수식·수치), 진행 상태 및 4x 크리틱 로그 |
| 1 | `plan/interview.md` | 청중·목적·근거·성공 기준·제약·전제 |
| 2 | `plan/brief.md` | 핵심 메시지와 스토리라인(후보와 추천, 또는 사용자가 정한 하나) |
| 3 | `plan/outline.md` | 슬라이드별 섹션·토픽·핵심 문장·근거·시간·그림(Chart / Anatomy / Scientific / Animation) |
| 4 | `slides.md` | 본문·그림·표·수식·출처·발표자 노트, 윤문·빌드·4x 크리틱 QA(`audit`) |

자료에서 먼저 답을 찾고 모르는 것만 묻는다. 사실·사용자 요구·에이전트 추정·미해결 항목을 구분하고, 근거 없는 주장과 숨은 전제를 짚는다. 단계가 끝나면 사용자가 파일을 열지 않고도 판단할 수 있게 채팅에 보고하고 명시적 승인을 받는다. 승인 절차와 보고 형식은 [워크플로우](docs/workflow.md), 문서 필드는 [스키마](docs/schemas.md)가 정한다.

승인은 사용자가 명시적으로 승인한 뒤 `uv run pptgen approve tasks/<task> --stage N --expected-hash <검토한-review_hash>`로만 기록한다. 승인 필드를 직접 고치지 않는다. 내용 승인(`content_approved`)은 디자인·렌더 QA 결과와 별개다.

## 멀티 프리셋 양식은 강제, 내용은 판단

**양식(코드가 강제):**
- `deck.preset`에 지정된 프리셋(`rvlab` 기본값, `modern-16x9`, `academic-16x9`, `executive-16x9`, `minimal-4x3` 또는 `pptgen register-template`로 등록한 커스텀 템플릿)의 파생 레퍼런스(`.pptx`)와 고정 토큰(`DESIGN.md` 또는 `templates/presets/<preset>.yaml`)을 따른다.
- 입력에서 좌표·폰트·색·크기·장식을 직접 지정하지 않는다. 표지·목차·섹션·감사합니다는 빌드가 만든다.
- 빌드가 측정한 넘침은 슬라이드를 나누거나 줄여서 고치며, 빌드 후 `uv run pptgen audit tasks/<task> --zoom 4`로 4배 확대 크롭(`critic-crops-sheet.png`)과 여백·대비(`critic-audit.json`)를 확인한다.

**내용(에이전트 판단):** 한 슬라이드에 메시지 하나, 불릿 5개 안팎, 짧은 핵심 문장을 기본으로 하되 lint 경고는 권고다. 문장·어조·구성·분량은 청중과 발표 목적에 맞춘다.

## 자료와 그림

- 수치·자료·인용·실험 결과를 만들지 않는다. 설명용 예시 데이터는 합성임을 명시한다. 인적사항을 추측하지 않는다.
- 기구·하드웨어·센서·다층 시스템 아키텍처 해부 도해는 벤더링된 `skills/anatomy`와 `uv run pptgen anatomy tasks/<task> --name <이름> [--example ... | --script ...]`로 300-DPI PNG·SVG·인터랙티브 HTML을 생성한다.
- 승인된 내용의 순서·구조·분류·비교를 다시 그리는 도식(흐름도·타임라인·매트릭스·카드)은 프리셋 팔레트(`--preset <preset_id>` / `charts.set_preset(...)`)에 맞춰 만든다.
- GIF는 같은 이름의 대표 PNG와 함께 `figures/`에 둔다. PPTX에는 GIF, PDF·미리보기에는 PNG가 들어간다.

## 스킬·외부 도구

프로젝트 스킬은 `skills/`가 본체이며 `.agents/skills/`와 `.claude/skills/`가 발견 진입점(symlink)이다. 외부 스킬은 고정 버전을 저장소에 포함하며 원문을 수정하지 않는다. 출처·라이선스·해시는 `skills/dependencies.yaml`, 사용 범위는 [docs/skills.md](docs/skills.md)를 따른다.

명령 목록은 `uv run pptgen --help`(또는 `uv run rvppt --help`)가 기준이다. 자주 쓰는 명령은 `new`, `presets`, `register-template`, `status`, `plan`, `approve`, `lint`, `build`, `preview`, `audit`, `anatomy`, `extract-paper`, `polish-check`, `doctor`다.

## 금지사항

원본 양식 변경, 승인 해시 조작, 에이전트가 PPTX만 직접 고치기, 인적사항 추측, task 원자료 덮어쓰기, 입력에 임의 스타일 지정, 외부 스킬 원문 임의 수정, 실제 task 내용의 Graphify 게시, 4x 확대 크롭 확인 없이 전체 썸네일만 보고 시각 검수 통과 처리를 금한다.
