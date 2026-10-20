"""Bridge between vendored skills/anatomy isometric figures and presentation tasks."""

from pathlib import Path
import re
import shutil
import subprocess

from .build import node_render
from .preview import resolve_fonts
from .state import StateError
from .template import ROOT, load_tokens

ANATOMY_ROOT = ROOT / "skills/anatomy"
THEMES = {
    "light": {
        "--anatomy-page": "#f2f2ef",
        "--anatomy-card": "#fbfbfa",
        "--anatomy-text": "#57575a",
        "--anatomy-strong": "#18181a",
        "--anatomy-muted": "#8c8c90",
        "--anatomy-paper": "#fbfbfa",
        "--anatomy-face": "#ffffff",
        "--anatomy-top": "#ffffff",
        "--anatomy-shade-0": "#dcdcd9",
        "--anatomy-shade-1": "#e5e5e2",
        "--anatomy-shade-2": "#ededea",
        "--anatomy-shade-3": "#f4f4f1",
        "--anatomy-lit-top": "#ffffff",
        "--anatomy-lit-shade": "#eeeeeb",
        "--anatomy-hi": "#26262a",
        "--anatomy-mid": "#8a8a8f",
        "--anatomy-lo": "#b4b4b8",
        "--anatomy-faint": "#d4d4d6",
        "--anatomy-lit": "#000000",
        "--anatomy-halo": "#8a8a80",
        "--anatomy-halo-opacity": ".32",
        "--anatomy-dot": "#3a3a3e",
        "--anatomy-red": "#e5484d",
        "--anatomy-green": "#30a46c",
        "--anatomy-blue": "#3e63dd",
        "--anatomy-weight": ".6px",
        "--anatomy-mono": "Liberation Mono, monospace",
    },
    "dark": {
        "--anatomy-page": "#0b0b0b",
        "--anatomy-card": "#131313",
        "--anatomy-text": "#a3a3a3",
        "--anatomy-strong": "#e6e6e6",
        "--anatomy-muted": "#6e6e6e",
        "--anatomy-paper": "#131313",
        "--anatomy-face": "#1b1b1b",
        "--anatomy-top": "#1c1c1c",
        "--anatomy-shade-0": "#0f0f0f",
        "--anatomy-shade-1": "#121212",
        "--anatomy-shade-2": "#151515",
        "--anatomy-shade-3": "#181818",
        "--anatomy-lit-top": "#262626",
        "--anatomy-lit-shade": "#1d1d1d",
        "--anatomy-hi": "#d4d4d4",
        "--anatomy-mid": "#6a6a6a",
        "--anatomy-lo": "#3e3e3e",
        "--anatomy-faint": "#2a2a2a",
        "--anatomy-lit": "#ffffff",
        "--anatomy-halo": "#050505",
        "--anatomy-halo-opacity": ".9",
        "--anatomy-dot": "#e6e6e6",
        "--anatomy-red": "#ff6b6b",
        "--anatomy-green": "#6be0a0",
        "--anatomy-blue": "#6b9bff",
        "--anatomy-weight": ".6px",
        "--anatomy-mono": "Liberation Mono, monospace",
    },
}


def _resolved_svg_css(theme="light"):
    variables = THEMES.get(theme, THEMES["light"])
    css = (ANATOMY_ROOT / "kit/iso.css").read_text(encoding="utf-8")
    # Remove the .iso and .iso[data-theme="light"] variable blocks and @keyframes/@media
    css = re.sub(r"\.iso(?:\[data-theme=\"light\"\])?\{[^}]*\}", "", css, flags=re.S)
    css = re.sub(r"@keyframes\s+[\w-]+\{(?:[^{}]*\{[^{}]*\})*[^{}]*\}", "", css, flags=re.S)
    css = re.sub(r"@media\s+[^{]+\{(?:[^{}]*\{[^{}]*\})*[^{}]*\}", "", css, flags=re.S)
    # Remove filter:blur(...) since resvg/strict SVG validators may reject CSS filter functions
    css = re.sub(r"filter:blur\([^)]+\);?", "", css)
    for key, val in sorted(variables.items(), key=lambda kv: -len(kv[0])):
        css = css.replace(f"var({key})", val)
    return css.strip(), variables


