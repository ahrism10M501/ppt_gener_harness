# Neo City (16:9) 디자인 문서

아래 첫 YAML 블록은 빌드가 읽는 토큰이다. 크기·색·폰트·좌표와 함께 `style`이 이 템플릿의 화면 구조(배경, 장식 도형, 표지·섹션·목차·본문 제목의 위치와 글꼴)를 정한다. 그 아래는 에이전트가 "이 덱에 어울리는가"를 판단할 때 읽는 성격과 규약이다. 규약은 출발점이며, `plan/interview.md`의 청중·목적과 부딪히면 청중을 따르고 보고에 그 판단을 밝힌다.

```yaml
schema_version: 1
preset_id: neo-city
name: Neo City (16:9)
description: Dark night-city canvas with neon cyan, magenta and violet, thin grid lines and corner brackets for tech demos, AI/robotics, gaming and keynote talks
mode: preset
reference: templates/neo-city/reference.pptx
slide:
  width_in: 13.333
  height_in: 7.5
  aspect: '16:9'
  masters: 1
  original_layouts: 4
palette:
  primary: 22D3EE
  band: F472B6
  secondary: A78BFA
  section_accent: FDE047
  text: E5E7EB
  background: 0B1020
fonts:
  latin: Arial
  korean: Malgun Gothic
  fallback_latin: Liberation Sans
  fallback_korean: Noto Sans CJK KR
  code: Liberation Mono
  heading_latin: Liberation Sans Narrow
  heading_korean: Noto Sans CJK KR Black
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
  title: [0.95, 0.45, 9.0, 0.4]
  header_rule: [0.6, 1.0, 12.13, 0.05]
  body: [0.8, 1.25, 11.73, 5.75]
  content_indent: 0.25
  closing_title: [0.8, 3.0, 11.73, 1.0]
  gap: 0.3
  caption_height: 0.36
limits:
  topic_units: 28
  headline_lines: 2
  headline_korean_chars: 68
  headline_latin_chars: 130
  bullets: 5
  bullet_depth: 2
  bullet_korean_chars: 56
  bullet_latin_chars: 105
  table_rows_with_header: 8
  table_columns: 7
  toc_lines: 14
  image_min_effective_dpi: 150
  generated_image_dpi: 300
layouts:
  cover: Title Slide
  toc: 1_제목 및 내용
  section: Section Header
  content: Title and Content
  columns: Two Content
  figure_2: Two Content
  figure_3: RVLAB Figure Grid 3
  figure_4: RVLAB Figure Grid 4
labels:
  ko:
    date: '발표일시 : '
    closing: 감사합니다.
    chapter: Chapter
  en:
    date: 'Date : '
    closing: Thank you.
    chapter: Chapter
table:
  header_fill: none
  header_text: primary
  header_rule: primary
  stripe: "111833"
  rule: 1E2A44
  rule_pt: 0.75
  first_column_bold: true
slide_kinds:
  statement: {size: 40, color: text, bar: band, note: secondary}
  number: {size: 96, color: primary, note: secondary}
  quote: {size: 30, color: text, mark: band, note: secondary}
style:
  background: background
  content:
    title:
      size: 15
      bold: true
      color: primary
      font: heading
      spacing: 2.5
      anchor: ctr
    number:
      box: [12.0, 6.95, 0.6, 0.3]
      size: 11
      color: secondary
      align: r
      font: heading
    decor:
    - shape: line
      box: [0.6, 1.0, 12.13, 0]
      line: 1E2A44
      line_pt: 1
    - shape: line
      box: [0.45, 0.4, 0.3, 0]
      line: primary
      line_pt: 2
    - shape: line
      box: [0.45, 0.4, 0, 0.3]
      line: primary
      line_pt: 2
    - shape: line
      box: [12.58, 7.1, 0.3, 0]
      line: band
      line_pt: 2
    - shape: line
      box: [12.88, 6.8, 0, 0.3]
      line: band
      line_pt: 2
    - shape: rect
      box: [12.55, 0.58, 0.1, 0.1]
      fill: band
  cover:
    date:
      box: [0.8, 0.7, 8, 0.4]
      size: 13
      color: primary
      font: heading
      spacing: 2
    title:
      box: [0.8, 2.35, 11.73, 1.15]
      size: 42
      font: heading
      anchor: b
    subtitle:
      box: [0.8, 3.65, 11.73, 0.6]
      size: 22
      color: primary
    presenter:
      box: [0.8, 5.55, 8, 0.4]
      size: 16
      bold: true
    affiliation:
      box: [0.8, 5.95, 10, 0.8]
      size: 13
      color: secondary
    decor:
    - shape: line
      box: [0, 6.85, 13.333, 0]
      line: 1E2A44
      line_pt: 1
    - shape: line
      box: [0, 7.05, 13.333, 0]
      line: 1E2A44
      line_pt: 1
    - shape: line
      box: [0, 7.3, 13.333, 0]
      line: 1E2A44
      line_pt: 1
    - shape: rect
      box: [0.8, 2.1, 1.0, 0.07]
      fill: band
    - shape: rect
      box: [1.85, 2.1, 0.35, 0.07]
      fill: primary
    - shape: line
      box: [12.2, 0.6, 0, 5.4]
      line: primary
      line_pt: 1.5
    - shape: line
      box: [12.35, 1.2, 0, 4.2]
      line: band
      line_pt: 0.75
  section:
    title:
      box: [0.8, 2.95, 11.73, 1.05]
      size: 42
      font: heading
      anchor: b
    subtitle:
      box: [0.8, 4.15, 11.73, 0.6]
      size: 20
      color: primary
      font: heading
      spacing: 2
    decor:
    - shape: rect
      box: [0.8, 2.7, 1.0, 0.07]
      fill: band
    - shape: line
      box: [0, 5.6, 13.333, 0]
      line: 1E2A44
      line_pt: 1
    - shape: line
      box: [0, 6.1, 13.333, 0]
      line: 1E2A44
      line_pt: 1
    - shape: line
      box: [0, 6.7, 13.333, 0]
      line: 1E2A44
      line_pt: 1
    - shape: line
      box: [12.2, 0.6, 0, 5.4]
      line: primary
      line_pt: 1.5
  toc:
    body:
      box: [4.4, 1.3, 8.1, 5.6]
      size: 22
      bold: true
      after: 6
      level2:
        size: 17
        bold: false
        color: secondary
        after: 4
    decor:
    - shape: text
      box: [0.8, 1.3, 3.2, 0.7]
      text: INDEX
      size: 30
      font: heading
      color: primary
      spacing: 4
    - shape: rect
      box: [0.8, 1.1, 0.6, 0.06]
      fill: band
    - shape: line
      box: [4.0, 1.3, 0, 5.4]
      line: 1E2A44
      line_pt: 1
```

