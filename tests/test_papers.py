"""Synthetic raster/vector figures, provenance, and non-destructive extraction."""

from io import BytesIO
import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest

from PIL import Image
import pymupdf

from rvppt.papers import extract_paper
from rvppt.state import StateError
from rvppt.template import ROOT, sha256


class PaperTests(unittest.TestCase):
    def setUp(self):
        (ROOT / "tasks").mkdir(exist_ok=True)
        self.temporary = TemporaryDirectory(prefix="paper-test-", dir=ROOT / "tasks")
        self.addCleanup(self.temporary.cleanup)
        self.task = Path(self.temporary.name)
        (self.task / "sources").mkdir()
        self.pdf = self.task / "sources/synthetic paper.pdf"
        image = BytesIO()
        Image.new("RGB", (600, 300), "red").save(image, format="PNG")
        with pymupdf.open() as doc:
            page = doc.new_page()
            page.insert_image(pymupdf.Rect(50, 80, 550, 330), stream=image.getvalue())
            page.insert_text((50, 360), "Figure 1. Synthetic robot image, not research evidence.")
            page = doc.new_page()
            page.draw_rect(pymupdf.Rect(50, 80, 550, 330), fill=(0, 0, 1))
            page.draw_circle((150, 180), 50)
            page.draw_line((200, 180), (400, 180))
            page.draw_circle((450, 180), 50)
            page.insert_text((50, 360), "Figure 2. Synthetic vector diagram, not research evidence.")
            doc.save(self.pdf)

    def test_extracts_text_raster_and_vector_with_relative_media(self):
        original = self.pdf.read_bytes()
        result = extract_paper(self.task, "sources/synthetic paper.pdf")
        folder = self.task / result["directory"]
        manifest = json.loads((folder / "pages.json").read_text())
        self.assertEqual(self.pdf.read_bytes(), original)
        self.assertEqual(result["pages"], 2)
        self.assertEqual(manifest["source_sha256"], sha256(self.pdf))
        self.assertEqual(manifest["source"], "sources/synthetic paper.pdf")
        self.assertEqual([p["page"] for p in manifest["pages"]], [1, 2])
        markdown = (folder / "paper.md").read_text()
        self.assertNotIn(str(self.task), markdown)
        self.assertIn("Figure 1.", markdown)
        self.assertIn("Figure 2.", markdown)
        for page, channel in zip(manifest["pages"], (0, 2)):
            self.assertTrue(page["media"])
            with Image.open(folder / page["media"][0]) as image:
                self.assertGreater(image.width, 700)
                self.assertEqual(image.convert("RGB").getpixel((100, 100))[channel], 255)
        self.assertFalse((self.task / "figures").exists())

    def test_existing_output_and_source_are_preserved(self):
        result = extract_paper(self.task, "sources/synthetic paper.pdf")
        output = self.task / result["directory"] / "paper.md"
        output.write_text("Researcher's notes")
        with self.assertRaisesRegex(StateError, "already exists"):
            extract_paper(self.task, "sources/synthetic paper.pdf")
        self.assertEqual(output.read_text(), "Researcher's notes")

    def test_rejects_paths_outside_sources_and_symlinks(self):
        for path in (str(self.pdf), "figures/test.pdf", "sources/../slides.pdf", "sources/test.png"):
            with self.subTest(path=path), self.assertRaises(StateError):
                extract_paper(self.task, path)
        (self.task / "sources/link.pdf").symlink_to(self.pdf)
        with self.assertRaisesRegex(StateError, "symlinks"):
            extract_paper(self.task, "sources/link.pdf")
        (self.task / ".build").symlink_to(self.task / "sources", target_is_directory=True)
        with self.assertRaisesRegex(StateError, "symlinks"):
            extract_paper(self.task, "sources/synthetic paper.pdf")

    def test_failed_extraction_leaves_no_partial_output(self):
        self.pdf.write_bytes(b"Not a PDF")
        with self.assertRaises(pymupdf.FileDataError):
            extract_paper(self.task, "sources/synthetic paper.pdf")
        self.assertEqual(list((self.task / ".build/editorial/papers").iterdir()), [])
        self.assertEqual(self.pdf.read_bytes(), b"Not a PDF")

    def test_cli_stdout_is_json_and_errors_preserve_output(self):
        args = [sys.executable, "-m", "rvppt", "extract-paper", str(self.task), "sources/synthetic paper.pdf"]
        first = subprocess.run(args, cwd=ROOT, capture_output=True, text=True, timeout=30)
        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertEqual(json.loads(first.stdout)["pages"], 2)
        second = subprocess.run(args, cwd=ROOT, capture_output=True, text=True, timeout=30)
        self.assertEqual(second.returncode, 2)
        self.assertIn("already exists", second.stderr)


if __name__ == "__main__":
    unittest.main()
