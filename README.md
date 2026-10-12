# RVLAB PPT Generator

> **에이전트에 붙여넣기**
> - 처음 설치: `AGENTS.md와 docs/setup.md를 읽고 셋업해줘.`
> - 발표 만들기: `tasks/<폴더>의 자료로 RVLAB PPT 만들어줘.` (폴더가 없으면 제목만 알려 주세요)

1. 처음 한 번 `profile.example.yaml`을 `profile.yaml`로 복사해 이름·소속을 채웁니다.
2. `uv run rvppt new <slug> --title "<발표 제목>" --date YYYY-MM-DD`로 발표 폴더를 만듭니다.
3. `sources/`에 논문·데이터·메모·초안 PPT를, `figures/`에 그림을 넣습니다.
4. 에이전트에게 “RVLAB PPT 만들어줘”라고 요청하고 인터뷰·핵심 메시지·목차·내용을 확인·승인합니다. 에이전트가 필요한 웹 사진·논문 figure를 찾아 출처와 함께 넣고, 도식·차트를 만들며, 새 연구 결과 그래프는 제안합니다. 한국어 발표는 승인 전에 윤문까지 거칩니다.
5. `slides.md`를 직접 고쳐도 됩니다. `uv run rvppt build tasks/<task>`가 폴더 안에 `YYYYMMDD_제목.pptx`와 PDF를 만듭니다.

`<slug>`는 폴더 이름에 붙는 짧은 영문 별칭입니다(소문자·숫자·하이픈). 아래 명령은 `tasks/260831-train-loop/`를 만듭니다.

```bash
cp profile.example.yaml profile.yaml   # 처음 한 번, 이름·영문 이름·소속 두 줄 입력
uv run rvppt new train-loop --title "학습루프개선 및 실험" --subtitle "Advanced Train Loop & Experiments" --date 2026-08-31
uv run rvppt build tasks/260831-train-loop
```

```text
tasks/260831-train-loop/
├── slides.md        # 발표 원본 (# 섹션 / ## 상단 바 토픽 / ### 핵심 문장)
├── figures/         # 연구자 그림·외부 사진·논문 figure. 없는 그림은 요청 상자로 표시
├── sources/         # 논문·데이터·초안 PPT (읽기 전용, Git 제외)
├── plan/            # 인터뷰·메시지·목차 승인 문서
├── 20260831_학습루프개선_및_실험.pptx / .pdf
└── .build/          # 미리보기 PNG·리포트
```

완성 예제: [tasks/261011-example-il-progress](tasks/261011-example-il-progress/slides.md). `uv run rvppt status tasks/<task>`로 이어갈 단계를 확인하고 `uv run rvppt preview tasks/<task>`로 최신 PNG를 봅니다.

교육용 GIF는 `figures/이름.gif`와 같은 크기의 대표 `figures/이름.png`를 함께 넣습니다. GIF는 PPTX에서, PNG는 PDF·미리보기에서 사용합니다. 제작·사용 기준은 [교육 애니메이션 스킬](skills/rvlab-animation/SKILL.md), Manim·SciencePlots 설치는 [setup](docs/setup.md)을 따릅니다.

## 문서 찾기

수식이 있는 발표는 편집형과 `_수식호환.pptx`를 함께 생성합니다. 용도와 원본 편집 방법은 [수식 문법](docs/rendering.md#수식)을 참고하세요.

외부 사진은 에이전트가 검색하고, 논문은 `uv run rvppt extract-paper tasks/<task> sources/<paper>.pdf`(에이전트가 내려받은 PDF는 `figures/external/<paper>.pdf`)로 Markdown·media를 분리해 설명에 맞는 figure를 고릅니다. [외부 시각 자료 절차](skills/rvlab-ppt/references/external-visuals.md)를 참고하세요.

| 필요한 정보 | 문서 |
| --- | --- |
| 설치·환경 점검 | [셋업](docs/setup.md) |
| 발표 기획·내용 승인 | [워크플로우](docs/workflow.md) |
| 그래프·도식·GIF 선택과 제작 연결 | [시각 설계 절차](skills/rvlab-ppt/references/visual-planning.md) |
| Markdown 작성·빌드·렌더 QA | [제작 문법](docs/rendering.md) |
| 단계 문서의 필드·승인 해시 | [문서 스키마](docs/schemas.md) |
| 고정 양식·디자인 토큰 | [양식 설계](DESIGN.md) |
| 코드 구조·유지보수 | [구조](docs/architecture.md) |
| 도구 선택·제약 | [도구 구성](docs/toolchain.md) |
| 에이전트 공통 규칙 | [AGENTS.md](AGENTS.md) |


## 포함한 외부 스킬

별도 설치 없이 프로젝트의 `skills/`에서 고정 버전을 사용합니다. 원문과 저작권 고지·라이선스 전문을 보존합니다.

- [im-not-ai](https://github.com/epoko77-ai/im-not-ai): 한국어 진단·윤문·검증. [MIT](skills/im-not-ai/LICENSE).
- [gstack / office-hours](https://github.com/garrytan/gstack): 인터뷰의 근거·전제·대안 탐색 참고 자료. [MIT](skills/office-hours/LICENSE), [제3자 고지](skills/office-hours/NOTICE.md).
- [superpowers / brainstorming](https://github.com/obra/superpowers): 의도 탐색·재진술 참고 자료. [MIT](skills/brainstorming/LICENSE).

고정 커밋과 파일 해시는 [dependencies.yaml](skills/dependencies.yaml), 실제 사용 범위와 제약은 [외부 스킬 안내](docs/skills.md)에 있습니다.

수식·PDF·Word·Excel 처리를 위한 `typst`, `pdf`, `minimax-docx`, `minimax-xlsx`도 포함했습니다. 일반 `pptx-generator`는 참고용입니다. 포맷별 도구 선택, 실제 라이선스, 미설치 의존성은 [수식·PDF·문서 도구 안내](docs/document-tools.md)를 확인하세요.
