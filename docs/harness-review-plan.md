# 지침·스킬·도구 검토와 수정 계획 (2026-10-12)

기준: **양식(마스터·레이아웃·폰트·색·좌표·렌더 넘침)은 강제**하고, **본문 내용(문장·분량·어조·구성·절차 서류)은 권고**로 둔다. 사실 날조 금지·원자료 보존·승인 해시는 유지한다.

## 1. 진입점

| 문제 | 근거 | 수정 |
| --- | --- | --- |
| 읽는 순서가 길다. AGENTS → README → rvlab-ppt → DESIGN → visual-planning → charts → animation → interview → workflow → schemas → polish를 처음부터 다 읽게 된다 | `AGENTS.md:7-13` | AGENTS는 "무엇을 하려는가 → 어느 스킬 하나"의 라우팅 표로 바꾼다. 세부 문서는 스킬이 필요할 때 연결한다 |
| DESIGN.md를 매번 읽게 하지만 앞 75줄은 빌드용 토큰 YAML이다. 에이전트에게 필요한 건 이름 규칙(표지·목차·섹션·토픽·핵심 문장) 정도다 | `skills/rvlab-ppt/SKILL.md:12`, `DESIGN.md:5-75` | rvlab-ppt는 DESIGN의 "슬라이드 문법과 이름 규칙" 절만 가리키게 한다. 토큰은 코드가 강제한다 |
| AGENTS가 Gemini·Antigravity를 말하지만 `GEMINI.md`는 없다. `CODEX.md`는 Codex가 읽지 않는 파일이다(Codex는 `AGENTS.md`를 읽음) | 루트 파일 목록 | `CODEX.md` 삭제, `GEMINI.md`(`@AGENTS.md`) 추가. Gemini·Antigravity의 스킬 발견 경로는 실제 도구로 확인한 뒤 적는다 |
| README 상단 "붙여넣기"는 셋업만 안내한다. 발표 제작을 시작하는 문장이 4번 항목 안에 묻혀 있다 | `README.md:3,8` | 상단에 셋업용·발표 시작용 붙여넣기 문장을 하나씩 둔다 |
| graphify-out을 지웠는데 AGENTS·architecture·CLI가 아직 참조한다. 지금 `rvppt graph-check`는 실패한다 | `AGENTS.md:13,56`, `docs/architecture.md:18,51`, `tools/rvppt/graph.py:48` | **결정 필요:** (a) 그래프를 다시 만들고 유지 / (b) graphify 참조·`graph-check`·`graph.py`·`.graphifyignore` 제거. 지운 상태가 의도였다면 (b)를 추천 |
| 추적 중인 예제 `2601-world-model1`은 `sources/`가 Git에서 빠져 있어, 새로 받은 저장소에서 status가 `stale`로 나온다 | `.gitignore` 예외 목록, `rvppt status tasks/2601-world-model1` | 그 예제의 sources를 추적하거나, 예제 목록에서 빼고 il-progress만 완성 예제로 둔다 |

## 2. 매끄럽지 않은 부분 (불일치·중복·낡은 내용)

1. **승인 절차를 여섯 군데에서 반복한다.** AGENTS·workflow(두 번)·interview·rvlab-ppt·schemas가 같은 내용을 조금씩 다른 표현으로 쓴다. 단계 보고 형식도 AGENTS·workflow·interview·rvlab-ppt에 흩어져 있다. → 승인 규칙은 `docs/workflow.md`, 필드는 `docs/schemas.md`, 단계 보고 형식은 `rvlab-interview`만 쓰고 나머지는 링크로 바꾼다.
2. **새 그림을 만들어도 되는지가 문서마다 다르다.**
   - rvlab-ppt `:37`은 꾸밈 차트를 그냥 만든다고 하고, `:38`과 lab-meeting `:30`, visual-planning `:13`은 "사용자가 요청한 범위에서"라고 한다.
   - "연구 결과 그래프는 요청 시에만" 문구가 6곳 이상에 반복된다.
   - → 규칙을 하나로 정리한다. 확인된 자료로 만드는 도식·꾸밈 차트·논문 figure 가공은 에이전트 재량으로 하고, **새 연구 결과 그래프와 GIF만** 요청을 받아서 만든다. 이 규칙은 AGENTS에만 적는다.
