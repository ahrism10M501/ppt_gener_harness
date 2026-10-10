# Task 문서 스키마 v1

네 Markdown 문서는 YAML frontmatter와 비어 있지 않은 본문을 갖는다. Stage 1~3은 task의 `plan/`에, Stage 4는 task 루트의 `slides.md`에 둔다. 아래 예시는 형식을 설명하는 합성 자료이며 실제 연구 결과가 아니다. task_id는 실제 폴더 이름으로 바꾼다. 자료의 날짜·`yes` 등 YAML에서 다른 타입으로 읽히는 값은 문자열 따옴표로 감싼다.

## 공통 frontmatter

```yaml
schema_version: 1
task_id: 261011-example-il-progress
stage: 1
status: draft
approval_hash: null
upstream_hashes: {}
assumptions:
  - 청중은 BC 개념을 알고 있다. 에이전트 추정이며 승인 요약에서 확인한다.
open_items:
  - id: Q06
    description: 독립 평가의 표본 수를 확인해야 한다.
    blocking: true
review: {} # 아래의 단계별 구조로 작성한다.
```

schema_version·task_id·stage·status·approval_hash·upstream_hashes는 필수다. assumptions/open_items는 생략 시 빈 목록으로 읽는다. 중복 YAML 키, 잘못된 타입, NaN/무한대, 폴더와 다른 task ID, 다른 문서의 stage 번호를 거부한다. open item ID는 유일해야 한다. draft 문서의 review는 작성 중일 수 있으나 승인 시 필수 항목이 완성되어야 한다.

status/approval_hash/upstream_hashes는 `approve`만 기록한다. 해시는 나머지 frontmatter와 본문을 대상으로 한다. 승인 필드의 표현 순서·포맷은 해시를 바꾸지 않는다. 본문과 중요한 가정·미해결·review·추가 frontmatter 변경은 해시를 바꾼다. Markdown 문서의 CRLF와 LF는 동일하게 정규화한다.

status의 content_hash는 문서 자체의 해시이며 approval_hash에 저장한다. review_hash는 content_hash와 현재 상위 입력 해시를 함께 묶은 **검토 대상 해시**다. 에이전트는 review_hash를 보여 승인받고 `--expected-hash`에 전달한다. 본문이 그대로여도 검토 이후 원자료가 바뀌면 review_hash가 달라져 승인하지 않는다. 이 옵션 없이 명령을 직접 실행하면 실행 시점의 입력을 승인한다.

## Stage 1 — plan/interview.md

stage는 1이다. 아래 내용을 공통 frontmatter의 review에 넣는다. 필수 문자열/목록은 비어 있거나 TBD/TODO일 수 없다. 본문에는 질문·선택지·실제 답변·근거 위치·추가 확인 횟수·합의한 전제·승인 요약을 남긴다.

```yaml
review:
  audience: BC를 아는 연구실 교수와 대학원생
  purpose: 다음 주에 수집할 실패 사례의 우선순위를 결정받는다.
  key_evidence:
    - sources/evaluation.csv — 독립 평가 자료의 위치와 실제 관찰 범위
  success_criteria:
    - 개선 주장과 남은 한계를 청중이 구분한다.
  constraints:
    - 진행보고 10분, 실제 실험 조건 포함
```

핵심 근거가 없는 경우 꾸며서 채우지 않는다. 알고 있는 범위와 필요한 근거를 기록하고 blocking 항목이 해결되거나 주장 범위가 좁아질 때까지 승인하지 않는다.

## Stage 2 — plan/brief.md

stage는 2다. 후보 2~3개의 ID는 유일해야 한다. 선택한 후보의 message/storyline이 최종 key_message/storyline과 같아야 한다. 후보를 수정했다면 그 내용을 먼저 갱신한다. 본문에 추천 이유·사용자 선택·범위·전제를 기록한다.

```yaml
review:
  topic: 모방학습 진행보고
  selected_candidate: A
  key_message: 실패 사례를 먼저 분류해 다음 수집의 우선순위를 정한다.
  storyline:
    - 관찰한 실패
    - 근거와 한계
    - 다음 수집 제안
  candidates:
    - id: A
      message: 실패 사례를 먼저 분류해 다음 수집의 우선순위를 정한다.
      storyline: [관찰한 실패, 근거와 한계, 다음 수집 제안]
      evidence: [sources/evaluation.csv]
      tradeoff: 피드백 목적에 적합하지만 전체 방법 설명은 짧아진다.
    - id: B
      message: 학습과 독립 평가의 차이를 통해 개선 과제를 정리한다.
      storyline: [학습 설정, 독립 평가, 개선 과제]
      evidence: [sources/training.csv, sources/evaluation.csv]
      tradeoff: 배경 설명에 적합하지만 수집 우선순위의 결론이 늦다.
```

## Stage 3 — plan/outline.md

