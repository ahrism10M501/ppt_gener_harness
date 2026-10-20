import re
import unittest

import yaml

from rvppt.template import ROOT, load_tokens, semantic_palette


class PaletteTests(unittest.TestCase):
    def test_every_preset_provides_complete_hex_palette(self):
        roles = {"accent", "band", "secondary", "tint", "neutral", "ink", "section_accent", "background"}
        paths = sorted((ROOT / "templates/presets").glob("*.yaml"))
        self.assertTrue(paths)
        for path in paths:
            with self.subTest(preset=path.stem):
                palette = semantic_palette(path.stem)
                self.assertEqual(set(palette), roles)
                for value in palette.values():
                    self.assertRegex(value, r"^#[0-9A-F]{6}$")

    def test_rvlab_yaml_matches_design_palette(self):
        preset = yaml.safe_load((ROOT / "templates/presets/rvlab.yaml").read_text(encoding="utf-8"))
        self.assertEqual(preset["palette"], load_tokens()["palette"])

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
        self.assertTrue({"ppt-charts", "ppt-animation"} <= declarations)


if __name__ == "__main__":
    unittest.main()
