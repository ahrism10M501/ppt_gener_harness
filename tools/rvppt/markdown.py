"""Pandoc AST validation at the task input boundary."""

from datetime import date
import json
from pathlib import Path
import re
import subprocess

import pypandoc
from PIL import Image

from .project import BUDGET_TIERS
from .state import StateError, read_document
from .template import load_tokens


def pandoc(arguments, data):
    try:
        result = subprocess.run([pypandoc.get_pandoc_path(), *arguments], input=data,
                                text=True, encoding="utf-8", capture_output=True, timeout=120)
    except (OSError, subprocess.TimeoutExpired) as error:
        raise StateError(f"Pandoc failed: {error}") from error
    if result.returncode:
        raise StateError(f"Pandoc failed: {result.stderr.strip()}")
    return result.stdout


def nodes(value):
    if isinstance(value, dict):
        if "t" in value:
            yield value
        yield from nodes(value.get("c", []))
    elif isinstance(value, list):
        for item in value:
            yield from nodes(item)


def plain(value):
    if isinstance(value, list):
        return "".join(plain(item) for item in value)
    if not isinstance(value, dict) or "t" not in value:
        return ""
    kind, content = value["t"], value.get("c")
    if kind == "Str":
        return content
    if kind in ("Space", "SoftBreak"):
        return " "
    if kind == "LineBreak":
        return "\n"
    if kind in ("Math", "Code", "CodeBlock"):
        return content[-1]
    if kind in ("Image", "Link", "Span", "Header"):
        return plain(content[-2] if kind in ("Image", "Link") else content[-1])
    if kind == "Div":
        return plain(content[1])
    if kind == "Cite":
        return plain(content[1])
    if kind == "Quoted":
        opening, closing = ("“", "”") if content[0]["t"] == "DoubleQuote" else ("‘", "’")
        return opening + plain(content[1]) + closing
    if kind in ("Para", "Plain"):
        return plain(content) + "\n"
    return plain(content)


def asset_path(task, value):
    path = Path(value)
    if path.is_absolute() or not path.parts or path.parts[0] not in ("figures", "sources") or ".." in path.parts:
        raise StateError(f"Image must be a task-local figures/ or sources/ path: {value}")
    if path.suffix.lower() not in (".png", ".jpg", ".jpeg", ".svg", ".pdf", ".gif"):
        raise StateError(f"Unsupported image type: {value}")
    current = task
    for part in path.parts:
        current = current / part
        if current.is_symlink():
            raise StateError(f"Image symlinks are forbidden: {value}")
    if path.parts[0] == "figures" and not current.exists():
        return current  # A requested figure: the build draws a labeled placeholder box.
    if not current.is_file() or not current.resolve().is_relative_to(task.resolve()):
        raise StateError(f"Missing task image: {value}")
    return current


def animation_metadata(task, source):
    """A GIF stays animated in PPTX; its matching PNG is the explicit static poster."""
    poster = asset_path(task, str(source.relative_to(task).with_suffix(".png")))
    if not poster.is_file():
        raise StateError(f"Animated GIF requires a matching PNG poster: {poster.relative_to(task)}")
    if source.stat().st_size > 64 * 1024 * 1024:
        raise StateError("Animated GIF exceeds 64 MiB; reduce its resolution or frame rate")
    try:
        with Image.open(source) as animation:
            frames = getattr(animation, "n_frames", 1)
            if animation.format != "GIF" or frames < 2:
                raise StateError("GIF must contain at least two animation frames")
            if frames > 600 or animation.width * animation.height * frames > 300_000_000:
                raise StateError("Animated GIF exceeds 600 frames or 300 million decoded pixels")
            size, loop, duration = animation.size, animation.info.get("loop"), 0
            for index in range(frames):
                animation.seek(index)
                animation.load()
                frame_duration = animation.info.get("duration", 0)
                if not isinstance(frame_duration, int) or frame_duration <= 0:
                    raise StateError(f"GIF frame {index + 1} requires a positive duration")
                duration += frame_duration
        with Image.open(poster) as picture:
            if picture.format != "PNG" or picture.size != size:
                raise StateError("GIF and PNG poster must have identical pixel dimensions")
            picture.load()
    except StateError:
        raise
    except (OSError, ValueError, EOFError, Image.DecompressionBombError) as error:
        raise StateError(f"Invalid GIF or PNG poster: {source.relative_to(task)}: {error}") from error
    return {"path": str(source.relative_to(task)), "poster": str(poster.relative_to(task)),
            "frame_count": frames, "duration_ms": duration, "size_px": list(size), "loop_count": loop}


