"""Multi-preset presentation project creation, approval, production, anatomy figure and QA commands."""

import argparse
import json
from pathlib import Path
import sys

from .state import StateError, approve, status
from .template import ROOT


def _task_path(value):
    path = Path(value).resolve()
    if path.parent != (ROOT / "tasks").resolve():
        raise StateError("Use a task folder directly under this repository's tasks/")
    return path


def main(argv=None):
    parser = argparse.ArgumentParser(prog="pptgen", description=__doc__)
    subcommands = parser.add_subparsers(dest="command", required=True)
    create = subcommands.add_parser("new", help="Create tasks/<YYMMDD>-<slug>/ with slides.md filled from profile.yaml")
    create.add_argument("slug")
    create.add_argument("--title", required=True)
    create.add_argument("--subtitle", default="")
    create.add_argument("--date", help="Presentation date YYYY-MM-DD (default: today)")
    create.add_argument("--lang", choices=("ko", "en"), default="ko")
    create.add_argument("--preset", default=None, help="Template ID under templates/ (e.g. rvlab, modern-minimal, retro, neo-city)")
    create.add_argument("--budget", choices=("quick", "standard", "thorough"), default=None, help="Deck effort tier; tiers are defined in skills/ppt-interview/SKILL.md")
    subcommands.add_parser("presets", help="List available built-in and custom presentation design presets")
    reg = subcommands.add_parser("register-template", help="Register a custom .pptx template as a reusable preset")
    reg.add_argument("pptx", help="Path to the .pptx file to register")
    reg.add_argument("--id", required=True, dest="preset_id", help="Preset ID (lowercase letters, digits, hyphens)")
    reg.add_argument("--name", default=None, help="Display name for the registered preset")
    reg.add_argument("--description", default="", help="Optional description for the preset")
    query = subcommands.add_parser("status", help="Show the next stage, approval freshness, and open items (read-only)")
    query.add_argument("task")
    plan = subcommands.add_parser("plan", help="Refresh plan/contracts.md approval diagram; preserve plan/revisions.md and plan/PROGRESS.md")
    plan.add_argument("task")
    approval = subcommands.add_parser("approve", help="Record an explicit user's approval of the current stage")
    approval.add_argument("task")
    approval.add_argument("--stage", type=int, choices=(1, 2, 3, 4), required=True)
    approval.add_argument("--expected-hash", help="The status review_hash; reject if document or input files changed")
    polish = subcommands.add_parser("polish-check", help="Verify Korean polishing kept facts and Markdown structure of slides.md")
    polish.add_argument("task")
    polish.add_argument("--before", required=True, help="Copy of slides.md saved before polishing (e.g. TASK/.build/editorial/before.md)")
    paper = subcommands.add_parser("extract-paper", help="Extract a sources/ or figures/external/ PDF into Markdown and media under TASK/.build/editorial/papers/")
    paper.add_argument("task")
    paper.add_argument("pdf", help="Task-relative sources/<paper>.pdf or figures/external/<paper>.pdf; source and existing outputs are preserved")
    anat = subcommands.add_parser("anatomy", help="Build a standalone PNG, SVG, and interactive HTML figure in the deck's palette using the vendored anatomy engine; a script that also writes frame-*.svg gets a GIF")
    anat.add_argument("task")
    anat.add_argument("--name", required=True, help="Output figure stem under tasks/<task>/figures/<name>.png and .svg (and .gif for animated scripts)")
    anat.add_argument("--example", default=None, help="Built-in anatomy example name (e.g. dial-indicator, push-button, test-rig; see skills/anatomy/examples/)")
    anat.add_argument("--script", default=None, help="Path to a custom .mjs anatomy builder script; .mjs files beside it can be imported")
    anat.add_argument("--theme", choices=("light", "dark"), default=None, help="Color theme for standalone SVG/PNG rendering (default: follows the task preset's background)")
    anat.add_argument("--width", type=int, default=1800, help="PNG and GIF width in pixels (default: 1800; use about 1200 for a GIF)")
    anat.add_argument("--fps", type=float, default=12, help="GIF frames per second (default: 12)")
    anat.add_argument("--hold", type=float, default=1.0, help="Seconds the GIF rests on its last frame before looping (default: 1.0)")
    subcommands.add_parser("doctor", help="Check tools, fonts, template and vendored skill hashes (offline, read-only)")
    graph = subcommands.add_parser("graph-check", help="Check the Graphify snapshot is fresh and excludes tasks/vendored sources")
    graph.add_argument("--record", action="store_true", help="Write graphify-out/snapshot.json after rebuilding the graph")
    for command in ("build", "lint", "preview"):
        subcommands.add_parser(command, help={"build": "Compile slides.md with render QA; outputs YYYYMMDD_title.pptx/.pdf beside it", "lint": "Check Markdown structure, limits and requested figures", "preview": "Show the current verified PDF/PNG preview"}[command]).add_argument("task")
    aud = subcommands.add_parser("audit", help="Run 4x close-up crop critic audit and box clearance/contrast verification on built slides")
    aud.add_argument("task")
    aud.add_argument("--zoom", type=float, default=4.0, help="Zoom factor for close-up crops (default: 4.0)")
    args = parser.parse_args(argv)
    try:
        if args.command in ("doctor", "graph-check"):
            if args.command == "doctor":
                from .doctor import doctor
                result = doctor()
            else:
                from .graph import graph_check
                result = graph_check(record=args.record)
            print(json.dumps(result, ensure_ascii=False, indent=2))
            return 0 if result["ok"] else 2
        if args.command == "presets":
            from .template import list_presets
            print(json.dumps({"presets": list_presets()}, ensure_ascii=False, indent=2))
            return 0
        if args.command == "register-template":
            from .template import register_template
            result = register_template(args.pptx, args.preset_id, name=args.name, description=args.description)
            print(json.dumps(result, ensure_ascii=False, indent=2))
            return 0
        if args.command == "new":
            from .project import new_project
            print(json.dumps(new_project(args.slug, args.title, args.subtitle, args.date, args.lang,
                                         preset=args.preset, budget=args.budget), ensure_ascii=False, indent=2))
            return 0
        task = _task_path(args.task)
        if args.command == "status":
            result = status(task)
        elif args.command == "plan":
            from .plan import write_plan
            result = write_plan(task)
        elif args.command == "approve":
            result = approve(task, args.stage, args.expected_hash)
        elif args.command == "extract-paper":
            from .papers import extract_paper
            result = extract_paper(task, args.pdf)
        elif args.command == "anatomy":
            from .anatomy_bridge import build_anatomy_figure
            result = build_anatomy_figure(task, args.name, example=args.example, script=args.script, theme=args.theme,
                                          width=args.width, fps=args.fps, hold=args.hold)
        elif args.command == "polish-check":
            from .polish import polish_check
            result = polish_check(task, args.before)
            if not result["ok"]:
                print(json.dumps(result, ensure_ascii=False, indent=2))
                return 2
        elif args.command == "audit":
            from . import build
            result = build.audit(task, zoom=args.zoom)
            if not result["ok"]:
                print(json.dumps(result, ensure_ascii=False, indent=2))
                return 2
        else:
            from . import build
            result = getattr(build, args.command)(task)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (ValueError, OSError, RuntimeError) as error:
        print(f"rvppt: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
