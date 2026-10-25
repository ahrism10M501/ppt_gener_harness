# Retro Editorial (16:9) 디자인 문서

아래 첫 YAML 블록은 빌드가 읽는 토큰이다. 크기·색·폰트·좌표와 함께 `style`이 이 템플릿의 화면 구조(배경, 장식 도형, 표지·섹션·목차·본문 제목의 위치와 글꼴)를 정한다. 그 아래는 에이전트가 "이 덱에 어울리는가"를 판단할 때 읽는 성격과 규약이다. 규약은 출발점이며, `plan/interview.md`의 청중·목적과 부딪히면 청중을 따르고 보고에 그 판단을 밝힌다.

```yaml
schema_version: 1
preset_id: retro
name: Retro Editorial (16:9)
description: Cream paper, serif type, terracotta, mustard and deep teal stripes with framed pages for storytelling, history, culture and lecture talks
mode: preset
reference: templates/retro/reference.pptx
slide:
  width_in: 13.333
  height_in: 7.5
  aspect: '16:9'
  masters: 1
  original_layouts: 4
palette:
  primary: A84432
  band: 2F5D62
  secondary: 8A5A12
  section_accent: E0A458
  text: 2B2118
  background: F4ECD8
fonts:
  latin: Liberation Serif
  korean: Noto Serif CJK KR
  fallback_latin: DejaVu Serif
  fallback_korean: Noto Serif CJK KR
  code: Liberation Mono
  heading_latin: Noto Serif CJK KR
  heading_korean: Noto Serif CJK KR
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
  title: [0.75, 0.38, 9.0, 0.55]
  header_rule: [0.75, 1.0, 11.83, 0.05]
  body: [0.75, 1.3, 11.83, 5.55]
  content_indent: 0.25
  closing_title: [0.8, 3.05, 11.73, 0.9]
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
  header_fill: band
  header_text: background
  header_rule: band
  stripe: EADFC4
  rule: C9B99A
  rule_pt: 0.75
  first_column_bold: true
slide_kinds:
  statement: {size: 38, color: band, bar: primary, note: secondary}
  number: {size: 88, color: primary, note: band}
  quote: {size: 30, color: text, mark: primary, note: band}
style:
  background: background
  content:
    title:
      size: 18
      bold: true
      color: band
      font: heading
      spacing: 1
      anchor: ctr
    number:
      box: [11.98, 6.98, 0.6, 0.3]
      size: 11
      color: primary
      align: r
      font: heading
    decor:
    - shape: rect
      box: [0.3, 0.25, 12.733, 7.0]
      line: band
      line_pt: 1.5
    - shape: line
      box: [0.75, 0.98, 11.83, 0]
      line: band
      line_pt: 2.25
    - shape: line
      box: [0.75, 1.06, 11.83, 0]
      line: band
      line_pt: 0.75
    - shape: rect
      box: [10.6, 0.55, 0.6, 0.12]
      fill: primary
    - shape: rect
      box: [11.25, 0.55, 0.6, 0.12]
      fill: section_accent
    - shape: rect
      box: [11.9, 0.55, 0.6, 0.12]
      fill: band
  cover:
    date:
      box: [0.8, 0.95, 11.73, 0.4]
      size: 13
      color: band
      align: ctr
      font: heading
      spacing: 1
    title:
      box: [0.8, 2.45, 11.73, 1.0]
      size: 38
      bold: true
      align: ctr
      font: heading
      anchor: b
    subtitle:
      box: [0.8, 3.65, 11.73, 0.6]
      size: 20
      color: primary
      align: ctr
      font: heading
    presenter:
      box: [0.8, 5.0, 11.73, 0.4]
      size: 16
      bold: true
      align: ctr
    affiliation:
      box: [0.8, 5.4, 11.73, 0.8]
      size: 13
      color: band
      align: ctr
    decor:
    - shape: rect
      box: [0, 0, 13.333, 0.28]
      fill: primary
    - shape: rect
      box: [0, 0.28, 13.333, 0.14]
      fill: section_accent
    - shape: rect
      box: [0, 0.42, 13.333, 0.1]
      fill: band
    - shape: rect
      box: [0, 6.98, 13.333, 0.1]
      fill: band
    - shape: rect
      box: [0, 7.08, 13.333, 0.14]
      fill: section_accent
    - shape: rect
      box: [0, 7.22, 13.333, 0.28]
      fill: primary
    - shape: line
      box: [5.17, 4.5, 3.0, 0]
      line: text
      line_pt: 1
    - shape: ellipse
      box: [6.59, 4.42, 0.16, 0.16]
      fill: primary
  section:
    title:
      box: [0.8, 2.95, 11.73, 1.0]
      size: 38
      bold: true
      color: background
      align: ctr
      font: heading
      anchor: b
    subtitle:
      box: [0.8, 4.15, 11.73, 0.6]
      size: 20
      color: section_accent
      align: ctr
      font: heading
    decor:
    - shape: rect
      box: [0, 0, 13.333, 7.5]
      fill: band
    - shape: rect
      box: [0.45, 0.45, 12.433, 6.6]
      line: section_accent
      line_pt: 1.5
    - shape: rect
      box: [0.6, 0.6, 12.133, 6.3]
      line: section_accent
      line_pt: 0.5
    - shape: ellipse
      box: [6.57, 2.55, 0.2, 0.2]
      fill: primary
  toc:
    body:
      box: [3.4, 1.6, 8.5, 5.2]
      size: 22
      bold: true
      font: heading
      after: 6
      level2:
        size: 17
        bold: false
        color: band
        after: 4
    decor:
    - shape: rect
      box: [0.3, 0.25, 12.733, 7.0]
      line: band
      line_pt: 1.5
    - shape: text
      box: [0.75, 0.55, 11.83, 0.7]
      text: Contents
      size: 30
      bold: true
      font: heading
      color: band
      align: ctr
    - shape: line
      box: [0.75, 1.3, 11.83, 0]
      line: band
      line_pt: 2.25
    - shape: line
      box: [0.75, 1.38, 11.83, 0]
      line: band
      line_pt: 0.75
```

