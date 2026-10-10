# 설치와 환경 점검

저장소 루트에서 실행한다. Python 3.11~3.14, uv, Node 22 이상, LibreOffice와 한글·영문 폰트가 필요하다. Python·Node 패키지는 lockfile로 고정하고 외부 스킬은 저장소에 포함한다.

## 처음 설치

```bash
uv sync --frozen
npm ci
cp profile.example.yaml profile.yaml
uv run rvppt doctor
```

`profile.yaml`에 이름·소속을 입력한다. 이 개인 파일은 Git에서 제외된다. 기존 파일이 있으면 복사하지 말고 내용을 확인한다. 배포된 `templates/RVLAB_reference.pptx`를 사용하므로 처음 설치할 때 양식을 재생성할 필요는 없다.

Mermaid는 Chrome 또는 Chromium을 사용한다. 기존 브라우저를 사용할 때는 `npm ci` 전에 `PUPPETEER_SKIP_DOWNLOAD=true`를 설정하고, 필요하면 `PUPPETEER_EXECUTABLE_PATH`에 실행 파일 경로를 지정한다.

## 환경 점검

`doctor`는 Python·Pandoc·양식·외부 스킬 해시·LibreOffice·폰트·Node 렌더러를 점검한다. Mermaid 브라우저와 `profile.yaml`은 선택 점검 항목이다. 네트워크를 쓰거나 파일을 수정하지 않으며 필수 항목이 실패하면 종료 코드 2를 반환한다.

폰트는 Arial·맑은 고딕을 우선하고 Liberation Sans·Noto Sans CJK KR 대체를 허용한다. 빌드에 사용한 실제 폰트는 task의 `.build/output/build-report.json`에 기록된다.

## OS별 도구 설치

없는 도구만 설치한다. 에이전트가 sudo·시스템 설치를 수행할 때는 명령과 이유를 제시해 사용자 확인을 받는다.

| OS | uv·Node | LibreOffice | 대체 폰트 |
| --- | --- | --- | --- |
| Ubuntu | [uv 설치 안내](https://docs.astral.sh/uv/getting-started/installation/), Node 22+ | `sudo apt install libreoffice-impress` | `sudo apt install fonts-liberation fonts-noto-cjk` |
| macOS | `brew install uv node` | `brew install --cask libreoffice` | `brew install --cask font-noto-sans-cjk-kr` |
| Windows (PowerShell) | `winget install astral-sh.uv`, `winget install OpenJS.NodeJS.LTS` | `winget install TheDocumentFoundation.LibreOffice` | Arial·맑은 고딕 설치 여부 확인 |

LibreOffice는 PATH에서 찾으며 macOS의 `/Applications/LibreOffice.app/Contents/MacOS/soffice`와 Windows의 Program Files 경로도 확인한다. Ubuntu snap 버전은 변환 입력을 읽을 수 있도록 `~/snap/libreoffice/common/`에 임시 파일을 둔다.

macOS·Windows 실행과 PowerPoint의 실제 편집·표시는 별도 확인이 필요하다. LibreOffice 미리보기로 PowerPoint의 OMML 편집성을 확인했다고 간주하지 않는다.

Typst·LaTeX·.NET·OCR 등 추가 문서 처리 도구는 자동 설치하지 않는다. 필요한 런타임과 라이선스는 [문서 도구 안내](document-tools.md)를 따른다.

설치 후 발표를 만들려면 [README](../README.md)와 [워크플로우](workflow.md)를, 코드·양식을 유지보수하려면 [구조](architecture.md)를 따른다.
