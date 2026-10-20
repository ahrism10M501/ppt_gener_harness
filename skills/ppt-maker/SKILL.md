---
name: ppt-maker
description: 범용 멀티 템플릿(16:9, 4:3, RVLAB, 사용자 커스텀 PPTX) 양식의 발표를 만들거나 수정할 때 slides.md와 PPTX를 제작한다. 주장과 근거에서 시각 자료(차트, 과학 그래프, anatomy 아이소메트릭 도해, 애니메이션)를 설계·연결하고, 4x 확대 크롭 크리틱 루프(audit)로 실제 슬라이드를 검수한다.
---

# 범용 PPT 제작 & 크리틱 하네스 (`ppt-maker`)

`slides.md`를 단일 원본(Source of Truth)으로 유지하며, 선택된 프리셋(`rvlab`, `modern-16x9`, `academic-16x9`, `executive-16x9`, `minimal-4x3` 또는 등록된 커스텀 템플릿)의 PPTX·PDF·검수 리포트를 생성한다.
Felo 등 상용 AI PPT 스킬의 장점(다양한 비율·테마 대응, 구조화된 레이아웃)과 `anatomy` 스킬의 하네스 규율(**Truth-first**, **PROGRESS.md 상태 추적**, **4x 확대 크롭 기반 시각 크리틱 루프**)을 결합한다.

## 시작 및 상태 복원

- 세션을 시작하거나 재개할 때 먼저 `tasks/<task>/plan/PROGRESS.md`와 `tasks/<task>/plan/contracts.md`, 그리고 `uv run pptgen status tasks/<task>`를 확인한다.
- Stage 1~3이 미승인이면 [ppt-interview](../ppt-interview/SKILL.md)부터 진행한다.
- 새 발표는 `uv run pptgen new <slug> --title <제목> [--preset modern-16x9] [--budget standard]`로 만든다.
- 사용자가 기존 `.pptx` 템플릿을 주면 `uv run pptgen register-template <file.pptx> --id <custom-id>`로 등록한 뒤 `slides.md`의 `deck.preset: <custom-id>`로 설정한다.

## 슬라이드 문법과 이름 규칙

문법은 `docs/rendering.md`, 기본 기하·타이포 토큰은 각 프리셋(`templates/presets/<preset>.yaml` 또는 `DESIGN.md`)을 따른다. 표지·목차·감사합니다 슬라이드는 빌드가 자동 생성한다.

- `# 섹션 | 부제`: 섹션 슬라이드이자 목차의 Chapter.
- `## 토픽`: 상단 바 제목이자 목차 항목(한글 10자·영문 20자 이내 짧은 이름).
- `### 핵심 문장`: 슬라이드 한 장의 결론(본문 첫 줄 ▪ 24pt, 두 줄 이내).
- 좌표·폰트·색·레이아웃을 `slides.md`에 하드코딩하지 않으며, 근거 없는 수치나 인용을 만들지 않는다.

## 시각 자료 라우팅 (Visual Harness)

글이나 표만으로 충분하면 그림을 만들지 않는다. 시각 자료가 필요한 슬라이드는 목적에 따라 아래 도구를 연결한다:

1. **절차·흐름·비교 카드·비율 (`[ppt-charts]`)**:
   - 흐름도·분기·상태도는 `skills/rvlab-charts/diagrams.py --preset <preset>`으로 렌더링한다.
   - 도넛·타임라인·2x2 매트릭스·퍼널·비교 카드는 `skills/rvlab-charts/charts.py`의 `set_preset("<preset>")`을 호출해 프리셋 팔레트에 맞춰 생성한다.
2. **기구·하드웨어·센서·아키텍처 아이소메트릭 도해 (`[anatomy]`)**:
   - 로봇 하드웨어, 센서 구조, 광학/기계 메커니즘, 다층 시스템 아키텍처처럼 **내부 구조와 작동 원리**를 보여줘야 할 때는 벤더링된 [anatomy](../anatomy/SKILL.md) 스킬과 브리지를 사용한다.
   - 실행: `uv run pptgen anatomy tasks/<task> --name <fig_name> [--example <name> | --script <script.mjs>]`
   - 결과물: 슬라이드 삽입용 300-DPI `figures/<fig_name>.png`, 벡터 `figures/<fig_name>.svg`, 그리고 발표 보충용 인터랙티브 HTML(`tasks/<task>/.build/editorial/anatomy/<fig_name>/index.html`)이 함께 생성된다.
3. **정량 실험·통계 그래프 (`[scientific-visualization]`)**:
   - 실험 결과·오차 막대·분포 비교는 [scientific-visualization](../scientific-visualization/SKILL.md)를 사용한다.
4. **최적화·상태 전이·기하 변환 애니메이션 (`[ppt-animation]`)**:
   - 정적 그림으로 전달할 수 없는 연속 변화는 [ppt-animation](../ppt-animation/SKILL.md)으로 `figures/<name>.gif`와 대표 정적 상태 `figures/<name>.png`를 함께 만든다.

## 제작 및 4x 확대 크리틱 QA 루프 (`build` + `audit`)

전체 슬라이드 썸네일(contact-sheet)만 보고 "깔끔하다"고 판단하는 것은 금지한다(`anatomy`의 Anti- Rationalization 규칙). 반드시 다음 3단계 검수를 수행한다:

1. **컴파일 및 기본 렌더 QA**:
   ```bash
   uv run pptgen lint tasks/<task>
   uv run pptgen build tasks/<task>
   ```
2. **4x 확대 크롭 및 여백·대비 감사 (`audit`)**:
   ```bash
   uv run pptgen audit tasks/<task> --zoom 4
   ```
   - `audit` 명령은 각 슬라이드의 헤드라인·본문·그림·출처 영역을 **4배 확대(300 DPI)한 크롭 이미지**(`crops/*.png`)와 크롭 시트(`critic-crops-sheet.png`), 그리고 상자 간 최소 여백·명도 대비 리포트(`critic-audit.json`)를 생성한다.
3. **시각 검수 및 `plan/PROGRESS.md` 기록**:
   - `uv run pptgen preview tasks/<task>`와 `critic-crops-sheet.png`를 직접 열어 텍스트 잘림, 라벨 겹침, 화살표 침범, 작은 글씨 가독성을 확인한다.
   - 발견된 문제와 수정 내역을 `tasks/<task>/plan/PROGRESS.md`의 **Critic Loop & 4x Crop Audit Log**에 기록한다.
