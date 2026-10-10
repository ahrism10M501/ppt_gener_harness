---
schema_version: 1
task_id: 261011-example-il-progress
stage: 3
status: approved
approval_hash: 8a0e669e284f3f2b8de0839aa04578678dcc7d52cd20ca381de9ec95d558827c
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
    headline: 지난 피드백에 따라 행동 청크 길이부터 비교했다
    evidence:
    - sources/eval.csv
    seconds: 60
  - id: S02
    section: 실험 설정
    topic: 과제와 데이터
    headline: 시연 200개로 학습하고 조건마다 40회 평가했다
    evidence:
    - sources/eval.csv
    seconds: 60
  - id: S03
    section: 실험 설정
    topic: 학습 목표
    headline: 청크 단위 L1 손실로 k개 행동을 한 번에 예측한다
    evidence:
    - sources/eval.csv
    seconds: 75
  - id: S04
    section: 결과
    topic: 성공률
    headline: 합성 평가에서 k = 8의 성공률이 가장 높았다
    evidence:
    - sources/eval.csv
    seconds: 90
    figure: 조건별 성공률 막대그래프, 막대 위 성공/시행 — sources/eval.csv로 작성
  - id: S05
    section: 결과
    topic: 성공률
    headline: k = 16의 하락은 아직 원인을 확인하지 못했다
    evidence:
    - sources/eval.csv
    - sources/failures.csv
    seconds: 75
  - id: S06
    section: 결과
    topic: 실패 분석
    headline: k = 8의 실패 11회 중 6회가 파지 단계에서 났다
    evidence:
    - sources/failures.csv
    seconds: 90
    figure: 실패 유형별 횟수 그래프와 연구자가 캡처한 실패 장면 프레임 3장
  - id: S07
    section: 다음 계획
    topic: 다음 실험
    headline: 파지 구간 시연을 보강해 같은 조건으로 다시 평가한다
    evidence:
    - sources/failures.csv
    seconds: 60
  - id: S08
    section: 다음 계획
    topic: 논의
    headline: 교수님께 두 가지 우선순위를 확인받고 싶다
    evidence:
    - sources/eval.csv
    seconds: 60
---

# 목차 (가상 예제)

진행 보고 뼈대(지난 피드백 → 설정 → 결과 → 다음 계획 → 결정 요청)를 따른다. k = 16 하락은 결과 섹션에서 가설로 분리하고, 마지막 장을 결정받을 질문으로 끝낸다. 실패 장면 사진은 연구자에게 요청한다(S06).
