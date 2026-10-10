# RVLAB 디자인 명세

아래 첫 YAML 블록은 파생 양식 생성기와 빌드가 읽는 **고정 토큰의 본체**다. 발표 입력에 좌표·폰트·색 토큰을 복사하지 않는다. 토큰 변경은 양식 변경이며 reference·QA deck·검사를 함께 재생성한다.

```yaml
schema_version: 1
source:
  path: templates/RVLAB_PPT양식.pptx
  sha256: 0c95f491b9638bc097a9761faf6e02d777a5da99af20f1b50c3262fea620b7e5
reference: templates/RVLAB_reference.pptx
slide:
  width_in: 10
  height_in: 7.5
  aspect: '4:3'
  masters: 1
  original_layouts: 4
palette:
  primary: '0070C0'
  band: '053F95'
  secondary: '5B9BD5'
  section_accent: 'FFFF00'
  text: '000000'
  background: 'FFFFFF'
fonts:
  latin: Arial
  korean: Malgun Gothic
  fallback_latin: Liberation Sans
  fallback_korean: Noto Sans CJK KR
  code: Liberation Mono
sizes_pt:
  headline: 24
  body: 20
  secondary: 18
  columns: 20
  caption: 12
  source: 12
  table: 18
  equation: 20
  code: 16
text_top_inset_pt: 4
geometry_in:
  title: [0.69, 0.10, 3.43, 0.56]
  header_rule: [0.85, 0.36, 9.15, 0.05]
  body: [0.33, 0.99, 9.34, 6.03]
  content_indent: 0.25
  closing_title: [0.45, 3.37, 9.09, 0.57]
  gap: 0.24
  caption_height: 0.36
limits:
  topic_units: 20
  headline_lines: 2
  headline_korean_chars: 52
  headline_latin_chars: 100
  bullets: 5
  bullet_depth: 2
  bullet_korean_chars: 42
  bullet_latin_chars: 80
  table_rows_with_header: 8
  table_columns: 6
  toc_lines: 14
  image_min_effective_dpi: 150
  generated_image_dpi: 300
layouts:
  cover: Title Slide
  toc: '1_제목 및 내용'
  section: Section Header
  content: Title and Content
  columns: Two Content
  figure_2: Two Content
  figure_3: RVLAB Figure Grid 3
  figure_4: RVLAB Figure Grid 4
labels:
  ko: {date: '발표일시 : ', closing: '감사합니다.', chapter: Chapter}
  en: {date: 'Date : ', closing: 'Thank you.', chapter: Chapter}
```

## 원본과 파생 양식

원본은 10×7.5인치·4:3, 마스터 1개, 레이아웃 4개, 표본 슬라이드 5개다. 레이아웃 이름은 `제목 슬라이드`, `1_제목 및 내용`, `2_제목 및 내용`, `OBJECT`다. 실제 좌표·폰트·색은 [template-manifest.json](docs/design/template-manifest.json)에 있다. 연구실 실제 발표 참고 자료는 `templates/examples/`에 있다.

원본 레이아웃은 변경하지 않는다. 파생 reference는 표본 슬라이드·노트·Google 메타데이터만 제거하고 Pandoc용 이름의 파생 레이아웃을 추가한다. 로고·파란 띠·노란 부제·상단 장식·하단 띠·테마는 그대로 둔다. 파생 본문 레이아웃은 **원본 표본과 같은 상단 바**를 쓴다. 제목 칸은 `[0.69, 0.10, 3.43, 0.56]`의 흰 바탕 24pt 굵은 글자이고, 그 뒤의 파란 선이 제목 오른쪽으로 이어진다. 제목 칸을 넓히거나 선을 옮기지 않는다.

표지·목차·섹션·마무리 슬라이드는 원본 레이아웃의 placeholder에 텍스트만 채운다. 글꼴·크기·색·정렬은 레이아웃에서 상속한다.

## 슬라이드 문법과 이름 규칙

`templates/examples/`의 연구실 발표 네 편과 원본 표본에서 확인한 규칙이다. 작성자는 Markdown 제목 수준만 고르고, 표지·목차·마무리는 빌드가 만든다.

| 슬라이드 | 입력 | 규칙 |
| --- | --- | --- |
| 표지 | `slides.md` frontmatter의 `deck` | 왼쪽 위 `발표일시 : YYYY.MM.DD`, 파란 띠의 제목(흰색)·부제(노란색), 발표자 `이름 (English Name)`, 소속 두 줄. 인적사항은 `rvppt new`가 `profile.yaml`에서 채운다. |
| 목차 | 자동 | 왼쪽 `Contents` 패널, 오른쪽에 `▪ Chapter N: 섹션 제목`(굵게)과 그 섹션의 `• 토픽`. 섹션 이름과 같은 토픽은 생략한다. 섹션이 2개 이상일 때만 만든다. 14줄을 넘으면 토픽을 모두 생략한다. |
| 섹션 | `# 섹션 제목 \| 부제` | 파란 띠의 흰 제목과 노란 부제. 섹션 제목은 목차의 Chapter 이름이다. 부제는 영문 이름이나 한 줄 설명이다. |
| 본문 | `## 토픽` + `### 핵심 문장` | 상단 바에는 **짧은 토픽 이름**(예: `GS-ICP SLAM`, `Gradient Vanishing`, `LoRA`)을 쓴다. 같은 토픽의 슬라이드가 이어지면 상단 바도 반복된다. 본문 첫 줄은 `▪` 24pt 핵심 문장이고 그 아래 내용은 한 칸 들여 쓴다. |
| 마무리 | 자동 | `감사합니다.`(영어 발표는 `Thank you.`). `# Appendix` 또는 `# 부록` 섹션이 있으면 그 앞에 둔다. |

