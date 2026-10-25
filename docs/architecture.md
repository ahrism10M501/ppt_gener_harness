# 코드 구조와 유지보수

사용 방법은 [README](../README.md), 설치는 [setup](setup.md), 발표 제작은 [workflow](workflow.md)와 [rendering](rendering.md)을 따른다. 이 문서는 코드와 설정의 역할을 설명한다.

## 저장소 구성

| 경로 | 역할 |
| --- | --- |
| `tools/rvppt/` | Python CLI, 문서·승인 상태, PPTX 제작과 QA |
| `tools/pptgen/` | `python -m pptgen`을 위한 범용 별칭 진입점 |
| `tools/rvppt/render.mjs` | MathJax·Mermaid·SVG 렌더링 |
| `templates/` | 보존할 원본 양식과 빌드에 쓰는 파생 reference |
| `templates/<id>/` | 템플릿 하나: `DESIGN.md`(첫 YAML 블록이 토큰, 그 아래가 스타일 규약), 파생 `reference.pptx`(슬라이드 0장), `preview.pdf/png`(레이아웃별 예시), 그 템플릿 전용 자산. 안내는 [templates/README](../templates/README.md)(rvlab의 `plot.mplstyle`·`template-manifest.json`) |
| `skills/` | 프로젝트 스킬과 고정 버전 외부 스킬·라이선스 |
| `.agents/`, `.claude/` | 에이전트별 스킬 발견 링크 |
| `tests/` | 승인·제작·파일 보존·양식의 회귀 테스트와 합성 fixture |
| `tasks/` | 발표별 원본·자료·승인 문서·산출물 |
| `graphify-out/` | 코드·문서 구조의 재생성 가능한 지식 그래프 |

## 실행 경로

`pyproject.toml`의 `pptgen`과 `rvppt` 명령은 모두 `tools/rvppt/cli.py`의 `main`을 호출한다. `tools/pptgen/__main__.py`도 같은 구현을 호출해 `python -m pptgen`을 제공한다. task 명령은 저장소의 `tasks/` 바로 아래 폴더를 대상으로 한다.

- `project.py`: 프로필에서 표지 정보를 가져와 새 task를 만든다.
- `state.py`: 네 단계 문서 스키마, 입력 해시, 승인 순서와 무효화를 검사한다.
- `plan.py`: `status`를 읽어 `plan/contracts.md`에 승인 관계도·상태를 생성하고, 덮어쓰지 않는 `plan/revisions.md` 수정 기록을 준비한다. `pptgen plan`으로 갱신하며 새 task에도 생성한다.
- `markdown.py`: Pandoc AST에서 슬라이드·본문·그림·수식·노트를 읽는다.
- `build.py`: lint, 프리셋 양식 PPTX 작성, LibreOffice 변환과 렌더 QA, 성공 산출물 게시를 수행한다. `audit` 명령은 빌드 결과에서 확대 크롭과 여백·대비 검사를 생성한다.
- `anatomy_bridge.py`: 벤더링된 anatomy 빌더를 호출해 task의 PNG·SVG·인터랙티브 HTML 도해를 프리셋 팔레트로 만들고, `frame-*.svg`가 있으면 GIF도 만든다.
- `preview.py`: 실제 폰트 선택, 그림 맞춤, PDF 변환과 contact sheet를 제공한다.
- `template.py`: `templates/<id>/DESIGN.md`의 토큰을 읽고(`design_path`, `load_tokens`) 원본을 보존하며 파생 reference를 만든다. 테마는 `style` 블록대로 RVLAB 레이아웃의 장식을 걷어 내고 배경·장식·placeholder를 다시 그린다(`apply_layout_style`). 커스텀 등록은 `templates/<id>/`에 원본·manifest·DESIGN.md(규약은 채울 틀)를 만든다. `list_presets`는 각 템플릿의 `design` 경로를 함께 돌려준다. 빌드 지문은 토큰 해시만 쓰므로 규약 본문을 고쳐도 빌드가 낡지 않는다.
- `polish.py`: 윤문 전후 AST를 비교해 구조·수치·수식·경로 보존을 검사한다.
- `doctor.py`: 도구·양식·폰트·외부 스킬 무결성을 읽기 전용으로 점검한다.
- `graph.py`: Graphify 스냅샷의 입력 변경과 task·외부 스킬 원문 제외를 점검한다.

`slides.md`가 발표 원본이다. 승인 해시는 문서 본문과 상위 입력을 함께 묶는다. 원자료 변경은 Stage 1부터, 그림만 변경하면 Stage 4부터 재확인한다. 내용 승인과 렌더 QA는 서로 다른 상태다. 빌드 실패 시 이전 성공 결과를 보존하며 사람이 편집한 PPTX를 덮어쓰지 않는다.

템플릿 구조와 `register-template`의 범위는 [templates/README](../templates/README.md#새-템플릿-추가), 렌더 QA 범위는 [toolchain](toolchain.md#렌더링-제약)에 있다.

## 유지보수 확인

```bash
uv run python -m unittest discover -s tests -v
uv run pptgen doctor
```

`tests/build_fixture.py`는 임시 디렉터리에 합성 발표를 만드는 테스트 입력이다. 자동 승인 값은 테스트용이며 연구 결과나 사용자 승인을 나타내지 않는다. 별도 QA task·이미지를 저장소에 보관할 필요 없이 테스트 실행 시 생성한다.

양식을 변경해야 할 때는 `templates/rvlab/DESIGN.md`를 검토한 뒤 다음 명령으로 파생 reference와 원본 구조 manifest를 재생성한다. 원본 `templates/rvlab/RVLAB_PPT양식.pptx`는 수정하지 않는다.

```bash
uv run python -m rvppt.template
```

Graphify는 `.graphifyignore`로 모든 task·개인 프로필·외부 스킬 원문을 제외한다. 코드나 문서를 수정하면 스냅샷이 오래될 수 있다. 그래프를 재생성한 뒤에만 `uv run pptgen graph-check --record`로 입력 해시를 기록하고, `uv run pptgen graph-check`로 확인한다. 실제 코드와 입력이 그래프보다 우선이다.
