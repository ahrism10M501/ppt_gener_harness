---
name: ppt-animation
description: 이 저장소(tasks/) 발표에서 최적화·상태 변화·기하 변환처럼 움직임이 이해에 필요한 개념을 GIF와 대표 정적 그림(PNG)으로 만든다. 실제 계산에서 궤적을 만들고 storyboard·프리셋 팔레트·정적 대안을 검수한다. Manim 구현은 manimce-best-practices를 함께 읽는다.
---

# 교육 애니메이션 (`ppt-animation`)

[시각 설계](../ppt-maker/references/visual-planning.md)에서 정한 주장·근거·배치를 받아 움직임을 설계한다. GIF는 사용자가 요청했을 때 만든다. 요청받은 범위에서는 다시 묻지 않고, 정적 그림이 더 나은 부분은 결과 보고에서 한 줄로 제안한다.

## 판단

**먼저 읽기:** task `slides.md`의 `deck.preset`(없으면 `rvlab`)에 해당하는 `templates/<deck.preset>/DESIGN.md`를 읽어 컨텍스트에 올린다. 그 템플릿의 색 사용·도식 모양·그래프 스타일·빌드 후 점검은 이 문서가 정하며, 이 스킬에는 템플릿에 따라 달라지는 규약을 두지 않는다.

- **움직임이 필요한가:** 변화의 방향·순서·속도·동시성 중 정적 그림에서 사라지는 정보를 한 문장으로 쓴다. 발표자가 단계마다 멈춰 설명해야 하는 과정이라면 여러 정적 상태가 나을 수 있다.
- **사실:** 움직임과 숫자는 `plan/PROGRESS.md`의 Truth Model과 실제 계산에서 온다. 보기 좋게 꾸민 궤적으로 수렴·성공을 주장하지 않는다. GIF 요청은 자료를 새로 만들어도 된다는 뜻이 아니다. 교육용 합성 예제는 캡션과 노트에 합성이라고 밝힌다.
- **인상:** 색은 `rvppt.template.semantic_palette(<preset>)`(키는 [ppt-charts](../ppt-charts/SKILL.md) 참고)에서 가져오고, 모서리·장식·밀도와 그래프 스타일은 그 DESIGN.md의 그림 인상을 따른다. 색의 의미를 장면 중간에 바꾸지 않고, 색 외에 선 모양·마커·직접 라벨로도 구분한다. 정의와 수식은 가능하면 슬라이드의 편집 가능한 본문에 남긴다.

장면이 여러 개이거나 계산이 복잡하면 [storyboard](references/storyboard.md)를 `plan/animation.md`에 적고 시작한다. 별도 승인 단계는 없다.

## 도구

기구·장비가 움직이는 장면은 `uv run pptgen anatomy --script`의 프레임 모드(`frame-*.svg` → GIF·대표 PNG, [anatomy](../anatomy/SKILL.md))로 만든다. 간단한 2D 그래프는 Matplotlib·Pillow, 좌표 변환이나 수식과 도형의 연속 관계는 Manim CE([manimce-best-practices](../manimce-best-practices/SKILL.md), ManimGL 문법과 섞지 않음), 정량 그래프의 축·불확실성은 [scientific-visualization](../scientific-visualization/SKILL.md)을 쓴다. 도구가 없으면 자동 설치하지 않고 가능한 작업을 진행하며, 시스템 설치가 필요하면 명령과 이유를 보여 주고 확인받는다.

## 파일 계약

- `figures/foo.gif`와 같은 픽셀 크기의 대표 상태 `figures/foo.png`를 함께 만든다. 대표 PNG는 고른 상태이며 임의의 첫 프레임이 아니다. PNG만 보아도 핵심 설명과 최종 상태를 이해할 수 있게 하고, 필요하면 이전 상태의 흔적·이동 방향·반복 번호를 남긴다.
- 계산·렌더 스크립트와 파라미터·데이터 출처·난수 시드를 `figures/`에 보존한다. 임시 렌더는 `.build/animation/`에 둔다.
- `slides.md`에는 `![짧은 설명](figures/foo.gif)`로 넣는다. PPTX에는 GIF가, PDF·미리보기에는 PNG가 들어간다([rendering](../../docs/rendering.md)).

## 검수와 전달

1. 계산식·갱신값·표시 숫자를 대조한다.
2. 처음·중간·마지막·대표 프레임과 재생을 직접 보고 겹침·잘림·읽을 시간·재시작 오해를 고친다.
3. `uv run pptgen build tasks/<task>`와 `uv run pptgen audit tasks/<task> --zoom 4`로 슬라이드 안의 대표 PNG·캡션·배치를 확인한다.
4. 실제 PowerPoint 재생을 확인하지 않았다면 그 점을 보고에 남긴다. 무엇을 보여 주는지, 합성인지 실측인지, 스크립트 위치, 남은 한계를 전달한다.
