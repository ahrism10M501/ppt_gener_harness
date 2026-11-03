"""Extract paper Markdown and figure candidates without changing source PDFs."""

from contextlib import redirect_stdout
from importlib.metadata import version
import io
import json
from pathlib import Path
import re
from tempfile import TemporaryDirectory

import pymupdf

from .markdown import asset_path
from .state import StateError
from .template import sha256


def extract_paper(task, pdf):
    task = Path(task).resolve()
    relative = Path(pdf)
    # Researcher papers live in sources/; papers the agent downloads go to figures/external/ so they do not reset stage 1.
    if relative.parts[:1] != ("sources",) and relative.parts[:2] != ("figures", "external") or relative.suffix.lower() != ".pdf":
        raise StateError("Paper must be a task-local sources/*.pdf or figures/external/*.pdf path")
    source = asset_path(task, pdf)
    digest = sha256(source)
    work = task
    for name in (".build", "editorial", "papers"):
        work = work / name
        if work.is_symlink():
            raise StateError(f"Paper output symlinks are forbidden: {work}")
    destination = work / f"{source.stem}-{digest[:12]}"
    if destination.exists():
        raise StateError(f"Paper extraction already exists; reuse {destination}. Existing files were preserved")
    work.mkdir(parents=True, exist_ok=True)
    with TemporaryDirectory(prefix=".extract-", dir=work) as directory:
        staging = Path(directory)
        media = staging / "media"
        media.mkdir()
        # The converter prints a layout-package suggestion; keep CLI stdout JSON-only.
        with redirect_stdout(io.StringIO()):
            import pymupdf4llm

            with pymupdf.open(source) as document:
                if document.needs_pass or not document.is_pdf:
                    raise StateError("Paper must be an unencrypted PDF")
                chunks = pymupdf4llm.to_markdown(
                    document, filename="paper.pdf", write_images=True,
                    image_path=media.as_posix(), page_chunks=True, dpi=200,
                )
        pages = []
        for number, chunk in enumerate(chunks, 1):
            text = chunk["text"].replace(media.as_posix() + "/", "media/")
            pages.append({"page": number, "text": text,
                          "media": re.findall(r"!\[[^\]]*\]\((media/[^)]+)\)", text)})
        manifest = {"source": relative.as_posix(), "source_sha256": digest,
                    "converter": f"pymupdf4llm=={version('pymupdf4llm')}", "pages": pages}
        (staging / "paper.md").write_text(
            "\n\n".join(f"<!-- PDF page {p['page']} -->\n\n{p['text']}" for p in pages), encoding="utf-8",
        )
        (staging / "pages.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
        staging.rename(destination)
    return {"directory": destination.relative_to(task).as_posix(), "source": relative.as_posix(),
            "pages": len(pages), "media": len(list((destination / "media").glob("*.png")))}
