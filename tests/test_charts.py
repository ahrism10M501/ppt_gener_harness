import sys
from pathlib import Path

import pytest

pytest.importorskip("matplotlib")
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "skills/rvlab-charts"))
import charts  # noqa: E402


def test_demo_writes_png_and_svg(tmp_path):
    charts.demo(tmp_path)
    names = {p.stem for p in tmp_path.glob("*.png")}
    assert names == {"donut", "flow", "flow-loop", "timeline", "matrix", "funnel", "cards"}
    assert all((tmp_path / f"{n}.svg").exists() for n in names)


def test_long_label_is_rejected_instead_of_overflowing(tmp_path):
    with pytest.raises(ValueError, match="라벨을 줄인다"):
        charts.flow(tmp_path / "f", ["카메라 RGB 입력과 깊이 영상을 함께 쓰는 인코더", "정책", "행동"])
    assert charts._fit("카메라 RGB 입력", 1.8, 1.1, 18).count("\n") == 1
