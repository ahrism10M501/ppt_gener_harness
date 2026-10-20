# ppt-gener — General-Purpose & RVLAB Presentation Harness

단일 양식(RVLAB 4:3)에 고정되어 있던 기존 파이프라인을 확장하여, **범용 멀티 프리셋(16:9 와이드·4:3·RVLAB·사용자 커스텀 PPTX)** 과 **[anatomy](https://skills.wheresryan.sh/anatomy) 하네스 아키텍처(사전 규모/예산 설정 · Truth-first 모델 · `PROGRESS.md` 상태 지속성 · 4x 확대 크롭 크리틱 루프 · 아이소메트릭 기구/시스템 도해)** 를 결합한 프레젠테이션 하네스입니다.

기존 `rvppt` CLI와 `rvlab-*` 스킬(`preset: rvlab`)을 100% 하위 호환으로 유지하면서, 범용 `pptgen` CLI와 `ppt-*` 스킬을 함께 제공합니다.

> **에이전트에 붙여넣기**
> - 처음 설치: `AGENTS.md와 docs/setup.md를 읽고 셋업해줘.`
> - 범용/와이드 발표 만들기: `tasks/<폴더>의 자료로 modern-16x9 프리셋 PPT 만들어줘.`
> - RVLAB 연구실 발표 만들기: `tasks/<폴더>의 자료로 RVLAB PPT 만들어줘.`
> - 발표 수정: `tasks/<폴더>의 PDF 7쪽 그림을 더 크게 해줘. 수치와 결론은 유지해줘.` ([수정 절차와 요청 예](docs/revisions.md))

## 핵심 기능 요약

1. **멀티 디자인 프리셋 & 커스텀 `.pptx` 템플릿 등록 (`presets`, `register-template`)**
   - `rvlab` (기본값, 4:3 `10×7.5 in`): 경기대학교 RVLAB 연구실 고정 양식
   - `modern-16x9` (16:9 `13.333×7.5 in`): 컨퍼런스·테크·제품 발표용 인디고/슬레이트 와이드 양식
   - `academic-16x9` (16:9 `13.333×7.5 in`): 학회·학위논문 디펜스용 딥 네이비 와이드 양식
   - `executive-16x9` (16:9 `13.333×7.5 in`): 제안서·경영진 보고·피치덱용 틸/슬레이트 와이드 양식
   - `minimal-4x3` (4:3 `10×7.5 in`): 기관 로고 없는 깔끔한 범용 4:3 양식
   - 사용자 `.pptx` 등록: `uv run pptgen register-template my_theme.pptx --id my-theme`
2. **Anatomy 스킬 통합 & 아이소메트릭 기술 도해 (`pptgen anatomy`)**
   - [wheresryan22/anatomy](https://github.com/wheresryan22/anatomy) (MIT) 스킬을 `skills/anatomy/`에 벤더링하고, 슬라이드 삽입용 300-DPI PNG + 독립형 SVG + 인터랙티브 HTML을 한 번에 빌드합니다.
   - 예: `uv run pptgen anatomy tasks/<task> --name sensor-iso --example dial-indicator`
3. **Anatomy 하네스 규율 이식 (`PROGRESS.md` + 4x 확대 크롭 크리틱 `pptgen audit`)**
   - **Up-front Sizing (`--budget quick|standard|thorough`)**: 작업 시작 시 발표와 시각 자료의 규모를 합의합니다.
   - **Truth-First & `plan/PROGRESS.md`**: 원자료의 수식·수치·불변 조건과 세션 간 진행 상태를 `plan/PROGRESS.md`에 기록합니다.
   - **4x Close-Up Critic Loop (`uv run pptgen audit tasks/<task> --zoom 4`)**: 전체 썸네일만 보고 통과시키지 않고, 텍스트·수식·그림·출처 영역을 4배 확대한 크롭 시트(`critic-crops-sheet.png`)와 박스 여백·명도 대비(`critic-audit.json`)를 자동 검증합니다.

## 빠른 시작

```bash
# 1. 처음 한 번, 이름·영문 이름·소속·기본 프리셋 입력
cp profile.example.yaml profile.yaml

# 2. 사용 가능한 프리셋 확인
uv run pptgen presets

# 3. 새 발표 프로젝트 생성 (16:9 모던 와이드 예시, 기본값은 rvlab)
uv run pptgen new train-loop \
  --title "학습루프 개선 및 실험" \
  --subtitle "Advanced Train Loop & Experiments" \
  --preset modern-16x9 \
  --budget standard \
  --date 2026-08-31

# 4. Anatomy 아이소메트릭 도해 생성 (선택)
uv run pptgen anatomy tasks/260831-train-loop --name mechanism --example dial-indicator

# 5. 빌드 및 4x 확대 크리틱 검수
uv run pptgen build tasks/260831-train-loop
uv run pptgen audit tasks/260831-train-loop --zoom 4
```

```text
tasks/260831-train-loop/
├── slides.md        # 발표 원본 (# 섹션 / ## 상단 바 토픽 / ### 핵심 문장, deck.preset / deck.budget)
├── figures/         # 연구자 그림·외부 사진·논문 figure·anatomy 도해·차트
├── sources/         # 논문·데이터·초안 PPT (읽기 전용, Git 제외)
├── plan/            # interview.md, brief.md, outline.md, contracts.md, revisions.md, PROGRESS.md
├── 20260831_학습루프_개선_및_실험.pptx / .pdf
└── .build/          # 미리보기 PNG·build-report.json·critic-crops-sheet.png·critic-audit.json
```

완성 예제: [tasks/261011-example-il-progress](tasks/261011-example-il-progress/slides.md). `uv run pptgen status tasks/<task>`로 이어갈 단계를 확인하고 `uv run pptgen preview tasks/<task>`로 최신 PNG를 봅니다.

## 문서 찾기

| 필요한 정보 | 문서 |
| --- | --- |
| 설치·환경 점검 | [셋업](docs/setup.md) |
| 발표 기획·내용 승인 | [워크플로우](docs/workflow.md) |
| 그래프·도식·Anatomy·GIF 선택과 제작 연결 | [시각 설계 절차](skills/rvlab-ppt/references/visual-planning.md) |
| Markdown 작성·빌드·렌더 QA | [제작 문법](docs/rendering.md) |
| 단계 문서의 필드·승인 해시 | [문서 스키마](docs/schemas.md) |
| 고정 양식·디자인 토큰·프리셋 | [양식 설계](DESIGN.md) |
| 코드 구조·유지보수 | [구조](docs/architecture.md) |
| 도구 선택·제약 | [도구 구성](docs/toolchain.md) |
| 에이전트 공통 규칙 | [AGENTS.md](AGENTS.md) |

## 포함한 외부 스킬

별도 설치 없이 프로젝트의 `skills/`에서 고정 버전을 사용합니다. 원문과 저작권 고지·라이선스 전문을 보존하며 `uv run pptgen doctor`가 해시를 검증합니다.

- [anatomy](https://github.com/wheresryan22/anatomy): 정밀 아이소메트릭 기술·기구·시스템 해부 도해 및 크리틱 루프 하네스. [MIT](skills/anatomy/LICENSE).
- [im-not-ai](https://github.com/epoko77-ai/im-not-ai): 한국어 진단·윤문·검증. [MIT](skills/im-not-ai/LICENSE).
- [gstack / office-hours](https://github.com/garrytan/gstack): 인터뷰의 근거·전제·대안 탐색 참고 자료. [MIT](skills/office-hours/LICENSE), [제3자 고지](skills/office-hours/NOTICE.md).
- [superpowers / brainstorming](https://github.com/obra/superpowers): 의도 탐색·재진술 참고 자료. [MIT](skills/brainstorming/LICENSE).

고정 커밋과 파일 해시는 [dependencies.yaml](skills/dependencies.yaml), 실제 사용 범위와 제약은 [외부 스킬 안내](docs/skills.md)에 있습니다.
