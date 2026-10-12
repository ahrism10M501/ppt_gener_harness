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
        self.temporary = tempfile.TemporaryDirectory()
        self.out = Path(self.temporary.name)

    def tearDown(self):
        self.temporary.cleanup()

    def test_demo_writes_png_and_svg(self):
        self.charts.demo(self.out)
        names = {p.stem for p in self.out.glob("*.png")}
        self.assertEqual(names, {"donut", "flow", "flow-loop", "timeline", "matrix", "funnel", "cards"})
        self.assertTrue(all((self.out / f"{n}.svg").exists() for n in names))

    def test_long_label_is_rejected_instead_of_overflowing(self):
        with self.assertRaisesRegex(ValueError, "라벨을 줄인다"):
            self.charts.flow(self.out / "f", ["카메라 RGB 입력과 깊이 영상을 함께 쓰는 인코더", "정책", "행동"])
        self.assertEqual(self.charts._fit("카메라 RGB 입력", 1.8, 1.1, 18).count("\n"), 1)
