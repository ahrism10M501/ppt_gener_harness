# RVLAB 디자인 명세

아래 첫 YAML 블록은 파생 양식 생성기와 빌드가 읽는 **고정 토큰의 본체**다. 발표 입력에 좌표·폰트·색 토큰을 복사하지 않는다. 토큰 변경은 양식 변경이며 `uv run python -m rvppt.template --preset rvlab`으로 reference·preview를 다시 만들고 테스트를 돌린다.

기본 `rvlab` 프리셋의 디자인 문서다. 다른 프리셋도 같은 형식으로 `templates/<id>/DESIGN.md`에 토큰과 규약을 함께 둔다. 이 프리셋에만 해당하는 스타일 규칙(색 사용, 도식 모양, 그래프 스타일, 표지·상단 바 점검)은 스킬이 아니라 이 문서에 쓴다. rvlab은 원본 PPTX의 마스터·장식을 그대로 쓰므로 `style` 블록이 없다.

렌더 QA는 LibreOffice와 설치된 폰트(Arial·맑은 고딕이 없으면 대체 폰트)를 기준으로 한다. PowerPoint 실제 렌더링은 아직 검증하지 않았다.

```yaml
schema_version: 1
preset_id: rvlab
name: RVLAB Lab Template (4:3)
description: Fixed RVLAB 4:3 research lab presentation template with institutional branding
mode: template
source:
  path: templates/rvlab/RVLAB_PPT양식.pptx
  sha256: 0c95f491b9638bc097a9761faf6e02d777a5da99af20f1b50c3262fea620b7e5
reference: templates/rvlab/reference.pptx
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
table:
  header_fill: primary
  header_text: background
  header_rule: band
  stripe: tint
  rule: neutral
  rule_pt: 0.5
  first_column_bold: false
slide_kinds:
  statement: {size: 34, color: band, bar: primary}
  number: {size: 80, color: primary}
  quote: {size: 28, color: text, mark: primary}
```

## 성격과 판단 기준

경기대학교 RVLAB 연구실의 랩미팅·논문 리뷰·스터디용이다. 교수님과 동료가 진행 상황을 판단하고 피드백하는 자리를 가정한다. 파란 띠·노란 부제·흰 바탕의 차분한 연구실 양식이며, 아래는 에이전트가 "어울리는가"를 판단할 때의 기준이다. 청중·목적과 부딪히면 청중을 따르고 보고에 밝힌다.

- **어울리는 것:** 결론형 핵심 문장 + 근거 2~4개, 비교 조건·표본 수를 적은 결과, 논문 figure와 출처, 핵심 15줄 이내 코드와 실행 결과, 지난 미팅 피드백을 잇는 구성. 발표 유형별 구성은 [발표 유형 가이드](../../skills/ppt-maker/references/talk-types.md).
- **어울리지 않는 것:** 문단형 슬라이드, 근거 없는 큰 숫자, 장식 아이콘·그라데이션·그림자, 둥근 카드 남용.
- **그림 인상:** 흰 배경·검정 글자·회색 보조 요소, 강조는 primary 파랑 한 곳. 도식 상자는 직각, 선·화살표·간격은 일정하게. 원·곡선은 수학적 의미가 있을 때 쓴다. 그래프는 [rvlab.mplstyle](plot.mplstyle).
- **빌드 후 볼 것:** 상단 바가 한 줄이고 파란 선이 제목 오른쪽에서 시작하는가, 노랑이 표지·섹션 부제 밖에 쓰이지 않았는가.

## 원본과 파생 양식

원본은 10×7.5인치·4:3, 마스터 1개, 레이아웃 4개, 표본 슬라이드 5개다. 레이아웃 이름은 `제목 슬라이드`, `1_제목 및 내용`, `2_제목 및 내용`, `OBJECT`다. 실제 좌표·폰트·색은 [template-manifest.json](template-manifest.json)에 있다. 연구실 실제 발표 참고 자료는 `templates/examples/`에 있다.