stage는 3이다. review.slides의 필수 필드는 id·topic·headline·evidence·seconds, 선택 필드는 section·figure다. 그 밖의 필드(좌표·폰트·색·layout 등)는 거부한다. ID는 영문자로 시작하는 1~32자의 영문/숫자/밑줄/하이픈이고 중복할 수 없다. topic은 상단 바에 들어갈 짧은 이름, headline은 그 슬라이드의 핵심 문장이다([DESIGN](../DESIGN.md)의 이름 규칙). figure는 연구자에게 요청할 그림 제안이다. seconds는 양의 정수, duration_minutes는 양의 유한 숫자다. 예상 시간 합이 시간 예산을 넘으면 승인하지 않는다.

```yaml
review:
  duration_minutes: 10
  slides:
    - id: S01
      section: 실패 분석
      topic: 실패 유형
      headline: 실패 분류로 다음 수집의 우선순위를 정한다
      evidence: [sources/evaluation.csv]
      figure: 실패 유형별 빈도 막대그래프 — sources/evaluation.csv로 연구자가 작성
      seconds: 90
    - id: S02
      section: 실패 분석
      topic: 독립 평가
      headline: 조건 차이를 줄인 독립 평가가 필요하다
      evidence: [sources/training.csv, sources/evaluation.csv]
      seconds: 120
```

레이아웃은 slides.md의 내용에서 정해지므로 목차에 적지 않는다. 표지·목차·마무리는 빌드가 만들므로 목차에 넣지 않는다. 근거 필드는 비어 있지 않아야 하지만 스키마 검사는 근거의 사실성·파일 존재·시간 추정의 타당성을 자동 판정하지 않는다. 에이전트와 사용자 검토가 필요하다.

## Stage 4 — slides.md

stage는 4다. `rvppt new`가 frontmatter를 만든다. `deck`에는 표지의 제목·부제·날짜·발표자·소속을, review에는 language(ko/en)를 넣는다. 본문의 `## 토픽`/`### 핵심 문장` 순서가 목차의 topic/headline과 일치해야 승인할 수 있다. 연구자가 본문을 직접 고쳐 달라지면 status가 `invalid`로 표시하므로 목차를 갱신해 다시 승인받는다. 빌드는 승인 전에도 가능하다. 코드 fence·HTML 주석 안의 제목 형태는 슬라이드로 세지 않는다.

```yaml
deck:
  title: 모방학습 진행보고
  date: '2026-10-11'
  presenter: 홍길동 (Gildong Hong)
  affiliation: [경기대학교 창의공과대학 전자공학과 N학년, Robotics and Vision Lab Robot Team]
review:
  language: ko
```

```markdown
# 실패 분석 | Failure Analysis

## 실패 유형

### 실패 분류로 다음 수집의 우선순위를 정한다

- 확인한 실패 사례와 근거를 여기에 적는다.

![실패 유형별 빈도 막대그래프](figures/failure-types.png)

## 독립 평가

### 조건 차이를 줄인 독립 평가가 필요하다

승인된 목차에 맞춰 내용·자료·출처를 적는다.
```

그림·표·수식·노트의 상세 문법과 빌드·QA는 [rendering](rendering.md)을 따른다. 제목/순서 확인과 승인 해시는 렌더 QA를 대신하지 않는다.

## 입력 해시와 유효성

모든 단계는 sources/의 상대 경로와 파일 바이트 해시를 기록한다. Stage 2~4는 모든 이전 단계의 내용 해시도 기록하고 Stage 4는 figures/ 해시를 추가한다. 폴더가 없거나 비어 있으면 동일한 빈 입력 해시다. 파일 추가/삭제/이름 변경도 입력 변경이다. 자료는 정규 파일로 task 안에 보관하며 입력 폴더·파일 및 단계 문서의 symlink는 거부한다.

| computed effective_status | 의미 |
| --- | --- |
| missing | 단계 문서가 없음 |
| draft | 작성 중 또는 재승인 필요 |
| approved | 내용/상위 입력/이전 단계 승인이 모두 현재와 일치 |
| stale | 저장된 승인은 있으나 내용·자료·상위 승인이 변경됨 |
| invalid | frontmatter/스키마 오류 또는 승인된 문서에 blocking/불완전 review가 있음 |

status는 읽기 전용이고 파일의 선언 status는 draft/approved 둘 중 하나다. approve는 이전 단계의 현재 승인을 요구하며 뒤 단계의 승인을 무효화한다. 동일한 유효 승인을 다시 기록하면 파일을 수정하지 않는다. 네 단계가 모두 유효하면 `content_approved`가 true이고 build 리포트에도 같은 값이 기록된다.

content_hash는 내용 동일성 검사이며 사용자 승인 자체의 인증 수단은 아니다. 에이전트는 명시적인 사용자 승인 후에만 approve를 호출한다.
