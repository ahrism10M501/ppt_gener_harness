# Modern Minimal (16:9) 디자인 문서

아래 첫 YAML 블록은 빌드가 읽는 토큰이다. 크기·색·폰트·좌표와 함께 `style`이 이 템플릿의 화면 구조(배경, 장식 도형, 표지·섹션·목차·본문 제목의 위치와 글꼴)를 정한다. 그 아래는 에이전트가 "이 덱에 어울리는가"를 판단할 때 읽는 성격과 규약이다. 규약은 출발점이며, `plan/interview.md`의 청중·목적과 부딪히면 청중을 따르고 보고에 그 판단을 밝힌다.

```yaml
schema_version: 1
preset_id: modern-minimal
name: Modern Minimal (16:9)
description: White, generous whitespace, near-black type and one electric-blue accent for tech talks, product and general presentations
mode: preset
reference: templates/modern-minimal/reference.pptx
slide:
  width_in: 13.333
  height_in: 7.5
  aspect: '16:9'
  masters: 1
  original_layouts: 4
palette:
  primary: 2B59FF
  band: '111827'
  secondary: 6B7280
  section_accent: 2B59FF
  text: '111827'
  background: FFFFFF
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
  title: [0.45, 0.42, 9.0, 0.4]
  header_rule: [0.45, 0.3, 0.6, 0.06]
  body: [0.45, 1.0, 12.43, 6.05]
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
  header_text: text
  header_rule: text
  stripe: F3F4F6
  rule: E5E7EB
  rule_pt: 0.75
  first_column_bold: true
slide_kinds:
  statement: {size: 40, color: text, bar: primary, note: secondary}
  number: {size: 96, color: primary, note: secondary}
  quote: {size: 32, color: text, mark: primary, note: secondary}
style:
  background: background
  content:
    title:
      size: 14
      color: secondary
      bold: true
      spacing: 1.5
      anchor: ctr
    number:
      box: [12.13, 6.95, 0.6, 0.3]
      size: 11
      color: secondary
      align: r
    decor:
    - shape: rect
      box: [0.45, 0.3, 0.6, 0.06]
      fill: primary
  cover:
    date:
      box: [0.8, 0.7, 8, 0.4]
      size: 13
      color: secondary
    title:
      box: [0.8, 2.45, 11.73, 1.1]
      size: 40
      bold: true
      font: heading
      anchor: b
    subtitle:
      box: [0.8, 3.65, 11.73, 0.6]
      size: 22
      color: secondary
    presenter:
      box: [0.8, 5.55, 8, 0.4]
      size: 16
      bold: true
    affiliation:
      box: [0.8, 5.95, 10, 0.8]
      size: 13
      color: secondary
    decor:
    - shape: rect
      box: [0.8, 2.2, 1.2, 0.08]
      fill: primary
    - shape: line
      box: [0.8, 5.3, 11.73, 0]
      line: E5E7EB
      line_pt: 1
  section:
    title:
      box: [0.8, 3.0, 11.73, 1.0]
      size: 40
      bold: true
      font: heading
      anchor: b
    subtitle:
      box: [0.8, 4.1, 11.73, 0.6]
      size: 20
      color: secondary
    decor:
    - shape: rect
      box: [0.8, 2.75, 1.2, 0.08]
      fill: primary
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
      text: Contents
      size: 30
      bold: true
      font: heading
    - shape: rect
      box: [0.8, 1.1, 0.6, 0.06]
      fill: primary
```

## 성격

컨퍼런스·사내 테크 토크·제품 소개·일반 발표용. 화면을 한눈에 읽고 넘기는 청중을 가정한다. 흰 바탕, 거의 검정에 가까운 글자, 넓은 여백, 강조색(전기 파랑 `primary`) 하나가 기본 인상이다. 상단 바 대신 작은 회색 토픽 라벨과 짧은 강조 막대가 있고, 표지와 섹션은 왼쪽 정렬의 큰 제목이다.

## 어울리는 것

- 슬라이드마다 큰 메시지 하나. 핵심 문장은 짧고 단정하게, 근거는 2~4개.
- 넓은 화면을 쓰는 좌우 대비: 문제 ↔ 해결, 이전 ↔ 이후, 텍스트 ↔ 그림 2단.
- 숫자 하나를 크게 보여 주는 슬라이드, 흐름도·카드·타임라인 같은 구조 도식.
- 강조색은 화면당 한 곳. 나머지는 검정·회색으로 위계를 만든다.
- 제품 화면·데모 캡처처럼 실물이 보이는 그림. 여백을 남기고 크게 둔다.

## 어울리지 않는 것

- 문단형 설명, 7개 넘는 불릿, 작은 글씨 표. 자세한 내용은 노트나 부록으로 옮긴다.
- 여러 강조색, 장식 아이콘, 그라데이션, 그림자, 테두리 상자 남발.

## 그림 인상

- 색은 `semantic_palette("modern-minimal")`. 강조 `accent` 한 계열 + `neutral` 회색. 비교 기준은 회색, 주인공만 파랑.
- 도식은 각진 상자 또는 아주 작은 둥근 모서리, 얇은 선. 상자 채움은 옅은 `tint`, 핵심 하나만 `accent`.
- matplotlib 그래프는 위·오른쪽 축선을 지우고 격자는 옅게, 범례 대신 선 끝 직접 라벨을 우선한다.
- 가로로 긴 도식(흐름·타임라인)은 16:9 폭을 활용해 한 줄로 둔다.
- 아이소메트릭 도해(`pptgen anatomy`)는 흰 바탕에 회색 부품, 주인공 부품(`lit`) 하나만 `accent`로 칠한다. 그림자와 카드 테두리는 없다.

## 빌드 후 볼 것

- 넓은 화면에서 내용이 왼쪽에만 몰려 오른쪽이 텅 비지 않는가.
- 파랑이 한 화면에 두 곳 이상 쓰이지 않았는가.
- 회색 보조 글자가 4x 크롭에서 충분히 읽히는가.
