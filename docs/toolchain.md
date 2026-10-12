# 도구 구성과 제약

제작 경로는 **Markdown → Pandoc AST·네이티브 블록 → python-pptx/XML 고정 배치 → LibreOffice 렌더 QA**다. 작성 문법은 [rendering](rendering.md), 코드 구조는 [architecture](architecture.md), 설치는 [setup](setup.md)을 따른다.

## 양식과 의존성

원본 마스터·로고·테마·장식은 보존하고 같은 마스터에 Pandoc 이름 7개와 RVLAB 고정 그림 그리드를 추가한다. 파생 reference에서만 표본 슬라이드·발표자·날짜·노트·Google 메타데이터를 제거한다. Pandoc이 본문 placeholder를 찾도록 `p:ph`의 `type` 속성을 생략하고 lxml로 기존 XML 네임스페이스를 보존한다.

Python 의존성은 python-pptx(구조·표·노트), lxml(OOXML), PyYAML(토큰), Pillow(측정·미리보기), PyMuPDF(PDF→PNG·텍스트 검사), pypandoc-binary(Pandoc)이며 `uv.lock`에 버전을 고정한다. LibreOffice는 외부 실행 파일이다. Node의 MathJax·Mermaid CLI·resvg는 `package-lock.json`에 고정하며 XML 파서 보정 버전은 `package.json`의 override를 따른다.

## 렌더링 제약

논문 PDF→Markdown·media 추출은 고정된 PyMuPDF4LLM 0.2.9와 기존 PyMuPDF를 사용한다. `uv run rvppt extract-paper TASK <sources/ 또는 figures/external/의 PDF>`는 `.build/editorial/papers/`에만 변환 결과를 쓰며 원본과 기존 결과를 덮어쓰지 않는다. API·OCR·layout 모델은 필요하지 않다. 캡션·본문 기반 선택과 출처 기록은 [외부 시각 자료 절차](../skills/rvlab-ppt/references/external-visuals.md)를 따른다.

Arial·맑은 고딕이 없으면 Liberation Sans·Noto Sans CJK KR로 대체한다. 글꼴 대체는 줄바꿈을 바꾸므로 실제 선택 폰트로 렌더링과 오버플로 검사를 수행한다.

수식의 작성·산출물·검수 기준은 [제작 문법](rendering.md#수식)을 따른다. 플랫폼별 실행·편집 검증 범위는 빌드 리포트에 기록한다.

수식·PDF·DOCX·XLSX 등 입력 자료 처리와 일반 문서 생성은 [문서 도구 안내](document-tools.md)를 따른다. 외부 스킬 원문과 추가 런타임이 포함되어 있다는 의미는 다르며, 일반 PPTX 스킬로 RVLAB 고정 양식·승인 절차를 우회하지 않는다.

## 연구 그림·애니메이션

`visual` extra의 Manim CE·Matplotlib·SciencePlots는 그림 자산을 만드는 선택 도구다. PPTX 생성은 기존 RVLAB 경로를 사용한다. `uv.lock`이 버전을 고정하고 `doctor`의 `visual_tools`는 설치·import 여부를 읽기 전용으로 확인한다. 빠져 있어도 일반 PPT 빌드를 막지 않는다.

Manim은 MIT, SciencePlots는 MIT, Matplotlib은 PSF 기반의 BSD 호환 라이선스다. Cairo/Pango 개발 패키지와 한글 폰트는 OS 의존성이며 Python extra로 설치되지 않는다. LaTeX는 `Tex`·`MathTex`를 쓸 때만 별도로 필요하다. 설치는 [setup](setup.md#그림애니메이션-선택-도구), 외부 스킬의 적용 범위는 [skills](skills.md)를 따른다.
