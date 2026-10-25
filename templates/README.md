# 템플릿

발표 양식 하나가 폴더 하나다. `slides.md`의 `deck.preset`에 폴더 이름을 쓰면 그 양식으로 빌드된다. 목록은 `uv run pptgen presets`로 볼 수 있다.

| 템플릿 | 비율 | 성격 | 미리보기 |
| --- | --- | --- | --- |
| [rvlab](rvlab/DESIGN.md) | 4:3 | 경기대 RVLAB 연구실 양식. 랩미팅·논문 리뷰·스터디 (기본값) | [png](rvlab/preview.png) · [pdf](rvlab/preview.pdf) |
| [modern-minimal](modern-minimal/DESIGN.md) | 16:9 | 흰 바탕, 넓은 여백, 강조색 하나. 테크 토크·제품·일반 발표 | [png](modern-minimal/preview.png) · [pdf](modern-minimal/preview.pdf) |
| [retro](retro/DESIGN.md) | 16:9 | 크림 종이, 세리프, 세 줄 띠와 액자. 이야기·역사·강의 | [png](retro/preview.png) · [pdf](retro/preview.pdf) |
| [neo-city](neo-city/DESIGN.md) | 16:9 | 어두운 바탕, 네온 시안·마젠타, 그리드와 브래킷. 테크 데모·AI·키노트 | [png](neo-city/preview.png) · [pdf](neo-city/preview.pdf) |

`examples/`는 RVLAB 실제 발표 참고 자료다. Git에서 제외되며 템플릿이 아니다.

## 폴더 구성

```text
templates/<id>/
├── DESIGN.md        # 첫 ```yaml 블록 = 토큰(빌드가 읽음), 그 아래 = 성격과 규약(에이전트가 읽음)
├── reference.pptx   # 빌드가 슬라이드를 얹는 틀. 마스터 1개 + 레이아웃 13개, 슬라이드는 0장이어야 한다
├── preview.pdf      # 레이아웃마다 예시 슬라이드 한 장(표지·목차·섹션·본문·2단·그림 그리드·마무리)
├── preview.png      # 위 PDF의 한눈 보기
└── (전용 자산)       # rvlab: 원본 RVLAB_PPT양식.pptx, plot.mplstyle, template-manifest.json
                     # 등록한 템플릿: source.pptx, template-manifest.json
```

`reference.pptx`, `preview.*`는 생성물이다. 직접 고치지 말고 `DESIGN.md`를 고친다. rvlab 외 템플릿의 `reference.pptx`는 빌드할 때마다 DESIGN.md에서 다시 만들어지며, `preview.*`와 rvlab reference는 아래 명령으로 다시 만든다.

```bash
uv run python -m rvppt.template                    # 모든 템플릿의 reference와 preview
uv run python -m rvppt.template --preset retro     # 하나만
```

## DESIGN.md

스킬은 작업을 시작할 때 task의 `deck.preset`에 해당하는 `DESIGN.md`를 읽는다. 그래서 그 템플릿에만 해당하는 규칙(색을 어디에 쓰는지, 도식 모양, 그래프 스타일, 빌드 후 점검)은 스킬이 아니라 여기에 쓴다.

**토큰 (YAML 블록).**

| 키 | 내용 |
| --- | --- |
| `preset_id`, `name`, `description` | 폴더 이름과 같은 ID, 표시 이름, 한 줄 설명 |
| `slide` | 크기(인치)와 비율 |
| `palette` | `primary`(강조) · `band`(묶음·짙은 면) · `secondary`(보조) · `section_accent`(표지·섹션 포인트) · `text` · `background`. 차트와 애니메이션은 `rvppt.template.semantic_palette(<id>)`로 이 색을 쓴다 |
| `fonts` | `latin`·`korean`과 대체 글꼴, `code`. 선택 키 `heading_latin`·`heading_korean`은 제목용 글꼴이다. 빌드는 설치된 글꼴로 넘침을 재므로 실제로 설치된 글꼴을 쓴다 |
| `sizes_pt`, `geometry_in`, `limits` | 본문 글자 크기, 본문 영역·간격, lint 권장 한도 |
| `layouts`, `labels` | 레이아웃 이름 매핑(바꾸지 않는다), 날짜·마무리 문구 |
| `table` | 표 모양: `header_fill`(`none`이면 채우지 않음), `header_text`, `header_rule`(헤더 아래·마지막 줄 선), `stripe`(짝수 행 채움, `none` 가능), `rule`(행 사이 선), `rule_pt`, `first_column_bold` |
| `slide_kinds` | `{.statement}`·`{.number}`·`{.quote}` 슬라이드의 `size`, `color`, `bar`(statement 막대), `mark`(quote 따옴표), `note`(보조 문단 색) |
| `style` | 16:9 테마의 화면 구조. 아래 참고. rvlab은 원본 PPTX의 장식을 그대로 쓰므로 이 키가 없다 |

**`style` 블록.** reference를 만들 때 RVLAB에서 파생한 레이아웃의 장식을 모두 걷어 내고 이 블록대로 다시 그린다. 좌표는 인치(`[x, y, w, h]`)이고, 색은 팔레트 역할 이름(`primary` 등) 또는 `RRGGBB`로 쓴다.

```yaml
style:
  background: background          # 마스터 배경색
  cover:                          # 표지. 섹션은 section, 목차는 toc, 본문 제목 줄은 content
    title:    {box: [0.8, 2.45, 11.73, 1.1], size: 40, bold: true, font: heading, anchor: b}
    subtitle: {box: [...], size: 22, color: secondary}
    presenter / affiliation / date: {...}   # 표지에만 있는 자리
    decor:                        # 자리 뒤에 깔리는 도형
      - {shape: rect, box: [0.8, 2.2, 1.2, 0.08], fill: primary}
      - {shape: line, box: [0.8, 5.3, 11.73, 0], line: E5E7EB, line_pt: 1}
      - {shape: text, box: [...], text: Contents, size: 30, font: heading}
  toc:
    body: {box: [...], size: 22, bold: true, level2: {size: 17, bold: false, color: secondary}}
  content:
    title:  {size: 14, color: secondary, spacing: 1.5, anchor: ctr}   # 상단 토픽
    number: {box: [...], size: 11, align: r}                          # 쪽 번호