def standalone_svg(html_text, theme="light"):
    match = re.search(r"(<svg\b[^>]*class=\"iso-svg\"[^>]*>)(.*?)(</svg>)", html_text, flags=re.S)
    if not match:
        raise StateError("No <svg class=\"iso-svg\"> found in generated anatomy HTML")
    open_tag, inner, close_tag = match.groups()
    if "xmlns=" not in open_tag:
        open_tag = open_tag[:-1] + ' xmlns="http://www.w3.org/2000/svg">'
    vb_match = re.search(r'viewBox="([^"]+)"', open_tag)
    bg_rect = ""
    css, variables = _resolved_svg_css(theme)
    if vb_match:
        parts = vb_match.group(1).split()
        if len(parts) == 4:
            bg_rect = f'<rect x="{parts[0]}" y="{parts[1]}" width="{parts[2]}" height="{parts[3]}" fill="{variables["--anatomy-card"]}"/>'
    # Strip inline style="filter:blur(...)" for strict SVG compatibility
    inner = re.sub(r'\s*style="filter:blur\([^"]*\)"', "", inner)
    return f"{open_tag}<style>{css}</style>{bg_rect}{inner}{close_tag}\n"


def build_anatomy_figure(task, name, *, example=None, script=None, theme="light", width=1800):
    """Build an isometric figure using skills/anatomy into task/figures/<name>.svg and .png."""
    task = Path(task)
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{0,60}", name):
        raise StateError("Figure name must be alphanumeric with hyphens/underscores")
    if theme not in ("light", "dark"):
        raise StateError("Theme must be 'light' or 'dark'")
    workspace = task / ".build/editorial/anatomy" / name
    if workspace.exists():
        shutil.rmtree(workspace)
    workspace.mkdir(parents=True, exist_ok=True)

    if example:
        example_dir = ANATOMY_ROOT / "examples" / example
        if not example_dir.is_dir() or not (example_dir / "build.mjs").is_file():
            available = sorted(p.name for p in (ANATOMY_ROOT / "examples").iterdir() if (p / "build.mjs").is_file())
            raise StateError(f"Unknown anatomy example '{example}'; available: {', '.join(available)}")
        for item in example_dir.iterdir():
            if item.is_file():
                text = item.read_text(encoding="utf-8")
                text = text.replace("../../kit/", (ANATOMY_ROOT / "kit").as_posix() + "/")
                text = text.replace("../../scripts/", (ANATOMY_ROOT / "scripts").as_posix() + "/")
                (workspace / item.name).write_text(text, encoding="utf-8")
        entry = workspace / "build.mjs"
    elif script:
        script_path = Path(script)
        if not script_path.is_absolute():
            script_path = task / script_path
        if not script_path.is_file():
            raise StateError(f"Anatomy build script not found: {script}")
        text = script_path.read_text(encoding="utf-8")
        text = text.replace("../../kit/", (ANATOMY_ROOT / "kit").as_posix() + "/")
        text = text.replace("../../scripts/", (ANATOMY_ROOT / "scripts").as_posix() + "/")
        entry = workspace / "build.mjs"
        entry.write_text(text, encoding="utf-8")
    else:
        raise StateError("Specify either --example <name> or --script <path>")

    cmd = ["node", str(entry)]
    if theme == "light":
        cmd.append("--light")
    result = subprocess.run(cmd, cwd=workspace, capture_output=True, text=True, timeout=120)
    if result.returncode != 0:
        raise StateError(f"Anatomy build failed: {result.stderr or result.stdout}")

    html_files = sorted(workspace.glob("*.html"))
    if not html_files:
        raise StateError("Anatomy build script did not produce an .html file")
    html_path = html_files[0]
    svg_text = standalone_svg(html_path.read_text(encoding="utf-8"), theme=theme)

    figures_dir = task / "figures"
    figures_dir.mkdir(exist_ok=True)
    svg_out = figures_dir / f"{name}.svg"
    png_out = figures_dir / f"{name}.png"
    svg_out.write_text(svg_text, encoding="utf-8", newline="\n")

    tokens = load_tokens()
    profile = resolve_fonts(tokens)
    node_render({"mode": "svg", "input": str(svg_out), "output": str(png_out), "width": int(width), "font": profile["korean"]["resolved"]})

    return {
        "ok": True,
        "task_id": task.name,
        "figure": name,
        "theme": theme,
        "svg": str(svg_out),
        "png": str(png_out),
        "html": str(html_path),
        "interactive_html": str(html_path.relative_to(task)),
        "width_px": int(width),
    }
