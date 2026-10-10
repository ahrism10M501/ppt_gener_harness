# 포함한 외부 스킬

외부 스킬은 GitHub의 고정 커밋에서 가져와 `skills/`에 보관한다. 스킬 원문을 별도로 다운로드하거나 전역 설치할 필요는 없다. 실행에 필요한 CLI·라이브러리는 스킬과 별개이며 설치 상태를 확인한다. 원문에 RVLAB 규칙을 삽입하지 않으며, 프로젝트 규칙은 `AGENTS.md`와 `rvlab-*` 스킬이 정의한다.

## 출처와 라이선스

각 저장소의 아래 고정 커밋에 있는 `LICENSE`를 직접 확인했다. 세 저장소의 주 라이선스는 MIT이며 저작권 고지와 라이선스 전문을 그대로 포함한다.

| 자료 | 고정 커밋 | 저작권 고지 | 포함한 라이선스 |
| --- | --- | --- | --- |
| [im-not-ai](https://github.com/epoko77-ai/im-not-ai/tree/2f3d943d08056b612a92e12bfb72ea94dd2acd18) | `2f3d943d08056b612a92e12bfb72ea94dd2acd18` | Copyright (c) 2026 epoko77-ai | [MIT](../skills/im-not-ai/LICENSE) |
| [gstack / office-hours](https://github.com/garrytan/gstack/tree/20eb6202fa8ea83a882e7c0463b722cd8a31af1e/office-hours) | `20eb6202fa8ea83a882e7c0463b722cd8a31af1e` | Copyright (c) 2026 Garry Tan | [MIT](../skills/office-hours/LICENSE) |
| [superpowers / brainstorming](https://github.com/obra/superpowers/tree/bb92a77741419a4ab5f06e711a283343f1ada0c3/skills/brainstorming) | `bb92a77741419a4ab5f06e711a283343f1ada0c3` | Copyright (c) 2025 Jesse Vincent | [MIT](../skills/brainstorming/LICENSE) |

gstack의 제3자 소재 고지도 보존하기 위해 원본 [NOTICE.md](../skills/office-hours/NOTICE.md)와 [Apache-2.0 전문](../skills/office-hours/licenses/Apache-2.0.txt)을 함께 포함한다.

## 배치와 사용 범위

- **`skills/im-not-ai/`**: 원본 `skills/`, `codex/`, 참조자료, 실행용 스크립트 9개, 실행용 에이전트 3개, README와 LICENSE를 포함한다. Codex launcher와 참조 symlink가 동작하도록 원래 상대 경로 구조를 유지한다.
- **`skills/office-hours/`**: 스킬 본문, sections, 생성용 템플릿, 라이선스 고지를 포함한다. gstack 전체 CLI·telemetry·외부 리뷰에 의존하므로 RVLAB 인터뷰의 참고 자료로 보관한다. 단독 실행 스킬로 등록하지 않는다.
- **`skills/brainstorming/`**: 스킬 본문, 참조자료, visual companion 스크립트를 포함한다. RVLAB 인터뷰의 참고 자료로 보관하며 원문의 “한 번에 한 질문” 등을 프로젝트의 질문·승인 규칙보다 우선하지 않는다. visual companion은 실행하지 않는다.

`im-not-ai`의 `humanize-korean`은 `.agents/skills/`에 Codex판, `.claude/skills/`에 Claude판을 연결한다. Claude 실행용 에이전트 3개는 `.claude/agents/`에 연결한다. 홈 디렉터리나 시스템 환경은 변경하지 않는다.

RVLAB task에 적용할 때는 외부 스킬의 작업 cwd를 `TASK/.build/editorial/`로 지정해 `_workspace/`를 그 안에 격리한다. `sources/`나 승인된 문서를 직접 덮어쓰지 않고, 차이를 검토해 Markdown 원본에 반영한 뒤 필요한 단계부터 재승인한다. 절차는 [윤문 절차](../skills/rvlab-ppt/references/polish.md)이며 `uv run rvppt polish-check TASK --before BEFORE.md`가 제목·목록·표·코드·수식·링크·그림 경로·인용·숫자 보존을 Pandoc AST로 검사한다. 고정 버전 파일의 해시는 `uv run rvppt doctor`가 매번 대조한다.

## 고정 버전 관리와 검증

[dependencies.yaml](../skills/dependencies.yaml)에 출처, 커밋, LICENSE의 GitHub URL, 진입점, 사용 범위, 파일별 upstream 경로와 SHA-256, symlink의 링크 대상을 기록한다. 포함한 원본 파일은 바이트 단위로 동일하다. 갱신은 새 고정 버전의 내용·라이선스·실행 검증을 검토한 뒤 진행한다. 자동 다운로드에 의한 복구·갱신은 하지 않는다.

## 수식·PDF·Office 문서 스킬

`pdf`(OpenAI, Apache-2.0), `typst`(akilrammohan, MIT), `minimax-docx`·`minimax-xlsx`·`pptx-generator`(MiniMax, MIT)를 고정 커밋에서 추가했다. 참조자료·스크립트·템플릿과 라이선스를 원본 그대로 보존하고 같은 manifest에 해시를 기록했다. `pdf`, `typst`, `minimax-docx`, `minimax-xlsx`는 프로젝트 발견 경로에 연결하고 일반 `pptx-generator`는 RVLAB 제작 규칙과 구분해 참고용으로 보관한다.

포맷별 선택, 라이선스로 제외한 후보, 실행 의존성과 실제 검증 범위는 [문서 도구 안내](document-tools.md)를 따른다. upstream DOCX frontmatter의 `triggers` 확장 필드는 원본 보존을 위해 그대로 두며 핵심 `name`·`description`과 YAML 형식을 확인한다. 이 필드가 도구별 자동 호출을 보장하지는 않는다.

새 파일 119개를 추가했고 전체 manifest는 파일 182개와 내부 symlink 1개를 기록한다. Typst·.NET·추가 Python 패키지·OCR 모델·MCP 서버를 설치하지 않았다. 포함한 갱신/설치 스크립트는 자동 실행하지 않는다.
