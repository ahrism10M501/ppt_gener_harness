---
schema_version: 1
task_id: 2601-world-model1
stage: 2
status: approved
approval_hash: e9edf10d0649eaa2b469f4d0a6f9df32bca1de7cfb0ac675252b60dd4bc1603b
upstream_hashes:
  sources/: 754954ff41e110fde710f584bc78e0e81242d3b27f6b81a1a40f3c0fef4a12d7
  plan/interview.md: 9aee69e28085180e08689a79acbd4ce9f83834a3e6377fadcee87f93522e3038
assumptions:
- 본 발표는 30분이며 질의응답은 별도다. Stage 1에서 승인한 기획 가정이다.
- 사용자가 후보 A를 선택하고 Stage 2를 승인했다. 승인 메타데이터는 rvppt approve로 기록한다.
- 대표 연구는 메커니즘 차이를 설명하기 위해 선정하며 동일 조건의 성능 순위로 제시하지 않는다.
open_items:
- id: B01
  description: Cosmos의 버전별 구조·공개 시점과 최신 사례의 상세 실험 조건은 목차에서 근거로 사용할 주장에 맞춰 원문 검토한다.
  blocking: false
- id: B02
  description: 최신 자료 기준일은 2026-10-11이며 발표일 2026-10-12까지의 새 공개 자료는 최종 내용 검토 때 확인한다.
  blocking: false
review:
  topic: 월드 모델의 종류·메커니즘·최신 동향과 한계
  selected_candidate: A
  key_message: 월드 모델은 미래를 예측해 행동을 돕지만, 표현 방식과 제어 연결에 따라 쓸모와 한계가 달라진다.
  storyline:
  - 월드 모델의 정의와 행동 조건
  - 예측 표현과 정책 연결의 메커니즘
  - 영상·게임·로봇의 대표 모델 비교
  - Cosmos와 리뷰 이후 연구에서 보는 최신 동향
  - 물리적 신뢰성·효율·일반화·평가의 한계
  - 모델을 비교하는 질문과 결론
  candidates:
  - id: A
    message: 월드 모델은 미래를 예측해 행동을 돕지만, 표현 방식과 제어 연결에 따라 쓸모와 한계가 달라진다.
    storyline:
    - 월드 모델의 정의와 행동 조건
    - 예측 표현과 정책 연결의 메커니즘
    - 영상·게임·로봇의 대표 모델 비교
    - Cosmos와 리뷰 이후 연구에서 보는 최신 동향
    - 물리적 신뢰성·효율·일반화·평가의 한계
    - 모델을 비교하는 질문과 결론
    evidence:
    - 'sources/World Model for Robot Learning: A Comprehensive.pdf — §2–5, §7–8'
    - https://danijar.com/dreamerv3/
    - https://ai.meta.com/research/publications/v-jepa-2-self-supervised-video-models-enable-understanding-prediction-and-planning/
    - https://deepmind.google/blog/genie-3-a-new-frontier-for-world-models/
    - https://research.nvidia.com/labs/cosmos-lab/cosmos3/
    - https://arxiv.org/abs/2610.08780
    tradeoff: 처음 접하는 청중에게 원리와 비교 기준을 먼저 제공한다. 개별 모델의 구조·학습 손실 전체를 상세히 다루기는 어렵다.
  - id: B
    message: 영상·게임·로봇은 미래 예측을 공유하지만, 행동의 의미와 검증 기준이 달라 같은 성능 척도로 비교할 수 없다.
    storyline:
    - 영상 생성·게임 환경·로봇 제어의 목표 차이
    - 각 영역의 대표 모델과 작동 과정
    - 공통 예측 구조와 서로 다른 행동 조건
    - Cosmos의 생성·추론·행동 연결과 최신 동향
    - 영역별 평가·일반화·물리적 신뢰성의 한계
    evidence:
    - 'sources/World Model for Robot Learning: A Comprehensive.pdf — §2, §4–8'
    - https://deepmind.google/blog/genie-3-a-new-frontier-for-world-models/
    - https://www.nvidia.com/en-us/ai/cosmos/llm-info/
    - https://research.nvidia.com/labs/cosmos-lab/cosmos3/
    tradeoff: 사례 중심으로 흥미를 끌고 응용 범위가 잘 드러난다. 영역별 설명에서 메커니즘이 반복되거나 로봇 중심 리뷰와의 연결이 약해질
      수 있다.
  - id: C
    message: 제어에 유용한 월드 모델을 만들려면 행동 조건·물리 구조·계산 효율·평가 신뢰성의 간극을 줄여야 한다.
    storyline:
    - 그럴듯한 미래 예측이 제어 성공을 보장하지 않는 이유
    - 실패 원인으로 정리하는 모델 종류와 메커니즘
    - Cosmos·잠재 예측·3D 구조화 연구의 대응 방식
    - 최신 연구가 해결한 부분과 남긴 문제
    - 연구실에서 검증할 비교 질문
    evidence:
    - 'sources/World Model for Robot Learning: A Comprehensive.pdf — §2, §7–8'
    - https://arxiv.org/abs/2607.22535
    - https://arxiv.org/abs/2610.08780
    - https://research.nvidia.com/labs/cosmos-lab/cosmos3/
    tradeoff: 한계와 연구 방향이 선명하다. 처음 접하는 청중에게 문제를 이해시키기 위한 배경 설명이 많아져 모델 종류의 전체 지도가 약해질
      수 있다.
