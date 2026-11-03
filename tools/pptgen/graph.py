"""Graphify snapshot record and freshness/exclusion check; building the graph itself is the graphify skill's job."""

from datetime import datetime, timezone
from fnmatch import fnmatch
import json
from pathlib import PurePosixPath
import shutil
import subprocess

from .state import StateError
from .template import ROOT, sha256

PUBLISHED = ("graph.json", "GRAPH_REPORT.md", "graph.html")


def ignored(path, patterns):
    """Minimal .graphifyignore matching: '/x/' anchors at the root, a trailing '/' means a directory, '*' stays in one segment."""
    parts = path.split("/")
    for raw in patterns:
        rule = raw.strip("/").split("/")
        for start in [0] if raw.startswith("/") else range(len(parts)):
            end = start + len(rule)
            if end <= len(parts) and all(fnmatch(p, r) for p, r in zip(parts[start:end], rule)) and (end < len(parts) or not raw.endswith("/")):
                return True
    return False


def _patterns(root):
    lines = (root / ".graphifyignore").read_text(encoding="utf-8").splitlines()
    return [line.strip() for line in lines if line.strip() and not line.startswith("#")]


def _graph_sources(root):
    graph = json.loads((root / "graphify-out/graph.json").read_text(encoding="utf-8"))
    items = graph.get("nodes", []) + graph.get("links", graph.get("edges", []))
    return sorted({item["source_file"] for item in items if item.get("source_file")})


def _candidates(root, suffixes, patterns):
    listed = subprocess.run(["git", "ls-files", "--cached", "--others", "--exclude-standard"], cwd=root, capture_output=True, text=True, check=True).stdout
    return sorted(p for p in listed.splitlines() if PurePosixPath(p).suffix in suffixes and not ignored(p, patterns) and (root / p).is_file())


def graph_check(root=ROOT, record=False):
    out = root / "graphify-out"
    missing = [name for name in PUBLISHED if not (out / name).is_file()]
    if missing:
        raise StateError(f"Graphify outputs missing: {missing}; run the graphify skill on the repository first")
    patterns = _patterns(root)
    sources = _graph_sources(root)
    # Task decks, vendored skills and absolute paths must never reach the published graph.
    leaks = [s for s in sources if ignored(s, patterns) or s.startswith("/") or ":" in s.split("/")[0]]
    snapshot_path = out / "snapshot.json"
    if record:
        if leaks:
            raise StateError(f"Excluded or absolute sources in graph.json; fix .graphifyignore and rebuild: {leaks}")
        suffixes = sorted({PurePosixPath(s).suffix for s in sources})
        inputs = {p: sha256(root / p) for p in _candidates(root, suffixes, patterns)}
        version = subprocess.run(["graphify", "--version"], capture_output=True, text=True).stdout.strip() if shutil.which("graphify") else "unknown"
        snapshot = {"schema_version": 1, "graphify": version, "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                    "suffixes": suffixes, "inputs": inputs, "outputs": {name: sha256(out / name) for name in PUBLISHED}}
        snapshot_path.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    if not snapshot_path.is_file():
        raise StateError("graphify-out/snapshot.json missing; run pptgen graph-check --record after building the graph")
    snapshot = json.loads(snapshot_path.read_text(encoding="utf-8"))
    current = {p: sha256(root / p) for p in _candidates(root, snapshot["suffixes"], patterns)}
    recorded = snapshot["inputs"]
    stale = sorted(p for p in recorded.keys() & current.keys() if recorded[p] != current[p])
    added, removed = sorted(current.keys() - recorded.keys()), sorted(recorded.keys() - current.keys())
    edited = [name for name, digest in snapshot["outputs"].items() if not (out / name).is_file() or sha256(out / name) != digest]
    ok = not (leaks or stale or added or removed or edited)
    return {"ok": ok, "graphify": snapshot["graphify"], "generated_at": snapshot["generated_at"], "inputs": len(recorded),
            "changed": stale, "added": added, "removed": removed, "outputs_edited": edited, "leaks": leaks,
            "next": None if ok else "Code or docs changed since the snapshot: rebuild with the graphify skill (graphify-out/ --update), then pptgen graph-check --record"}
