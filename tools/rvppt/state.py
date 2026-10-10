"""Task document schemas, approval hashes, and read-only resumption state."""

from dataclasses import dataclass
import hashlib
import json
import math
import os
from pathlib import Path
import re
import stat
import tempfile

import yaml


# Planning documents live in plan/; slides.md is the researcher-facing source, like main.tex.
STAGES = ("plan/interview.md", "plan/brief.md", "plan/outline.md", "slides.md")
APPROVAL_FIELDS = {"status", "approval_hash", "upstream_hashes"}
HASH_PATTERN = re.compile(r"[0-9a-f]{64}\Z")
ID_PATTERN = re.compile(r"[A-Za-z][A-Za-z0-9_-]{0,31}\Z")
HEADING = re.compile(r"^(#{1,3}) +(.+?)\s*$")
SLIDE_FIELDS = {"id", "section", "topic", "headline", "evidence", "seconds", "figure"}


class StateError(ValueError):
    pass


class UniqueLoader(yaml.SafeLoader):
    """Reject duplicate keys instead of silently replacing approval metadata."""


def _mapping(loader, node, deep=False):
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if not isinstance(key, str) or key in result:
            raise StateError("YAML mappings require unique string keys")
        result[key] = loader.construct_object(value_node, deep=deep)
    return result


UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _mapping)


def _digest(value):
    data = json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":"), allow_nan=False)
    return hashlib.sha256(data.encode("utf-8")).hexdigest()


def _string(value):
    return isinstance(value, str) and bool(value.strip()) and value.strip() not in {"TBD", "TODO", "..."}


def _strings(value):
    return isinstance(value, list) and bool(value) and all(_string(v) for v in value)


@dataclass
class Document:
    path: Path
    metadata: dict
    body: str
    original_bytes: bytes

    @property
    def content_hash(self):
        return _digest({"metadata": {k: v for k, v in self.metadata.items() if k not in APPROVAL_FIELDS}, "body": self.body})


def read_document(path, task_id, stage):
    path = Path(path)
    if path.is_symlink():
        raise StateError(f"Stage documents cannot be symlinks: {path.name}")
    raw = path.read_bytes()
    lines = raw.decode("utf-8-sig").replace("\r\n", "\n").splitlines(keepends=True)
    if not lines or lines[0].rstrip("\n") != "---":
        raise StateError(f"{path.name}: missing YAML frontmatter")
    end = next((i for i in range(1, len(lines)) if lines[i].rstrip("\n") == "---"), None)
    if end is None:
        raise StateError(f"{path.name}: unclosed YAML frontmatter")
    try:
        metadata = yaml.load("".join(lines[1:end]), Loader=UniqueLoader)
    except yaml.YAMLError as error:
        raise StateError(f"{path.name}: invalid YAML ({error.problem})") from error
    if not isinstance(metadata, dict):
        raise StateError(f"{path.name}: frontmatter must be a mapping")
    if type(metadata.get("schema_version")) is not int or metadata["schema_version"] != 1:
        raise StateError(f"{path.name}: schema_version must be 1")
    if metadata.get("task_id") != task_id:
        raise StateError(f"{path.name}: task_id must match its task folder")
    if type(metadata.get("stage")) is not int or metadata["stage"] != stage:
        raise StateError(f"{path.name}: wrong stage number")
    if not isinstance(metadata.get("status"), str) or metadata["status"] not in {"draft", "approved"}:
        raise StateError(f"{path.name}: status must be draft or approved")
    approval = metadata.get("approval_hash")
    if "approval_hash" not in metadata or (approval is not None and (not isinstance(approval, str) or not HASH_PATTERN.fullmatch(approval))):
        raise StateError(f"{path.name}: invalid approval_hash")
    if metadata["status"] == "approved" and approval is None:
        raise StateError(f"{path.name}: approved document has no approval hash")
    upstream = metadata.get("upstream_hashes")
    if not isinstance(upstream, dict) or not all(isinstance(v, str) and HASH_PATTERN.fullmatch(v) for v in upstream.values()):
        raise StateError(f"{path.name}: invalid upstream_hashes")
    items = metadata.get("open_items", [])
    if not isinstance(items, list) or not all(isinstance(item, dict) and _string(item.get("id")) and _string(item.get("description")) and type(item.get("blocking")) is bool for item in items):
        raise StateError(f"{path.name}: open_items require id, description, and boolean blocking")
    if len({item["id"] for item in items}) != len(items):
        raise StateError(f"{path.name}: duplicate open item ID")
    assumptions = metadata.get("assumptions", [])
    if not isinstance(assumptions, list) or not all(_string(v) for v in assumptions):
        raise StateError(f"{path.name}: assumptions must be strings")
    document = Document(path, metadata, "".join(lines[end + 1:]), raw)
    try:
        document.content_hash
    except (TypeError, ValueError) as error:
        raise StateError(f"{path.name}: use YAML strings, finite numbers, lists, and mappings") from error
    return document