## 성격

테크 데모·AI/로보틱스·게임·키노트용. 어두운 밤 도시 화면 위에 네온 시안(`primary`), 마젠타(`band`), 바이올렛(`secondary`)이 빛나는 인상이다. 얇은 그리드 선과 모서리 브래킷이 HUD처럼 화면을 감싸고, 제목은 좁고 굵은 글꼴로 쓴다. 어두운 강연장에서 화면이 주인공인 발표를 가정한다.

## 어울리는 것

- 짧고 강한 핵심 문장, 큰 숫자 하나, 시스템 구조도·데이터 흐름·파이프라인.
- 데모 화면·시뮬레이션 캡처·로봇 영상 GIF. 어두운 배경이라 화면 캡처가 잘 녹아든다.
- 시안 = 주 경로·핵심, 마젠타 = 경고·대비·하이라이트, 바이올렛 = 보조 계열로 의미를 고정한다.
- 섹션 사이를 장면 전환처럼 쓰는 구성(문제 → 시스템 → 데모 → 다음 단계).

## 어울리지 않는 것

- 흰 배경 그림을 그대로 넣기(화면에 흰 구멍이 뚫린다). 투명 배경이나 어두운 배경으로 다시 그린다.
- 긴 문단과 작은 글씨. 어두운 배경에서는 같은 크기라도 더 작아 보인다.
- 네온색 여러 개를 한 도형에 섞기, 형광 노랑(`section_accent`)을 본문에 쓰기.

## 그림 인상

- 색은 `semantic_palette("neo-city")`. `background`가 어두우므로 차트 도구(`charts.py`·`diagrams.py`)는 자동으로 어두운 배경·밝은 글자를 쓴다. 다른 도구로 그린 그림도 배경 `#0B1020`, 글자 `#E5E7EB`에 맞춘다.
- 도식은 얇은 선(1~1.5pt), 각진 상자, 테두리만 있는 상자와 채운 상자 하나의 대비. 노드 강조는 시안 테두리.
- matplotlib 그래프는 어두운 배경, 옅은 그리드(`#1E2A44`), 네온 선. 선 굵기는 2pt 이상으로 둔다.
- 애니메이션은 스캔·글리치보다 데이터가 흐르는 방향을 보여 주는 움직임이 낫다.

## 빌드 후 볼 것

- 흰 배경으로 남은 그림·수식 이미지·표가 없는가.
- 바이올렛·회색 보조 글자가 4x 크롭에서 배경과 충분히 대비되는가(`critic-audit.json`).
- 좁은 제목 글꼴(Liberation Sans Narrow, Noto Sans CJK KR Black)이 실제로 쓰였는가. 발표 PC에 없으면 대체 글꼴로 바뀐다.