def table_rows(block):
    _, _, specs, head, bodies, foot = block["c"]
    rows = list(head[1])
    for body in bodies:
        rows.extend(body[2]); rows.extend(body[3])
    rows.extend(foot[1])
    if any(len(row[1]) != len(specs) or any(cell[2:4] != [1, 1] for cell in row[1]) for row in rows):
        raise StateError("Merged or irregular table cells are not supported")
    return [[plain(cell[4]).strip() for cell in row[1]] for row in rows]


def image_node(block):
    images = [n for n in nodes(block) if n["t"] == "Image"]
    if len(images) == 1 and block["t"] in ("Figure", "Para", "Plain"):
        # Only standalone images get a fixed figure slot.
        inline = block["c"][2] if block["t"] == "Figure" else [block]
        if plain(inline).strip() == plain(images[0]).strip():
            return images[0]
    return None


def bullet_items(block, depth=1):
    if block["t"] not in ("BulletList", "OrderedList"):
        return []
    items = block["c"] if block["t"] == "BulletList" else block["c"][1]
    result = []
    for item in items:
        result.append((depth, plain([b for b in item if b["t"] not in ("BulletList", "OrderedList")]).strip()))
        for child in item:
            result.extend(bullet_items(child, depth + 1))
    return result


def validate_blocks(blocks, task, tokens):
    """Reject what cannot be rendered or is unsafe; return advisory warnings for the rest."""
    warnings = []
    allowed = {"Para", "Plain", "BulletList", "OrderedList", "Table", "Figure", "CodeBlock"}
    for block in blocks:
        if block["t"] not in allowed:
            raise StateError(f"Unsupported content block: {block['t']}")
        for node in nodes(block):
            kind, content = node["t"], node.get("c")
            if kind in ("RawBlock", "RawInline", "Note", "Div", "Header"):
                raise StateError(f"Unsupported nested content: {kind}")
            if kind in ("Image", "Link", "Span", "Table", "Figure", "Code", "CodeBlock"):
                attr = content[0]
                classes = attr[1]
                permitted = ["mermaid"] if kind == "CodeBlock" and classes == ["mermaid"] else classes if kind == "CodeBlock" and len(classes) <= 1 and all(re.fullmatch(r"[\w+-]+", c) for c in classes) else []
                if attr[0] or attr[2] or classes != permitted:
                    raise StateError("Coordinates, styles and arbitrary attributes are forbidden")
            if kind == "Image":
                source = asset_path(task, content[2][0])
                if source.suffix.lower() == ".gif" and source.is_file():
                    animation_metadata(task, source)
                if any(n["t"] == "Math" for n in nodes(content[1])):
                    raise StateError("Figure captions use text; put equations in the slide body")
            if kind == "Math" and re.search(r"\\(?:class|cssId|style|href|html\w*|def|newcommand|require|includegraphics)\b", content[1]):
                raise StateError("LaTeX definitions, HTML hooks and external macros are not supported")
            if kind == "Link" and not re.match(r"^(https?://|mailto:|#)", content[2][0]):
                raise StateError("Links must use HTTPS/HTTP, mailto or a slide anchor")
            if kind == "Table":
                rows = table_rows(node)
                if not rows:
                    raise StateError("Table has no rows")
                if len(rows) > tokens["limits"]["table_rows_with_header"] or len(rows[0]) > tokens["limits"]["table_columns"]:
                    # Build measures the real table height and stops on overflow.
                    warnings.append(f"Large table ({len(rows)}x{len(rows[0])}; guide {tokens['limits']['table_rows_with_header']}x{tokens['limits']['table_columns']}) may need splitting")
                if any(n["t"] in ("Math", "Image", "CodeBlock", "BulletList", "OrderedList") for n in nodes(node)):
                    raise StateError("Table cells support plain text and emphasis only")
        if any(n["t"] == "Image" for n in nodes(block)) and image_node(block) is None:
            raise StateError("Images must be standalone with a caption")
    return warnings


def units(value):
    """Top-bar width budget: Hangul/CJK count 2, everything else 1."""
    return sum(2 if re.match(r"[가-힣一-龥]", c) else 1 for c in value)