## 성격

이야기·역사·문화·강의·회고 발표용. 잡지나 오래된 포스터처럼 천천히 읽히는 인상을 준다. 크림색 종이 바탕, 세리프 글꼴, 테라코타(`primary`)·머스터드(`section_accent`, 짙은 글자용 `secondary`)·딥 틸(`band`) 세 줄 띠, 이중 테두리 액자가 기본이다. 섹션은 틸 바탕에 크림색 글자로 장을 넘기는 느낌을 준다.

## 어울리는 것

- 서사가 있는 구성: 배경 → 사건·전환점 → 의미. 핵심 문장은 문장다운 문장으로.
- 연표·타임라인, 인물·사례 카드, 인용문 한 줄을 크게 둔 슬라이드.
- 옛 사진·문서 스캔·지도 같은 질감 있는 그림. 액자 안에 여백을 두고 배치한다.
- 강조는 테라코타 한 곳, 구분은 틸, 머스터드는 작은 포인트로만.

## 어울리지 않는 것

- 네온·형광색, 사진 위 반투명 그라데이션, 채도 높은 아이콘.
- 수치가 빽빽한 대시보드형 표. 숫자는 몇 개만 크게, 나머지는 노트로.
- 산세리프로 바꾼 제목, 크림 바탕을 흰색으로 덮는 그림 배경(그림은 투명 배경이나 크림 배경으로 만든다).

## 그림 인상

- 색은 `semantic_palette("retro")`. 계열 순서는 테라코타 → 틸 → 머스터드 → 회갈색. 배경은 크림(`background`)으로 맞춰 흰 사각형이 뜨지 않게 한다.
- 도식은 각진 상자와 두꺼운 선(2pt 안팎), 화살표는 단순하게. 둥근 카드는 피한다.
- matplotlib 그래프는 크림 배경, 세리프 글꼴, 굵은 축선, 격자 없음. 막대는 단색 채움.
- 애니메이션은 느린 전환, 종이 위에 그려지는 듯한 순차 등장이 어울린다.

## 빌드 후 볼 것

- 세리프 한글이 4x 크롭에서 뭉개지지 않는가(18pt 이하 보조 글자).
- 그림이 흰 배경으로 떠 보이지 않는가.
- 섹션의 크림 글자와 틸 바탕 대비가 충분한가(`critic-audit.json`).