def review_issues(document, previous):
    """Validate stage-specific review summaries; humans judge the actual evidence."""
    issues = []
    stage = document.metadata["stage"]
    review = document.metadata.get("review")
    if not document.body.strip():
        issues.append("Document body is empty")
    if not isinstance(review, dict):
        return issues + ["Missing stage review summary"]
    fields = {
        1: {"audience": _string, "purpose": _string, "key_evidence": _strings, "success_criteria": _strings, "constraints": _strings},
        2: {"topic": _string, "key_message": _string, "storyline": _strings, "selected_candidate": _string},
        3: {},
        4: {},
    }[stage]
    issues.extend(f"review.{key} is missing or incomplete" for key, check in fields.items() if not check(review.get(key)))
    if stage == 2:
        candidates = review.get("candidates")
        valid = isinstance(candidates, list) and 2 <= len(candidates) <= 3
        if valid:
            valid = all(isinstance(c, dict) and _string(c.get("id")) and _string(c.get("message")) and _strings(c.get("storyline")) and _strings(c.get("evidence")) and _string(c.get("tradeoff")) for c in candidates)
        if not valid:
            issues.append("review.candidates requires 2–3 grounded message/storyline alternatives")
        elif len({c["id"] for c in candidates}) != len(candidates):
            issues.append("Duplicate candidate ID")
        else:
            chosen = next((c for c in candidates if c["id"] == review.get("selected_candidate")), None)
            if chosen is None or chosen["message"] != review.get("key_message") or chosen["storyline"] != review.get("storyline"):
                issues.append("Selected candidate, key_message, and storyline do not agree")
    if stage == 3:
        slides = review.get("slides")
        valid = isinstance(slides, list) and bool(slides)
        if valid:
            valid = all(isinstance(s, dict) and {"id", "topic", "headline", "evidence", "seconds"} <= set(s) <= SLIDE_FIELDS and isinstance(s["id"], str) and ID_PATTERN.fullmatch(s["id"]) and _string(s["topic"]) and _string(s["headline"]) and _strings(s["evidence"]) and type(s["seconds"]) is int and s["seconds"] > 0 and all(_string(s[k]) for k in ("section", "figure") if k in s) for s in slides)
        if not valid:
            issues.append("review.slides requires IDs, topics, headlines, evidence, and positive seconds")
        elif len({s["id"] for s in slides}) != len(slides):
            issues.append("Duplicate slide ID")
        duration = review.get("duration_minutes")
        if type(duration) not in (int, float) or duration <= 0 or (isinstance(duration, float) and not math.isfinite(duration)):
            issues.append("review.duration_minutes must be a positive finite number")
        elif valid and sum(s["seconds"] for s in slides) > duration * 60:
            issues.append("Outline exceeds the presentation time budget")
    if stage == 4:
        if not isinstance(review.get("language"), str) or review["language"] not in {"ko", "en"}:
            issues.append("review.language must be ko or en")
        headings = slide_headings(document.body)
        if not headings:
            issues.append("slides.md needs '## topic' and '### headline' slides")
        if 3 in previous:
            outline_review = previous[3].metadata.get("review")
            outline = outline_review.get("slides") if isinstance(outline_review, dict) else None
            if isinstance(outline, list) and all(isinstance(s, dict) and "topic" in s and "headline" in s for s in outline):
                if headings != [(s["topic"], s["headline"]) for s in outline]:
                    issues.append("Slide topics and headlines differ from the outline")
    issues.extend(f"Blocking open item {i['id']}: {i['description']}" for i in document.metadata.get("open_items", []) if i["blocking"])
    return issues


def slide_headings(body):
    """Return (topic, headline) per slide; headings inside code fences and comments are content."""
    visible, fence = [], None
    for line in body.splitlines():
        marker = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line)
        if marker:
            run, tail = marker.groups()
            if fence is None:
                fence = run
            elif run[0] == fence[0] and len(run) >= len(fence) and not tail.strip():
                fence = None
            continue
        if fence is None:
            visible.append(line)
    markdown = re.sub(r"<!--[\s\S]*?-->", "", "\n".join(visible))
    slides, topic = [], None
    for match in filter(None, map(HEADING.match, markdown.splitlines())):
        level, text = len(match[1]), match[2]
        if level == 3:
            slides.append((topic, text))
        else:
            topic = text if level == 2 else None
    return slides


def _walk_error(error):
    raise error


def tree_hash(root):
    """Hash portable relative names and bytes, without following input symlinks."""
    root = Path(root)
    if root.is_symlink():
        raise StateError(f"Input folder cannot be a symlink: {root.name}")
    if root.exists() and not root.is_dir():
        raise StateError(f"Expected input folder: {root.name}")
    if not root.exists():
        return _digest({})
    entries = {}
    for current, directories, files in os.walk(root, followlinks=False, onerror=_walk_error):
        for name in directories + files:
            path = Path(current) / name
            if path.is_symlink():
                raise StateError(f"Input symlinks are not supported: {root.name}/{path.relative_to(root)}")
            if path.is_file():
                with path.open("rb") as file:
                    entries[path.relative_to(root).as_posix()] = hashlib.file_digest(file, "sha256").hexdigest()
            elif not path.is_dir():
                raise StateError(f"Input must be a regular file: {path.name}")
    return _digest(entries)


