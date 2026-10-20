# 포함한 외부 스킬

외부 스킬은 GitHub의 고정 커밋에서 가져와 `skills/`에 보관한다. 스킬 원문을 별도로 다운로드하거나 전역 설치할 필요는 없다. 실행에 필요한 CLI·라이브러리는 스킬과 별개이며 설치 상태를 확인한다. 원문에 로컬 규칙을 삽입하지 않으며, 프로젝트 규칙은 `AGENTS.md`와 `ppt-*` / `rvlab-*` 스킬이 정의한다.

## 출처와 라이선스

각 저장소의 아래 고정 커밋에 있는 `LICENSE`를 직접 확인했다. 주 라이선스는 MIT(및 PDF 스킬의 Apache-2.0)이며 저작권 고지와 라이선스 전문을 그대로 포함한다.

| 자료 | 고정 커밋 | 저작권 고지 | 포함한 라이선스 |
| --- | --- | --- | --- |
| [anatomy](https://github.com/wheresryan22/anatomy/tree/1482e8469b0a9e0d8cc18ea2740a01423d29ae80) | `1482e8469b0a9e0d8cc18ea2740a01423d29ae80` | Copyright (c) 2026 ryan | [MIT](../skills/anatomy/LICENSE) |
| [im-not-ai](https://github.com/epoko77-ai/im-not-ai/tree/2f3d943d08056b612a92e12bfb72ea94dd2acd18) | `2f3d943d08056b612a92e12bfb72ea94dd2acd18` | Copyright (c) 2026 epoko77-ai | [MIT](../skills/im-not-ai/LICENSE) |
| [gstack / office-hours](https://github.com/garrytan/gstack/tree/20eb6202fa8ea83a882e7c0463b722cd8a31af1e/office-hours) | `20eb6202fa8ea83a882e7c0463b722cd8a31af1e` | Copyright (c) 2026 Garry Tan | [MIT](../skills/office-hours/LICENSE) |
| [superpowers / brainstorming](https://github.com/obra/superpowers/tree/bb92a77741419a4ab5f06e711a283343f1ada0c3/skills/brainstorming) | `bb92a77741419a4ab5f06e711a283343f1ada0c3` | Copyright (c) 2025 Jesse Vincent | [MIT](../skills/brainstorming/LICENSE) |

gstack의 제3자 소재 고지도 보존하기 위해 원본 [NOTICE.md](../skills/office-hours/NOTICE.md)와 [Apache-2.0 전문](../skills/office-hours/licenses/Apache-2.0.txt)을 함께 포함한다.

## 배치와 사용 범위

- **`skills/anatomy/`**: 원본 `SKILL.md`, `kit/`(아이소메트릭 기하·4톤 셰이딩·콜아웃·부품 카탈로그), `references/`, `examples/`(14개 완성 예제), `scripts/`, `LICENSE`를 포함한다. `.agents/skills/anatomy`와 `.claude/skills/anatomy`에 연결하며, `uv run pptgen anatomy tasks/<task> --name <fig> [--example ... | --script ...]` 브리지(`tools/rvppt/anatomy_bridge.py`)가 `TASK/.build/editorial/anatomy/<fig>/`에서 실행해 슬라이드용 300-DPI PNG와 독립형 SVG를 `TASK/figures/`에 생성한다.
- **`skills/im-not-ai/`**: 원본 `skills/`, `codex/`, 참조자료, 실행용 스크립트 9개, 실행용 에이전트 3개, README와 LICENSE를 포함한다. Codex launcher와 참조 symlink가 동작하도록 원래 상대 경로 구조를 유지한다.
- **`skills/office-hours/`**: 스킬 본문, sections, 생성용 템플릿, 라이선스 고지를 포함한다. 인터뷰의 참고 자료로 보관한다. 단독 실행 스킬로 등록하지 않는다.
- **`skills/brainstorming/`**: 스킬 본문, 참조자료, visual companion 스크립트를 포함한다. 인터뷰의 참고 자료로 보관하며 visual companion은 실행하지 않는다.

### 스킬 발견 진입점

`.agents/skills/`와 `.claude/skills/`는 같은 스킬 목록을 제공한다. `im-not-ai`의 `humanize-korean`은 `skills/dependencies.yaml`의 `entrypoints.codex`와 `entrypoints.claude`에 따라 각각 Codex판(`skills/im-not-ai/codex/skills/humanize-korean`)과 Claude판(`skills/im-not-ai/skills/humanize-korean`)을 연결한다. 이 대상 차이는 의도된 것이므로 링크를 하나로 통일하지 않는다. Claude 실행용 에이전트 3개는 `.claude/agents/`에 연결한다. 홈 디렉터리나 시스템 환경은 변경하지 않는다.

`uv run pptgen doctor`의 `skill_entrypoints` 점검은 `.agents/skills/`, `.claude/skills/`, `.gemini/skills/`의 스킬 목록 차이, 깨진 링크, 대상의 `SKILL.md` 누락을 경고한다. Windows에서 링크 대신 스킬 폴더를 복사한 경우도 검사할 수 있다. Git이 링크를 대상 경로만 적힌 일반 파일로 체크아웃한 경우에는 복구 방법을 안내한다. `.gemini/skills/`는 현재 비어 있으며, 채울지는 사용자가 결정한다.

task에 적용할 때는 외부 스킬의 작업 cwd를 `TASK/.build/editorial/`로 지정해 `_workspace/`를 그 안에 격리한다. `sources/`나 승인된 문서를 직접 덮어쓰지 않고, 차이를 검토해 Markdown 원본에 반영한 뒤 필요한 단계부터 재승인한다. 절차는 [윤문 절차](../skills/rvlab-ppt/references/polish.md)이며 `uv run pptgen polish-check TASK --before BEFORE.md`가 제목·목록·표·코드·수식·링크·그림 경로·인용·숫자 보존을 Pandoc AST로 검사한다. 고정 버전 파일의 해시는 `uv run pptgen doctor`가 매번 대조한다.

## 고정 버전 관리와 검증

[dependencies.yaml](../skills/dependencies.yaml)에 출처, 커밋, LICENSE의 GitHub URL, 진입점, 사용 범위, 파일별 upstream 경로와 SHA-256, symlink의 링크 대상을 기록한다. 포함한 원본 파일은 바이트 단위로 동일한다. 갱신은 새 고정 버전의 내용·라이선스·실행 검증을 검토한 뒤 진행한다. 자동 다운로드에 의한 복구·갱신은 하지 않는다.

## 수식·PDF·Office 문서 스킬

`pdf`(OpenAI, Apache-2.0), `typst`(akilrammohan, MIT), `minimax-docx`·`minimax-xlsx`·`pptx-generator`(MiniMax, MIT)는 고정 커밋의 원본을 참조자료·스크립트·템플릿·라이선스와 함께 보존하고 manifest에 해시를 기록한다. `pdf`, `typst`, `minimax-docx`, `minimax-xlsx`는 프로젝트 발견 경로에 연결하고, 일반 `pptx-generator`는 프로젝트 제작 규칙과 구분해 참고용으로 보관한다.

## 연구 그림·애니메이션 스킬

다음 원문은 고정 커밋의 것이며 각 폴더의 `UPSTREAM_LICENSE`에 저장소 라이선스를 별도로 보존한다. 모든 원문·참조자료·스크립트의 SHA-256은 `dependencies.yaml`에 기록한다.

| 스킬 | 고정 출처 | 발견·사용 범위 |
| --- | --- | --- |
| `anatomy` | [wheresryan22/anatomy](https://github.com/wheresryan22/anatomy/tree/1482e8469b0a9e0d8cc18ea2740a01423d29ae80), MIT | `.agents/skills`·`.claude/skills`에 연결. 기구·센서·하드웨어·시스템 해부 아이소메트릭 도해 생성 및 4x 크리틱 하네스. |
| `manim-composer` | [adithya-s-k/manim_skill](https://github.com/adithya-s-k/manim_skill/tree/cef045011722d285692e3381d12d4d637da56e18), MIT | 참고용. 장면 기획·전개·강조 순서를 프로젝트 `ppt-animation` / `rvlab-animation`에서 필요할 때 읽는다. |
| `manimce-best-practices` | 같은 고정 커밋, MIT | `.agents/skills`·`.claude/skills`에 연결. Manim CE의 코드·장면·렌더링 참조. ManimGL은 설치하지 않는다. |
| `scientific-visualization` | [K-Dense-AI/scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills/tree/92ace75ac21efe19a620434e0ca4e356081fe807), MIT | `.agents/skills`·`.claude/skills`에 연결. 실제 자료의 그래프 선택·축·단위·비교·내보내기 참조. |
| `scientific-slides` | 같은 고정 커밋, MIT | 참고용. 발표 구조·그림 배치·시각 검토에 필요한 부분만 읽는다. |

## 도식 렌더러

프로젝트 스킬 `ppt-charts` / `rvlab-charts`는 [beautiful-mermaid](https://github.com/lukilabs/beautiful-mermaid) 1.1.3(MIT)을 로컬 렌더러로 사용한다.
