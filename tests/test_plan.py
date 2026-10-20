from contextlib import redirect_stdout
from copy import deepcopy
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import yaml

from rvppt import cli, project
from rvppt.plan import write_plan
from rvppt.state import STAGES, StateError, approve, status
from test_state import REVIEWS, SLIDES


class PlanTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.task = self.root / "tasks/261020-synthetic"
        for folder in ("sources", "figures", "plan"):
            (self.task / folder).mkdir(parents=True)
        for stage, name in enumerate(STAGES, 1):
            metadata = {"schema_version": 1, "task_id": self.task.name, "stage": stage,
                        "status": "draft", "approval_hash": None, "upstream_hashes": {},
                        "review": deepcopy(REVIEWS[stage])}
            body = SLIDES if stage == 4 else "\nSynthetic fixture, not research evidence.\n"
            (self.task / name).write_text("---\n" + yaml.safe_dump(metadata, allow_unicode=True) + "---\n" + body)

    def text(self):
        return (self.task / "plan/contracts.md").read_text()

    def approve_all(self):
        for stage in range(1, 5):
            approve(self.task, stage)

    def test_plan_preserves_inputs_approvals_and_revision_history(self):
        self.approve_all()
        before = status(self.task)
        inputs = {name: (self.task / name).read_bytes() for name in STAGES}
        result = write_plan(self.task)
        self.assertTrue(result["content_approved"])
        log = self.task / "plan/revisions.md"
        log.write_text(log.read_text() + "\n## R001 — keep this history\n")
        saved = log.read_bytes()
        write_plan(self.task)
        self.assertEqual(log.read_bytes(), saved)
        self.assertEqual(status(self.task), before)
        self.assertEqual(inputs, {name: (self.task / name).read_bytes() for name in STAGES})
        self.assertIn("```mermaid", self.text())
        self.assertIn("SRC --> S4", self.text())
        self.assertIn("S1 --> S4", self.text())
        self.assertIn("FIG --> S4", self.text())
        self.assertIn("[slides.md](../slides.md)", self.text())
        self.assertIn(REVIEWS[2]["key_message"], self.text())
        self.assertIn("S01", self.text())
        for item in before["stages"]:
            self.assertIn(item["review_hash"], self.text())

    def test_refresh_tracks_figures_outline_and_sources(self):
        self.approve_all()
        (self.task / "figures/synthetic.svg").write_text("<svg/>")
        self.assertEqual(write_plan(self.task)["next_stage"], 4)
        self.assertIn("변경으로 재검토 필요", self.text())
        approve(self.task, 4)
        outline = self.task / STAGES[2]
        outline.write_text(outline.read_text() + "\nChanged outline rationale.\n")
        self.assertEqual(write_plan(self.task)["next_stage"], 3)
        self.assertIn("Content changed after approval", self.text())
        (self.task / "sources/synthetic.csv").write_text("synthetic,value\nexample,1\n")
        self.assertEqual(write_plan(self.task)["next_stage"], 1)

    def test_missing_and_invalid_documents_are_visible(self):
        (self.task / STAGES[0]).unlink()
        (self.task / STAGES[1]).write_text("broken YAML")
        self.assertEqual(write_plan(self.task)["next_stage"], 1)
        self.assertIn("미작성", self.text())
        self.assertIn("문서 오류", self.text())
        self.assertIn("missing YAML frontmatter", self.text())

    def test_cli_and_new_project_create_plan_files(self):
        with patch("rvppt.cli.ROOT", self.root), redirect_stdout(io.StringIO()) as output:
            self.assertEqual(cli.main(["plan", str(self.task)]), 0)
        self.assertEqual(json.loads(output.getvalue())["next_stage"], 1)
        profile = self.root / "profile.yaml"
        profile.write_text("name: Synthetic\nname_en: Example\naffiliation: [Lab, University]\n")
        result = project.new_project("new", "Synthetic", day="2026-10-20", profile_path=profile,
                                     tasks=self.root / "tasks")
        self.assertTrue(Path(result["contracts"]).is_file())
        self.assertTrue(Path(result["revisions"]).is_file())

    def test_refuses_symlinks_and_preserves_unowned_contracts(self):
        external = self.root / "external.md"
        external.write_text("Keep user content")
        for name in ("contracts.md", "revisions.md"):
            with self.subTest(name=name):
                path = self.task / "plan" / name
                path.symlink_to(external)
                with self.assertRaisesRegex(StateError, "symlink"):
                    write_plan(self.task)
                self.assertEqual(external.read_text(), "Keep user content")
                path.unlink()
        contracts = self.task / "plan/contracts.md"
        contracts.write_text("User-authored contract")
        with self.assertRaisesRegex(StateError, "not generated"):
            write_plan(self.task)
        self.assertEqual(contracts.read_text(), "User-authored contract")
        self.assertFalse((self.task / "plan/revisions.md").exists())
        contracts.unlink()
        (self.task / "plan").rename(self.root / "old-plan")
        external_folder = self.root / "external"
        external_folder.mkdir()
        (self.task / "plan").symlink_to(external_folder, target_is_directory=True)
        with self.assertRaisesRegex(StateError, "symlink"):
            write_plan(self.task)
        self.assertEqual(list(external_folder.iterdir()), [])


if __name__ == "__main__":
    unittest.main()