3. **애니메이션 스킬 안에서 지시가 충돌한다.** `rvlab-animation/SKILL.md:8`은 "GIF를 직접 요청해도 의도와 정적 대안을 확인한다"고 하고, `:12`·`:16`은 "제작 허가를 다시 묻지 않는다"고 한다. → 요청이 있으면 만들고, 정적 대안은 질문하지 않고 결과 보고에서 한 줄로 제안한다.
4. **외부 논문 PDF를 어디에 둘지가 승인 해시와 맞지 않는다.**
   - `extract-paper`는 `sources/*.pdf`만 받는다(`tools/rvppt/papers.py:21`).
   - 그런데 `sources/`에 파일을 더하면 Stage 1부터 모든 승인이 풀린다.
   - 그래서 Stage 4에 논문 figure가 필요해지면 처음부터 다시 승인받아야 한다(`external-visuals.md:14`).
   - → 에이전트가 내려받은 공개 PDF는 `figures/external/`(Stage 4 해시)에 두고, `extract-paper`가 그 경로도 받게 한다.
5. **그림 요청 문법이 문서마다 다르다.** workflow `:57`은 `![요청 내용](path)`, rendering `:78-81`은 `![캡션](path "요청")`이다. → rendering 문법 하나로 맞춘다.
6. **설명이 낡았거나 서로 다르다.**
   - rendering `:121`은 `figures/`를 "연구자가 넣는 그림"이라고만 쓴다.
   - document-tools `:9`에는 "OMML 우선, 이미지 fallback"이라는 옛 표현이 남아 있다.
   - document-tools `:18`은 MarkItDown을 미설치라고 하지만, workflow `:18`은 `uvx markitdown`으로 바로 쓰라고 한다.
7. **안내 문서에 변경 기록이 섞여 있다.**
   - `docs/skills.md:33-37`: "새 파일 119개를 추가했고…", "이번에 실행하지 않았다".
   - `docs/document-tools.md:3,71,97`: "이번 추가는…".
   - document-tools `:48-52`는 합니다체이고 나머지는 한다체다.
   - → 변경 기록은 커밋 메시지로 옮기고, 문서에는 현재 상태만 남긴다.
8. **AGENTS의 "현재 명령" 문단이 CLI `--help`와 중복된다**(`AGENTS.md:55`). 명령이 추가될 때마다 같이 고쳐야 한다. → `uv run rvppt --help`를 가리키는 한 줄과 핵심 명령 3~4개만 남긴다.
9. **"검증하지 않은 걸 검증했다고 쓰지 않는다"는 문구가 10곳 넘게 반복된다**(GIF 재생·OMML·PowerPoint). → AGENTS 금지사항 한 줄과 rendering 한 곳에만 둔다.

## 3. 자유도를 과하게 억압하는 하네스

