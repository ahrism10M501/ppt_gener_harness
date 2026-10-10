---
schema_version: 1
task_id: 2601-world-model1
stage: 3
status: approved
approval_hash: 7211cf83bd8cfe671dff8c04ef974f804d8d34148bddeaf693964eb2e2bc9279
upstream_hashes:
  sources/: 754954ff41e110fde710f584bc78e0e81242d3b27f6b81a1a40f3c0fef4a12d7
  plan/interview.md: 9aee69e28085180e08689a79acbd4ce9f83834a3e6377fadcee87f93522e3038
  plan/brief.md: e9edf10d0649eaa2b469f4d0a6f9df32bca1de7cfb0ac675252b60dd4bc1603b
assumptions:
- 승인된 후보 A의 순서에 따라 본문 슬라이드 20장을 제안한다.
- 본문 설명 27분과 표지·목차·섹션 전환·마무리 3분을 확보하며 질의응답은 별도다.
open_items:
- id: O01
  description: 그림은 제안만 했으며 아직 제작하지 않았다. 연구자가 준비할 figures/ 후보 경로를 기록한다.
  blocking: false
- id: O02
  description: Cosmos 3 기술 보고서 PDF를 확보하지 못했으므로 공식 페이지에서 확인한 통합 개요로 주장 범위를 제한한다. 세부
    구조나 성능 수치를 채택하려면 원문 확인이 필요하다.
  blocking: false
- id: O03
  description: 최신 정보 확인일은 2026-10-11이다. 발표일 2026-10-12까지의 추가 공개는 최종 본문 검토 시 확인한다.
  blocking: false
