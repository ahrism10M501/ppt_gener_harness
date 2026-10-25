"""Bridge between vendored skills/anatomy isometric figures and presentation tasks."""

from pathlib import Path
import re
import shutil
import subprocess

from PIL import Image, ImageChops

from .build import node_render
from .markdown import animation_metadata
from .preview import resolve_fonts
from .state import StateError
from .template import ROOT, load_tokens, palette_roles, task_preset

ANATOMY_ROOT = ROOT / "skills/anatomy"
# Share of the paper color in each tone (0 = ink, 1 = paper). Light shades darken the paper;
# dark shades stay close to it, so a dark card keeps the vendored look.
TONES = {
    "light": {"top": 1, "face": 1, "shade": (.76, .83, .89, .94), "mid": .45, "lo": .68, "faint": .84, "dot": .15,
              "lit_top": .88, "lit_shade": .76, "halo": 0, "weight": "1px"},
    "dark": {"top": .90, "face": .93, "shade": (.965, .95, .935, .92), "mid": .55, "lo": .75, "faint": .88, "dot": .1,
             "lit_top": .62, "lit_shade": .78, "halo": 0, "weight": "1px"},
}
# The preset has no role for these; they only mark red/green series, which decks rarely use.
SIGNALS = {"light": ("#e5484d", "#30a46c"), "dark": ("#ff6b6b", "#6be0a0")}


def _channels(color):
    return [int(color[i:i + 2], 16) for i in (1, 3, 5)]


def _mix(ink, paper, share):
    """`share` of paper blended into ink, as #rrggbb."""
    return "#" + "".join(f"{round(a * (1 - share) + b * share):02x}" for a, b in zip(_channels(ink), _channels(paper)))


def theme_variables(tokens, theme):
    """The anatomy palette for a deck: the preset's paper, ink and accent, so figures match their slides."""
    roles = palette_roles(tokens)
    dark = theme == "dark"
    paper, ink = roles["background"].lower(), roles["ink"].lower()
    if (sum(_channels(paper)) < 384) != dark:
        # --theme against the preset: keep its accent, take a neutral paper and ink.
        paper, ink = ("#0b0b0b", "#e6e6e6") if dark else ("#ffffff", "#18181a")
    accent = roles["accent"].lower()
    tone = TONES[theme]
    red, green = SIGNALS[theme]
    shade = [_mix(ink, paper, s) for s in tone["shade"]]
    return {
        "--anatomy-page": paper, "--anatomy-card": paper, "--anatomy-paper": paper,
        "--anatomy-text": _mix(ink, paper, .3), "--anatomy-strong": ink, "--anatomy-muted": _mix(ink, paper, .5),
        "--anatomy-face": _mix(ink, paper, tone["face"]), "--anatomy-top": _mix(ink, paper, tone["top"]),
        **{f"--anatomy-shade-{i}": value for i, value in enumerate(shade)},
        "--anatomy-lit-top": _mix(accent, paper, tone["lit_top"]), "--anatomy-lit-shade": _mix(accent, paper, tone["lit_shade"]),
        "--anatomy-hi": ink, "--anatomy-mid": _mix(ink, paper, tone["mid"]), "--anatomy-lo": _mix(ink, paper, tone["lo"]),
        "--anatomy-faint": _mix(ink, paper, tone["faint"]), "--anatomy-lit": accent,
        "--anatomy-halo": _mix(ink, paper, .5), "--anatomy-halo-opacity": str(tone["halo"]),
        "--anatomy-dot": _mix(ink, paper, tone["dot"]),
        "--anatomy-red": red, "--anatomy-green": green, "--anatomy-blue": accent,
        "--anatomy-weight": tone["weight"], "--anatomy-mono": "Liberation Mono, monospace",
    }


def _resolve_vars(text, variables):
    for key, value in sorted(variables.items(), key=lambda item: -len(item[0])):
        text = text.replace(f"var({key})", value)
    return text


def _resolved_svg_css(variables):
    css = (ANATOMY_ROOT / "kit/iso.css").read_text(encoding="utf-8")
    # Remove the .iso and .iso[data-theme="light"] variable blocks and @keyframes/@media
    css = re.sub(r"\.iso(?:\[data-theme=\"light\"\])?\{[^}]*\}", "", css, flags=re.S)
    css = re.sub(r"@keyframes\s+[\w-]+\{(?:[^{}]*\{[^{}]*\})*[^{}]*\}", "", css, flags=re.S)
    css = re.sub(r"@media\s+[^{]+\{(?:[^{}]*\{[^{}]*\})*[^{}]*\}", "", css, flags=re.S)
    # Remove filter:blur(...) since resvg/strict SVG validators may reject CSS filter functions
    return re.sub(r"filter:blur\([^)]+\);?", "", css).strip()


def standalone_svg(html_text, variables):
    match = re.search(r"(<svg\b[^>]*class=\"iso-svg\"[^>]*>)(.*?)(</svg>)", html_text, flags=re.S)
    if not match:
        raise StateError("No <svg class=\"iso-svg\"> found in generated anatomy HTML")
    open_tag, inner, close_tag = match.groups()
    if "xmlns=" not in open_tag:
        open_tag = open_tag[:-1] + ' xmlns="http://www.w3.org/2000/svg">'
    vb_match = re.search(r'viewBox="([^"]+)"', open_tag)
    bg_rect = ""
    if vb_match:
        parts = vb_match.group(1).split()
        if len(parts) == 4:
            bg_rect = f'<rect x="{parts[0]}" y="{parts[1]}" width="{parts[2]}" height="{parts[3]}" fill="{variables["--anatomy-card"]}"/>'
    # Strip inline style="filter:blur(...)" for strict SVG compatibility
    inner = re.sub(r'\s*style="filter:blur\([^"]*\)"', "", inner)
    return _resolve_vars(f"{open_tag}<style>{_resolved_svg_css(variables)}</style>{bg_rect}{inner}{close_tag}\n", variables)


