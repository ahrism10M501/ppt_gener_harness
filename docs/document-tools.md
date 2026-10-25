# 입력 자료 도구 안내

발표에 넣을 자료(논문 PDF, 초안 PPT, 문서, 데이터)를 읽는 도구다. 실행 도구는 스킬과 별개이며, 시스템 설치·모델 다운로드·외부 API는 필요할 때 따로 확인받는다.

| 작업 | 도구 | 상태와 범위 |
| --- | --- | --- |
| 논문 PDF → Markdown·figure 후보 | `uv run pptgen extract-paper` (PyMuPDF4LLM 0.2.9) | 기본 의존성. [외부 시각 자료](../skills/ppt-maker/references/external-visuals.md) |
| PDF 페이지 렌더·크롭·텍스트 | PyMuPDF, Poppler `pdftoppm` | 사용 가능 |
| 초안 PPT·DOCX·XLSX 등 → 텍스트 | Microsoft MarkItDown | `uvx --from 'markitdown[pptx]' markitdown FILE`로 실행 시 받아 쓴다. 배치·편집성은 보장하지 않음 |
| 초안 PPT 그림 꺼내기 | `unzip -j FILE.pptx 'ppt/media/*' -d figures/draft/` | 표준 도구 |
| CSV·간단한 표 | 표준 `csv`/`sqlite3` | 표 분석이 필요하면 `uv run --with pandas --with openpyxl`로 임시 실행 |
| 문서 변환 | Pandoc(pypandoc-binary) | 변환 후 표·수식·출처 확인 |

## 논문 PDF

`extract-paper`는 `.build/editorial/papers/`에 페이지별 Markdown·PNG 후보·원본 해시를 쓰며 원본과 기존 결과를 덮어쓰지 않는다. [PyMuPDF4LLM API](https://pymupdf.readthedocs.io/en/latest/pymupdf4llm/api.html)의 `write_images`, `image_path`, `page_chunks`를 쓰고 layout 확장·OCR·모델 가중치는 설치하지 않는다. 스캔·복잡한 패널·수식은 원본 페이지를 렌더링해 확인하고, 추출이 실패하면 페이지 렌더링·크롭으로 보완한다. 대안으로 [Marker](https://github.com/datalab-to/marker), [Docling](https://docling-project.github.io/docling/examples/export_figures/)이 있다.

## 이미지 속 수식 OCR

필요할 때 따로 고른다. 출력은 원문 이미지와 대조하며, 지수·첨자·기호·표 셀을 자동 추출만으로 확정하지 않는다.

| 후보 | 용도 | 조건 |
| --- | --- | --- |
| [Mathpix](https://docs.mathpix.com/) | 수식 이미지 → LaTeX/MathML | 외부 유료 API. 계정·자료 전송 동의 필요 |
| [Nougat](https://github.com/facebookresearch/nougat#license) | 학술 PDF → 텍스트·LaTeX | 코드 MIT, 모델 가중치 CC-BY-NC |
| [Marker](https://github.com/datalab-to/marker#commercial-usage) | PDF → Markdown·표·수식 | 코드 Apache-2.0, 모델은 수정된 OpenRAIL-M |

## 라이선스

PyMuPDF·PyMuPDF4LLM은 [AGPL-3.0 / 상용 이중 라이선스](https://pymupdf.readthedocs.io/en/latest/about.html#license-and-copyright), Pandoc은 [GPL](https://github.com/jgm/pandoc/blob/main/COPYING), MarkItDown은 [MIT](https://github.com/microsoft/markitdown/blob/main/LICENSE)다. 이 도구들을 MIT라고 안내하지 않는다.
