# 도구 구성과 제약

제작 경로는 **Markdown → Pandoc AST·네이티브 블록 → python-pptx/XML 고정 배치 → LibreOffice 렌더 QA**다. 작성 문법은 [rendering](rendering.md), 코드 구조는 [architecture](architecture.md), 설치는 [setup](setup.md)을 따른다.

## 양식과 의존성

원본 마스터·로고·테마·장식은 보존하고 같은 마스터에 Pandoc 이름 7개와 RVLAB 고정 그림 그리드를 추가한다. 파생 reference에서만 표본 슬라이드·발표자·날짜·노트·Google 메타데이터를 제거한다. Pandoc이 본문 placeholder를 찾도록 `p:ph`의 `type` 속성을 생략하고 lxml로 기존 XML 네임스페이스를 보존한다.

Python 의존성은 python-pptx(구조·표·노트), lxml(OOXML), PyYAML(토큰), Pillow(측정·미리보기), PyMuPDF(PDF→PNG·텍스트 검사), pypandoc-binary(Pandoc)이며 `uv.lock`에 버전을 고정한다. LibreOffice는 외부 실행 파일이다. Node의 MathJax·Mermaid CLI·resvg는 `package-lock.json`에 고정하며 XML 파서 보정 버전은 `package.json`의 override를 따른다.

## 렌더링 제약

Arial·맑은 고딕이 없으면 Liberation Sans·Noto Sans CJK KR로 대체한다. 글꼴 대체는 줄바꿈을 바꾸므로 실제 선택 폰트로 렌더링과 오버플로 검사를 수행한다.

편집용 PPTX에는 OMML 수식을 우선 보존한다. LibreOffice에서 표시되지 않는 수식은 미리보기 사본에서 이미지로 대체하며 검사 리포트에 기록한다. LibreOffice PNG·PDF 검사는 PowerPoint의 네이티브 수식 표시·편집성 검사를 대신하지 않는다. macOS·Windows 실행과 PowerPoint 앱의 실제 편집은 별도 확인이 필요하다.

수식·PDF·DOCX·XLSX 등 입력 자료 처리와 일반 문서 생성은 [문서 도구 안내](document-tools.md)를 따른다. 외부 스킬 원문과 추가 런타임이 포함되어 있다는 의미는 다르며, 일반 PPTX 스킬로 RVLAB 고정 양식·승인 절차를 우회하지 않는다.
