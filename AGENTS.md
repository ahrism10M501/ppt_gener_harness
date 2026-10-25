# PPT-Gener 공통 지침

Claude Code·Codex·Gemini 등 모든 에이전트의 공통 지침이다. `CLAUDE.md`, `GEMINI.md`는 이 파일을 가리키며 규칙을 복제하지 않는다.

## 무엇을 읽을까

하려는 일에 맞는 스킬 하나에서 시작하고, 스킬이 가리키는 문서는 필요할 때 연다. 스킬과 문서의 절차는 기본값이다. 사용자의 요청과 발표 상황에 더 맞는 방법이 있으면 이유를 밝히고 그 방법을 쓴다. 동작은 실제 코드를 기준으로 확인한다.

| 하려는 일 | 시작점 |
| --- | --- |
| 발표 기획: 청중·프리셋·규모·메시지·목차 (Stage 1~3) | [ppt-interview](skills/ppt-interview/SKILL.md) |
| 본문 작성·빌드·검수·전달, 기존 발표 수정 (Stage 4) | [ppt-maker](skills/ppt-maker/SKILL.md) |
| 초보자가 혼자 따라 하는 A-Z 튜토리얼 (위 두 스킬에 더함) | [ppt-tutorial](skills/ppt-tutorial/SKILL.md) |
| 그림이 필요한지, 어떤 표현·도구로 만들지 | [시각 설계](skills/ppt-maker/references/visual-planning.md) |
| 흐름도·도넛·타임라인·매트릭스·카드 | [ppt-charts](skills/ppt-charts/SKILL.md) |
| 개념 설명용 GIF | [ppt-animation](skills/ppt-animation/SKILL.md) |
| 기구·센서·시스템 해부도 | [anatomy](skills/anatomy/SKILL.md), `uv run pptgen anatomy` |
| 설치·도구 문제 | [setup](docs/setup.md), `uv run pptgen doctor` |
| 템플릿 추가·수정 | [templates/README](templates/README.md) |
| 코드 유지보수 | [구조](docs/architecture.md) |

단계·승인·보고 형식은 [워크플로우](docs/workflow.md), 문서 필드는 [스키마](docs/schemas.md), `slides.md` 문법은 [rendering](docs/rendering.md)이 정한다. 명령 목록은 `uv run pptgen --help`가 기준이다(`rvppt`는 같은 명령의 옛 이름). `graphify-out/`은 구조 참고 자료일 뿐이며 실제 코드가 우선한다.

## 양식은 프리셋, 내용은 판단

- **코드가 막는 것:** 렌더할 수 없는 입력(병합 셀, 임의 좌표·크기 속성, task 밖 경로의 그림, LaTeX 매크로 정의)과 빌드가 측정한 실제 넘침. 넘치면 나누거나 줄인다.
- **프리셋이 정하는 것:** 레이아웃·폰트·기본 색. 표지·목차·섹션·감사합니다는 빌드가 만든다. 각 템플릿의 `templates/<id>/DESIGN.md`가 토큰(첫 YAML 블록)과 그 템플릿의 스타일 규약을 함께 담는다.
- **에이전트가 판단하는 것:** 그 밖의 전부. 문장·어조·구성·분량, 불릿·표·강조색(`\color`, Mermaid `style`)의 사용, 그림의 표현과 인상이 여기에 든다. lint 경고는 권고다.

task의 슬라이드·그림·차트·애니메이션을 다루는 스킬은 시작할 때 `deck.preset`의 `templates/<id>/DESIGN.md`를 읽어 컨텍스트에 올린다. 어울리는지는 청중·목적 → 그 DESIGN.md → 덱 안의 일관성 순서로 판단한다([ppt-maker](skills/ppt-maker/SKILL.md#어울림-판단)). 어떤 템플릿에만 해당하는 스타일 규칙(색 사용, 도식 모양, 그래프 스타일, 표지 점검)은 스킬이 아니라 그 템플릿의 DESIGN.md에 쓴다.

## 지킬 것

- 수치·자료·인용·실험 결과·인적사항을 만들지 않는다. 설명용 예시 데이터는 합성임을 밝힌다.
- 승인은 사용자가 명시적으로 승인한 뒤 `uv run pptgen approve`로만 기록한다. 승인 필드를 직접 고치지 않는다.
- `sources/` 원자료, 원본 양식 `templates/rvlab/RVLAB_PPT양식.pptx`, 외부 스킬 원문은 수정하지 않는다.
- 결과 PPTX만 직접 고치지 않는다. `slides.md`나 그림 원본을 고쳐 다시 빌드한다.
- 실제 task 내용을 Graphify에 넣지 않는다.

## 스킬과 외부 도구

`skills/`가 본체이고 `.agents/skills/`·`.claude/skills/`는 발견용 링크다. 외부 스킬(anatomy, humanize-korean, scientific-visualization, manimce-best-practices)은 고정 버전을 포함하며 출처·해시는 `skills/dependencies.yaml`, 사용 범위는 [docs/skills.md](docs/skills.md)에 있다. 자동 설치·다운로드는 하지 않고, 시스템 설치가 필요하면 명령과 이유를 보여 주고 확인받는다.
