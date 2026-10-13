---
schema_version: 1
task_id: 261011-example-il-progress
stage: 3
status: approved
approval_hash: 482aacdbaec321d6abccd1923a8ec509f14330a8018d16aa170f4de4f0ff76f0
upstream_hashes:
  sources/: 7caf77c746d8228fdc6ef56dc127342adebe114c96f7f00ba5cf4694071e938a
  plan/interview.md: 097aca58a6de81c83d5a92b1006748fbf75d208bc554d4bd0dd03229730c56d3
  plan/brief.md: ee7a9647d53056f12333ff39f613756a272a073910b39d043bbc4a369b121bfa
assumptions:
- '가상 예제: 인물·과제·수치가 모두 합성이며 실제 실험 결과가 아니다.'
- 예제 시연용으로 에이전트가 자동 승인했다. 실제 발표자의 승인이 아니다.
open_items: []
review:
  duration_minutes: 10
  slides:
  - id: S01
    section: 지난 미팅 이후
    topic: 진행 목표
    headline: 원리와 실패 분석을 연결해 다음 실험을 정합니다
    evidence:
    - sources/eval.csv
    - figures/external/act-2023.pdf
    seconds: 30
    figure: figures/aloha-teleoperation.png — ACT Fig. 1 왼쪽 원문 사진; 외부 시연 사례
  - id: S02
    section: 실험 설정
    topic: BC 원리
    headline: BC는 시연의 관측에서 전문가 행동을 예측합니다
    evidence:
    - figures/external/dagger-2011.pdf
    seconds: 40
    figure: figures/bc-illustrated.png — 로봇·물체·전문가를 담은 AI 설명용 삽화; 실험 증거 아님
  - id: S03
    section: 실험 설정
    topic: 분포 이동
    headline: 작은 행동 오차가 시연에 없던 상태로 이어집니다
    evidence:
    - figures/external/dagger-2011.pdf
    seconds: 45
    figure: figures/distribution-shift-illustrated.png — 로봇·물체·전문가를 담은 AI 설명용 삽화;
      실험 증거 아님
  - id: S04
    section: 실험 설정
    topic: DAgger
    headline: DAgger는 정책이 방문한 상태에 전문가 행동을 붙입니다
    evidence:
    - figures/external/dagger-2011.pdf
    seconds: 40
    figure: figures/dagger-illustrated.png — 로봇·물체·전문가를 담은 AI 설명용 삽화; 실험 증거 아님
  - id: S05
    section: 실험 설정
    topic: ACT 구조
    headline: ACT는 현재 관측에서 여러 단계의 행동을 예측합니다
    evidence:
    - figures/external/act-2023.pdf
    seconds: 40
    figure: figures/act-architecture.png — 원문 기반 도식 또는 기존 합성 CSV의 재시각화
  - id: S06
    section: 실험 설정
    topic: 학습 목표
    headline: 예제의 청크 손실은 ACT의 전체 목적을 단순화했습니다
    evidence:
    - figures/external/act-2023.pdf
    seconds: 45
  - id: S07
    section: 실험 설정
    topic: 시간 앙상블
    headline: 같은 시점의 행동 예측을 모아 실행을 부드럽게 합니다
    evidence:
    - figures/external/act-2023.pdf
    seconds: 45
    figure: figures/temporal-ensemble.png — 원문 기반 도식 또는 기존 합성 CSV의 재시각화
  - id: S08
    section: 실험 설정
    topic: 과제와 데이터
    headline: 시연 200개와 조건별 40회 평가를 가정했습니다
    evidence:
    - sources/eval.csv
    seconds: 30
  - id: S09
    section: 결과
    topic: 성공률
    headline: 합성 평가에서는 k = 8의 성공 횟수가 가장 많았습니다
    evidence:
    - sources/eval.csv
    seconds: 55
    figure: figures/success-by-chunk.png — 원문 기반 도식 또는 기존 합성 CSV의 재시각화
  - id: S10
    section: 결과
    topic: 성공률
    headline: k = 16의 하락 원인은 이 집계만으로 알 수 없습니다
    evidence:
    - sources/eval.csv
    seconds: 40
  - id: S11
    section: 결과
    topic: 실패 분석
    headline: k = 8의 실패 11회 중 파지 실패가 6회였습니다
    evidence:
    - sources/failures.csv
    seconds: 45
    figure: figures/failure-types.png — 원문 기반 도식 또는 기존 합성 CSV의 재시각화
  - id: S12
    section: 다음 계획
    topic: 다음 실험
    headline: 파지 시연을 보강하고 실행 조건을 고정해 비교합니다
    evidence:
    - sources/failures.csv
    seconds: 40
    figure: figures/next-experiment.png — 원문 기반 도식 또는 기존 합성 CSV의 재시각화
  - id: S13
    section: 다음 계획
    topic: 논의
    headline: 시연 보강의 우선순위와 실제 로봇 평가 기준을 정합니다
    evidence:
    - sources/eval.csv
    seconds: 35
  - id: S14
    section: 부록
    topic: 방법 비교
    headline: 세 방법은 서로 다른 모방학습 문제를 다룹니다
    evidence:
    - figures/external/diffusion-policy-2023.pdf
    seconds: 15
  - id: S15
    section: 부록
    topic: 논문 레퍼런스
    headline: 원리 설명은 원문 논문, 결과는 합성 CSV에 근거합니다
    evidence:
    - figures/visual-sources.yaml
    seconds: 15
---

# 개선 목차 (합성 예제)

기존 진행 보고의 목적·핵심 메시지를 유지한다. 실험 설정 섹션에 BC·분포 이동·DAgger·ACT 원리를 보강했다. 본문 13장, 부록 2장이다. 본문 예상 530초, 선택 부록 30초이며 자동 슬라이드 설명 시간은 별도다. 도식은 순서·구조만 나타내며 실측 로봇 궤적이 아니다. 새로운 실험 데이터나 실제 실패 영상을 요청하지 않는다.

수치의 인과 해석을 피하고 ACT의 전체 목적과 단순화한 손실을 구분한다. 실제 실행 주기·앙상블 유무는 미확인이다. 목차와 본문은 검토 초안이며 이전 승인은 변경 내용에 적용되지 않는다.

사용자 시각 자료 개선 피드백 반영: 추상 상자 흐름도 3개를 구체적인 로봇 장면 삽화로 교체하고 S01에 ALOHA의 실제 시연 사진을 추가했다. 장수·토픽·순서·핵심 문장은 유지했다.
