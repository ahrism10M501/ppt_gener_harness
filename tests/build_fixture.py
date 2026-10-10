"""Synthetic RVLAB feature deck. Automated approvals are test fixtures, not user consent."""

from copy import deepcopy
from pathlib import Path

from PIL import Image, ImageDraw
import pymupdf
import yaml

from rvppt.state import STAGES, approve

TABLE = "| 조건 | 합성 값 | 검증 범위 |\n|---|---:|---|\n| A | 12 | 셀 편집 |\n| B | 18 | 정렬 |\n| C | 24 | 폰트 |\n\n::: source\n출처: sources/synthetic.csv — 합성 자료\n:::"
MATH = "인라인 수식 $x^2 + y^2$를 문장에 포함한다.\n\n$$\\mathcal{L} = \\frac{1}{N} \\sum_{i=1}^{N} (y_i - \\hat{y}_i)^2$$\n\n$N$은 합성 표본 수, $y_i$는 합성 목표값이다."
COLUMNS = ":::: columns\n::: column\n- 합성 관찰 A\n  - 확인할 조건\n- 비교 기준을 기록한다\n:::\n::: column\n- 다음 확인 B\n- 실제 근거를 추가한다\n:::\n::::"
COMPARISON = ":::: columns\n::: column\nBaseline\n\n합성 조건 A를 확인한다.\n:::\n::: column\nCandidate\n\n합성 조건 B를 확인한다.\n:::\n::::"
MERMAID = "```mermaid\nflowchart LR\n    A[Markdown] --> B[Pandoc]\n    B --> C[RVLAB Layout]\n    C --> D[Render QA]\n```"
CODE = "```python\ndef approved_inputs(task):\n    return task.status == 'approved'\n```\n\nSynthetic example; no research results."

# (section, [(topic, headline, body)]); every number and figure is synthetic.
SECTIONS = [
    ("기능 검증 | Feature QA", [
        ("표와 수식", "합성 표의 모든 셀을 편집할 수 있다", TABLE),
        ("표와 수식", "블록과 인라인 수식을 함께 편집한다", MATH),
        ("2단 본문", "2단에서 관찰과 다음 행동을 구분한다", COLUMNS),
        ("2단 본문", "두 조건을 같은 규칙으로 비교한다", COMPARISON),
    ]),
    ("그림 배치 | Figure Layout", [
        ("그림 슬롯", "합성 그래프의 종횡비를 보존한다", "![합성 그래프](figures/chart.svg)"),
        ("그림 슬롯", "SVG와 PDF를 같은 두 슬롯에 배치한다", "![합성 그래프](figures/chart.svg)\n\n![합성 PDF](figures/diagram.pdf)"),
        ("그림 슬롯", "세 그림을 같은 높이의 슬롯에 배치한다", "![가로 도형](figures/wide.png)\n\n![세로 도형](figures/tall.png)\n\n![정사각 도형](figures/square.png)"),
        ("그림 슬롯", "네 그림을 고정 2×2 그리드에 배치한다", "![도형 A](figures/wide.png)\n\n![도형 B](figures/tall.png)\n\n![도형 C](figures/square.png)\n\n![도형 D](figures/wide.png)"),
        ("그림 요청", "아직 없는 그림은 요청 상자로 표시한다", "- 연구자가 같은 이름으로 그림을 넣는다\n\n![합성 학습 곡선](figures/requested-curve.png \"x축 epoch, y축 성공률인 합성 곡선. sources/synthetic.csv로 작성\")"),
        ("Mermaid", "원본 코드를 보존하며 흐름도를 렌더한다", MERMAID),
        ("Code", "Code and notes remain editable", CODE),
    ]),
    ("Appendix", [("추가 자료", "본문에서 뺀 합성 자료를 보관한다", "- 합성 부록 항목")]),
]
DECK = {"title": "합성 자료로 제작 기능을 검증한다", "subtitle": "RVLAB 제작·QA 검증", "date": "2026-10-11",
        "presenter": "홍길동 (Gildong Hong)", "affiliation": ["경기대학교 창의공과대학 전자공학과 N학년", "Robotics and Vision Lab Robot Team"]}


