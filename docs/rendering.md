# Markdown 제작과 QA

`slides.md`는 Overleaf의 `main.tex`처럼 연구자와 에이전트가 함께 고치는 원본이다. 고정 크기·레이아웃·이름 규칙은 [DESIGN](../DESIGN.md), 승인 문서 형식은 [schemas](schemas.md)를 따른다. Pandoc AST로 검증하고 Pandoc이 만든 네이티브 텍스트·표·OMML 블록을 RVLAB 고정 슬롯에 배치한다. 입력에서 좌표·크기·폰트·색·레이아웃·임의 클래스/스타일을 지정할 수 없다. 글꼴을 줄여 내용을 끼워 넣지 않는다.

## 프로젝트와 표지

```bash
cp profile.example.yaml profile.yaml   # 처음 한 번: 이름·영문 이름·소속 두 줄
uv run rvppt new train-loop --title "학습루프개선 및 실험" --subtitle "Advanced Train Loop & Experiments" --date 2026-08-31
```

`tasks/260831-train-loop/`가 만들어진다. 표지 정보는 `slides.md` frontmatter의 `deck`에 복사되므로 발표마다 고칠 수 있다. 날짜는 따옴표로 감싼 `YYYY-MM-DD`다. 영어 발표는 `--lang en`이며 날짜 라벨과 마무리 문구가 영어가 된다.

```yaml
deck:
  title: 학습루프개선 및 실험
  subtitle: Advanced Train Loop & Experiments
  date: '2026-08-31'
  presenter: 홍길동 (Gildong Hong)
  affiliation:
    - 경기대학교 창의공과대학 전자공학과 N학년
    - Robotics and Vision Lab Robot Team
```

## 섹션·토픽·핵심 문장

```markdown
# 연구 배경 | Research Background

## Gradient Vanishing

### 층이 깊어질수록 앞쪽 층의 기울기가 사라진다

- 연쇄 법칙의 미분값이 층마다 곱해진다
  - Sigmoid 미분의 최댓값은 0.25다

::: notes
발표 설명과 전체 서지·DOI/URL을 적는다.
:::

### 같은 토픽의 다음 슬라이드는 상단 바를 반복한다

인라인 수식 $x^2$는 문장에 포함한다.

$$\mathcal{L} = \frac{1}{N}\sum_i (y_i-\hat y_i)^2$$

::: source
출처: 저자/기관, 연도, DOI/URL 또는 sources/자료 파일
:::
```

- `# 제목 | 부제`: 섹션 슬라이드와 목차의 `Chapter N`. 섹션이 2개 이상이면 표지 다음에 목차가 생긴다. `# Appendix`/`# 부록`은 목차에서 빠지고 `감사합니다.` 뒤에 놓인다.
- `## 토픽`: 상단 바 제목이자 목차 항목. 한 줄 이름이며 한글 2·그 외 1로 세어 20 이하다.
- `### 핵심 문장`: 슬라이드 한 장. 본문 첫 줄 `▪` 24pt이며 최대 두 줄이다. 모든 본문은 `###` 아래에 쓴다.
- `<!-- -->` 주석은 무시한다(LaTeX의 `%`).

위 예시는 문법 설명이며 실험 결과가 아니다. 본문은 일반 문단·강조·짧은 코드·불릿/번호 목록·파이프 표·LaTeX를 사용한다. 슬라이드의 불릿은 최대 5개·2단계(20pt·18pt), 표는 헤더 포함 최대 8행·6열(18pt)이다. 병합 셀과 표 안의 그림/수식/목록은 지원하지 않는다. 텍스트 셀은 왼쪽, 숫자 셀은 오른쪽 정렬하며 헤더는 파랑·흰 글자, 세로선 없이 헤더/끝 가로선만 사용한다.