def _localized(path):
    """Builder source with the kit paths pointed at the vendored anatomy folder."""
    text = Path(path).read_text(encoding="utf-8")
    text = text.replace("../../kit/", (ANATOMY_ROOT / "kit").as_posix() + "/")
    return text.replace("../../scripts/", (ANATOMY_ROOT / "scripts").as_posix() + "/")


def _gif(frames, out, variables, *, width, font, fps, hold):
    """Render frame SVGs with the deck palette into one looping GIF that holds on its last frame."""
    shots = []
    for index, source in enumerate(frames):
        svg = source.with_name(f"deck-{source.stem}.svg")
        svg.write_text(standalone_svg(source.read_text(encoding="utf-8"), variables), encoding="utf-8", newline="\n")
        png = svg.with_suffix(".png")
        node_render({"mode": "svg", "input": str(svg), "output": str(png), "width": width, "font": font})
        with Image.open(png) as image:
            shots.append(image.convert("RGB"))
    if len({shot.size for shot in shots}) != 1:
        raise StateError("Anatomy frames render at different sizes; keep one width, height and viewBox")
    # One palette for every frame, so smooth shading does not flicker between frames.
    sample = shots[::max(1, len(shots) // 8)]
    sheet = Image.new("RGB", (shots[0].width, shots[0].height * len(sample)))
    for row, shot in enumerate(sample):
        sheet.paste(shot, (0, row * shot.height))
    palette = sheet.quantize(colors=255, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
    # Median cut drops pure white and the nearest-color search ignores a spare slot, so pin the paper
    # color in slot 255 and paint the exact-paper pixels with it: no faint box on the slide.
    entries = (palette.getpalette() or [])[:765]
    paper = tuple(int(variables["--anatomy-paper"][i:i + 2], 16) for i in (1, 3, 5))
    palette.putpalette(entries + [0] * (765 - len(entries)) + list(paper))
    blank = Image.new("RGB", shots[0].size, paper)
    quantized = []
    for shot in shots:
        frame = shot.quantize(palette=palette, dither=Image.Dither.NONE)
        frame.paste(255, mask=ImageChops.difference(shot, blank).convert("L").point(lambda v: 255 if v == 0 else 0))
        quantized.append(frame)
    step = max(20, round(1000 / fps / 10) * 10)  # GIF delays are whole centiseconds
    durations = [step] * (len(shots) - 1) + [step + round(hold * 1000)]
    quantized[0].save(out, save_all=True, append_images=quantized[1:], duration=durations, loop=0, optimize=False)
    return shots[0].size


def build_anatomy_figure(task, name, *, example=None, script=None, theme=None, width=1800, fps=12, hold=1.0):
    """Build an isometric figure using skills/anatomy into task/figures/<name>.svg and .png.

    A script that also writes frame-*.svg (each a figureSvg, zero-padded so they sort in order) gets a
    looping figures/<name>.gif; the figure's own html is then the poster PNG, so it should show the state
    worth keeping when the GIF does not play. Other .mjs files beside --script are copied so it can import them.
    """
    task = Path(task)
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{0,60}", name):
        raise StateError("Figure name must be alphanumeric with hyphens/underscores")
    tokens = load_tokens(preset=task_preset(task))
    if theme is None:
        # Match the deck: a white card on a dark preset reads as a hole in the slide.
        background = tokens["palette"]["background"].lstrip("#")
        theme = "dark" if sum(int(background[i:i + 2], 16) for i in (0, 2, 4)) < 384 else "light"
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
                (workspace / item.name).write_text(_localized(item), encoding="utf-8")
        entry = workspace / "build.mjs"
    elif script:
        script_path = Path(script)
        if not script_path.is_absolute():
            script_path = task / script_path
        if not script_path.is_file():
            raise StateError(f"Anatomy build script not found: {script}")
        for item in {script_path, *script_path.parent.glob("*.mjs")}:
            (workspace / item.name).write_text(_localized(item), encoding="utf-8")
        entry = workspace / script_path.name
    else:
        raise StateError("Specify either --example <name> or --script <path>")

    cmd = ["node", str(entry)]
    if theme == "light":
        cmd.append("--light")
    result = subprocess.run(cmd, cwd=workspace, capture_output=True, text=True, timeout=300)
    if result.returncode != 0:
        raise StateError(f"Anatomy build failed: {result.stderr or result.stdout}")

    html_files = sorted(workspace.glob("*.html"))
    if not html_files:
        raise StateError("Anatomy build script did not produce an .html file")
    html_path = html_files[0]
    variables = theme_variables(tokens, theme)
    svg_text = standalone_svg(html_path.read_text(encoding="utf-8"), variables)

    figures_dir = task / "figures"
    figures_dir.mkdir(exist_ok=True)
    svg_out = figures_dir / f"{name}.svg"
    png_out = figures_dir / f"{name}.png"
    svg_out.write_text(svg_text, encoding="utf-8", newline="\n")

    font = resolve_fonts(tokens)["korean"]["resolved"]
    node_render({"mode": "svg", "input": str(svg_out), "output": str(png_out), "width": int(width), "font": font})

    report = {
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
    frames = sorted(workspace.glob("frame-*.svg"))
    if frames:
        if len(frames) < 2:
            raise StateError("An animated figure needs at least two frame-*.svg files")
        gif_out = figures_dir / f"{name}.gif"
        _gif(frames, gif_out, variables, width=int(width), font=font, fps=fps, hold=hold)
        report.update(gif=str(gif_out), animation=animation_metadata(task, gif_out))
    return report