원본 레이아웃은 변경하지 않는다. 파생 reference는 표본 슬라이드·노트·Google 메타데이터만 제거하고 Pandoc용 이름의 파생 레이아웃을 추가한다. 로고·파란 띠·노란 부제·상단 장식·하단 띠·테마는 그대로 둔다. 파생 본문 레이아웃은 **원본 표본과 같은 상단 바**를 쓴다. 제목 칸은 `[0.69, 0.10, 3.43, 0.56]`의 흰 바탕 24pt 굵은 글자이고, 그 뒤의 파란 선이 제목 오른쪽으로 이어진다. 제목 칸을 넓히거나 선을 옮기지 않는다.

표지·목차·섹션·마무리 슬라이드는 원본 레이아웃의 placeholder에 텍스트만 채운다. 글꼴·크기·색·정렬은 레이아웃에서 상속한다.

## 슬라이드 문법과 이름 규칙

연구실 발표 네 편(저장소에 포함하지 않는 로컬 `templates/examples/`)과 원본 표본에서 확인한 규칙이다. 작성자는 Markdown 제목 수준만 고르고, 표지·목차·마무리는 빌드가 만든다.

| 슬라이드 | 입력 | 규칙 |
| --- | --- | --- |
| 표지 | `slides.md` frontmatter의 `deck` | 왼쪽 위 `발표일시 : YYYY.MM.DD`, 파란 띠의 제목(흰색)·부제(노란색), 발표자 `이름 (English Name)`, 소속 두 줄. 인적사항은 `pptgen new`가 `profile.yaml`에서 채운다. |
| 목차 | 자동 | 왼쪽 `Contents` 패널, 오른쪽에 `▪ Chapter N: 섹션 제목`(굵게)과 그 섹션의 `• 토픽`. 섹션 이름과 같은 토픽은 생략한다. 섹션이 2개 이상일 때만 만든다. 14줄을 넘으면 토픽을 모두 생략한다. |
| 섹션 | `# 섹션 제목 \| 부제` | 파란 띠의 흰 제목과 노란 부제. 섹션 제목은 목차의 Chapter 이름이다. 부제는 영문 이름이나 한 줄 설명이다. |
| 본문 | `## 토픽` + `### 핵심 문장` | 상단 바에는 **짧은 토픽 이름**(예: `GS-ICP SLAM`, `Gradient Vanishing`, `LoRA`)을 쓴다. 같은 토픽의 슬라이드가 이어지면 상단 바도 반복된다. 본문 첫 줄은 `▪` 24pt 핵심 문장이고 그 아래 내용은 한 칸 들여 쓴다. |
| 마무리 | 자동 | `감사합니다.`(영어 발표는 `Thank you.`). `# Appendix` 또는 `# 부록` 섹션이 있으면 그 앞에 둔다. |

상단 바 토픽은 **한 줄**을 권장한다. 한글 2·그 외 1로 세어 20 이하(약 한글 10자·영문 20자)를 넘으면 lint가 경고한다. 문장이나 결론이 아니라 목차에 그대로 실릴 주제 이름이다. 결론형 메시지는 `###` 핵심 문장에 쓴다. 핵심 문장은 최대 두 줄이다.

```markdown
# 연구 배경 | Research Background

## Gradient Vanishing

### 층이 깊어질수록 앞쪽 층의 기울기가 사라진다

- 연쇄 법칙의 미분값이 층마다 곱해진다
  - Sigmoid 미분의 최댓값은 0.25다
```

## 본문·제목·언어

슬라이드당 주장 1개를 핵심 문장으로 쓴다. 글꼴을 자동 축소하지 않는다. 넘치면 메시지를 줄이거나 슬라이드를 나눈다. 본문 불릿은 1단 20pt·2단 18pt이며 깊이 2단계, 5개 안팎을 권장한다. 긴 문장 대신 짧은 구를 쓰되 의미·인과·불확실성을 지우지 않는다. 약어는 처음 나올 때 정의한다. 한국어가 기본이고 영어 발표도 허용한다. 한·영 폰트는 각각 맑은 고딕·Arial이다.

