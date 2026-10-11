from contextlib import redirect_stderr, redirect_stdout
from copy import deepcopy
import io
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import yaml

from rvppt import cli, state
from rvppt.state import StateError, STAGES, approve, read_document, status


REVIEWS = {
    1: {"audience": "BC를 아는 연구실 구성원", "purpose": "다음 수집 우선순위 결정", "key_evidence": ["sources/evaluation.csv"], "success_criteria": ["관찰과 가정을 구분"], "constraints": ["진행보고 3분"]},
    2: {"topic": "합성 상태 검증", "selected_candidate": "A", "key_message": "실패 분류로 수집 순서를 정한다", "storyline": ["관찰", "제안"], "candidates": [
        {"id": "A", "message": "실패 분류로 수집 순서를 정한다", "storyline": ["관찰", "제안"], "evidence": ["sources/evaluation.csv"], "tradeoff": "방법 설명은 짧게"},
        {"id": "B", "message": "독립 평가의 한계를 먼저 정리한다", "storyline": ["설정", "한계"], "evidence": ["sources/evaluation.csv"], "tradeoff": "수집 제안이 늦어짐"},
    ]},
    3: {"duration_minutes": 3, "slides": [
        {"id": "S01", "section": "관찰", "topic": "실패 분류", "headline": "실패 분류로 수집 순서를 정한다", "evidence": ["sources/evaluation.csv"], "seconds": 90},
        {"id": "S02", "topic": "독립 평가", "headline": "독립 평가의 한계를 밝힌다", "evidence": ["sources/evaluation.csv"], "seconds": 60, "figure": "조건별 성공률 막대그래프"},
    ]},
    4: {"language": "ko"},
}
SLIDES = "\n# 관찰\n\n## 실패 분류\n\n### 실패 분류로 수집 순서를 정한다\n\n합성 검증 내용.\n\n## 독립 평가\n\n### 독립 평가의 한계를 밝힌다\n\n실험 결과가 아닌 상태 검증 픽스처.\n"


class StateTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.task = self.root / "tasks/261011-state-test"
        for folder in ("sources", "figures", "plan"):
            (self.task / folder).mkdir(parents=True)
        (self.task / "sources/evaluation.csv").write_text("type,value\nsynthetic,0\n")
        (self.task / "figures/diagram.svg").write_text("<svg/>")
        for stage in range(1, 5):
            self.write_stage(stage)

    def tearDown(self):
        self.temp.cleanup()

    def write_stage(self, stage_number, *, review=None, body=None, **changes):
        metadata = {"schema_version": 1, "task_id": self.task.name, "stage": stage_number, "status": "draft", "approval_hash": None, "upstream_hashes": {}, "assumptions": ["Synthetic fixture, not research evidence"], "open_items": [], "review": deepcopy(REVIEWS[stage_number] if review is None else review)}
        metadata.update(changes)
        body = (SLIDES if stage_number == 4 else "\n# 합성 검증\n\n사용자 요구·사실·추정을 구분하는 상태 검증 픽스처.\n") if body is None else body
        (self.task / STAGES[stage_number - 1]).write_text("---\n" + yaml.safe_dump(metadata, allow_unicode=True, sort_keys=False) + "---\n" + body, encoding="utf-8", newline="\n")

    def document(self, stage):
        return read_document(self.task / STAGES[stage - 1], self.task.name, stage)

    def edit(self, stage, *, body=None, **changes):
        document = self.document(stage)
        metadata = dict(document.metadata, **changes)
        body = document.body if body is None else body
        document.path.write_text("---\n" + yaml.safe_dump(metadata, allow_unicode=True, sort_keys=False) + "---\n" + body, encoding="utf-8", newline="\n")

    def snapshot(self):
        return {p.relative_to(self.task).as_posix(): p.read_bytes() for p in self.task.rglob("*.md")}

    def approve_all(self):
        for stage in range(1, 5):
            approve(self.task, stage)

    def test_status_is_read_only_and_resumes_first_unapproved_stage(self):
        before = self.snapshot()
        result = status(self.task)
        self.assertEqual(result["next_stage"], 1)
        self.assertEqual(result["next_document"], "plan/interview.md")
        self.assertFalse(result["content_approved"])
        self.assertEqual(self.snapshot(), before)

    def test_approval_chain_is_required_and_build_gate_opens_after_four_stages(self):
        with self.assertRaisesRegex(StateError, "upstream"):
            approve(self.task, 2)
        self.approve_all()
        self.assertTrue(status(self.task)["content_approved"])
        self.assertIsNone(status(self.task)["next_stage"])
        self.assertEqual(set(self.document(4).metadata["upstream_hashes"]), {"sources/", "figures/", "plan/interview.md", "plan/brief.md", "plan/outline.md"})

    def test_body_edit_invalidates_own_and_downstream_approvals(self):
        self.approve_all()
        self.edit(2, body=self.document(2).body + "새 사용자 요구.\n")
        result = status(self.task)
        self.assertEqual(result["next_stage"], 2)
        self.assertEqual([s["effective_status"] for s in result["stages"]], ["approved", "stale", "stale", "stale"])
        self.assertFalse(result["content_approved"])

    def test_sources_change_requires_interview_review_without_mutating_documents(self):
        self.approve_all()
        before = self.snapshot()
        (self.task / "sources/evaluation.csv").write_text("type,value\nsynthetic,1\n")
        result = status(self.task)
        self.assertEqual(result["next_stage"], 1)
        self.assertTrue(all(s["effective_status"] == "stale" for s in result["stages"]))
        self.assertEqual(self.snapshot(), before)

    def test_figures_change_requires_only_final_content_review(self):
        self.approve_all()
        (self.task / "figures/diagram.svg").write_text("<svg><!-- edited --></svg>")
        result = status(self.task)
        self.assertEqual(result["next_stage"], 4)
        self.assertEqual([s["effective_status"] for s in result["stages"]], ["approved", "approved", "approved", "stale"])

    def test_source_rename_addition_and_deletion_are_input_changes(self):
        self.approve_all()
        original = self.task / "sources/evaluation.csv"
        original.rename(original.with_name("renamed.csv"))
        self.assertEqual(status(self.task)["next_stage"], 1)
        approve(self.task, 1)
        added = self.task / "sources/extra.txt"
        added.write_text("new material")
        self.assertEqual(status(self.task)["next_stage"], 1)
        approve(self.task, 1)
        added.unlink()
        self.assertEqual(status(self.task)["next_stage"], 1)

    def test_reapproval_resets_downstream_saved_approvals(self):
        self.approve_all()
        self.edit(1, body=self.document(1).body + "전제 변경.\n")
        result = approve(self.task, 1)
        self.assertEqual(result["invalidated_stages"], [2, 3, 4])
        for stage in (2, 3, 4):
            self.assertEqual(self.document(stage).metadata["status"], "draft")
            self.assertIsNone(self.document(stage).metadata["approval_hash"])
        self.assertEqual(status(self.task)["next_stage"], 2)

    def test_repeating_a_current_approval_is_a_noop(self):
        self.approve_all()
        before = self.snapshot()
        result = approve(self.task, 1)
        self.assertFalse(result["changed"])
        self.assertEqual(result["invalidated_stages"], [])
        self.assertEqual(self.snapshot(), before)

    def test_hash_excludes_only_approval_metadata(self):
        document = self.document(1)
        before = document.content_hash
        document.metadata.update(status="approved", approval_hash="a" * 64, upstream_hashes={"sources/": "b" * 64})
        self.assertEqual(document.content_hash, before)
        document.metadata["custom_context"] = "new substantive frontmatter"
        self.assertNotEqual(document.content_hash, before)

    def test_assumption_and_custom_frontmatter_edits_require_reapproval(self):
        self.approve_all()
        self.edit(1, assumptions=["추가로 확인해야 할 가정"])
        self.assertEqual(status(self.task)["next_stage"], 1)
        approve(self.task, 1)
        self.edit(1, audience_context="Changed understanding of audience")
        self.assertEqual(status(self.task)["next_stage"], 1)

    def test_expected_review_hash_rejects_a_changed_revision(self):
        reviewed = status(self.task)["stages"][0]["review_hash"]
        self.edit(1, body=self.document(1).body + "review 이후 수정.\n")
        before = self.snapshot()
        with self.assertRaisesRegex(StateError, "review again"):
            approve(self.task, 1, reviewed)
        self.assertEqual(self.snapshot(), before)

    def test_review_hash_also_rejects_source_changes_without_document_edits(self):
        reviewed = status(self.task)["stages"][0]["review_hash"]
        content = self.document(1).content_hash
        before = self.snapshot()
        (self.task / "sources/evaluation.csv").write_text("type,value\nsynthetic,2\n")
        self.assertEqual(self.document(1).content_hash, content)
        with self.assertRaisesRegex(StateError, "review again"):
            approve(self.task, 1, reviewed)
        self.assertEqual(self.snapshot(), before)

    def test_approval_preserves_body_math_tables_paths_and_file_mode(self):
        body = "\n# 자료\n\n수식 $L = \\|a-\\hat a\\|^2$.\n\n| 항목 | 값 |\n| --- | --- |\n| 합성 | 0 |\n\n`sources/경로 with space.csv`\n"
        self.write_stage(1, body=body)
        self.document(1).path.chmod(0o640)
        before = self.document(1)
        result = approve(self.task, 1, status(self.task)["stages"][0]["review_hash"])
        after = self.document(1)
        self.assertEqual(after.body, body)
        self.assertEqual(after.content_hash, result["approval_hash"])
        if os.name != "nt":  # Windows keeps only the read-only bit.
            self.assertEqual(after.path.stat().st_mode & 0o777, 0o640)

    def test_blocking_items_prevent_approval_nonblocking_items_are_reported(self):
        item = {"id": "Q06", "description": "독립 평가 표본 수 확인", "blocking": True}
        self.edit(1, open_items=[item])
        before = self.snapshot()
        with self.assertRaisesRegex(StateError, "Blocking open item"):
            approve(self.task, 1)
        self.assertEqual(self.snapshot(), before)
        self.edit(1, open_items=[dict(item, blocking=False)])
        approve(self.task, 1)
        self.assertEqual(status(self.task)["stages"][0]["open_items"][0]["description"], item["description"])

    def test_brief_requires_distinct_grounded_candidates_and_consistent_selection(self):
        approve(self.task, 1)
        cases = []
        one = deepcopy(REVIEWS[2]); one["candidates"] = one["candidates"][:1]; cases.append(one)
        mismatch = deepcopy(REVIEWS[2]); mismatch["key_message"] = "unsupported alternative"; cases.append(mismatch)
        duplicate = deepcopy(REVIEWS[2]); duplicate["candidates"][1]["id"] = "A"; cases.append(duplicate)
        no_evidence = deepcopy(REVIEWS[2]); no_evidence["candidates"][0]["evidence"] = []; cases.append(no_evidence)
        for review in cases:
            with self.subTest(review=review):
                self.write_stage(2, review=review)
                with self.assertRaises(StateError):
                    approve(self.task, 2)

    def test_unknown_topic_can_finish_interview_but_not_message_selection(self):
        self.write_stage(1, topic="TBD")
        approve(self.task, 1)
        review = deepcopy(REVIEWS[2])
        review["topic"] = "TBD"
        self.write_stage(2, review=review)
        with self.assertRaisesRegex(StateError, "topic"):
            approve(self.task, 2)

    def test_outline_rejects_arbitrary_styles_bad_ids_and_time_overrun(self):
        approve(self.task, 1); approve(self.task, 2)
        cases = []
        style = deepcopy(REVIEWS[3]); style["slides"][0]["font"] = "Comic Sans"; cases.append(style)
        layout = deepcopy(REVIEWS[3]); layout["slides"][0]["layout"] = "freeform"; cases.append(layout)
        sentence = deepcopy(REVIEWS[3]); del sentence["slides"][0]["headline"]; cases.append(sentence)
        duplicate = deepcopy(REVIEWS[3]); duplicate["slides"][1]["id"] = "S01"; cases.append(duplicate)
        boolean = deepcopy(REVIEWS[3]); boolean["slides"][0]["seconds"] = True; cases.append(boolean)
        overrun = deepcopy(REVIEWS[3]); overrun["duration_minutes"] = 1; cases.append(overrun)
        for review in cases:
            with self.subTest(review=review):
                self.write_stage(3, review=review)
                with self.assertRaises(StateError):
                    approve(self.task, 3)

    def test_topics_headlines_and_order_must_match_approved_outline(self):
        for stage in (1, 2, 3):
            approve(self.task, stage)
        for body in [SLIDES.replace("## 실패 분류", "## 다른 토픽"), SLIDES.replace("독립 평가의 한계를 밝힌다", "과장한 새 주장"), SLIDES + "\n### 실패 분류로 수집 순서를 정한다\n"]:
            with self.subTest(body=body):
                self.write_stage(4, body=body)
                with self.assertRaises(StateError):
                    approve(self.task, 4)

    def test_slide_like_headings_inside_fences_and_comments_are_not_slides(self):
        body = SLIDES + "\n```markdown\n### Example inside code\n```\n\n<!--\n### Hidden comment\n-->\n\n~~~~text\n### Tilde fence\n~~~~\n"
        self.write_stage(4, body=body)
        self.approve_all()
        self.assertTrue(status(self.task)["content_approved"])

    def test_invalid_frontmatter_is_reported_without_approving(self):
        path = self.task / STAGES[0]
        cases = ["# No frontmatter", "---\nschema_version: 1\n", "---\nschema_version: 1\nschema_version: 1\n---\nbody"]
        for text in cases:
            with self.subTest(text=text):
                path.write_text(text)
                self.assertEqual(status(self.task)["stages"][0]["effective_status"], "invalid")
                with self.assertRaises(StateError):
                    approve(self.task, 1)

    def test_wrong_task_stage_types_and_forged_empty_approval_are_invalid(self):
        for change in [{"task_id": "other-task"}, {"stage": True}, {"schema_version": True}, {"status": []}, {"status": "approved", "approval_hash": None}, {"open_items": [{"id": "Q1", "description": "check", "blocking": "yes"}]}]:
            with self.subTest(change=change):
                self.write_stage(1, **change)
                self.assertEqual(status(self.task)["stages"][0]["effective_status"], "invalid")

    def test_unhashable_review_types_do_not_crash_status(self):
        review = deepcopy(REVIEWS[3]); review["slides"][0]["layout"] = []
        self.write_stage(3, review=review)
        self.write_stage(4, review={"language": []})
        report = status(self.task)
        self.assertTrue(report["stages"][2]["issues"])
        self.assertTrue(report["stages"][3]["issues"])
        self.write_stage(3, review=["unfinished outline"])
        self.assertTrue(status(self.task)["stages"][2]["issues"])

    def test_nonfinite_numbers_and_yaml_dates_require_correction(self):
        for value in [float("nan"), float("inf")]:
            self.write_stage(1, custom_value=value)
            self.assertEqual(status(self.task)["stages"][0]["effective_status"], "invalid")
        self.write_stage(1)
        path = self.task / STAGES[0]
        path.write_text(path.read_text(encoding="utf-8").replace("stage: 1", "stage: 1\ncustom_date: 2026-10-11"), encoding="utf-8", newline="\n")
        self.assertEqual(status(self.task)["stages"][0]["effective_status"], "invalid")

    def test_missing_stages_and_incomplete_drafts_keep_build_gate_closed(self):
        self.document(1).path.unlink()
        report = status(self.task)
        self.assertEqual(report["next_stage"], 1)
        self.assertEqual(report["stages"][0]["effective_status"], "missing")
        self.assertFalse(report["content_approved"])
        self.write_stage(1, review={}, body="")
        with self.assertRaises(StateError):
            approve(self.task, 1)

    def test_input_and_document_symlinks_are_rejected(self):
        outside = self.root / "outside.txt"
        outside.write_text("outside fixture")
        link = self.task / "sources/link.txt"
        link.symlink_to(outside)
        with self.assertRaisesRegex(StateError, "symlink"):
            status(self.task)
        link.unlink()
        doc = self.task / STAGES[0]
        doc.unlink(); doc.symlink_to(outside)
        report = status(self.task)
        self.assertEqual(report["stages"][0]["effective_status"], "invalid")
        self.assertEqual(outside.read_text(), "outside fixture")

    def test_input_change_during_approval_is_rejected_before_writes(self):
        before = self.snapshot()
        original_inspect = state._inspect
        calls = 0

        def inspect(task):
            nonlocal calls
            calls += 1
            if calls == 2:
                (self.task / "sources/new.txt").write_text("new source")
            return original_inspect(task)

        with patch("rvppt.state._inspect", side_effect=inspect):
            with self.assertRaisesRegex(StateError, "inputs changed"):
                approve(self.task, 1)
        self.assertEqual(self.snapshot(), before)

    def test_failed_atomic_replace_preserves_documents_and_cleans_temporary(self):
        before = self.snapshot()
        with patch.object(Path, "replace", side_effect=OSError("simulated disk failure")):
            with self.assertRaises(OSError):
                approve(self.task, 1)
        self.assertEqual(self.snapshot(), before)
        self.assertFalse(list(self.task.rglob(".rvppt-*.tmp")))

    def test_last_moment_editor_change_is_not_overwritten(self):
        document = self.document(1)
        self.edit(1, body=document.body + "new editor input\n")
        changed = document.path.read_bytes()
        with self.assertRaisesRegex(StateError, "changed while approving"):
            state._write(document, dict(document.metadata, status="approved", approval_hash=document.content_hash))
        self.assertEqual(document.path.read_bytes(), changed)

    def test_crlf_and_lf_documents_have_the_same_content_hash(self):
        document = self.document(1)
        document.path.write_bytes(document.original_bytes.replace(b"\n", b"\r\n"))
        self.assertEqual(self.document(1).content_hash, document.content_hash)

    def test_cli_status_approval_and_repository_boundary(self):
        with patch("rvppt.cli.ROOT", self.root):
            output = io.StringIO()
            with redirect_stdout(output):
                self.assertEqual(cli.main(["status", str(self.task)]), 0)
            report = json.loads(output.getvalue())
            output = io.StringIO()
            with redirect_stdout(output):
                self.assertEqual(cli.main(["approve", str(self.task), "--stage", "1", "--expected-hash", report["stages"][0]["review_hash"]]), 0)
            self.assertEqual(json.loads(output.getvalue())["stage"], 1)
            error = io.StringIO()
            with redirect_stderr(error):
                self.assertEqual(cli.main(["status", str(self.root)]), 2)
            self.assertIn("tasks/", error.getvalue())


if __name__ == "__main__":
    unittest.main()
