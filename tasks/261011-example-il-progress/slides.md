---
schema_version: 1
task_id: 261011-example-il-progress
stage: 4
status: approved
approval_hash: c81e0c306f706848010c7dbbe231f9f08b185591305c9dba4ec7e806d9ccd057
upstream_hashes:
  sources/: 7caf77c746d8228fdc6ef56dc127342adebe114c96f7f00ba5cf4694071e938a
  plan/interview.md: 097aca58a6de81c83d5a92b1006748fbf75d208bc554d4bd0dd03229730c56d3
  plan/brief.md: ee7a9647d53056f12333ff39f613756a272a073910b39d043bbc4a369b121bfa
  plan/outline.md: 8a0e669e284f3f2b8de0839aa04578678dcc7d52cd20ca381de9ec95d558827c
  figures/: eb34b55455b899ebb182bfd62516bd07a7dc6e6381344cd4b507fd79059def96
assumptions:
- '가상 예제: 인물·과제·수치가 모두 합성이며 실제 실험 결과가 아니다.'
- 예제 시연용으로 에이전트가 자동 승인했다. 실제 발표자의 승인이 아니다.
open_items: []
deck:
  title: 모방학습 진행 보고
  subtitle: 행동 청크 길이 비교 · 가상 예제
  date: '2026-10-11'
  presenter: 홍길동 (Gildong Hong)
  affiliation:
  - 경기대학교 창의공과대학 전자공학과 N학년
  - Robotics and Vision Lab Robot Team
review:
  language: ko
---

# 지난 미팅 이후 | Since Last Meeting

## 진행 목표

### 지난 피드백에 따라 행동 청크 길이부터 비교했다

- 지난 피드백: 성공률보다 실패 원인을 먼저 볼 것
- 이번 목표: 청크 길이 $k$별 성공률과 실패 유형 확인
- 범위: 합성 pick-and-place 과제 1개

::: notes
가상 예제다. 모든 수치는 sources/의 합성 자료이며 실제 실험 결과가 아니다.
:::

# 실험 설정 | Setup

## 과제와 데이터

### 시연 200개로 학습하고 조건마다 40회 평가했다

| 조건 | 청크 길이 k | 학습 시연 | 평가 시행 |
|---|---:|---:|---:|
| BC | 1 | 200 | 40 |
| ACT-4 | 4 | 200 | 40 |
| ACT-8 | 8 | 200 | 40 |
| ACT-16 | 16 | 200 | 40 |

::: source
출처: sources/eval.csv (합성 자료)
:::

::: notes
네 조건 모두 같은 시연 200개와 같은 평가 환경을 사용했다고 가정한 합성 설정이다.
:::

## 학습 목표

### 청크 단위 L1 손실로 k개 행동을 한 번에 예측한다

$$\mathcal{L} = \frac{1}{k}\sum_{j=0}^{k-1} \left\| a_{t+j} - \hat{a}_{t+j} \right\|_1$$

$a_{t+j}$는 시연 행동, $\hat{a}_{t+j}$는 예측 행동, $k$는 청크 길이다.

- $k = 1$이면 한 단계씩 예측하는 BC와 같다

::: notes
청크로 예측하면 한 번의 추론으로 k단계 행동을 낸다. 수식은 예제용 단순화다.
:::

# 결과 | Results

## 성공률

### 합성 평가에서 k = 8의 성공률이 가장 높았다

![청크 길이별 성공률](figures/success-by-chunk.png)

::: source
출처: sources/eval.csv (합성 자료, 조건별 40회)
:::

::: notes
조건별 40회라 차이를 단정하지 않는다. ACT-8과 ACT-4의 차이는 4회다.
:::

### k = 16의 하락은 아직 원인을 확인하지 못했다

:::: columns
::: column
**관찰**

- 성공 29회(k = 8) → 24회(k = 16)
- 표본은 조건별 40회뿐이다
:::
::: column
**가설과 확인 방법**

- 긴 청크가 접촉 후 보정을 늦춘다
  - temporal ensemble 유무로 비교
:::
::::

::: notes
가설은 아직 근거가 없다. 다음 실험에서 확인한다.
:::

## 실패 분석

### k = 8의 실패 11회 중 6회가 파지 단계에서 났다

![실패 유형별 횟수](figures/failure-types.png)

![실패 장면](figures/failure-frames.png "ACT-8 실패 장면 3장(파지·정렬·놓기). 연구자가 평가 영상에서 캡처")

::: source
출처: sources/failures.csv (합성 자료)
:::

::: notes
실패 장면 사진은 연구자가 넣을 자리다. 빌드는 요청 상자로 표시한다.
:::

# 다음 계획 | Next Steps

## 다음 실험

### 파지 구간 시연을 보강해 같은 조건으로 다시 평가한다

- 파지 직전 구간 시연 50개를 추가로 수집한다
- $k = 8$에서 temporal ensemble 유무를 비교한다
- 평가 시행을 조건별 100회로 늘린다

::: notes
추가 수집량과 시행 수는 예제용 계획이다.
:::

## 논의

### 교수님께 두 가지 우선순위를 확인받고 싶다

1. 시연 보강과 평가 확대 중 무엇을 먼저 할지
2. 실제 로봇 평가로 넘어갈 성공률 기준

::: notes
랩미팅에서 결정받을 질문으로 끝낸다.
:::
