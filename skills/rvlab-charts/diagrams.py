"""Render content-only Mermaid locally with the active preset palette and fonts."""
import argparse
import json
from pathlib import Path
import re
import subprocess
import tempfile
import xml.etree.ElementTree as ET

from PIL import Image

from rvppt.preview import resolve_fonts
from rvppt.template import ROOT, load_tokens

HERE = Path(__file__).resolve().parent


def validate_source(code):
    # Match the content-only constraint used by slides.md; focus is a semantic role.
    if not re.match(r"\s*(?:graph\s+(?:LR|RL|TD|TB|BT)|flowchart\s+(?:LR|RL|TD|TB|BT)|sequenceDiagram|stateDiagram-v2)\b", code):
        raise ValueError("flowchart / sequenceDiagram / stateDiagram-v2만 지원한다.")
    if (re.search(r"%%\{|^\s*---|\b(?:click|style|classDef|linkStyle|class)\s|:::((?!focus\b)\w+)", code, re.M)
            or re.search(r"<(?!br\s*/?>)|https?://|file://|data:", code, re.I)):
        raise ValueError("스타일·설정·외부 링크는 입력하지 않는다. 강조는 :::focus만 쓴다.")


def render(source, out, preset="rvlab"):
    source, out = Path(source), Path(out)
    code = source.read_text(encoding="utf-8")
    validate_source(code)
    tokens = load_tokens(preset=preset)
    fonts = resolve_fonts(tokens)
    font = fonts["korean"]["resolved"]
    width_in = tokens["geometry_in"]["body"][2] - tokens["geometry_in"]["content_indent"]
    # Reserve space for a two-line headline, its gap and the figure caption.
    height_in = tokens["geometry_in"]["body"][3] - 1.4
    dpi = tokens["limits"]["generated_image_dpi"]
    out.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as temporary:
        svg, png = [Path(temporary) / f"diagram.{suffix}" for suffix in ("svg", "png")]
        request = dict(code=code, palette=tokens["palette"], font=font,
                       width=round(width_in * dpi), svg=str(svg), png=str(png))
        result = subprocess.run(["node", str(HERE / "diagrams.mjs")],
                                input=json.dumps(request), text=True, capture_output=True, cwd=ROOT)
        if result.returncode:
            raise RuntimeError(f"로컬 도식 렌더 실패 (의존성: npm ci):\n{result.stderr}")
        root = ET.parse(svg).getroot()
        _, _, width, height = map(float, root.attrib["viewBox"].split())
        scale = min(width_in / width, height_in / height) * 72
        sizes = [float(el.attrib["font-size"]) * scale for el in root.iter()
                 if el.tag.endswith("}text") and "font-size" in el.attrib]
        if not sizes:
            raise ValueError("도식에 표시할 라벨이 없다. Mermaid 문법을 확인한다.")
        minimum = tokens["sizes_pt"]["secondary"]
        if min(sizes) < minimum:
            raise ValueError(f"슬라이드에서 최소 글자 {min(sizes):.1f}pt < {minimum}pt. "
                             "라벨을 줄이거나 줄바꿈하고 도식을 나눈다.")
        # Check before replacing outputs so an invalid edit preserves the previous figure.
        image = Image.open(png)
        image.save(png, dpi=(dpi, dpi))
        report = dict(renderer="beautiful-mermaid", source=source.name, preset=preset, dpi=dpi,
                      width_px=image.width, height_px=image.height,
                      min_font_pt=round(min(sizes), 1), fonts=fonts,
                      usage="전체 폭 단독 그림; 2단 배치 금지")
        out.with_suffix(".svg").write_bytes(svg.read_bytes())
        out.with_suffix(".png").write_bytes(png.read_bytes())
        out.with_suffix(".json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    single = sub.add_parser("render")
    single.add_argument("source", type=Path)
    single.add_argument("out", type=Path, help="출력 경로, 확장자 제외")
    single.add_argument("--preset", default="rvlab", help="디자인 프리셋 ID (기본: rvlab)")
    demo = sub.add_parser("demo")
    demo.add_argument("out", type=Path)
    demo.add_argument("--preset", default="rvlab", help="디자인 프리셋 ID (기본: rvlab)")
    args = parser.parse_args()
    sources = [args.source] if args.command == "render" else sorted((HERE / "examples").glob("*.mmd"))
    for source in sources:
        out = args.out if args.command == "render" else args.out / source.stem
        report = render(source, out, preset=args.preset)
        print(f"{out}: PNG + SVG, 최소 {report['min_font_pt']}pt (preset={args.preset})")


if __name__ == "__main__":
    main()
