---
schema_version: 1
task_id: 261011-example-il-progress
stage: 2
status: approved
approval_hash: ee7a9647d53056f12333ff39f613756a272a073910b39d043bbc4a369b121bfa
upstream_hashes:
  sources/: 7caf77c746d8228fdc6ef56dc127342adebe114c96f7f00ba5cf4694071e938a
  plan/interview.md: 097aca58a6de81c83d5a92b1006748fbf75d208bc554d4bd0dd03229730c56d3
assumptions:
- '가상 예제: 인물·과제·수치가 모두 합성이며 실제 실험 결과가 아니다.'
- 예제 시연용으로 에이전트가 자동 승인했다. 실제 발표자의 승인이 아니다.
open_items: []
review:
  topic: 행동 청크 길이 비교 진행 보고
  selected_candidate: A
  key_message: k = 8이 가장 좋았지만 실패의 절반이 파지에서 나므로 시연 보강부터 결정받는다
  storyline:
  - 지난 피드백과 목표
  - 실험 설정
  - 성공률과 실패 분석
  - 다음 계획과 결정 요청
  candidates:
  - id: A
    message: k = 8이 가장 좋았지만 실패의 절반이 파지에서 나므로 시연 보강부터 결정받는다
    storyline:
    - 지난 피드백과 목표
    - 실험 설정
    - 성공률과 실패 분석
    - 다음 계획과 결정 요청
    evidence:
    - sources/eval.csv
    - sources/failures.csv
    tradeoff: 결정 요청이 분명하지만 방법 설명은 짧다
  - id: B
    message: 청크 길이가 성공률에 미치는 영향을 정리한다
    storyline:
    - 배경
    - 방법
    - 결과
    evidence:
    - sources/eval.csv
    tradeoff: 설명은 충실하지만 받을 결정이 드러나지 않는다
---

# 핵심 메시지 (가상 예제)

추천안 A를 선택했다. 지난 미팅의 피드백(실패 원인 우선)과 이번 발표의 목적(다음 실험 결정)에 맞는다. 유의성 주장과 실제 로봇 결과는 범위에서 뺀다.