| # | 현재 | 영향 | 제안 |
| --- | --- | --- | --- |
| H1 | Stage 4의 `##`·`###`가 outline의 topic·headline과 **문자열까지 같아야** 승인된다(`tools/rvppt/state.py:173`). 윤문은 `###`를 못 바꾸고, 바꾸려면 Stage 3을 다시 승인받아야 한다(`polish.md:29`) | 본문을 쓰다 핵심 문장을 다듬기만 해도 목차 재승인이 필요하다. 사실상 승인 전 문장을 고칠 수 없는 구조 | 슬라이드 **수·순서·토픽**만 맞추고, headline 차이는 status·보고에 diff로 보여 주기만 한다(에러 → 경고). 윤문도 `###`를 다듬을 수 있게 하고 polish-check가 숫자·고유명사 보존을 확인한다 |
| H2 | 불릿 한 줄 42자(한글)·80자, 핵심 문장 52자, 불릿 5개를 **lint에서 하드 에러**로 막는다(`markdown.py:252,316-321`) | 실제 렌더 넘침 검사가 따로 있는데도 글자 수만으로 막는다. 짧은 불릿 6개 같은 정상적인 슬라이드도 실패한다 | 양식 강제는 렌더 QA(상자 넘침·줄 수)가 맡는다. 글자 수·불릿 개수는 lint 경고로 바꾼다. 상단 바 토픽 길이(한 줄 고정 양식)와 깊이 2는 유지한다 |
| H3 | Stage 2는 후보 2~3개가 **필수**다(`state.py:138`) | 사용자가 이미 메시지를 정해 와도 가짜 대안을 만들어야 한다 | 1~3개 허용. 1개면 본문에 "사용자 지정"이라고 적는다 |
| H4 | outline 시간 합이 발표 시간을 넘으면 승인이 거부된다(`state.py:161`) | 추정 시간에 불과한데 하드 게이트다 | 경고로 바꾸고 단계 보고에서 알린다 |
| H5 | 같이 만들기에서 질문해야 할 목록(5종), "3~5개 묶음", "추가 확인 최대 두 차례", 질문 기록(ID·이유·선택지·답·횟수·결론)이 정해져 있다(`rvlab-interview/SKILL.md:31-41`, `interview-guide.md:37`) | 회의록 같은 서류가 많고, 질문 수를 맞추려는 압박이 생긴다 | 원칙("자료로 답 못 하는 것만, 한 번에 몇 개씩")만 남긴다. 질문 기록은 결론·남은 가정 중심으로 줄이고 횟수 세기는 없앤다 |
| H6 | 한국어 핵심 문장 어미를 "섞는다"고 정해 두었다(`rvlab-ppt/SKILL.md:33`, `lab-meeting.md:20`) | 어조를 기계적으로 섞게 만든다 | "`~한다`로만 통일하지 말고 발표자 말투(기본 합니다체)를 따른다"로 완화한다 |
| H7 | 한국어 발표는 승인 전에 humanize-korean을 **기본 실행**한다(opt-out)(`rvlab-ppt/SKILL.md:44`, `polish.md:3`) | 매번 무거운 다중 에이전트 윤문을 돌리게 된다 | opt-in으로 바꾼다. Stage 4 보고에서 "윤문 돌릴까요?"를 한 줄로 제안한다 |
| H8 | 그림마다 6항목 인계 요약(visual-planning `:35-42`)을 쓰고, 애니메이션은 YAML storyboard `plan/animation.md`를 필수로 쓴다(`rvlab-animation/SKILL.md:16-34`) | 단순한 그림에도 설계 서류가 붙는다 | 그림을 새로 만들 때만 짧게 쓰고, 재사용 그림에는 출처만 남긴다. storyboard는 체크리스트로 남기되 파일 작성은 권장으로 바꾼다 |
| H9 | `### ` 아래 HTML 주석 외의 텍스트, 섹션 아래 notes 외 블록, 표 셀 서식 등은 모두 첫 번째 하드 에러에서 멈춘다(`markdown.py` 전반, `raise StateError`) | lint 한 번에 에러 하나만 보여서 고치고 다시 돌리는 일이 반복된다 | (선택) lint가 슬라이드별 오류를 모아 한 번에 보여 준다. 코드 변경이 커서 H1~H4 뒤로 미룬다 |

### 그대로 둘 것

원본 양식·파생 reference, 좌표·폰트·색·클래스 입력 금지, 렌더 넘침 QA, 상단 바 한 줄, 수치·인용 날조 금지, 인적사항 추측 금지, `sources/` 보존, 승인 해시와 `--expected-hash`, 사람이 고친 PPTX 덮어쓰기 방지.

## 4. 실행 순서

1. **결정 받기:** graphify 유지/제거, H1 완화 수준, H2 경고화 범위, H7 opt-in 여부, world-model 예제 처리.
2. **문서 정리(코드 무관):** 1장 진입점, 2장 1·2·3·5·6·7·8·9, H5·H6·H7·H8. AGENTS를 라우팅 표 중심으로 다시 쓴다.
3. **코드 완화:** H1(`state.py`), H2(`markdown.py` → `deck_findings` 경고), H3·H4(`state.py`), 2장 4번(`papers.py` 경로 허용). 각 항목마다 `tests/`의 해당 회귀 테스트를 고친다.
4. **확인:** `uv run python -m unittest discover -s tests`, `uv run rvppt doctor`, il-progress 예제 `status`·`lint`·`build`가 통과하는지 본다.
5. (선택) H9 lint 오류 모아 보기.