review:
  duration_minutes: 30
  slides:
  - id: S01
    section: 기본 개념
    topic: 월드 모델
    headline: 월드 모델은 현재 관측과 행동에서 미래를 예측한다
    evidence:
    - 'sources/World Model for Robot Learning: A Comprehensive.pdf — §2.1, 식 (1),
      Figure 1'
    seconds: 100
    figure: figures/world-model-loop.png — 관측·행동 → 미래 예측 → 의사결정의 순환도; 리뷰 식 (1)을 바탕으로
      연구자가 제작
  - id: S02
    section: 기본 개념
    topic: 월드 모델
    headline: 그럴듯한 미래 영상만으로 제어에 유용함을 입증할 수 없다
    evidence:
    - 'sources/World Model for Robot Learning: A Comprehensive.pdf — §2.1.1–2.1.2,
      §7.1'
    seconds: 80
  - id: S03
    section: 작동 메커니즘
    topic: 분류 기준
    headline: 예측 표현과 활용 목적은 서로 다른 분류 축이다
    evidence:
    - 'sources/World Model for Robot Learning: A Comprehensive.pdf — Figure 1, §2.1,
      §3–5'
    seconds: 75
    figure: figures/classification-axes.png — 예측 표현·행동 조건·활용 목적의 별도 축; 리뷰의 분류를 배타적
      종류로 바꾸지 않도록 연구자가 제작
  - id: S04
    section: 작동 메커니즘
    topic: 예측 표현
    headline: 잠재 공간 모델은 관측을 압축한 표현에서 미래를 예측한다
    evidence:
    - 'sources/World Model for Robot Learning: A Comprehensive.pdf — §2.1.1, §3.6'
    - https://github.com/danijar/dreamerv3 — 공식 README의 상상 궤적과 정책 학습 설명
    - https://github.com/facebookresearch/vjepa2 — V-JEPA 2와 2-AC 설명
    seconds: 90
    figure: figures/latent-prediction.png — 관측 인코딩 → 잠재 예측 → 학습·계획; Dreamer와 JEPA의
      학습 목표 차이는 별도 주석으로 구분해 연구자가 제작
  - id: S05
    section: 작동 메커니즘
    topic: 예측 표현
    headline: 영상 생성형 모델은 미래를 영상으로 표현한다
    evidence:
    - 'sources/World Model for Robot Learning: A Comprehensive.pdf — §2.1.2, §5.2–5.5'
    seconds: 90
    figure: figures/video-prediction.png — 관측·언어·행동 조건과 미래 영상의 관계; 조건 종류가 모델마다 다름을
      표시해 연구자가 제작
  - id: S06
    section: 작동 메커니즘
    topic: 제어 연결
    headline: 미래 예측은 역동역학·공동 예측·잠재 학습으로 정책에 연결된다
    evidence:
    - 'sources/World Model for Robot Learning: A Comprehensive.pdf — §3.2–3.6, Table
      1'
    seconds: 75
    figure: figures/policy-coupling.png — 미래 → 행동 추론 / 미래·행동 공동 예측 / 예측 표현으로 정책 학습의
      세 경로; 리뷰를 근거로 연구자가 제작
  - id: S07
    section: 작동 메커니즘
    topic: 제어 연결
    headline: 학습된 시뮬레이터는 정책 학습·계획·평가에 쓰인다
    evidence:
    - 'sources/World Model for Robot Learning: A Comprehensive.pdf — §4.1–4.2, Figure
      1'
    seconds: 60
  - id: S08
    section: 대표 모델 비교
    topic: DreamerV3
    headline: DreamerV3는 상상한 궤적으로 행동 정책을 학습한다
    evidence:
    - https://github.com/danijar/dreamerv3 — 공식 README
    - https://danijar.com/dreamerv3/ — 저자 프로젝트
    seconds: 90
    figure: figures/dreamer-loop.png — 실제 경험 → 월드 모델 학습 → 상상 궤적 → actor-critic 학습;
      공식 자료를 근거로 연구자가 제작
  - id: S09
    section: 대표 모델 비교
    topic: V-JEPA 2
    headline: V-JEPA 2-AC는 행동 조건을 더한 잠재 예측을 계획에 활용한다
    evidence:
    - https://github.com/facebookresearch/vjepa2 — 공식 README의 V-JEPA 2-AC와 energy
      landscape 예제
    - 'sources/World Model for Robot Learning: A Comprehensive.pdf — §4.2'
    seconds: 90
    figure: figures/vjepa-planning.png — 영상 기반 표현 학습과 로봇 데이터로 행동 조건을 추가하는 과정을 구분;
      공식 자료를 바탕으로 연구자가 제작
  - id: S10
    section: 대표 모델 비교
    topic: Genie 3
    headline: Genie 3는 상호작용 가능한 영상 환경을 생성한다
    evidence:
    - https://deepmind.google/blog/genie-3-a-new-frontier-for-world-models/ — 공식 기능
      소개와 Limitations
    seconds: 90
    figure: figures/genie-interaction.png — 시작 장면 → 사용자 입력 → 갱신된 환경의 흐름; 저수준 로봇 행동과
      다른 입력 조건을 명시해 연구자가 제작
  - id: S11
    section: 대표 모델 비교
    topic: NVIDIA Cosmos
    headline: Cosmos의 예측·변환·추론 모델은 서로 다른 역할을 맡는다
    evidence:
    - https://www.nvidia.com/en-us/ai/cosmos/llm-info/ — Predict·Transfer·Reason 공식
      역할 안내
    seconds: 110
  - id: S12
    section: 대표 모델 비교
    topic: NVIDIA Cosmos
    headline: Cosmos Policy는 행동·미래 상태·가치를 함께 예측한다
    evidence:
    - 'sources/World Model for Robot Learning: A Comprehensive.pdf — §3.3'
    - https://arxiv.org/abs/2601.16163 — Cosmos Policy 원문 초록
    - https://github.com/NVlabs/cosmos-policy — 공식 README의 세 출력과 직접 정책·계획 사용 방식
    seconds: 100
    figure: figures/cosmos-policy.png — 관측 → 행동·미래 상태·가치, 직접 실행과 후보 평가의 분기; 리뷰와 공식
      자료를 근거로 연구자가 제작
  - id: S13
    section: 최신 동향
    topic: NVIDIA Cosmos
    headline: Cosmos 3는 여러 모달리티의 이해·생성·행동을 연결한다
    evidence:
    - https://research.nvidia.com/labs/cosmos-lab/cosmos3/ — 공식 페이지의 통합 설명과 전방·역동역학
      기능
    seconds: 110
    figure: figures/cosmos3-modalities.png — 텍스트·이미지·영상·오디오·행동의 연결도; 공식 페이지의 확인 범위에서
      연구자가 제작
  - id: S14
    section: 최신 동향
    topic: 구조화
    headline: DepthWorld는 미래 RGB와 깊이를 함께 예측한다
    evidence:
    - https://arxiv.org/abs/2610.08780 — 2026-10-06 제출, 초록의 다중 시점 RGB·깊이 공동 예측
    seconds: 90
    figure: figures/depthworld-geometry.png — RGB 미래 예측과 RGB·깊이 공동 예측의 차이; 성능 수치 없이
      원문을 근거로 연구자가 제작
  - id: S15
    section: 최신 동향
    topic: 구조화
    headline: 로봇의 행동 실현과 렌더링을 동역학 예측에서 분리할 수 있다
    evidence:
    - https://arxiv.org/abs/2607.22535 — 2026-07-24 제출, 초록의 controller·kinematics와
      robot rendering 분리
    seconds: 60
    figure: figures/robot-factored.png — 행동 명령 → 제어기·기구학의 명목 궤적 → 로봇 렌더링 → 환경 예측;
      실제 미래 상태를 입력하는 누설과 구분해 연구자가 제작
  - id: S16
    section: 한계와 평가
    topic: 배포 한계
    headline: 행동 조건이 약하면 그럴듯한 예측도 제어에서 어긋날 수 있다
    evidence:
    - 'sources/World Model for Robot Learning: A Comprehensive.pdf — §8.1'
    - https://arxiv.org/abs/2607.22535 — 초록의 미래 상태 조건화와 누설 문제
    seconds: 65
  - id: S17
    section: 한계와 평가
    topic: 배포 한계
    headline: 오차 누적·물성 관측·계산 지연은 실제 배포를 제한한다
    evidence:
    - 'sources/World Model for Robot Learning: A Comprehensive.pdf — §7.2, §8.2–8.5'
    seconds: 65
  - id: S18
    section: 한계와 평가
    topic: 평가
    headline: 영상 품질과 폐루프 제어 성능은 따로 검증해야 한다
    evidence:
    - 'sources/World Model for Robot Learning: A Comprehensive.pdf — §7.1, §7.3, §8.6'
    seconds: 80
  - id: S19
    section: 정리
    topic: 정리
    headline: 입력 조건·예측 표현·제어 연결·평가로 모델을 비교한다
    evidence:
    - plan/brief.md — 승인된 A안의 공통 비교 기준
    - 'sources/World Model for Robot Learning: A Comprehensive.pdf — §2–5, §7–8'
    - https://github.com/danijar/dreamerv3
    - https://github.com/facebookresearch/vjepa2
    - https://deepmind.google/blog/genie-3-a-new-frontier-for-world-models/
    - https://github.com/NVlabs/cosmos-policy
    seconds: 70
  - id: S20
    section: 정리
    topic: 정리
    headline: 표현 방식과 제어 연결에 따라 월드 모델의 쓸모와 한계가 달라진다
    evidence:
    - plan/brief.md — 승인된 A안 핵심 메시지
    - 'sources/World Model for Robot Learning: A Comprehensive.pdf — §2.1, §8'
    seconds: 30
