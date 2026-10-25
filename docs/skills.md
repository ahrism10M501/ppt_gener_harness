# 스킬 구성

## 프로젝트 스킬

| 스킬 | 역할 | 함께 있는 것 |
| --- | --- | --- |
| [ppt-interview](../skills/ppt-interview/SKILL.md) | 기획(Stage 1~3) | `references/interview-guide.md` |
| [ppt-maker](../skills/ppt-maker/SKILL.md) | 본문·빌드·검수·전달·수정(Stage 4) | `references/` 시각 설계·외부 시각 자료·윤문·발표 유형 |
| [ppt-tutorial](../skills/ppt-tutorial/SKILL.md) | 따라 하는 A-Z 튜토리얼(`review.tutorial`이 있는 task만) | 없음 |
| [ppt-charts](../skills/ppt-charts/SKILL.md) | 도식·꾸밈 차트 | `charts.py`, `diagrams.py`/`diagrams.mjs`, `examples/`, `references/local-diagrams.md` |
| [ppt-animation](../skills/ppt-animation/SKILL.md) | 교육용 GIF | `references/storyboard.md` |

템플릿에 따라 달라지는 스타일 규약은 스킬에 두지 않고 각 템플릿의 `templates/<id>/DESIGN.md`에 둔다. 스킬은 작업을 시작할 때 task의 `deck.preset`에 해당하는 DESIGN.md를 읽는다. 예전 `rvlab-*` 스킬 넷은 `ppt-interview`·`ppt-maker`·`ppt-charts`·`ppt-animation`으로 옮겼다. 기존 task 스크립트가 쓰던 경로를 위해 `skills/rvlab-charts/`의 `charts.py`·`diagrams.py`와 `docs/design/rvlab.mplstyle`은 새 위치를 가리키는 링크로만 남아 있다. 새 스크립트는 `skills/ppt-charts/`와 `templates/rvlab/plot.mplstyle`을 쓴다.

## 포함한 외부 스킬

GitHub의 고정 커밋에서 가져와 `skills/`에 보관한다. 원문에 로컬 규칙을 넣지 않고, 저작권 고지와 라이선스 전문을 보존한다. 출처·커밋·파일별 SHA-256·링크 대상은 [dependencies.yaml](../skills/dependencies.yaml)에 있고 `uv run pptgen doctor`가 매번 대조한다. 자동 다운로드로 복구·갱신하지 않으며, 갱신할 때는 새 버전의 내용·라이선스·실행을 검토한다.

| 스킬 | 출처 | 사용 범위 |
| --- | --- | --- |
| `anatomy` | [wheresryan22/anatomy](https://github.com/wheresryan22/anatomy/tree/1482e8469b0a9e0d8cc18ea2740a01423d29ae80), MIT | 기구·센서·시스템 아이소메트릭 해부도. `uv run pptgen anatomy tasks/<task> --name <fig> [--example ... \| --script ...]`(`tools/rvppt/anatomy_bridge.py`)가 `TASK/.build/editorial/anatomy/<fig>/`에서 실행해 덱 프리셋의 바탕·잉크·강조색으로 칠한 PNG·SVG를 `figures/`에, 인터랙티브 HTML을 작업 폴더에 만든다. 스크립트가 `frame-*.svg`(`figureSvg` 결과, 번호를 0으로 채움)도 쓰면 같은 이름의 GIF와 같은 크기의 대표 PNG를 함께 만든다(`--width`·`--fps`·`--hold`). `--script`와 같은 폴더의 `.mjs`는 `import`할 수 있다. |
| `im-not-ai` (`humanize-korean`) | [epoko77-ai/im-not-ai](https://github.com/epoko77-ai/im-not-ai/tree/2f3d943d08056b612a92e12bfb72ea94dd2acd18), MIT | 한국어 윤문. 절차는 [윤문](../skills/ppt-maker/references/polish.md). |
| `scientific-visualization` | [K-Dense-AI/scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills/tree/92ace75ac21efe19a620434e0ca4e356081fe807), MIT | 실제 자료의 정량 그래프: 축·단위·불확실성·내보내기. |
| `manimce-best-practices` | [adithya-s-k/manim_skill](https://github.com/adithya-s-k/manim_skill/tree/cef045011722d285692e3381d12d4d637da56e18), MIT | Manim CE 장면 구현·렌더 참조. ManimGL은 설치하지 않는다. |

외부 스킬을 task에 적용할 때는 작업 폴더(cwd)를 `TASK/.build/editorial/`로 두어 중간 파일을 격리한다. 결과는 검토한 뒤 `slides.md`에 반영한다.

## 발견 진입점

`.agents/skills/`와 `.claude/skills/`는 같은 스킬 목록을 링크로 제공한다. `humanize-korean`만 `dependencies.yaml`의 `entrypoints`에 따라 Codex판(`skills/im-not-ai/codex/skills/humanize-korean`)과 Claude판(`skills/im-not-ai/skills/humanize-korean`)을 따로 연결하며, 이 차이는 의도된 것이다. Claude 실행용 에이전트 3개는 `.claude/agents/`에 연결한다.

`uv run pptgen doctor`의 `skill_entrypoints`는 `.agents/skills/`, `.claude/skills/`, `.gemini/skills/`의 목록 차이, 깨진 링크, `SKILL.md` 누락, 일반 파일로 체크아웃된 링크를 경고한다. `.gemini/skills/`는 선택 사항이다. Git은 빈 폴더를 담지 못하므로 비어 있거나 없으면 건너뛰고, 링크를 넣으면 다른 두 목록과 같은지 확인한다.

## 도식 렌더러

`ppt-charts`는 [beautiful-mermaid](https://github.com/lukilabs/beautiful-mermaid) 1.1.3(MIT)을 로컬 렌더러로 쓴다. 버전은 `package.json`·`package-lock.json`에 고정한다.

## 정리한 스킬

참고용으로만 보관하던 office-hours·brainstorming·pptx-generator·scientific-slides·manim-composer와, 발표 제작에 쓰지 않던 문서 포맷 스킬 pdf·typst·minimax-docx·minimax-xlsx는 저장소에서 뺐다. 인터뷰 방식이 참고한 원문은 [워크플로우](workflow.md#참고한-의도-탐색-방식)의 고정 커밋 링크로 남아 있다.
