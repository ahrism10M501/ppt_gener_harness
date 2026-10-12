# 수식·PDF·문서 포맷 도구 안내

스킬은 에이전트의 작업 지침과 참조자료이며, CLI·라이브러리·MCP 서버는 실제 파일을 처리하는 실행 도구다. 스킬을 포함했다고 실행 도구나 모델까지 설치되는 것은 아니다. 이번 추가는 스킬 원문 보관과 안내이며 시스템 설치·모델 다운로드·외부 API 등록은 수행하지 않았다.

## 포맷별 선택

| 작업 | 포함한 스킬 / 권장 도구 | 현재 상태와 적용 범위 |
| --- | --- | --- |
| RVLAB PPT 수식 | `rvlab-ppt`, Pandoc, MathJax | 기존 제작기 제공. LaTeX→OMML 우선, 이미지 fallback. [제작 문법](rendering.md) 참고 |
| 독립 수식·논문·보고서 | [typst](../skills/typst/SKILL.md), Typst CLI | 스킬 포함, CLI 미설치. Typst의 수식 문법은 LaTeX와 다름 |
| 기존 `.tex` 논문 | Tectonic 또는 TeX Live | 선택 도구, 미설치. 학회·학술지의 클래스와 패키지 호환성에 맞춰 선택 |
| PDF 읽기·추출·생성 | [pdf](../skills/pdf/SKILL.md), PyMuPDF, pdfplumber, pypdf, ReportLab | 스킬 포함. PyMuPDF·Poppler 사용 가능, 나머지 Python 패키지는 미설치 |
| DOCX 작성·편집·추적 변경 | [minimax-docx](../skills/minimax-docx/SKILL.md), Open XML SDK | 원본 스킬·C# 코드·참조자료 포함. .NET 8 SDK 미설치 |
| XLSX·XLSM·CSV·TSV | [minimax-xlsx](../skills/minimax-xlsx/SKILL.md), OOXML 스크립트, pandas/openpyxl | XML 편집·정적 수식 검사 실행 확인. 데이터 분석용 pandas/openpyxl 미설치 |
| PPTX | `rvlab-ppt`; 일반 PPT 참고용 [pptx-generator](../skills/pptx-generator/SKILL.md) | RVLAB 제작은 기존 승인·고정 양식 사용. 일반 스킬은 발견 경로에 등록하지 않음 |
| EPUB·Markdown·HTML·DOCX 변환 | 기존 Pandoc / pypandoc | Pandoc 바이너리 포함. 변환 후 표·수식·출처·메타데이터 확인 필요 |
| CSV·Parquet·DB 조회 | 표준 `csv`/`sqlite3`, 선택적으로 DuckDB | 표준 라이브러리 사용 가능, DuckDB 미설치. 대용량 집계는 SQL로 필요한 범위만 조회 |
| 다양한 문서→텍스트/Markdown | 선택적으로 Microsoft MarkItDown | 미설치. 내용 추출용이며 원래 페이지 배치나 Office 편집성을 보장하지 않음 |

새 스킬은 `skills/`가 본체다. `pdf`, `typst`, `minimax-docx`, `minimax-xlsx`는 `.agents/skills/`와 `.claude/skills/`에 연결했다. Cursor 등 다른 에이전트는 자체 발견 경로 설정에 따라 인식이 달라지므로 해당 `SKILL.md`를 직접 지정하거나 도구별 설정을 확인한다. Cursor 실행은 검증하지 않았다.

## 수식 작성과 추출