def _inspect(task):
    task = Path(task)
    if not task.is_dir():
        raise StateError(f"Task folder does not exist: {task}")
    source_hash, figure_hash = tree_hash(task / "sources"), tree_hash(task / "figures")
    documents, stages = {}, []
    for stage, filename in enumerate(STAGES, 1):
        path = task / filename
        item = {"stage": stage, "file": filename, "effective_status": "missing", "issues": []}
        stages.append(item)
        if not path.exists() and not path.is_symlink():
            continue
        try:
            document = read_document(path, task.name, stage)
        except (StateError, UnicodeError, OSError) as error:
            item.update(effective_status="invalid", issues=[str(error)])
            continue
        documents[stage] = document
        expected = {"sources/": source_hash, **{STAGES[s - 1]: documents[s].content_hash for s in range(1, stage) if s in documents}}
        if stage == 4:
            expected["figures/"] = figure_hash
        issues = review_issues(document, documents)
        upstream_issues = [f"Upstream stage {s} is {stages[s - 1]['effective_status']}" for s in range(1, stage) if stages[s - 1]["effective_status"] != "approved"]
        declared = document.metadata["status"]
        effective = declared
        if declared == "approved":
            if issues:
                effective = "invalid"
            elif document.metadata["approval_hash"] != document.content_hash or document.metadata["upstream_hashes"] != expected or upstream_issues:
                effective = "stale"
            if document.metadata["approval_hash"] != document.content_hash:
                issues.append("Content changed after approval")
            if document.metadata["upstream_hashes"] != expected:
                issues.append("Upstream inputs changed after approval")
        review_hash = _digest({"content_hash": document.content_hash, "upstream_hashes": expected})
        item.update(declared_status=declared, effective_status=effective, content_hash=document.content_hash, review_hash=review_hash, approval_hash=document.metadata["approval_hash"], current_upstream_hashes=expected, assumptions=document.metadata.get("assumptions", []), open_items=document.metadata.get("open_items", []), issues=issues + upstream_issues)
    next_stage = next((s["stage"] for s in stages if s["effective_status"] != "approved"), None)
    report = {"schema_version": 1, "task_id": task.name, "content_approved": next_stage is None, "next_stage": next_stage, "next_document": STAGES[next_stage - 1] if next_stage else None, "stages": stages}
    return report, documents


def status(task):
    return _inspect(task)[0]


def _write(document, metadata):
    data = "---\n" + yaml.safe_dump(metadata, allow_unicode=True, sort_keys=False) + "---\n" + document.body
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", newline="\n", dir=document.path.parent, prefix=".rvppt-", suffix=".tmp", delete=False) as file:
            temporary = Path(file.name)
            file.write(data)
        temporary.chmod(stat.S_IMODE(document.path.stat().st_mode))
        if document.path.is_symlink() or document.path.read_bytes() != document.original_bytes:
            raise StateError(f"{document.path.name} changed while approving; rerun status and review")
        temporary.replace(document.path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def approve(task, stage, expected_hash=None):
    if type(stage) is not int or not 1 <= stage <= 4:
        raise StateError("Stage must be 1, 2, 3, or 4")
    report, documents = _inspect(task)
    if stage not in documents:
        raise StateError(f"Cannot approve missing/invalid {STAGES[stage - 1]}")
    document = documents[stage]
    issues = review_issues(document, documents)
    if issues:
        raise StateError("Cannot approve: " + "; ".join(issues))
    if any(s["effective_status"] != "approved" for s in report["stages"][:stage - 1]):
        raise StateError("Approve current upstream stages first")
    reviewed = report["stages"][stage - 1]["review_hash"]
    if expected_hash is not None and expected_hash != reviewed:
        raise StateError("Reviewed document/input hash differs from current inputs; review again")
    if report["stages"][stage - 1]["effective_status"] == "approved":
        return {"task_id": report["task_id"], "stage": stage, "approval_hash": document.content_hash, "review_hash": reviewed, "invalidated_stages": [], "changed": False}
    # Verify the full input snapshot before writing approval or revoking later stages.
    fresh, fresh_documents = _inspect(task)
    if fresh != report or any(d.original_bytes != fresh_documents[s].original_bytes for s, d in documents.items()):
        raise StateError("Task inputs changed while approving; rerun status and review")
    invalidated = []
    for later in range(stage + 1, 5):
        if later in documents and documents[later].metadata["status"] == "approved":
            other = documents[later]
            _write(other, dict(other.metadata, status="draft", approval_hash=None, upstream_hashes={}))
            invalidated.append(later)
    metadata = dict(document.metadata, status="approved", approval_hash=document.content_hash, upstream_hashes=report["stages"][stage - 1]["current_upstream_hashes"])
    _write(document, metadata)
    return {"task_id": report["task_id"], "stage": stage, "approval_hash": document.content_hash, "review_hash": reviewed, "invalidated_stages": invalidated, "changed": True}
