"""Check that Korean polishing of slides.md kept its facts and Markdown structure."""

from collections import Counter
from difflib import SequenceMatcher
import json
from pathlib import Path
import re

from .markdown import nodes, pandoc, plain, table_rows
from .state import APPROVAL_FIELDS, read_document

NUMBER = re.compile(r"\d+(?:[.,]\d+)*")
LATIN = re.compile(r"[A-Za-z][A-Za-z0-9+\-]*[A-Za-z0-9]")


def skeleton(blocks):
    """What polishing must not touch: headings, block/list/table shapes, code, math, links, image paths, citations."""
    shape = []
    for node in nodes(blocks):
        kind, content = node["t"], node.get("c")
        if kind == "Header":
            shape.append((kind, content[0], plain(content[2]).strip()))
        elif kind in ("Para", "Plain"):
            shape.append((kind,))
        elif kind in ("BulletList", "OrderedList"):
            shape.append((kind, len(content if kind == "BulletList" else content[1])))
        elif kind == "Table":
            rows = table_rows(node)
            shape.append((kind, len(rows), len(rows[0])))
        elif kind in ("CodeBlock", "Code", "Math", "RawBlock", "RawInline"):
            shape.append((kind, content[-1]))
        elif kind in ("Image", "Link"):
            shape.append((kind, content[2][0]))
        elif kind == "Cite":
            shape.append((kind, tuple(c["citationId"] for c in content[0])))
        elif kind == "Div":
            shape.append((kind, tuple(content[0][1])))
    return shape


def difference(before, after):
    removed, added = before - after, after - before
    return {"removed": sorted(removed.elements()), "added": sorted(added.elements())}


def polish_check(task, before_path):
    before = read_document(Path(before_path), task.name, 4)
    after = read_document(task / "slides.md", task.name, 4)
    errors, warnings = [], []
    strip = lambda doc: {k: v for k, v in doc.metadata.items() if k not in APPROVAL_FIELDS}
    if strip(before) != strip(after):
        errors.append("Frontmatter (deck, review, assumptions) changed; polishing edits body text only")
    old, new = (json.loads(pandoc(["-f", "markdown-smart", "-t", "json"], d.body))["blocks"] for d in (before, after))
    old_shape, new_shape = skeleton(old), skeleton(new)
    if old_shape != new_shape:
        index = next((i for i, (a, b) in enumerate(zip(old_shape, new_shape)) if a != b), min(len(old_shape), len(new_shape)))
        pair = [s[index] if index < len(s) else None for s in (old_shape, new_shape)]
        errors.append(f"Markdown structure changed at item {index}: {pair[0]} → {pair[1]}. Headings, lists, tables, code, math, links and figure paths must stay identical")
    old_text, new_text = plain(old), plain(new)
    numbers = difference(Counter(NUMBER.findall(old_text)), Counter(NUMBER.findall(new_text)))
    if numbers["removed"] or numbers["added"]:
        errors.append(f"Numbers changed: {numbers}")
    terms = difference(Counter(LATIN.findall(old_text)), Counter(LATIN.findall(new_text)))
    if terms["removed"] or terms["added"]:
        warnings.append(f"Latin terms changed; confirm technical terms and citations survived: {terms}")
    return {"task_id": task.name, "before": str(before_path), "ok": not errors, "errors": errors, "warnings": warnings,
            "similarity": round(SequenceMatcher(None, before.body, after.body).ratio(), 3)}