---

# 발표 핵심 메시지와 스토리라인 후보

## 승인된 발표 조건

월드 모델을 처음 접하는 로보틱스 연구실 청중을 대상으로 30분 동안 종류·메커니즘·최신 연구·한계를 설명한다. 영상·게임·로봇을 폭넓게 비교하며, 사용자 요청에 따라 **NVIDIA Cosmos를 후보군에 포함**한다. 기준 자료는 Hou et al.의 2026-04-30 리뷰 v1이고, 리뷰 이후 연구는 별도로 표시한다.

## 추천: A — 원리를 이해한 뒤 최신 모델을 비교한다

**핵심 메시지:** 월드 모델은 미래를 예측해 행동을 돕지만, 표현 방식과 제어 연결에 따라 쓸모와 한계가 달라진다.

처음 접하는 청중에게 모델 이름보다 공통 구조를 먼저 제공한다. 각 사례를 **입력 조건 → 예측 표현 → 행동 선택/학습 연결 → 평가**의 같은 순서로 설명하면 모델 간 차이와 최신 동향을 비교하기 쉽다. 사용자의 필수 내용 네 가지를 모두 다루면서 30분 안에서 설명 깊이를 조절할 수 있어 A를 추천한다.

| 흐름 | 설명할 내용 | 제안 시간 |
| --- | --- | --- |
| 정의와 행동 조건 | 현재 관측과 행동에서 미래를 예측하는 문제, 일반 영상 생성과 제어 목적의 차이 | 4분 |
| 메커니즘 | 잠재 동역학·잠재 표현 예측·생성형 영상 예측, 예측에서 행동으로 이어지는 경로 | 7분 |
| 대표 모델 비교 | DreamerV3, V-JEPA 2/2-AC, Genie 3, Cosmos 계열을 공통 질문으로 비교 | 7분 |
| 최신 동향 | Cosmos 3의 통합 방향과 리뷰 이후 3D·로봇 구조 분리 연구 | 6분 |
| 한계와 평가 | 행동 인과성, 오차 누적, 접촉/물성, 일반화, 지연, 영상 품질과 제어 효용의 차이 | 4분 |
| 결론 | 새로운 모델을 읽을 때 던질 비교 질문 | 2분 |

합계 30분. 이는 구간별 기획안이며 슬라이드 ID·핵심 문장·개별 시간은 Stage 3에서 정한다. 대표 사례 구간은 앞에서 설명한 메커니즘을 다시 길게 반복하지 않는다.

## 후보 B — 영상·게임·로봇의 목적 차이로 시작한다

**핵심 메시지:** 영상·게임·로봇은 미래 예측을 공유하지만, 행동의 의미와 검증 기준이 달라 같은 성능 척도로 비교할 수 없다.

영역별 예시에서 시작해 각 모델이 해결하려는 문제를 비교한다. 영상 생성은 미래 장면 생성, 게임형 환경은 반복적인 상호작용, 로봇은 행동 결과와 실제 실행을 중심으로 설명한다. 이 구분은 설명 관점이며 각 모델의 모든 기능을 배타적으로 분류하지 않는다.

응용 분야가 가장 중요하면 B가 적합하다. 다만 공통 메커니즘을 영역마다 반복할 수 있어, 마지막 비교표로 구조를 다시 묶어야 한다. 필요한 추가 자료는 영역별 대표 입출력 예시와 상호작용 조건이며 그림 제작은 연구자에게 제안한다.

## 후보 C — 실패와 한계에서 최신 연구 방향을 끌어낸다

**핵심 메시지:** 제어에 유용한 월드 모델을 만들려면 행동 조건·물리 구조·계산 효율·평가 신뢰성의 간극을 줄여야 한다.

시각적으로 그럴듯한 미래가 실제 행동 결과와 어긋날 수 있다는 문제에서 시작한다. 각 간극에 대응하는 표현과 구조를 설명하고, 최신 연구가 어디까지 해결했는지 검토한다. 실패 사례는 출처가 있는 관찰만 사용하고 설명용 가정은 가정임을 표시한다.

