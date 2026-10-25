from pathlib import Path
import re
import tempfile
import unittest

from rvppt.template import ROOT, load_tokens, semantic_palette, task_preset


class PaletteTests(unittest.TestCase):
    def test_every_preset_provides_complete_hex_palette(self):
        roles = {"accent", "band", "secondary", "tint", "neutral", "ink", "section_accent", "background"}
        paths = sorted((ROOT / "templates").glob("*/DESIGN.md"))
        self.assertTrue(paths)
        for path in paths:
            with self.subTest(preset=path.parent.name):
                palette = semantic_palette(path.parent.name)
                self.assertEqual(set(palette), roles)
                for value in palette.values():
                    self.assertRegex(value, r"^#[0-9A-F]{6}$")

    def test_default_tokens_are_the_rvlab_design(self):
        self.assertEqual(load_tokens()["preset_id"], "rvlab")
        self.assertEqual(load_tokens(), load_tokens(preset="rvlab"))

    def test_skill_palette_keys_match_shared_contract(self):
        roles = set(semantic_palette())
        declarations = set()
        for path in sorted((ROOT / "skills").rglob("SKILL.md")):
            text = path.read_text(encoding="utf-8")
            with self.subTest(skill=str(path.relative_to(ROOT))):
                self.assertNotRegex(text, r"`(?:accent_blue|band_blue|table_tint|neutral_gray)`")
                for line in text.splitlines():
                    if "팔레트 키:" in line:
                        keys = set(re.findall(r"`([a-z_]+)`", line))
                        self.assertEqual(keys, roles)
                        declarations.add(path.parent.name)
        self.assertIn("ppt-charts", declarations)

    def test_figure_tools_default_to_the_task_preset(self):
        with tempfile.TemporaryDirectory() as directory:
            task = Path(directory) / "tasks/261024-x"
            (task / "figures").mkdir(parents=True)
            self.assertEqual(task_preset(task / "figures/flow"), "rvlab")
            (task / "slides.md").write_text("---\ndeck:\n  title: T\n  preset: modern-minimal\n---\n", encoding="utf-8")
            self.assertEqual(task_preset(task / "figures/flow"), "modern-minimal")


if __name__ == "__main__":
    unittest.main()
