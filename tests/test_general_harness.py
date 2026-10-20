from copy import deepcopy
from pathlib import Path
import shutil
import tempfile
import unittest

from pptx import Presentation
import yaml

from rvppt import anatomy_bridge, build, plan, project, template
from rvppt.state import STAGES, approve
from test_state import REVIEWS


class GeneralHarnessTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.tasks = self.root / "tasks"
        self.tasks.mkdir(parents=True)
        self.profile = self.root / "profile.yaml"
        self.profile.write_text(
            "name: 홍길동\nname_en: Gildong Hong\n"
            "affiliation:\n  - 경기대학교 전자공학과\n  - Robotics and Vision Lab\n"
            "default_preset: modern-16x9\ndefault_budget: thorough\n",
            encoding="utf-8",
        )

    def test_presets_list_includes_4x3_and_16x9_presets(self):
        res = template.list_presets()
        ids = {p["preset_id"]: p for p in res["presets"]}
        for expected in ("rvlab", "modern-16x9", "academic-16x9", "executive-16x9", "minimal-4x3"):
            self.assertIn(expected, ids)
            self.assertTrue(ids[expected]["reference_ready"])
        self.assertEqual(ids["rvlab"]["aspect"], "4:3")
        self.assertEqual(ids["modern-16x9"]["aspect"], "16:9")
        self.assertAlmostEqual(float(ids["modern-16x9"]["slide_in"][0]), 13.333, places=2)

    def test_new_project_creates_progress_md_and_inherits_preset_and_budget(self):
        res = project.new_project(
            "wide-deck",
            "와이드 발표 테스트",
            subtitle="16:9 Harness Verification",
            day="2026-10-20",
            profile_path=self.profile,
            tasks=self.tasks,
        )
        task = Path(res["task"])
        self.assertEqual(res["preset"], "modern-16x9")
        self.assertEqual(res["budget"], "thorough")
        progress = Path(res["progress"])
        self.assertTrue(progress.is_file())
        self.assertIn("`thorough`", progress.read_text(encoding="utf-8"))
        self.assertIn("`modern-16x9`", progress.read_text(encoding="utf-8"))
        # Custom edits to PROGRESS.md must be preserved across write_plan()
        progress.write_text(progress.read_text(encoding="utf-8") + "\n- Verified truth model entry\n", encoding="utf-8")
        saved = progress.read_bytes()
        plan.write_plan(task)
        self.assertEqual(progress.read_bytes(), saved)

    def test_register_custom_template_creates_preset_and_reference(self):
        sandbox = self.root / "repo"
        (sandbox / "templates/presets").mkdir(parents=True)
        for p in (template.ROOT / "templates/presets").glob("*.yaml"):
            shutil.copy2(p, sandbox / "templates/presets" / p.name)
        shutil.copy2(template.ROOT / "templates/RVLAB_PPT양식.pptx", sandbox / "templates/RVLAB_PPT양식.pptx")
        reg = template.register_template(
            sandbox / "templates/RVLAB_PPT양식.pptx",
            "user-custom",
            name="User Custom Template",
            description="Custom template registered in test",
            root=sandbox,
        )
        self.assertEqual(reg["preset_id"], "user-custom")
        self.assertTrue(Path(reg["preset_yaml"]).is_file())
        self.assertTrue(Path(reg["reference"]).is_file())

    def test_anatomy_bridge_renders_standalone_svg_png_and_html(self):
        task = self.tasks / "261020-anatomy-test"
        for folder in ("figures", "sources", "plan"):
            (task / folder).mkdir(parents=True)
        result = anatomy_bridge.build_anatomy_figure(
            task,
            "dial-mechanism",
            example="dial-indicator",
            theme="light",
        )
        self.assertTrue(result["ok"])
        svg_path = Path(result["svg"])
        png_path = Path(result["png"])
        html_path = Path(result["html"])
        self.assertTrue(svg_path.is_file())
        self.assertTrue(png_path.is_file())
        self.assertTrue(html_path.is_file())
        svg_text = svg_path.read_text(encoding="utf-8")
        self.assertNotIn("var(--anatomy-", svg_text)
        self.assertNotIn("filter:blur", svg_text)
        self.assertGreaterEqual(result["width_px"], 600)

    def test_widescreen_16x9_build_and_4x_critic_audit(self):
        res = project.new_project(
            "modern-wide",
            "모던 와이드 테스트",
            subtitle="Multi-Preset Build & Audit",
            day="2026-10-20",
            preset="modern-16x9",
            budget="standard",
            profile_path=self.profile,
            tasks=self.tasks,
        )
        task = Path(res["task"])
        (task / "sources/evaluation.csv").write_text("type,value\nsynthetic,0\n", encoding="utf-8")
        for stage in (1, 2, 3):
            meta = {
                "schema_version": 1,
                "task_id": task.name,
                "stage": stage,
                "status": "draft",
                "approval_hash": None,
                "upstream_hashes": {},
                "review": deepcopy(REVIEWS[stage]),
            }
            (task / STAGES[stage - 1]).write_text(
                "---\n" + yaml.safe_dump(meta, allow_unicode=True, sort_keys=False) + "---\n\nSynthetic stage doc.\n",
                encoding="utf-8",
            )
            approve(task, stage)

        slides_meta = {
            "schema_version": 1,
            "task_id": task.name,
            "stage": 4,
            "status": "draft",
            "approval_hash": None,
            "upstream_hashes": {},
            "deck": {
                "title": "모던 와이드 테스트",
                "subtitle": "Multi-Preset Build & Audit",
                "date": "2026-10-20",
                "presenter": "홍길동 (Gildong Hong)",
                "affiliation": ["경기대학교 전자공학과", "Robotics and Vision Lab"],
                "preset": "modern-16x9",
                "budget": "standard",
            },
            "review": {"language": "ko"},
        }
        slides_body = (
            "\n# 관찰 | Observation\n\n"
            "## 실패 분류\n\n"
            "### 실패 분류로 수집 순서를 정한다\n\n"
            "- 합성 검증 내용\n"
            "  - 16:9 와이드 슬라이드 배치 검증\n\n"
            "## 독립 평가\n\n"
            "### 독립 평가의 한계를 밝힌다\n\n"
            "- 실험 결과가 아닌 상태 검증 픽스처\n"
        )
        (task / "slides.md").write_text(
            "---\n" + yaml.safe_dump(slides_meta, allow_unicode=True, sort_keys=False) + "---\n" + slides_body,
            encoding="utf-8",
        )
        approve(task, 4)

        built = build.build(task)
        self.assertEqual(built["detected_overflows"], 0)
        self.assertEqual(built["preset"], "modern-16x9")
        self.assertEqual(built["aspect"], "16:9")
        pptx_path = Path(built["pptx"])
        prs = Presentation(str(pptx_path))
        self.assertAlmostEqual(prs.slide_width / 914400, 13.333, places=2)
        self.assertAlmostEqual(prs.slide_height / 914400, 7.5, places=2)

        audit_res = build.audit(task, zoom=4.0)
        self.assertTrue(audit_res["ok"])
        self.assertTrue(Path(audit_res["critic_sheet"]).is_file())
        self.assertTrue((task / ".build/output/critic-audit.json").is_file())
        self.assertGreater(audit_res["crops_count"], 0)


if __name__ == "__main__":
    unittest.main()
