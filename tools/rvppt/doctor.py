"""Offline environment and vendored-skill integrity check; reports fixes, never downloads or installs."""

import os
import shutil
import sys

import yaml

from .template import ROOT, load_tokens, sha256


SYMLINK_FIX = "symlink checked out as a plain file; enable symlinks (Windows: Developer Mode), run git config core.symlinks true, then git checkout -- {path}"


def link_stand_in(path):
    """Git without symlink support checks a link out as a one-line file holding its target."""
    if path.is_symlink() or not path.is_file() or path.stat().st_size > 260:
        return False
    target = path.read_bytes().decode("utf-8", "replace")
    return "\n" not in target and (path.parent / target).exists()


def skill_integrity(root=ROOT):
    """Compare every vendored skill file and symlink with skills/dependencies.yaml."""
    problems = []
    manifest = yaml.safe_load((root / "skills/dependencies.yaml").read_text(encoding="utf-8"))
    for skill in manifest["skills"]:
        base = root / "skills" / skill["id"]
        for name, record in skill["files"].items():
            path = base / name
            if not path.is_file() or sha256(path) != record["sha256"]:
                problems.append(f"{path.relative_to(root).as_posix()}: {'missing' if not path.is_file() else 'modified'}; restore with git or copy {skill['repository']}@{skill['commit']}:{record['upstream_path']}")
        for name, record in (skill.get("symlinks") or {}).items():
            path = base / name
            relative = path.relative_to(root).as_posix()
            if link_stand_in(path):
                problems.append(f"{relative}: {SYMLINK_FIX.format(path=relative)}")
            # Git for Windows stores link targets with backslashes.
            elif not path.is_symlink() or os.readlink(path).replace("\\", "/") != record["target"]:
                problems.append(f"{relative}: symlink must point to {record['target']}")
    for folder in (".agents/skills", ".claude/skills", ".claude/agents"):
        for link in sorted((root / folder).glob("*")):
            relative = link.relative_to(root).as_posix()
            if link_stand_in(link):
                problems.append(f"{relative}: {SYMLINK_FIX.format(path=relative)}")
            elif not link.exists():
                problems.append(f"{relative}: broken discovery link")
    return problems


def doctor():
    checks = []

    def check(name, required, test):
        try:
            detail = test()
            checks.append({"check": name, "status": "ok", "detail": detail})
        except Exception as error:  # Each probe reports independently; one missing tool must not hide the rest.
            checks.append({"check": name, "status": "fail" if required else "warn", "detail": str(error)})

    def python():
        if sys.version_info < (3, 11):
            raise RuntimeError(f"Python {sys.version.split()[0]}; need 3.11–3.14 (uv sync)")
        return sys.version.split()[0]

    def pandoc():
        import pypandoc
        return f"pandoc {pypandoc.get_pandoc_version()}"

    def node():
        if not shutil.which("node") or not (ROOT / "node_modules/@resvg/resvg-js").is_dir():
            raise RuntimeError("Node 22+ and project renderers are needed: npm ci")
        return "node_modules present"

    def libreoffice():
        from .preview import libreoffice_binary
        return str(libreoffice_binary())

    def fonts():
        from .preview import resolve_fonts
        profile = resolve_fonts(load_tokens())
        return {script: profile[script]["resolved"] for script in ("latin", "korean")}

    def browser():
        from .preview import chrome_binary
        found = chrome_binary()
        if not found:
            raise RuntimeError("No Chrome/Chromium for Mermaid; set PUPPETEER_EXECUTABLE_PATH or use figures instead")
        return found

    def template():
        tokens = load_tokens()
        if sha256(ROOT / tokens["source"]["path"]) != tokens["source"]["sha256"]:
            raise RuntimeError("Original template changed; restore templates/RVLAB_PPT양식.pptx from git")
        if not (ROOT / tokens["reference"]).is_file():
            raise RuntimeError("Reference missing: uv run python -m rvppt.template")
        return "original and reference present"

    def profile():
        if not (ROOT / "profile.yaml").is_file():
            raise RuntimeError("profile.yaml missing: cp profile.example.yaml profile.yaml (needed by rvppt new)")
        return "profile.yaml present"

    def skills():
        problems = skill_integrity()
        if problems:
            raise RuntimeError("; ".join(problems))
        return "all vendored files match skills/dependencies.yaml"

    for name, required, test in [("python", True, python), ("pandoc", True, pandoc), ("template", True, template),
                                 ("skills", True, skills), ("libreoffice", True, libreoffice), ("fonts", True, fonts),
                                 ("node_renderers", True, node), ("mermaid_browser", False, browser), ("profile", False, profile)]:
        check(name, required, test)
    return {"ok": all(c["status"] != "fail" for c in checks), "platform": sys.platform, "checks": checks}