`::: source`는 12pt·최대 두 줄, `::: notes`는 PPTX 발표자 노트다. 섹션 제목 아래에는 notes만 둘 수 있다. 노트 안 LaTeX는 원문 텍스트로 보존한다. 인용은 확인한 저자·연도와 링크를 본문/출처에, 전체 서지를 노트에 적는다. `[@key]`는 입력 그대로 표시하며 자동 서지 조회는 제공하지 않는다.

## 2단과 그림

레이아웃은 내용에서 정해진다. `columns` 블록이 있으면 2단, `###` 아래가 독립 그림(또는 Mermaid) 2~4개뿐이면 그림 그리드, 그 밖은 본문이다.

```markdown
:::: columns
::: column
- 실제 관찰
:::
::: column
- 제안과 남은 확인
:::
::::
```

그림은 독립된 `![짧은 설명](figures/figure.png)` 문단이다. 경로는 같은 task의 `figures/` 또는 `sources/` 아래 정규 파일이어야 하며 외부 URL·절대 경로·상위 폴더·symlink를 거부한다. PNG/JPEG/SVG/단일 페이지 PDF를 지원한다. SVG의 외부 리소스·스크립트·foreignObject는 거부한다. 3개는 가로 세 슬롯, 4개는 2×2다. 종횡비를 유지해 중앙에 맞추고 아래 0.36인치에 `그림 n. 설명`을 붙인다. 작은 그림은 유효 해상도가 150dpi 아래로 내려가지 않도록 늘리지 않고 작게 놓는다. 리포트의 `effective_dpi`로 확인하고 더 큰 원본을 구할 수 있으면 교체한다.

**그림 요청.** `figures/` 아래 아직 없는 파일을 가리키면 빌드는 그 자리에 점선 상자와 `그림 필요: 요청 / 경로`를 넣는다. 대괄호는 짧은 캡션, 따옴표 제목은 연구자에게 보낼 요청이다. `lint`와 build 리포트의 `missing_figures`가 목록을 보여 준다. 연구자가 같은 이름으로 그림을 저장하고 다시 빌드한다.

```markdown
![조건별 성공률](figures/success-by-condition.png "x: 조건(BC·ACT·제안), y: 성공률(%), 시행 수 표시. sources/eval.csv로 작성")
```

Mermaid는 단순한 흐름도에만 `mermaid` 코드 fence로 쓴다. 고정 RVLAB 색·폰트·strict 모드로 렌더하며 `.mmd`·SVG·PNG를 `.build/output/generated-assets/`에 보존한다. init/frontmatter·style/classDef/linkStyle·click 지시를 거부한다.

## GIF 애니메이션

움직임이 설명에 필요한 경우 독립 그림 문단에 GIF를 넣는다. 사용 기준과 장면 기획은 프로젝트의 애니메이션 스킬을 따른다.

```markdown
![음의 기울기 방향으로 이동하는 교육용 합성 예시](figures/gradient-descent.gif)
```

`figures/gradient-descent.png`를 같은 폴더에 함께 둔다. GIF와 PNG는 픽셀 크기가 같아야 하며, PNG는 PDF·미리보기에서 보여줄 대표 장면으로 제작자가 직접 선택한다. GIF를 자동으로 첫 프레임에 고정하지 않는다. 일반 그림과 같은 task 내부 경로·symlink 검사와 150dpi 해상도 기준을 적용한다.

GIF는 두 프레임 이상이어야 하고 모든 프레임에 양수 재생 시간이 있어야 한다. 디코딩 자원 한계는 64MiB, 600프레임, `가로 × 세로 × 프레임 수` 합계 3억 픽셀이다. 설명에 적합한 길이·반복·멈춤은 스킬에서 검토한다.

최종 PPTX에는 GIF 원본 바이트를 보존하고, 별도 `presentation-preview-copy.pptx`에서만 동일 위치의 PNG로 바꿔 PDF·PNG를 만든다. 원본 GIF·PNG는 수정하지 않는다. 빌드 리포트의 `images[].animation`에 GIF·대표 PNG 경로, 프레임 수, 전체 재생 시간, 픽셀 크기, 반복 횟수를 기록한다. `loop_count=0`은 무한 반복, 값이 없으면 반복 설정이 없는 GIF다.