def slides_body(sections=SECTIONS):
    parts = []
    for section, slides in sections:
        parts.append(f"# {section}")
        topic = None
        for i, (new_topic, headline, body) in enumerate(slides):
            if new_topic != topic:
                parts.append(f"## {new_topic}"); topic = new_topic
            parts.append(f"### {headline}\n\n{body}\n\n::: notes\n{headline}: 합성 기능 검증용 발표자 노트. 연구 결과가 아니다.\n:::")
    return "\n\n".join(parts) + "\n"


def make_task(task):
    task = Path(task)
    if task.exists():
        raise FileExistsError(f"Fixture must use a new task: {task}")
    for folder in ("sources", "figures", "plan"):
        (task / folder).mkdir(parents=True)
    figures = task / "figures"
    (task / "sources/synthetic.csv").write_text("condition,synthetic_value\nA,12\nB,18\nC,24\n")
    for name, size in [("wide", (2200, 1200)), ("tall", (1200, 2200)), ("square", (1800, 1800))]:
        image = Image.new("RGB", size, "white"); draw = ImageDraw.Draw(image)
        draw.rectangle((80, 80, size[0] - 80, size[1] - 80), outline="#0070C0", width=12)
        draw.ellipse((size[0] // 4, size[1] // 4, size[0] * 3 // 4, size[1] * 3 // 4), fill="#5B9BD5")
        image.save(figures / f"{name}.png", dpi=(300, 300))
    (figures / "chart.svg").write_text('<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="850" viewBox="0 0 1600 850"><rect width="1600" height="850" fill="white"/><path d="M140 80V700H1500" stroke="black" stroke-width="4" fill="none"/><path d="M200 620L550 420L950 340L1400 150" stroke="#0070C0" stroke-width="12" fill="none"/><text x="520" y="780" font-family="Arial" font-size="40">Synthetic step</text><text x="230" y="100" font-family="Arial" font-size="40">SYNTHETIC QA DATA</text></svg>')
    with pymupdf.open() as pdf:
        page = pdf.new_page(width=600, height=450)
        page.draw_rect(pymupdf.Rect(50, 80, 550, 350), color=(0, .44, .75), width=4)
        page.insert_text((140, 220), "Synthetic PDF diagram", fontsize=24)
        pdf.save(figures / "diagram.pdf")
    outline = [{"id": f"S{n:02}", "section": section.split(" | ")[0], "topic": topic, "headline": headline, "evidence": ["sources/synthetic.csv"], "seconds": 30}
               for n, (section, topic, headline) in enumerate(((s, t, h) for s, slides in SECTIONS for t, h, _ in slides), 1)]
    reviews = {
        1: {"audience": "제작기 검토자", "purpose": "합성 자료로 기능을 검증한다", "key_evidence": ["sources/synthetic.csv"], "success_criteria": ["양식과 렌더 QA 통과"], "constraints": ["연구 결과로 사용하지 않는다"]},
        2: {"topic": "합성 기능 검증", "selected_candidate": "A", "key_message": "모든 제작 기능을 합성 자료로 확인한다", "storyline": ["텍스트와 표", "수식과 그림", "렌더 QA"], "candidates": [
            {"id": "A", "message": "모든 제작 기능을 합성 자료로 확인한다", "storyline": ["텍스트와 표", "수식과 그림", "렌더 QA"], "evidence": ["sources/synthetic.csv"], "tradeoff": "실제 발표 효과는 검증하지 않음"},
            {"id": "B", "message": "텍스트만 먼저 확인한다", "storyline": ["텍스트", "QA"], "evidence": ["sources/synthetic.csv"], "tradeoff": "수식과 표를 놓침"}]},
        3: {"duration_minutes": 15, "slides": outline},
        4: {"language": "ko"},
    }
    for stage, filename in enumerate(STAGES, 1):
        metadata = {"schema_version": 1, "task_id": task.name, "stage": stage, "status": "draft", "approval_hash": None, "upstream_hashes": {}, "assumptions": ["Automated fixture approvals are not human consent"], "open_items": [], "review": deepcopy(reviews[stage])}
        if stage == 4:
            metadata["deck"] = dict(DECK)
        (task / filename).write_text("---\n" + yaml.safe_dump(metadata, allow_unicode=True, sort_keys=False) + "---\n" + (slides_body() if stage == 4 else "# 합성 검증\n\n연구 자료가 아닌 자동 검증 픽스처.\n"), encoding="utf-8")
        approve(task, stage)
    return task