```

- **자리 글꼴 키:** `size`, `bold`, `color`, `font`(`heading`이면 제목 글꼴), `align`(`l`/`ctr`/`r`), `anchor`(`t`/`ctr`/`b`), `spacing`(자간 pt), `line`(줄 간격 배수), `after`(문단 뒤 pt), `level2`(목차 둘째 단계 덮어쓰기).
- **도형 `shape`:** `rect`, `round`, `ellipse`, `line`, `text`. 키는 `fill`, `line`, `line_pt`이고, `text` 도형은 위의 글꼴 키도 받는다.
- **본문 영역:** 핵심 문장·불릿·그림·표가 들어가는 영역은 `geometry_in.body`가 정한다. 상단 장식과 겹치지 않게 둔다.

**성격과 규약 (YAML 아래 본문).** 다음 다섯 절을 쓴다. 각 절은 규칙이 아니라 에이전트가 "어울리는가"를 판단할 출발점이다.

| 절 | 내용 |
| --- | --- |
| 성격 | 누구를 위한 어떤 자리인지 |
| 어울리는 것 | 잘 맞는 구성·밀도·표현 |
| 어울리지 않는 것 | 피할 구성·표현 |
| 그림 인상 | 색 사용, 도식 모양, 그래프 스타일 |
| 빌드 후 볼 것 | 이 템플릿에서 특히 확인할 점 |

## 새 템플릿 추가

1. **폴더 만들기:** 가장 가까운 테마 폴더의 `DESIGN.md`를 `templates/<새-id>/DESIGN.md`로 복사한다. ID는 소문자·숫자·하이픈만 쓴다.
2. **토큰 고치기:** `preset_id`, `name`, `description`, `reference: templates/<새-id>/reference.pptx`, `palette`, `fonts`, `style`을 고친다.
3. **규약 쓰기:** 아래 본문의 성격과 규약을 새 양식에 맞게 쓴다.
4. **확인:** `uv run python -m rvppt.template --preset <새-id>`로 reference와 preview를 만들고 `preview.png`를 본다. 합성 덱을 빌드한 뒤 `uv run pptgen audit tasks/<task> --zoom 4`로 대비·여백도 확인한다.

**기존 PPTX에서 시작하기:** `uv run pptgen register-template <file.pptx> --id <id>`는 원본을 `templates/<id>/source.pptx`로 보관하고, 크기와 색 3개를 가져와 `DESIGN.md`·reference·preview를 만든다. 16:9면 modern-minimal의 `style`을 바탕으로 한다. 다시 등록해도 이미 쓴 규약은 보존된다. 원본 PPTX의 레이아웃·로고·배경을 그대로 옮기지는 않으므로, `style`과 규약은 원본을 보며 직접 다듬는다.

## 지킬 것

- `rvlab/RVLAB_PPT양식.pptx`는 연구실 원본이다. 수정하지 않는다. 해시는 `rvlab/DESIGN.md`에 있고 `pptgen doctor`가 확인한다.
- 어두운 배경 템플릿에서는 `text`가 밝고 `background`가 어둡다. 빌드·차트 도구는 이 두 색을 따르지만, 직접 만든 그림은 배경색을 맞춰야 흰 사각형이 뜨지 않는다.
- 렌더 QA는 LibreOffice 기준이다. 발표 PC에 제목 글꼴이 없으면 PowerPoint가 대체 글꼴로 바꾼다.
