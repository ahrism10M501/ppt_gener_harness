# 로컬 자동 도식

`beautiful-mermaid`는 배치와 렌더링을 맡고, 내용 해석과 구성 선택은 에이전트가 맡는다. 승인된 주장·노드·관계만 재구성하며 연구 결과나 확인되지 않은 인과를 덧붙이지 않는다.

## 관계에서 구성을 고른다

| 보여줄 관계 | 구성 | 출발 예시 |
| --- | --- | --- |
| 조건에 따라 달라지는 경로 | 마름모 판단 + 라벨이 있는 분기 | `examples/branch.mmd` |
| 여러 입력의 결합·모듈 소속 | 그룹 컨테이너 + 합류 | `examples/grouped.mmd` |
| 실행 결과가 다음 입력에 반영 | 주 경로 + 구분되는 되돌림 선 | `examples/feedback.mmd` |
| 주체 사이의 요청·응답 순서 | `sequenceDiagram` | `examples/sequence.mmd` |
| 상태 전이 | `stateDiagram-v2` | 상태 이름과 전이 조건을 명시 |

순서만 있으면 짧은 파이프라인, 구분이 핵심이면 그룹, 시간 순서가 핵심이면 시퀀스를 고른다. 꾸미기 위해 분기나 반복을 만들지 않는다. 비교 카드·타임라인·매트릭스는 `charts.py`가 적합하다.

## 제작

1. 노드·화살표·그룹의 의미를 자료와 대조하고 주 경로와 핵심 처리 하나를 정한다. 방향은 화면 비율과 라벨 길이에 맞춘다(16:9는 가로, 4:3은 세로도 검토).
2. `examples/`에서 맞는 문법을 가져와 task의 `figures/이름.mmd`에 쓴다. 노드는 한두 줄의 짧은 이름, 화살표는 필요한 데이터·조건만 쓴다. 긴 라벨은 `<br>`로 나눈다.
3. 저장소 루트에서 실행한다.

   ```bash
   uv run python skills/ppt-charts/diagrams.py render tasks/<task>/figures/이름.mmd tasks/<task>/figures/이름
   ```

4. 생성 PNG를 직접 열어 한글 누락·겹침·화살표 방향·강조를 확인하고 `![설명](figures/이름.png)`를 단독 문단으로 넣는다. 최종 슬라이드 미리보기에서 다시 확인한다.

이 렌더러는 내용과 구조만 받는다. 색과 모양은 프리셋 팔레트에서 오며 `style`·`classDef`·`linkStyle`·설정 frontmatter·외부 링크·아이콘·HTML은 지원하지 않는다. 강조는 `:::focus` 하나로 한다. 렌더러는 단독 전체 폭 배치를 가정하고 프리셋의 최소 글자 크기를 검사한다. 오류가 나면 라벨을 줄이거나 `<br>`·방향·그룹을 조정하거나 도식을 나눈다.

예시 전체는 `uv run python skills/ppt-charts/diagrams.py demo .cache/diagram-demo --preset <id>`로 다시 만들 수 있다. `slides.md` 안의 `mermaid` 코드 블록은 빌드가 따로 렌더하는 별개 경로다.