RVLAB 수식은 `slides.md`에 LaTeX로 작성한다. 산출물과 검수 기준은 [수식 문법](rendering.md#수식)을 따른다.

독립 문서를 만들 때 Typst CLI가 준비되어 있다면 다음처럼 컴파일한다. 수식 문법·정렬·행렬은 포함한 [math.md](../skills/typst/references/math.md)를 참고한다.

```sh
typst compile document.typ document.pdf
typst compile document.typ --format svg
typst compile document.typ --format png
```

`.tex` 원본은 Tectonic 또는 TeX Live로 처리한다. Tectonic은 필요한 TeX 자료를 내려받을 수 있으므로 완전한 오프라인 실행이 필요하면 캐시와 패키지를 먼저 준비한다. `align`·사용자 매크로·학술지 클래스의 지원은 실제 컴파일로 확인해야 하며 MathJax/KaTeX·MathML·OMML이 모든 LaTeX를 같은 방식으로 지원한다고 가정하지 않는다.

이미지나 스캔 PDF의 수식은 OCR 후보를 별도로 선택한다.

| 후보 | 용도 | 라이선스·운영 조건 |
| --- | --- | --- |
| [Mathpix](https://docs.mathpix.com/) | 캡처·수식 이미지→LaTeX/MathML 등 | 외부 유료 API/서비스. 계정·API 키와 자료 전송 동의가 필요한 별도 선택 |
| [Nougat](https://github.com/facebookresearch/nougat#license) | 학술 PDF→텍스트·LaTeX 구조 추출 | 코드 MIT, 모델 가중치 CC-BY-NC. 모델을 포함하거나 다운로드하지 않음 |
| [Marker](https://github.com/datalab-to/marker#commercial-usage) | PDF→Markdown·표·수식 추출 | 현재 코드 Apache-2.0, 모델은 수정된 OpenRAIL-M 조건. 코드와 가중치의 사용 조건을 따로 확인 |

OCR 출력은 원문 이미지와 대조한다. 지수·첨자·기호·표 셀·인용을 자동 추출 결과만으로 확정하지 않는다. PyMuPDF는 PDF 텍스트·페이지 렌더링 도구이며 복잡한 수식 의미나 학술 Markdown 구조를 자동 복원하는 모델이 아니다.

## PDF와 Office 파일 처리

논문 입력은 **PyMuPDF4LLM 0.2.9**를 기본 의존성으로 제공합니다. `uv run rvppt extract-paper TASK sources/PAPER.pdf`가 `.build/editorial/papers/`에 페이지별 Markdown·PNG 후보·원본 해시를 추출합니다. 선택은 캡션·본문 설명과 원본 PDF 시각 확인을 바탕으로 에이전트가 수행합니다. [외부 사진·figure 절차](../skills/rvlab-ppt/references/external-visuals.md)를 따릅니다.

[PyMuPDF4LLM API](https://pymupdf.readthedocs.io/en/latest/pymupdf4llm/api.html)의 `write_images`, `image_path`, `page_chunks`를 사용합니다. 모델이 필요 없는 기존 변환 API를 사용하도록 버전을 고정했으며 layout 확장·OCR·모델 가중치는 설치하지 않습니다. 스캔·복잡한 패널·수식은 원본 페이지로 확인하고 추출 실패 시 페이지 렌더링·크롭으로 보완합니다. PyMuPDF4LLM은 PyMuPDF와 같은 AGPL-3.0/상용 이중 라이선스이며 MIT 라이브러리로 기록하지 않습니다.

PDF→Markdown·이미지 분리 도구로는 [Marker](https://github.com/datalab-to/marker)와 [Docling](https://docling-project.github.io/docling/examples/export_figures/)도 있습니다. 이 저장소에서는 기존 PyMuPDF를 재사용하는 PyMuPDF4LLM을 적용합니다. MarkItDown은 일반 문서 내용 추출용으로 남기며 논문 figure 분리 명령에 사용하지 않습니다.

PDF는 텍스트 추출과 페이지 이미지를 함께 확인한다. 디지털 PDF의 간단한 추출·렌더링은 이미 설치된 PyMuPDF를 재사용한다. 표 추출은 pdfplumber, 병합·분할·폼 필드는 pypdf, 새 PDF 생성은 ReportLab을 후보로 둔다. 글꼴·표·수식·페이지 배치는 렌더 결과로 검토한다.

XLSX 스크립트는 XML을 편집하는 방식과 pandas 기반 내용 분석을 구분한다. `formula_check.py`는 깨진 참조 등을 정적으로 검사하며 수식 값을 재계산하는 엔진이 아니다. 실제 계산 값은 Excel/LibreOffice 등에서 재계산하고 다시 검사한다. XLSM 매크로 실행, 차트·외부 링크·서식의 완전한 보존은 이번 검증 범위가 아니다.

다음은 필요할 때 사용할 실행 예다. 입력 파일을 수정하지 않고 결과를 새 경로에 만든다. 외부 스크립트의 `SKILL_DIR`은 실제 `skills/` 경로로 잡는다.

```sh
# 정적 수식 검사: 추가 Python 패키지 없이 실행 가능
uv run python skills/minimax-xlsx/scripts/formula_check.py INPUT.xlsx --json

# 내용 분석: 필요할 때만 임시 실행 환경에 의존성 제공
uv run --with pandas --with openpyxl python skills/minimax-xlsx/scripts/xlsx_reader.py INPUT.xlsx --json

# PDF 페이지 미리보기: Poppler가 설치된 환경
pdftoppm -png -r 150 INPUT.pdf OUTPUT_PREFIX
```

`xlsx_unpack.py`는 지정한 출력 디렉터리가 이미 있으면 삭제하므로 반드시 새 임시 디렉터리를 사용한다. 원본 파일·자료 폴더·기존 성공 산출물 경로를 출력 디렉터리로 넘기지 않는다. DOCX의 `setup.sh`/`setup.ps1`은 시스템 설치를 수행할 수 있어 이번에 실행하지 않았다. Typst 스킬의 갱신 스크립트도 자동 실행하지 않는다.

일반 문서의 새 결과는 사용자가 지정한 경로에 보관한다. RVLAB task 작업은 원자료를 수정하지 않으며 외부 도구의 중간 파일을 `TASK/.build/editorial/`에 격리한다. 승인된 PPT 내용을 바꾸면 필요한 단계부터 검토·재승인한다. 일반 문서 스킬의 스타일 예시를 RVLAB PPT의 좌표·폰트·색 입력으로 옮기지 않는다.

## 라이선스

포함한 원문과 파일 해시는 [dependencies.yaml](../skills/dependencies.yaml)에 기록했다. 아래 GitHub 링크는 확인한 고정 커밋의 라이선스다.

| 포함한 스킬 | 출처 | 라이선스 |
| --- | --- | --- |
| `pdf` | [openai/skills](https://github.com/openai/skills/blob/49f948faa9258a0c61caceaf225e179651397431/skills/.curated/pdf/LICENSE.txt) | [Apache-2.0 전문](../skills/pdf/LICENSE.txt) |
| `typst` | [akilrammohan/typst-skill](https://github.com/akilrammohan/typst-skill/blob/aa839eded0536a0537fa0968974ce54001cb6865/LICENSE) | [MIT 전문](../skills/typst/LICENSE) |
| `minimax-docx` | [MiniMax-AI/skills](https://github.com/MiniMax-AI/skills/blob/60aaae52bb2af8162732751a4332f62a5fef518b/skills/minimax-docx/LICENSE) | [MIT 전문](../skills/minimax-docx/LICENSE), 저장소 [고지](../skills/minimax-docx/UPSTREAM_LICENSE) |
| `minimax-xlsx` | [MiniMax-AI/skills](https://github.com/MiniMax-AI/skills/blob/60aaae52bb2af8162732751a4332f62a5fef518b/LICENSE) | [MIT 전문](../skills/minimax-xlsx/LICENSE) |
| `pptx-generator` | [MiniMax-AI/skills](https://github.com/MiniMax-AI/skills/blob/60aaae52bb2af8162732751a4332f62a5fef518b/LICENSE) | [MIT 전문](../skills/pptx-generator/LICENSE), 참고용 |

Anthropic의 [`pdf`](https://github.com/anthropics/skills/blob/dbd4588f9e1033efb41dad4bef2f7947c8993d44/skills/pdf/LICENSE.txt), `docx`, `xlsx`, `pptx`는 서비스 계약 기반의 독자 라이선스다. 공개 저장소라는 이유로 MIT 재배포 대상으로 취급하지 않으며 이번 저장소에는 복사하지 않았다.


도구 라이선스는 스킬과 별개다. Typst 엔진은 [Apache-2.0](https://github.com/typst/typst/blob/main/LICENSE), Tectonic 엔진은 [MIT](https://github.com/tectonic-typesetting/tectonic/blob/master/LICENSE), MarkItDown은 [MIT](https://github.com/microsoft/markitdown/blob/main/LICENSE), DuckDB는 [MIT](https://github.com/duckdb/duckdb/blob/main/LICENSE)다. 기존 PyMuPDF는 [AGPL-3.0 / 상용 라이선스](https://pymupdf.readthedocs.io/en/latest/about.html#license-and-copyright)이고 EbookLib는 [AGPL-3.0](https://github.com/aerkalov/ebooklib/blob/master/LICENSE.txt)이므로 이 도구들을 MIT라고 안내하지 않는다. Pandoc은 [GPL](https://github.com/jgm/pandoc/blob/main/COPYING)이다.

MCP는 파일 처리기를 에이전트에 연결하는 인터페이스다. `mcp-server-fetch`는 웹 가져오기 도구이며 그 자체를 PDF 수식·표 파서로 간주하지 않는다. 로컬 도구로 충분한 작업에는 MCP 서버를 추가하지 않았다. 별도 서버나 플러그인이 필요하면 정확한 저장소·라이선스·로컬 파일 접근 범위를 확인해 선택한다.

## 실행 의존성과 제약


Typst/LaTeX 컴파일, DOCX .NET 빌드, pandas 기반 XLSX 분석, 실제 Excel 재계산, OCR 모델, 외부 API, 일반 PPTX 제작, Cursor·OS별 실행은 검증하지 않았다. 추가 런타임은 필요한 작업에 맞춰 별도로 설치한다.