def deck_info(metadata):
    deck = metadata.get("deck")
    # Unknown deck keys are kept for the agent's own notes; only known ones are rendered.
    if not isinstance(deck, dict) or not all(isinstance(deck.get(k), str) and deck[k].strip() for k in ("title", "date", "presenter")):
        raise StateError("slides.md needs deck.title, deck.presenter and a quoted deck.date; create projects with pptgen new")
    try:
        # Python also accepts 20261012; normalise so labels and file names stay YYYY-MM-DD based.
        deck = dict(deck, date=date.fromisoformat(deck["date"]).isoformat())
    except ValueError as error:
        raise StateError("deck.date must be a quoted 'YYYY-MM-DD'") from error
    affiliation = deck.get("affiliation", [])
    affiliation = [affiliation] if isinstance(affiliation, str) else affiliation
    if not isinstance(affiliation, list) or len(affiliation) > 2 or not all(isinstance(a, str) for a in affiliation):
        raise StateError("deck.affiliation allows up to two lines")
    subtitle = deck.get("subtitle") or ""
    if not isinstance(subtitle, str):
        raise StateError("deck.subtitle must be text")
    preset = deck.get("preset") or "rvlab"
    if not isinstance(preset, str) or not preset.strip():
        raise StateError("deck.preset must be a non-empty string")
    budget = deck.get("budget")
    if budget is not None and budget not in BUDGET_TIERS:
        raise StateError(f"deck.budget must be one of {', '.join(BUDGET_TIERS)}")
    result = dict(deck, subtitle=subtitle, affiliation=affiliation, preset=preset.strip())
    if budget is not None:
        result["budget"] = budget
    return result


def is_figure(block):
    return image_node(block) is not None or (block["t"] == "CodeBlock" and block["c"][0][1] == ["mermaid"])


APPENDIX = {"Appendix", "부록"}
# '### text {.kind}' slides break the headline-and-bullets rhythm; each takes short paragraphs only.
SLIDE_KINDS = {"statement", "number", "quote"}


def parse_task(task):
    """Return the full deck: generated cover/TOC/closing around # section, ## topic, ### headline slides."""
    document = read_document(task / "slides.md", task.name, 4)
    deck = deck_info(document.metadata)
    try:
        tokens = load_tokens(preset=deck.get("preset"))
    except ValueError as error:
        raise StateError(str(error)) from error
    review = document.metadata.get("review")
    language = review.get("language", "ko") if isinstance(review, dict) else "ko"
    if language not in tokens["labels"]:
        raise StateError("review.language must be ko or en")
    labels, limits = tokens["labels"][language], tokens["limits"]
    # Exact punctuation must survive rather than Pandoc's smart quote conversion.
    ast = json.loads(pandoc(["-f", "markdown-smart", "-t", "json"], document.body))
    body, section, topic, current = [], None, None, None
    for block in ast["blocks"]:
        if block["t"] == "RawBlock" and block["c"][1].lstrip().startswith("<!--"):
            continue  # Author comments, like LaTeX %.
        if block["t"] == "Header":
            level, attr, inlines = block["c"]
            kinds = attr[1]
            if attr[2] or (kinds and (level != 3 or len(kinds) != 1 or kinds[0] not in SLIDE_KINDS)):
                raise StateError(f"Only '### headline {{.kind}}' with one of {sorted(SLIDE_KINDS)} is supported on headings")
            text = plain(inlines).strip()
            current = None
            if level == 1:
                title, _, subtitle = (part.strip() for part in text.partition(" | "))
                section = {"layout": "section", "id": title, "title": title, "subtitle": subtitle, "topics": [], "notes": []}
                body.append(section); topic = None
            elif level == 2:
                topic = text
            elif level == 3:
                # Without '## topic' the top bar repeats the section (or deck) title.
                topic = topic or (section and section["title"]) or deck["title"]
                current = {"layout": "content", "id": f"S{sum(s['layout'] != 'section' for s in body) + 1:02}", "section": section and section["title"], "topic": topic, "headline": text, "blocks": [], "notes": [], "source": [], "warnings": []}
                if kinds:
                    current["kind"] = kinds[0]
                # Length limits are advice; build measures and render-checks the real two-line fit.
                if len(text) > limits["headline_korean_chars" if re.search(r"[가-힣]", text) else "headline_latin_chars"]:
                    current["warnings"].append(f"Headline may exceed two lines; build checks the real fit: {text}")
                if units(topic) > limits["topic_units"]:
                    current["warnings"].append(f"Top-bar topic is long (Hangul 2, others 1; guide {limits['topic_units']}): {topic}")
                body.append(current)
                if section and topic not in section["topics"]:
                    section["topics"].append(topic)
            else:
                raise StateError("Use # section, ## topic and ### headline; deeper headings are not supported")
        elif current is not None:
            current["blocks"].append(block)
        elif block["t"] == "Div" and block["c"][0][1] == ["notes"] and body and body[-1] is section:
            section["notes"].extend(block["c"][1])
        else:
            raise StateError("Slide content must follow a '### headline' (sections allow only ::: notes)")
    if not any(s["layout"] == "content" for s in body):
        raise StateError("slides.md has no slides; add '## topic' and '### headline'")
    for slide in body:
        if slide["layout"] == "content":
            build_slots(slide, task, tokens)
    chapters = [s for s in body if s["layout"] == "section" and s["title"] not in APPENDIX]
    # A topic that repeats its chapter name (e.g. "GS-ICP SLAM" under "GS-ICP SLAM") adds nothing to the contents.
    toc = [(f"{labels['chapter']} {i}: {c['title']}", [t for t in c["topics"] if t != c["title"]]) for i, c in enumerate(chapters, 1)]
    if sum(1 + len(topics) for _, topics in toc) > limits["toc_lines"]:
        toc = [(chapter, []) for chapter, _ in toc]  # ponytail: drop topics instead of measuring; split chapters if even this overflows.
    appendix = next((i for i, s in enumerate(body) if s["layout"] == "section" and s["title"] in APPENDIX), len(body))
    cover = {"layout": "cover", "id": "cover", "notes": [], **deck, "date_label": labels["date"] + deck["date"].replace("-", ".")}
    closing = {"layout": "closing", "id": "closing", "title": labels["closing"], "notes": []}
    contents = [{"layout": "toc", "id": "toc", "chapters": toc, "notes": []}] if len(chapters) >= 2 else []
    return ast["pandoc-api-version"], [cover, *contents, *body[:appendix], closing, *body[appendix:]], tokens


