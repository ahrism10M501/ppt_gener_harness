from copy import deepcopy
import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest

import yaml

from rvppt.state import STAGES
from rvppt.template import ROOT
from test_state import REVIEWS, SLIDES


def run_cli_smoke():
    """Exercise the CLI in its actual repository task boundary, then clean up."""
    def command(task, *arguments, code=0):
        result = subprocess.run([sys.executable, "-m", "rvppt", arguments[0], str(task), *arguments[1:]], cwd=ROOT, capture_output=True, text=True, timeout=30)
        assert result.returncode == code, (result.returncode, result.stdout, result.stderr)
        return json.loads(result.stdout) if code == 0 else result.stderr

    (ROOT / "tasks").mkdir(exist_ok=True)
    with TemporaryDirectory(prefix="261011-cli-test-", dir=ROOT / "tasks") as directory:
        task = Path(directory)
        for folder in ("sources", "figures", "plan"):
            (task / folder).mkdir()
        (task / "sources/evaluation.csv").write_text("type,value\nsynthetic,0\n")
        for stage, name in enumerate(STAGES, 1):
            metadata = {"schema_version": 1, "task_id": task.name, "stage": stage, "status": "draft", "approval_hash": None, "upstream_hashes": {}, "open_items": [], "assumptions": ["Synthetic CLI smoke test"], "review": deepcopy(REVIEWS[stage])}
            body = SLIDES if stage == 4 else "\n# Synthetic QA\n\nNot research evidence.\n"
            (task / name).write_text("---\n" + yaml.safe_dump(metadata, allow_unicode=True, sort_keys=False) + "---\n" + body, encoding="utf-8")
        before = {str(p): p.read_bytes() for p in task.rglob("*.md")}
        assert command(task, "status")["next_stage"] == 1
        assert before == {str(p): p.read_bytes() for p in task.rglob("*.md")}
        assert "upstream" in command(task, "approve", "--stage", "2", code=2)
        for stage in range(1, 5):
            current = command(task, "status")
            approved = command(task, "approve", "--stage", str(stage), "--expected-hash", current["stages"][stage - 1]["review_hash"])
            assert approved["stage"] == stage
        assert command(task, "status")["content_approved"]
        (task / "figures/qa.svg").write_text("<svg/>")
        changed = command(task, "status")
        assert changed["next_stage"] == 4
        command(task, "approve", "--stage", "4", "--expected-hash", changed["stages"][3]["review_hash"])
        reviewed = command(task, "status")["stages"][0]["review_hash"]
        (task / "sources/evaluation.csv").write_text("type,value\nsynthetic,1\n")
        assert "review again" in command(task, "approve", "--stage", "1", "--expected-hash", reviewed, code=2)
        changed = command(task, "status")
        assert changed["next_stage"] == 1
        revised = command(task, "approve", "--stage", "1", "--expected-hash", changed["stages"][0]["review_hash"])
        assert revised["invalidated_stages"] == [2, 3, 4]
        assert command(task, "status")["next_stage"] == 2
    assert not task.exists()


class CliIntegrationTests(unittest.TestCase):
    def test_cli_state_transitions_and_input_review_guard(self):
        run_cli_smoke()


if __name__ == "__main__":
    unittest.main()