---

# 슬라이드별 목차 — A안

## 발표 흐름과 시간

승인된 A안의 순서대로 **기본 개념 → 작동 메커니즘 → 대표 모델 비교 → 최신 동향 → 한계와 평가 → 정리**를 구성한다. 본문은 20장, 설명 시간은 1,620초(27분)다. 자동 생성되는 표지·목차·섹션 전환·마무리에 180초를 배분해 전체 30분을 맞춘다. 질의응답은 별도다. 자동 생성 슬라이드는 본문 ID에 넣지 않는다.

| 구간 | 본문 ID | 설명 시간 | 내용 |
| --- | --- | --- | --- |
| 기본 개념 | S01–S02 | 3분 | 정의, 행동 조건, 시각적 품질과 제어 효용 |
| 작동 메커니즘 | S03–S07 | 6분 30초 | 분류 축, 잠재·영상 예측, 정책·시뮬레이터 연결 |
| 대표 모델 비교 | S08–S12 | 8분 | DreamerV3, V-JEPA 2-AC, Genie 3, Cosmos 제품군·Policy |
| 최신 동향 | S13–S15 | 4분 20초 | Cosmos 3의 통합, 3D 기하, 로봇 구조 분리 |
| 한계와 평가 | S16–S18 | 3분 30초 | 행동 인과성, 배포 한계, 기능별 평가 |
| 정리 | S19–S20 | 1분 40초 | 비교표와 핵심 메시지 |

Stage 2의 구간별 시간은 제안값이었다. 이 목차에서는 Cosmos의 제품군·Policy·Cosmos 3를 구분해 설명하는 시간을 늘리고, 전환 시간을 별도로 확보했다. 모델마다 입력·예측·제어·평가를 같은 순서로 짧게 설명해 반복을 줄인다.

## 슬라이드별 내용 범위

