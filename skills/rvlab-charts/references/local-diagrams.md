# 로컬 자동 도식

`beautiful-mermaid`는 그림의 배치와 렌더링을 맡는다. 내용의 해석과 구성 선택은 에이전트가 맡는다. 승인된 주장·노드·관계만 재구성하며 연구 결과나 확인되지 않은 인과를 덧붙이지 않는다. 사용자가 이미 요청한 자동 제작 범위에서는 도식별로 다시 허락받지 않는다.

## 관계에서 구성을 고른다

| 보여줄 관계 | 구성 | 출발 예시 |
| --- | --- | --- |
| 조건에 따라 달라지는 경로 | 마름모 판단 + 라벨이 있는 분기 | `examples/branch.mmd` |
| 여러 입력의 결합·모듈 소속 | 그룹 컨테이너 + 합류 | `examples/grouped.mmd` |
| 실행 결과가 다음 입력에 반영 | 주 경로 + 구분되는 되돌림 선 | `examples/feedback.mmd` |
| 주체 사이의 요청·응답 순서 | `sequenceDiagram` | `examples/sequence.mmd` |
| 상태 전이 | `stateDiagram-v2` | 상태 이름과 전이 조건을 명시 |

순서만 있으면 짧은 파이프라인을 쓴다. 구분이 핵심이면 그룹을, 시간 순서가 핵심이면 시퀀스를 고른다. 도식을 복잡하게 꾸미기 위해 분기나 반복을 만들지 않는다. 비교 카드·타임라인·매트릭스는 기존 `charts.py`가 적합하다.

## 제작

1. 노드·화살표·그룹의 의미를 자료와 대조한다. 주 경로와 핵심 처리 하나를 정한다. 가로/세로 방향은 화면 비율과 라벨 길이에 맞춰 선택한다.
2. `examples/`에서 맞는 문법을 가져와 같은 task의 `figures/이름.mmd`에 작성한다. 새 예시는 설명용 구성임을 밝힌다. 노드는 한두 줄의 짧은 이름, 화살표는 필요한 데이터·조건만 쓴다. 긴 라벨은 `<br>`로 나눌 수 있다.
3. 저장소 루트에서 실행한다.

   ```bash
   uv run python skills/rvlab-charts/diagrams.py render tasks/<task>/figures/이름.mmd tasks/<task>/figures/이름
   ```

4. 생성 PNG를 직접 열어 한글 누락·겹침·화살표 방향·강조를 확인하고 `![설명](figures/이름.png)`를 단독 문단에 넣는다. 캡션·출처는 기존 슬라이드 규칙을 따른다. 최종 슬라이드 미리보기에서 다시 확인한다.

입력에는 내용과 구조만 쓴다. 임의 `style`, `classDef`, `linkStyle`, 설정 frontmatter, 외부 링크·아이콘·HTML은 지원하지 않는다. `<br>`와 노드의 `:::focus`만 허용하며 `focus`의 모양은 렌더러가 고정 토큰으로 정한다. SVG의 외부 폰트 참조와 CSS 변수를 제거해 로컬 폰트와 PNG 변환에서 같은 색이 나오게 한다.

전체 폭 단독 그림을 기준으로 한국어 폰트와 최소 18pt를 검사한다. 본문·출처를 함께 넣거나 2단에 축소하면 이 추정치가 유효하지 않다. 오류가 나면 라벨을 줄이고 `<br>`·방향·그룹을 조정하거나 도식을 나눈다. 폰트를 임의로 줄이거나 검사를 끄지 않는다. 슬라이드 수·토픽·순서 변경은 기존 목차 승인 규칙을 따른다.

## 도구 선택 근거와 재현

- [beautiful-mermaid](https://github.com/lukilabs/beautiful-mermaid): MIT, Node.js에서 SVG를 직접 생성하고 ELK로 자동 배치한다. 기존 `@resvg/resvg-js`로 300dpi PNG를 만든다. 버전은 `package.json`, 전이 의존성과 무결성은 `package-lock.json`으로 고정한다.
- [D2](https://github.com/terrastruct/d2): 무료 로컬 CLI 대안이다. 이 프로젝트에는 이미 Node 렌더러가 있어 추가 실행 파일 없이 쓸 수 있는 위 경로를 선택했다.
- MCP 서버는 추가하지 않는다. 현재 에이전트가 로컬 CLI를 호출할 수 있어 상시 서버·포트·외부 계정이 필요하지 않다.

다른 환경에서는 `npm ci` 후 위 명령을 실행한다. 예시 전체는 `uv run python skills/rvlab-charts/diagrams.py demo .cache/diagram-demo`로 재생성한다. 기존 `slides.md`의 Mermaid 코드 블록 빌드 경로는 별개이며, 이 스킬은 PNG 삽입 경로를 사용한다.
