import importlib.util
from pathlib import Path
import re
import tempfile
import unittest

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("diagrams", ROOT / "skills/rvlab-charts/diagrams.py")
diagrams = importlib.util.module_from_spec(spec)
spec.loader.exec_module(diagrams)


class DiagramTests(unittest.TestCase):
    def test_source_keeps_content_but_rejects_style_and_remote_assets(self):
        diagrams.validate_source('flowchart LR\n A["관측<br>입력"] --> B[정책]:::focus')
        for code in (
            'flowchart LR\n A --> B\nclassDef other fill:red',
            'flowchart LR; A-->B; style A fill:red',
            'flowchart LR\n A["<img src=x>"]',
            'flowchart LR\n %%{init: {}}%%\n A --> B',
            'flowchart LR\n A[입력]:::other',
            'flowchart LR\n A["https://example.com"]',
        ):
            with self.subTest(code=code), self.assertRaises(ValueError):
                diagrams.validate_source(code)

    @unittest.skipUnless((ROOT / "node_modules/beautiful-mermaid").exists(), "needs npm ci")
    def test_examples_render_local_svg_and_colored_png(self):
        with tempfile.TemporaryDirectory() as temporary:
            for source in sorted((diagrams.HERE / "examples").glob("*.mmd")):
                with self.subTest(source=source.name):
                    out = Path(temporary) / source.stem
                    report = diagrams.render(source, out)
                    self.assertGreaterEqual(report["min_font_pt"], 18)
                    svg = out.with_suffix(".svg").read_text()
                    self.assertNotRegex(svg, r"@import|var\(|color-mix\(|<script|<foreignObject")
                    self.assertNotRegex(svg, r"(?:href|src)=[\"'](?:https?:|file:)")
                    self.assertTrue(re.search(r"[가-힣]", svg))
                    with Image.open(out.with_suffix(".png")) as image:
                        self.assertAlmostEqual(image.info["dpi"][0], 300, places=1)
                        colors = image.convert("RGB").getcolors(image.width * image.height)
                        self.assertTrue(any(b > r + 40 and b > g for count, (r, g, b) in colors if count > 100))

    @unittest.skipUnless((ROOT / "node_modules/beautiful-mermaid").exists(), "needs npm ci")
    def test_unreadable_edit_preserves_previous_output(self):
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / "source.mmd"
            out = Path(temporary) / "figure"
            source.write_text("flowchart LR\n A[입력] --> B[정책]:::focus", encoding="utf-8")
            diagrams.render(source, out)
            before = {s: out.with_suffix(s).read_bytes() for s in (".svg", ".png", ".json")}
            source.write_text("flowchart LR\n" + " --> ".join(f'N{i}["긴 라벨이 반복되는 처리 단계 {i}"]' for i in range(12)), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "도식을 나눈다"):
                diagrams.render(source, out)
            for suffix, content in before.items():
                self.assertEqual(out.with_suffix(suffix).read_bytes(), content)