- **S01–S02:** 리뷰의 정의와 식 (1)을 사용한다. 관측·언어 지시·저수준 행동의 차이를 먼저 설명한다. 설명용 상황은 가정으로 표시하고 실험 결과처럼 제시하지 않는다.
- **S03:** 표현 방식과 활용 목적이 서로 다른 축임을 보인다. 잠재·영상·3D/객체/기호 표현과 정책·계획·시뮬레이션·평가를 대응시키되 배타적 분류로 만들지 않는다.
- **S04–S05:** 잠재 동역학과 JEPA식 표현 예측의 학습 목표가 같다고 설명하지 않는다. 영상 모델도 압축 잠재 공간에서 계산할 수 있으므로 분류 기준은 내부 연산 위치보다 최종 예측 대상과 활용에 둔다.
- **S06–S07:** 역동역학에서 미래를 행동으로 바꾸는 경로, 미래와 행동을 함께 예측하는 경로, 예측 표현으로 정책을 학습하는 경로를 비교한다. 정책 학습·계획·평가는 별도 기능이다.
- **S08:** DreamerV3의 실제 경험과 상상한 궤적을 구분하고 actor-critic 정책 학습 연결을 설명한다. 상상에 기반한 정책 학습을 매 시점 온라인 탐색과 동일시하지 않는다.
- **S09:** V-JEPA 2의 영상 기반 표현 학습과 2-AC의 행동 조건 후학습을 구분한다. 해당 모델 전체를 최신 JEPA 연구의 전수 조사로 소개하지 않는다.
- **S10:** Genie 3의 상호작용 환경을 설명하고 공식 소개의 제한된 행동 공간·상호작용 조건을 함께 짚는다. 키 입력이나 환경 이벤트를 로봇 관절 명령과 같은 조건으로 해석하지 않는다.
- **S11:** Predict·Transfer·Reason의 역할을 최대 4행·4열 표로 비교한다. Cosmos 플랫폼 전체에 하나의 학습 목표나 동역학 구조를 부여하지 않는다.
- **S12:** 리뷰 §3.3과 Cosmos Policy 공식 자료를 연결한다. 직접 정책 사용과 미래 상태·가치로 후보를 평가하는 계획 사용을 구분한다. 리뷰 이전 사례이며 ‘리뷰 이후 신규 연구’로 표시하지 않는다.
- **S13:** Cosmos 3 공식 페이지가 소개하는 다중 모달 연결과 이해·생성·전방/역동역학·정책 활용을 설명한다. 기술 보고서의 세부 구조·정확한 발표일·성능 수치는 검증 전 채택하지 않는다.
- **S14:** 2026-10-06 공개 사례로 DepthWorld의 다중 시점 RGB·깊이 공동 예측과 3D 감독 방향을 소개한다. 3D 일관성 확보가 모든 접촉 동역학 문제를 해결한다고 주장하지 않는다.
- **S15:** 2026-07-24 공개 사례로 로봇별 제어기·기구학과 렌더링을 분리하는 아이디어를 소개한다. 실행 전에 계산할 수 있는 명목 궤적과 실행 후에 얻는 실제 미래 상태를 구분한다.
- **S16:** 행동을 바꾸었을 때 미래가 적절히 달라지는지를 묻는다. 상관관계 기반의 그럴듯한 예측과 행동 개입의 결과 예측을 구분한다.
- **S17:** 오차 누적, 미관측 물성/접촉, 분포 밖 조건, 추론 지연을 제한 요인으로 정리한다. 효과가 확인되지 않은 해결책을 성공한 방법으로 제시하지 않는다.
- **S18:** 개방 루프 영상·행동 일관성 평가와 폐루프 과제 성공·정책 순위 신뢰성 평가를 구분한다. 수치 비교가 필요하면 데이터·환경·행동 공간·평가 프로토콜을 함께 명시한다.
- **S19:** 모델별 공통 비교표를 최대 6행·5열로 만든다. 행은 DreamerV3, V-JEPA 2-AC, Genie 3, Cosmos Policy, Cosmos 3와 헤더다. 성능 순위 대신 각 모델의 입력·예측·제어 연결·평가 확인 항목을 기록한다.
- **S20:** 승인된 핵심 메시지로 끝내고, 연구실에서 검토할 질문으로 ‘어떤 행동 조건과 실패 상황을 실제 폐루프에서 검증할 것인가’를 제시한다. 이미 정해진 연구 과제로 표현하지 않는다.

## 그림과 근거의 준비

frontmatter의 `figure`는 연구자에게 요청할 자산과 후보 경로다. 실제 그림을 생성하거나 원논문의 그림을 자동 추출하지 않았다. 본문 작성 시 의미가 같은 도식을 재사용해 그림 수를 줄일 수 있으며, 캡션과 출처는 각각 기록한다.

공식 문서·저장소·원문 초록의 확인일은 2026-10-11이다. 리뷰의 개념·분류·한계는 해당 절에 근거한다. Cosmos Policy는 리뷰 설명과 공식 저장소의 출력 정의를 확인했다. Cosmos 3는 공식 페이지에서 확인한 기능 범위만 사용한다. 최신 두 구조화 사례는 현재 원문 초록에 근거하며 성능 수치를 포함하지 않는다.

## 검토 대상

20개 본문 슬라이드의 순서·토픽·핵심 문장·근거 범위·시간 배분을 검토한다. 그림 미준비와 최신 모델의 상세 실험 미검토는 기록한 주장 범위를 지키는 한 목차 승인을 막지 않는다. 승인 후 Stage 4에서 이 토픽·핵심 문장 순서를 그대로 사용해 `slides.md`를 작성한다. 본문이나 주장 범위가 달라지면 목차도 갱신해 재검토한다.