def build_slots(slide, task, tokens):
    content, columns = [], None
    for block in slide.pop("blocks"):
        if block["t"] == "Div":
            attr, children = block["c"]
            if attr[0] or attr[2] or len(attr[1]) != 1 or attr[1][0] not in ("notes", "source", "columns"):
                raise StateError("Allowed blocks: notes, source, columns with exactly two column blocks")
            role = attr[1][0]
            if role == "columns":
                if columns is not None or len(children) != 2 or any(c["t"] != "Div" or c["c"][0] != ["", ["column"], []] for c in children):
                    raise StateError("Exactly two ::: column blocks are required")
                columns = [c["c"][1] for c in children]
            else:
                slide["warnings"] += validate_blocks(children, task, tokens)
                if any(n["t"] in ("Image", "Table", "CodeBlock") for n in nodes(children)):
                    raise StateError(f"{role} supports text, lists and LaTeX only")
                slide[role].extend(children)
        else:
            content.append(block)
    if slide.get("kind"):
        if columns is not None or any(b["t"] not in ("Para", "Plain") for b in content):
            raise StateError(f"{slide['id']}: {{.{slide['kind']}}} slides take short paragraphs only (no lists, tables, figures or columns)")
        # Large kind text is drawn as plain runs, where LaTeX would show up as its source.
        if any(n["t"] == "Math" for n in nodes(content)):
            raise StateError(f"{slide['id']}: {{.{slide['kind']}}} slides take plain text; write 3.2× rather than LaTeX")
        if slide["kind"] == "number" and not content:
            raise StateError(f"{slide['id']}: {{.number}} needs the number as its first paragraph")
    # Layout follows the content, so authors never pick coordinates or layouts.
    if columns is not None:
        if content:
            raise StateError(f"{slide['id']}: put all content inside the two columns")
        slide["layout"], slide["slots"] = "columns", columns
    elif 2 <= len(content) <= 4 and all(is_figure(b) for b in content):
        slide["layout"], slide["slots"] = f"figure_{len(content)}", [[b] for b in content]
    else:
        slide["slots"] = [content]
    bullets = []
    for blocks in slide["slots"]:
        slide["warnings"] += validate_blocks(blocks, task, tokens)
        for b in blocks:
            bullets.extend(bullet_items(b))
    if any(depth > 2 for depth, _ in bullets):
        slide["warnings"].append("Bullets deeper than 2 levels are hard to read; consider flattening")
    # Count and length are advice; build stops on real overflow.
    if len(bullets) > tokens["limits"]["bullets"]:
        slide["warnings"].append(f"{len(bullets)} bullets (guide: {tokens['limits']['bullets']}); consider splitting the slide")
    for _, value in bullets:
        limit = tokens["limits"]["bullet_korean_chars" if re.search(r"[가-힣]", value) else "bullet_latin_chars"]
        if len(value) > limit:
            slide["warnings"].append(f"Long bullet ({len(value)} > {limit} chars) may wrap: {value}")
