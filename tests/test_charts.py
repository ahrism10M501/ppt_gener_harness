import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "skills/rvlab-charts"))


@unittest.skipUnless(importlib.util.find_spec("matplotlib"), "needs the visual extra: uv sync --extra visual")
class ChartTests(unittest.TestCase):
    def setUp(self):
        import charts
        self.charts = charts
        self.charts.set_preset()
        self.temporary = tempfile.TemporaryDirectory()
        self.out = Path(self.temporary.name)

    def tearDown(self):
        self.charts.set_preset()
        self.temporary.cleanup()

    def test_rvlab_palette_is_unchanged_after_switching_presets(self):
        self.charts.set_preset("modern-16x9")
        self.charts.set_preset("rvlab")
        self.assertEqual(
            [getattr(self.charts, name) for name in ("BLUE", "BAND", "SKY", "TINT", "GRAY", "INK")],
            ["#0070C0", "#053F95", "#5B9BD5", "#DEEBF7", "#A6A6A6", "#000000"],
        )
        self.assertEqual(self.charts.SHADES, ["#053F95", "#0070C0", "#5B9BD5", "#9DC3E6", "#A6A6A6"])

    def test_chart_roles_follow_every_preset(self):
        from rvppt.template import ROOT, semantic_palette
        for path in sorted((ROOT / "templates/presets").glob("*.yaml")):
            with self.subTest(preset=path.stem):
                result = self.charts.set_preset(path.stem)
                palette = semantic_palette(path.stem)
                self.assertEqual(result["palette"], palette)
                for name, role in {
                    "BLUE": "accent", "BAND": "band", "SKY": "secondary",
                    "TINT": "tint", "GRAY": "neutral", "INK": "ink",
                }.items():
                    self.assertEqual(getattr(self.charts, name), palette[role])

    def test_demo_writes_png_and_svg(self):
        self.charts.demo(self.out)
        names = {p.stem for p in self.out.glob("*.png")}
        self.assertEqual(names, {"donut", "flow", "flow-loop", "timeline", "matrix", "funnel", "cards"})
        self.assertTrue(all((self.out / f"{n}.svg").exists() for n in names))

    def test_long_label_is_rejected_instead_of_overflowing(self):
        with self.assertRaisesRegex(ValueError, "라벨을 줄인다"):
            self.charts.flow(self.out / "f", ["카메라 RGB 입력과 깊이 영상을 함께 쓰는 인코더", "정책", "행동"])
        self.assertEqual(self.charts._fit("카메라 RGB 입력", 1.8, 1.1, 18).count("\n"), 1)