연구 방향 토론을 가장 중요하게 보면 C가 적합하다. 그러나 현재 청중은 월드 모델에 대한 배경이 없으므로 A보다 도입 설명이 길어질 수 있다. 추가로 필요한 자료는 원문에 보고된 실패·제약·평가 조건이다.

## 대표 모델 후보와 확인 수준

아래는 설명 역할에 따른 후보다. 최종 포함 여부와 버전은 목차에서 정하고, 모델별 수치·세부 구조는 해당 원문을 확인한 뒤 본문에 넣는다.

| 후보 | 발표에서 맡을 역할 | 현재 확인한 근거 |
| --- | --- | --- |
| DreamerV3 | 잠재 동역학과 상상한 궤적에서 정책을 학습하는 방식 | 저자 공식 프로젝트·저장소 소개 확인 |
| V-JEPA 2 / 2-AC | 표현 공간의 예측과 행동 조건을 추가한 계획 연결 | Meta 공식 연구 소개, 리뷰 §3.6·§4.2 |
| Genie 3 | 상호작용 가능한 생성 환경과 로봇 제어의 조건 차이 | Google DeepMind 공식 소개 |
| Cosmos 제품군·Cosmos Policy | 생성·변환·추론의 역할 구분, 영상 모델의 로봇 제어 연결 | NVIDIA 공식 모델군 안내, 공식 Policy 소개, 리뷰 §3.3 |
| Cosmos 3 | 여러 모달리티와 생성·예측·행동을 연결하는 통합 방향 | NVIDIA 공식 연구 페이지; 기술 보고서의 상세 검토 전 |
| Robot-Factored World Models | 로봇별 행동 실현과 렌더링을 분리하는 방향 | 2026-07-24 arXiv 초록 |
| DepthWorld | RGB 영상 예측을 3D 기하와 연결하는 방향 | 2026-10-06 arXiv 초록 |

### Cosmos를 설명할 때의 범위

Cosmos는 하나의 모델 이름으로 통칭하지 않고 **제품군의 기능**, **정책으로의 연결**, **최신 통합 모델**로 나누어 설명한다. Predict·Transfer·Reason을 모두 같은 행동 조건 동역학 모델로 묶지 않는다. 리뷰에 등장하는 Cosmos Policy와 리뷰 이후 보완 후보인 Cosmos 3도 구분한다.

Cosmos 3 공식 페이지는 텍스트·이미지·영상·오디오·행동을 연결하고 전방/역동역학과 로봇 정책 활용을 소개한다. 이는 통합 방향을 설명할 근거이며, 모든 환경에서 물리적으로 정확하다는 결론은 아니다. 최종 본문에서는 버전·학습 조건·추론 경로를 기술 보고서로 확인한다.

## 자료와 판단의 구분

- **확인한 사실:** 기준 리뷰의 범위와 분류 축, 사용자 요구, 각 후보의 공식 소개와 원문 초록.
- **기획 판단:** A의 추천, 사례의 설명 역할, 시간 배분, 최신 동향을 통합·구조화·제어 연결로 묶는 방식.
- **추가 확인:** 최신 버전의 공개 시점, 상세 구조와 학습 과정, 폐루프 실험·일반화·계산 비용의 조건.
- **주장 범위:** 대표 연구를 비교하는 발표다. 전수 조사나 서로 다른 벤치마크를 섞은 성능 순위를 제시하지 않는다.

## 주요 출처

- 제공 리뷰: `sources/World Model for Robot Learning: A Comprehensive.pdf`.
- DreamerV3: https://danijar.com/dreamerv3/ , https://github.com/danijar/dreamerv3 .
- V-JEPA 2: https://ai.meta.com/research/publications/v-jepa-2-self-supervised-video-models-enable-understanding-prediction-and-planning/ .
- Genie 3: https://deepmind.google/blog/genie-3-a-new-frontier-for-world-models/ .
- Cosmos 모델군: https://www.nvidia.com/en-us/ai/cosmos/llm-info/ .
- Cosmos Policy: https://research.nvidia.com/labs/dir/cosmos-policy/ , https://github.com/NVlabs/cosmos-policy .
- Cosmos 3: https://research.nvidia.com/labs/cosmos-lab/cosmos3/ .
- 리뷰 이후 연구: https://arxiv.org/abs/2607.22535 , https://arxiv.org/abs/2610.08780 .

공식 자료 확인일은 2026-10-11이다. 실험 성능 수치는 아직 채택하지 않았다.

## 사용자 선택과 승인

사용자가 **“A안으로 승인”**이라고 명시했다. 후보 A의 메시지와 스토리라인을 선택한 것으로 기록하며, `rvppt approve`로 Stage 2 승인을 기록한 뒤 해당 흐름으로 Stage 3의 슬라이드별 목차를 작성한다.