폰트 누락 시 Latin은 Liberation Sans, 한국어는 Noto Sans CJK KR로 대체하고 리포트에 기록한다. 숫자는 천 단위·소수 자릿수를 통일하고 값과 단위 사이에 공백을 둔다(예: `25 ms`, `0.8 m`). 원자료의 단위와 유효숫자를 보존한다.

## 표·그래프·그림

표는 헤더 포함 8행·6열 이하를 권장하며 18pt로 작성한다. 가로 구분선을 최소화하고 세로선은 피한다. 텍스트는 왼쪽, 수치는 오른쪽 정렬하고 비교 기준과 단위를 헤더에 적는다. 최선 값만 굵게 표시한다. 표가 넘치면 분할한다.

에이전트는 [외부 시각 자료 절차](../../skills/ppt-maker/references/external-visuals.md)에 따라 웹 사진·논문 figure를 직접 확보하고, 캡션·본문 설명과 핵심 문장을 대조해 선정한다. 출처와 함께 `![그림 설명](figures/파일명.png)`로 넣는다. 연구자가 새로 만들어야 하는 그림은 제안하고 자리를 잡는다. 파일이 아직 없으면 빌드는 점선 상자에 요청 내용을 표시하고 리포트의 `missing_figures`에 남긴다. 연구자가 같은 이름으로 그림을 넣고 다시 빌드한다. 에이전트가 그래프를 그릴 때는 [rvlab.mplstyle](plot.mplstyle)을 쓴다.

그래프는 축·범례·단위를 표시하고 색만으로 구분하지 않는다. 원자료에서 오차·표본 수를 확인한 경우만 기재한다. 강조는 primary, 보조는 secondary, 추가 계열은 검정과 선 모양으로 구분한다. 노랑은 표지·섹션 부제에만 사용한다.

SVG/PDF 원본을 보존하고 호환 PNG를 함께 만든다. 삽입 지점의 유효 해상도는 최소 150dpi다. 작은 그림은 늘리지 않고 그만큼 작게 놓는다. 생성 PNG는 300dpi를 목표로 한다. 캡션·출처는 12pt, `그림 n. 설명`과 `출처: 저자/기관, 연도, 링크` 형식이다. 논문 그림은 출처를 반드시 달고, 전체 서지·DOI/URL은 노트에 둔다.

교육용 GIF도 같은 그림 슬롯과 색·폰트·해상도 규칙을 따른다. 변화 자체가 주장 이해에 필요한 경우에 사용하며, GIF와 동일한 픽셀 크기의 대표 PNG를 같은 이름으로 보존한다. 최종 PPTX에는 GIF를, PDF·미리보기에는 대표 PNG를 넣는다. 선택·장면 기획은 [ppt-animation](../../skills/ppt-animation/SKILL.md)을 따른다.

그림 슬롯은 핵심 문장 아래 본문 영역을 균등 분할한다. 1개는 전체, 2개는 좌우, 3개는 가로 3개, 4개는 2×2다. 간격 0.24인치, 각 슬롯 아래 0.36인치는 캡션이다. 그림은 자르거나 늘리지 않고 종횡비를 보존해 중앙에 맞춘다.

## 수식·코드·다이어그램

수식은 LaTeX로 작성한다. 인라인 수식은 문장 안에, 주요 수식은 독립 블록에 배치한다. 제작과 검수는 [수식 문법](../../docs/rendering.md#수식)을 따른다.

코드는 핵심 부분만 16pt 고정폭으로 표시한다. 긴 코드는 자료 링크로 옮긴다. Mermaid는 단순한 흐름도에 쓰고 RVLAB 색·폰트를 기본으로 한다. 강조가 필요한 노드만 `style`·`classDef`로 바꾼다.

## 금지·검사

임의 좌표, 자동 글꼴 축소, 그림 늘리기·무단 자르기는 쓰지 않는다. 강조 색과 장식은 전달에 도움이 될 때만 쓴다. 대조도·출처·폰트·그림 해상도·슬라이드 경계·텍스트 넘침을 실제 렌더로 검사한다.
