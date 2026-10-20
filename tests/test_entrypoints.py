import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import yaml

from rvppt.doctor import SKILL_ENTRYPOINTS, doctor, skill_entrypoints
from rvppt.template import ROOT


class SkillEntrypointTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.skill = self.root / "skills/example"
        self.skill.mkdir(parents=True)
        (self.skill / "SKILL.md").write_text("# Example\n", encoding="utf-8")
        for folder in SKILL_ENTRYPOINTS:
            (self.root / folder).mkdir(parents=True)

    def link_all(self):
        for folder in SKILL_ENTRYPOINTS:
            (self.root / folder / "example").symlink_to(self.skill, target_is_directory=True)

    def test_links_and_copied_directories_are_supported(self):
        self.link_all()
        copied = self.root / ".claude/skills/example"
        copied.unlink()
        copied.mkdir()
        (copied / "SKILL.md").write_text("# Copied for Windows\n", encoding="utf-8")
        self.assertEqual(skill_entrypoints(self.root), [])

    def test_broken_link_warns_in_doctor(self):
        self.link_all()
        broken = self.root / ".agents/skills/example"
        broken.unlink()
        broken.symlink_to(self.root / "missing", target_is_directory=True)
        problems = skill_entrypoints(self.root)
        self.assertTrue(any(".agents/skills/example: broken discovery link" in p for p in problems))
        with patch("rvppt.doctor.skill_entrypoints", return_value=problems):
            result = next(check for check in doctor()["checks"] if check["check"] == "skill_entrypoints")
        self.assertEqual(result["status"], "warn")
        self.assertIn("broken discovery link", result["detail"])

    def test_missing_skill_document_is_reported(self):
        self.link_all()
        (self.skill / "SKILL.md").unlink()
        problems = skill_entrypoints(self.root)
        self.assertEqual(sum("missing SKILL.md" in p for p in problems), 3)

    def test_empty_or_missing_discovery_directory_is_reported(self):
        (self.root / ".agents/skills/example").symlink_to(self.skill, target_is_directory=True)
        (self.root / ".gemini/skills").rmdir()
        problems = skill_entrypoints(self.root)
        self.assertIn(".gemini/skills: missing discovery directory", problems)
        self.assertIn(".claude/skills: skill list differs; missing example", problems)
        self.assertIn(".gemini/skills: skill list differs; missing example", problems)

    def test_plain_file_symlink_checkout_is_reported(self):
        self.link_all()
        plain = self.root / ".agents/skills/example"
        plain.unlink()
        plain.write_text("../../skills/example", encoding="utf-8")
        problems = skill_entrypoints(self.root)
        self.assertTrue(any("symlink checked out as a plain file" in p for p in problems))

    def test_codex_and_claude_follow_manifest_entrypoints(self):
        manifest = yaml.safe_load((ROOT / "skills/dependencies.yaml").read_text(encoding="utf-8"))
        for skill in manifest["skills"]:
            for agent, folder in (("codex", ".agents/skills"), ("claude", ".claude/skills")):
                entrypoint = skill.get("entrypoints", {}).get(agent)
                if not entrypoint:
                    continue
                expected = ROOT / entrypoint
                actual = ROOT / folder / expected.parent.name / "SKILL.md"
                if actual.parent.is_symlink():
                    self.assertEqual(actual.resolve(), expected.resolve())
                else:
                    self.assertEqual(actual.read_bytes(), expected.read_bytes())

    def test_codex_and_claude_discover_the_same_skills(self):
        names = [{path.name for path in (ROOT / folder).iterdir()} for folder in SKILL_ENTRYPOINTS[:2]]
        self.assertEqual(*names)


if __name__ == "__main__":
    unittest.main()
