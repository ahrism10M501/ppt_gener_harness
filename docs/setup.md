# 설치와 환경 점검

저장소 루트에서 실행한다. Python 3.11~3.14, uv, Node 22 이상, LibreOffice와 한글·영문 폰트가 필요하다. Python·Node 패키지는 lockfile로 고정하고 외부 스킬은 저장소에 포함한다.

## 처음 설치

```bash
uv sync --frozen
npm ci
cp profile.example.yaml profile.yaml
uv run rvppt doctor
```

스킬 진입점(`.claude/skills/`, `.agents/skills/`, `.claude/agents/`)은 `skills/`를 가리키는 심볼릭 링크다. Windows에서는 먼저 설정 → 시스템 → 개발자용에서 개발자 모드를 켜고 `git clone -c core.symlinks=true <저장소 URL>`로 받는다. 이미 받았다면 `git config core.symlinks true` 후 `doctor`가 알려 주는 경로를 `git checkout -- <경로>`로 다시 받는다. 링크가 한 줄짜리 텍스트 파일로 받아지면 에이전트가 프로젝트 스킬을 찾지 못한다.

`profile.yaml`에 이름·소속을 입력한다. 이 개인 파일은 Git에서 제외된다. 기존 파일이 있으면 복사하지 말고 내용을 확인한다. 배포된 `templates/RVLAB_reference.pptx`를 사용하므로 처음 설치할 때 양식을 재생성할 필요는 없다.

Mermaid는 Chrome 또는 Chromium을 사용한다. 기존 브라우저를 사용할 때는 `npm ci` 전에 `PUPPETEER_SKIP_DOWNLOAD=true`를 설정한다. 설치된 Chrome은 자동으로 찾으며, 다른 위치라면 `PUPPETEER_EXECUTABLE_PATH`에 실행 파일 경로를 지정한다.

## 환경 점검

`doctor`는 Python·Pandoc·양식·외부 스킬 해시·LibreOffice·폰트·Node 렌더러를 점검한다. Mermaid 브라우저와 `profile.yaml`은 선택 점검 항목이다. 네트워크를 쓰거나 파일을 수정하지 않으며 필수 항목이 실패하면 종료 코드 2를 반환한다.

폰트는 Arial·맑은 고딕을 우선하고 Liberation Sans·Noto Sans CJK KR 대체를 허용한다. 빌드에 사용한 실제 폰트는 task의 `.build/output/build-report.json`에 기록된다.

## OS별 도구 설치

없는 도구만 설치한다. 에이전트가 sudo·시스템 설치를 수행할 때는 명령과 이유를 제시해 사용자 확인을 받는다.

| OS | uv·Node | LibreOffice | 대체 폰트 |
| --- | --- | --- | --- |
| Ubuntu | [uv 설치 안내](https://docs.astral.sh/uv/getting-started/installation/), Node 22+ | `sudo apt install libreoffice-impress` | `sudo apt install fonts-liberation fonts-noto-cjk` |
| macOS | `brew install uv node` | `brew install --cask libreoffice` | `brew install --cask font-noto-sans-cjk-kr` |
| Windows (PowerShell) | `winget install astral-sh.uv`, `winget install OpenJS.NodeJS.LTS`, 개발자 모드 | `winget install TheDocumentFoundation.LibreOffice` | Arial·맑은 고딕 설치 여부 확인 |

LibreOffice는 PATH에서 찾으며 macOS의 `/Applications/LibreOffice.app/Contents/MacOS/soffice`와 Windows의 Program Files 경로도 확인한다. Ubuntu snap 버전은 변환 입력을 읽을 수 있도록 `~/snap/libreoffice/common/`에 임시 파일을 둔다. Mermaid용 Chrome도 PATH 다음에 macOS 응용 프로그램 폴더와 Windows 설치 경로를 확인한다.

모든 OS가 같은 LibreOffice 렌더링을 기준으로 미리보기·넘침 검사를 한다. 외부 스킬 해시와 단계 승인 해시는 LF 바이트 기준이므로 `.gitattributes`가 체크아웃 줄바꿈을 LF로 고정한다. Windows에서 이 파일이 생기기 전에 clone했다면 `git config core.autocrlf false` 후 작업 트리를 다시 체크아웃해야 `doctor`의 skills 점검이 통과한다.

macOS·Windows 실행과 PowerPoint의 실제 편집·표시는 별도 확인이 필요하다. LibreOffice 미리보기로 PowerPoint의 OMML 편집성을 확인했다고 간주하지 않는다.

Typst·LaTeX·.NET·OCR 등 추가 문서 처리 도구는 자동 설치하지 않는다. 필요한 런타임과 라이선스는 [문서 도구 안내](document-tools.md)를 따른다.

설치 후 발표를 만들려면 [README](../README.md)와 [워크플로우](workflow.md)를, 코드·양식을 유지보수하려면 [구조](architecture.md)를 따른다.

## 그림·애니메이션 선택 도구

Manim Community Edition, Matplotlib, SciencePlots는 선택 의존성 `visual`로 설치한다. 일반 PPT 빌드에는 필요하지 않다.

```bash
uv sync --frozen --extra visual
uv run --extra visual python -m manim --version
uv run --extra visual rvppt doctor
```

Linux에서는 Manim의 pycairo/manimpango 빌드에 Cairo·Pango 개발 헤더와 pkg-config, C 컴파일러가 필요하다. Ubuntu에서 컴파일러와 pkg-config가 이미 있을 때 필요한 명령은 `sudo apt-get install libcairo2-dev libpango1.0-dev`다. 에이전트는 시스템 설치 전에 명령·이유를 보여 주고 확인받는다. Windows·macOS 설치는 [Manim 설치 안내](https://docs.manim.community/en/stable/installation.html)를 따른다.

한글은 `Text`와 설치된 Noto Sans CJK KR/맑은 고딕으로 처리한다. `Tex`·`MathTex`는 별도 LaTeX 환경이 필요하며 `visual` 설치에 포함되지 않는다. SciencePlots의 논문용 크기·색·폰트를 RVLAB 슬라이드에 그대로 적용하지 않고 [rvlab.mplstyle](design/rvlab.mplstyle)을 사용한다. Matplotlib 호출자는 `resolve_fonts(load_tokens())`로 확인한 영문·한글 폰트를 `font.family`에 함께 지정해 한글 누락을 피한다. 외부 스킬 원문과 라이선스는 저장소에 포함되므로 실행 중 다시 내려받지 않는다.

### 로컬 자동 도식

`rvlab-charts`의 흐름·분기·그룹·피드백·순차 도식은 `beautiful-mermaid`와 기존 resvg를 사용한다. `npm ci`로 고정 버전을 설치하며 별도 MCP 서버·브라우저·외부 계정·API 키가 필요하지 않다. 렌더링은 로컬에서 실행한다. 이 경로에는 `visual` extra도 필요하지 않다.

```bash
uv run python skills/rvlab-charts/diagrams.py demo .cache/diagram-demo
```

PNG·SVG와 실제 폰트/가독성 JSON을 생성한다. 자세한 입력·검수 절차는 [로컬 도식](../skills/rvlab-charts/references/local-diagrams.md)을 따른다. 기존 `slides.md`의 Mermaid 코드 블록 빌드는 Chromium 경로를 그대로 사용한다.
