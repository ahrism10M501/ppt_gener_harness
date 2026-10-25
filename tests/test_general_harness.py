from copy import deepcopy
from pathlib import Path
import shutil
import tempfile
import unittest

from PIL import Image
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
            "default_preset: modern-minimal\ndefault_budget: thorough\n",
            encoding="utf-8",
        )

    def test_presets_list_includes_rvlab_and_16x9_themes(self):
        res = template.list_presets()
        ids = {p["preset_id"]: p for p in res["presets"]}
        for expected in ("rvlab", "modern-minimal", "retro", "neo-city"):
            self.assertIn(expected, ids)
            self.assertTrue(ids[expected]["reference_ready"])
        self.assertEqual(ids["rvlab"]["aspect"], "4:3")
        self.assertEqual(ids["modern-minimal"]["aspect"], "16:9")
        self.assertAlmostEqual(float(ids["modern-minimal"]["slide_in"][0]), 13.333, places=2)

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
        self.assertEqual(res["preset"], "modern-minimal")
        self.assertEqual(res["budget"], "thorough")
        progress = Path(res["progress"])
        self.assertTrue(progress.is_file())
        self.assertIn("`thorough`", progress.read_text(encoding="utf-8"))
        self.assertIn("`modern-minimal`", progress.read_text(encoding="utf-8"))
        # Custom edits to PROGRESS.md must be preserved across write_plan()
        progress.write_text(progress.read_text(encoding="utf-8") + "\n- Verified truth model entry\n", encoding="utf-8")
        saved = progress.read_bytes()
        plan.write_plan(task)
        self.assertEqual(progress.read_bytes(), saved)

    def test_register_custom_template_creates_preset_and_reference(self):
        sandbox = self.root / "repo"
        shutil.copytree(template.ROOT / "templates", sandbox / "templates", ignore=shutil.ignore_patterns("examples", "reference.pptx"))
        original = sandbox / template.RVLAB_ORIGINAL
        reg = template.register_template(
            original,
            "user-custom",
            name="User Custom Template",
            description="Custom template registered in test",
            root=sandbox,
        )
        self.assertEqual(reg["preset_id"], "user-custom")
        self.assertTrue(Path(reg["reference"]).is_file())
        design = Path(reg["design"])
        self.assertEqual(template.load_tokens(design)["preset_id"], "user-custom")
        listed = {p["preset_id"]: p["design"] for p in template.list_presets(sandbox)["presets"]}
        self.assertEqual(listed["user-custom"], "templates/user-custom/DESIGN.md")
        # Conventions written under the tokens survive re-registration.
        design.write_text(design.read_text(encoding="utf-8").replace("## 성격과 판단 기준", "## 성격과 판단 기준\n\n작성한 규약"), encoding="utf-8")
        template.register_template(original, "user-custom", root=sandbox)
        self.assertIn("작성한 규약", design.read_text(encoding="utf-8"))
        # A 16:9 source inherits the modern-minimal structure (style) rather than the stretched RVLAB one.
        wide = template.register_template(template.ROOT / "templates/modern-minimal/reference.pptx", "user-wide", root=sandbox)
        self.assertIn("style", template.load_tokens(wide["design"]))
        # A narrower 16:9 source (Google Slides' 10 x 5.625 in) keeps every inherited box on the slide.
        small = Presentation(template.ROOT / "templates/modern-minimal/reference.pptx")
        small.slide_width, small.slide_height = 9144000, 5143500
        small.save(sandbox / "small.pptx")
        tokens = template.load_tokens(template.register_template(sandbox / "small.pptx", "user-small", root=sandbox)["design"])
        boxes = []
        def collect(node):
            for key, value in node.items() if isinstance(node, dict) else enumerate(node) if isinstance(node, list) else ():
                boxes.append(value) if key == "box" else collect(value)
        collect(tokens["style"])
        self.assertTrue(boxes)
        for x, y, w, h in boxes:
            self.assertLessEqual(x + w, 10 + 1e-3)
            self.assertLessEqual(y + h, 5.625 + 1e-3)
        for builtin in ("rvlab", "retro"):
            with self.assertRaisesRegex(ValueError, "built-in"):
                template.register_template(original, builtin, root=sandbox)

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
        # Without --theme the figure follows the deck: a dark preset gets the dark card.
        (task / "slides.md").write_text("---\ndeck:\n  preset: neo-city\n---\n", encoding="utf-8")
        self.assertEqual(anatomy_bridge.build_anatomy_figure(task, "dial-dark", example="dial-indicator", width=600)["theme"], "dark")
        self.assertNotIn("gif", result)

    def test_anatomy_bridge_uses_the_preset_palette_and_builds_a_gif_from_frames(self):
        task = self.tasks / "261020-anatomy-gif"
        for folder in ("figures", "sources", "plan"):
            (task / folder).mkdir(parents=True)
        (task / "slides.md").write_text("---\ndeck:\n  preset: modern-minimal\n---\n", encoding="utf-8")
        (task / "figures/parts.mjs").write_text(
            'import * as k from "../../kit/iso-kit.mjs";\n'
            "const P = k.fitProjection(k.boxCorners({ x: -20, y: -20, w: 40, d: 40, r: 2 }, 0, 40), 300, 200, { pad: 20 });\n"
            # the gradient is what median-cut quantization turns paper white into (252,252,252)
            "const shade = '<defs><linearGradient id=\"g\"><stop offset=\"0\" stop-color=\"#ffffff\"/><stop offset=\"1\" stop-color=\"#303040\"/></linearGradient></defs>';\n"
            "export const scene = (z) => k.figureSvg({ width: 300, height: 200, label: 'test', "
            "body: [shade, `<rect x=\"20\" y=\"20\" width=\"${100 + z}\" height=\"60\" fill=\"url(#g)\"/>`, "
            "k.solidSvg(k.cylinder(0, 0, 10, 0, 10 + z, P, 24), { tone: 'mid', lit: true })] });\n",
            encoding="utf-8")
        (task / "figures/spin.mjs").write_text(
            'import { writeFileSync } from "node:fs";\nimport { scene } from "./parts.mjs";\n'
            "writeFileSync('spin.html', `<html><body>${scene(30)}</body></html>`);\n"
            "[0, 15, 30].forEach((z, i) => writeFileSync(`frame-${i}.svg`, scene(z)));\n",
            encoding="utf-8")
        result = anatomy_bridge.build_anatomy_figure(task, "spin", script="figures/spin.mjs", width=400, fps=12, hold=0.5)
        svg_text = Path(result["svg"]).read_text(encoding="utf-8")
        accent = template.semantic_palette("modern-minimal")["accent"].lower()
        self.assertIn(accent, svg_text)  # the lit part wears the deck's accent
        self.assertNotIn("#fbfbfa", svg_text)  # no off-white card on a white slide
        animation = result["animation"]
        self.assertEqual(animation["frame_count"], 3)
        self.assertEqual(animation["duration_ms"], 3 * 80 + 500)  # 12 fps steps plus the hold on the last frame
        self.assertEqual(animation["loop_count"], 0)
        with Image.open(result["png"]) as poster:
            self.assertEqual(list(poster.size), animation["size_px"])
        with Image.open(result["gif"]) as gif:
            self.assertEqual(gif.convert("RGB").getpixel((0, 0)), (255, 255, 255))  # paper stays pure white

    def test_widescreen_16x9_build_and_4x_critic_audit(self):
        res = project.new_project(
            "modern-wide",
            "모던 와이드 테스트",
            subtitle="Multi-Preset Build & Audit",
            day="2026-10-20",
            preset="modern-minimal",
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
                "preset": "modern-minimal",
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
        self.assertEqual(built["preset"], "modern-minimal")
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