PDF·PNG 검사는 대표 정지 화면의 배치와 읽기성만 확인한다. PowerPoint 슬라이드 쇼의 GIF 재생·타이밍·호환성은 별도로 확인해야 하며 자동 QA가 검증했다고 표시하지 않는다.

## 수식

수식 원본은 `slides.md`의 LaTeX다. 문장 안에서는 `$...$`, 독립 블록에서는 `$$...$$`를 사용한다.

편집형 PPTX는 Cambria Math와 고정 크기를 적용한 OMML, 호환 이미지를 함께 저장한다. `_수식호환.pptx`와 PDF는 수식 포함 블록을 300dpi 이미지로 표시하며 종횡비를 유지한다. 내용 수정은 LaTeX 원본을 고쳐 재생성한다.

생성된 PPTX와 PDF를 열어 기호·첨자·분수·배치를 확인한다. 검수에 사용한 앱과 확인 범위를 기록한다.

## 명령과 결과

```bash
uv run rvppt lint tasks/<task>      # 문법·제한·경로·그림 요청 (읽기 전용)
uv run rvppt build tasks/<task>     # 언제든 컴파일 (Overleaf의 Recompile)
uv run rvppt preview tasks/<task>   # 최신 검증 결과의 경로
```

```text
tasks/260831-train-loop/
├── slides.md                         # 원본
├── figures/                          # 연구자가 넣는 그림
├── sources/                          # 논문·데이터·초안 PPT (읽기 전용)
├── plan/                             # interview·brief·outline
├── 20260831_학습루프개선_및_실험.pptx  # 최신 성공 빌드
├── 20260831_학습루프개선_및_실험.pdf
└── .build/output/                    # 슬라이드 PNG·contact sheet·리포트
```

build는 승인 여부와 관계없이 `slides.md`를 컴파일하고 리포트의 `content_approved`에 내용 승인 상태를 기록한다. 에이전트의 승인 절차는 [workflow](workflow.md)를 따른다. 오류는 종료 코드 2로 반환한다.

빌드는 `.build/` 안 임시 폴더에서 제작·패키지 무결성·4:3/마스터/레이아웃·브랜딩 보존·그림 DPI·텍스트 측정·LibreOffice 렌더 QA를 수행한다. 실제 PDF에서 텍스트 누락/변형/잘림, 상단 바·핵심 문장·출처·캡션의 줄 수와 상자 경계를 검사한다. 성공 후에만 `.build/output/`을 교체하고 PPTX/PDF를 `slides.md` 옆에 연구실 이름 규칙(`YYYYMMDD_제목`)으로 복사한다. 제목이 바뀌면 이전 이름의 관리 산출물을 지운다.

**손으로 고친 PPTX는 덮어쓰지 않는다.** 산출 PPTX/PDF가 마지막 빌드와 다르면(PowerPoint에서 다듬은 경우) 빌드를 멈춘다. 파일 이름을 바꾸거나 옮긴 뒤 다시 빌드한다. 반복해서 고칠 내용은 `slides.md`에 반영한다. `.build/.lock`은 동시 빌드를 막으며 프로세스 강제 종료 뒤에는 실행 중인 빌드가 없는지 확인한 후 제거한다.

PNG를 직접 열어 주장–근거 연결·그래프 읽기·시각적 균형·대조도·출처를 확인한다. 자동 검사만으로 전달력이나 근거의 사실성을 입증하지 않는다. 일반 task 폴더는 통째로 Git에서 제외되며 예제 task 두 개(`261011-example-il-progress`, `2601-world-model1`)만 추적한다. 예제에서도 `.build/`는 제외하고 PPTX/PDF만 추적한다.
