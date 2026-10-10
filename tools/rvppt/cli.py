"""RVLAB project creation, approval, production and QA commands."""

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
    parser = argparse.ArgumentParser(prog="rvppt", description=__doc__)
    subcommands = parser.add_subparsers(dest="command", required=True)
    create = subcommands.add_parser("new", help="Create tasks/<YYMMDD>-<slug>/ with slides.md filled from profile.yaml")
    create.add_argument("slug")
    create.add_argument("--title", required=True)
    create.add_argument("--subtitle", default="")
    create.add_argument("--date", help="Presentation date YYYY-MM-DD (default: today)")
    create.add_argument("--lang", choices=("ko", "en"), default="ko")
    query = subcommands.add_parser("status", help="Show the next stage, approval freshness, and open items (read-only)")
    query.add_argument("task")
    approval = subcommands.add_parser("approve", help="Record an explicit user's approval of the current stage")
    approval.add_argument("task")
    approval.add_argument("--stage", type=int, choices=(1, 2, 3, 4), required=True)
    approval.add_argument("--expected-hash", help="The status review_hash; reject if document or input files changed")
    polish = subcommands.add_parser("polish-check", help="Verify Korean polishing kept facts and Markdown structure of slides.md")
    polish.add_argument("task")
    polish.add_argument("--before", required=True, help="Copy of slides.md saved before polishing (e.g. TASK/.build/editorial/before.md)")
    subcommands.add_parser("doctor", help="Check tools, fonts, template and vendored skill hashes (offline, read-only)")
    graph = subcommands.add_parser("graph-check", help="Check the Graphify snapshot is fresh and excludes tasks/vendored sources")
    graph.add_argument("--record", action="store_true", help="Write graphify-out/snapshot.json after rebuilding the graph")
    for command in ("build", "lint", "preview"):
        subcommands.add_parser(command, help={"build": "Compile slides.md with render QA; outputs YYYYMMDD_title.pptx/.pdf beside it", "lint": "Check Markdown structure, limits and requested figures", "preview": "Show the current verified PDF/PNG preview"}[command]).add_argument("task")
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
        if args.command == "new":
            from .project import new_project
            print(json.dumps(new_project(args.slug, args.title, args.subtitle, args.date, args.lang), ensure_ascii=False, indent=2))
            return 0
        task = _task_path(args.task)
        if args.command == "status":
            result = status(task)
        elif args.command == "approve":
            result = approve(task, args.stage, args.expected_hash)
        elif args.command == "polish-check":
            from .polish import polish_check
            result = polish_check(task, args.before)
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