상단 바 토픽은 **한 줄**이다. 한글 2·그 외 1로 세어 20 이하(약 한글 10자·영문 20자)로 쓴다. 문장이나 결론이 아니라 목차에 그대로 실릴 주제 이름이다. 결론형 메시지는 `###` 핵심 문장에 쓴다. 핵심 문장은 최대 두 줄이다.

```markdown
# 연구 배경 | Research Background

## Gradient Vanishing

### 층이 깊어질수록 앞쪽 층의 기울기가 사라진다

- 연쇄 법칙의 미분값이 층마다 곱해진다
  - Sigmoid 미분의 최댓값은 0.25다
```

## 본문·제목·언어

슬라이드당 주장 1개를 핵심 문장으로 쓴다. 글꼴을 자동 축소하지 않는다. 길면 메시지를 줄이거나 슬라이드를 나눈다. 본문은 최대 5개 불릿·깊이 2단계, 1단 20pt·2단 18pt다. 긴 문장 대신 짧은 구를 쓰되 의미·인과·불확실성을 지우지 않는다. 약어는 처음 나올 때 정의한다. 한국어가 기본이고 영어 발표도 허용한다. 한·영 폰트는 각각 맑은 고딕·Arial이다.

폰트 누락 시 Latin은 Liberation Sans, 한국어는 Noto Sans CJK KR로 대체하고 리포트에 기록한다. 숫자는 천 단위·소수 자릿수를 통일하고 값과 단위 사이에 공백을 둔다(예: `25 ms`, `0.8 m`). 원자료의 단위와 유효숫자를 보존한다.

## 표·그래프·그림

표는 헤더 포함 8행·6열 이하, 18pt로 작성한다. 가로 구분선을 최소화하고 세로선은 피한다. 텍스트는 왼쪽, 수치는 오른쪽 정렬하고 비교 기준과 단위를 헤더에 적는다. 최선 값만 굵게 표시한다. 표가 넘치면 분할한다.

그림은 연구자가 만든다. 에이전트는 필요한 그림을 **제안**하고 슬라이드에 `![그림 설명](figures/파일명.png)`로 자리를 잡는다. 파일이 아직 없으면 빌드는 점선 상자에 요청 내용을 표시하고 리포트의 `missing_figures`에 남긴다. 연구자가 같은 이름으로 그림을 넣고 다시 빌드한다. 사용자가 요청한 경우에만 에이전트가 자료로 그래프를 그리며, 이때 [rvlab.mplstyle](docs/design/rvlab.mplstyle)을 쓴다.

그래프는 축·범례·단위를 표시하고 색만으로 구분하지 않는다. 원자료에서 오차·표본 수를 확인한 경우만 기재한다. 강조는 primary, 보조는 secondary, 추가 계열은 검정과 선 모양으로 구분한다. 노랑은 표지·섹션 부제에만 사용한다.

SVG/PDF 원본을 보존하고 호환 PNG를 함께 만든다. 삽입 지점의 유효 해상도는 최소 150dpi다. 작은 그림은 늘리지 않고 그만큼 작게 놓는다. 생성 PNG는 300dpi를 목표로 한다. 캡션·출처는 12pt, `그림 n. 설명`과 `출처: 저자/기관, 연도, 링크` 형식이다. 논문 그림은 출처를 반드시 달고, 전체 서지·DOI/URL은 노트에 둔다.

그림 슬롯은 핵심 문장 아래 본문 영역을 균등 분할한다. 1개는 전체, 2개는 좌우, 3개는 가로 3개, 4개는 2×2다. 간격 0.24인치, 각 슬롯 아래 0.36인치는 캡션이다. 그림은 자르거나 늘리지 않고 종횡비를 보존해 중앙에 맞춘다.

## 수식·코드·다이어그램

입력 수식은 LaTeX다. 짧은 인라인 수식은 문장 안에, 주요 수식은 20pt 블록으로 표시한다. 번호는 참조가 필요한 블록에만 붙이고 바로 아래에 변수 정의를 둔다. OMML을 우선하고 변환 문제가 있으면 고해상도 이미지 fallback을 허용하며 리포트에 기록한다. LibreOffice에서는 네이티브 수식이 안 보일 수 있으므로 preview copy에만 이미지 대체를 적용한다.

코드는 핵심 부분만 16pt 고정폭으로 표시한다. 긴 코드는 자료 링크로 옮긴다. Mermaid는 단순한 흐름도에만 쓰고 RVLAB 색·폰트를 적용한다.

## 금지·검사

양식 외 폰트/색, 임의 좌표, 자동 글꼴 축소, 그림 늘리기·무단 자르기, 새 그림자·3D·장식 아이콘, 무의미한 강조를 추가하지 않는다. 상단 바 제목을 문장으로 쓰거나 두 줄로 만들지 않는다. 대조도·출처·폰트·그림 해상도·슬라이드 경계·텍스트 넘침을 실제 렌더로 검사한다.
