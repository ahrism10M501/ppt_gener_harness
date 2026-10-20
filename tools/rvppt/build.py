"""Compile approved Pandoc blocks into fixed RVLAB or preset layouts, then publish after QA."""

from copy import deepcopy
import hashlib
import json
import math
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
from zipfile import ZipFile

from lxml import etree
from PIL import Image, ImageDraw, ImageFont, ImageStat
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.dml import MSO_LINE
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.xmlchemy import OxmlElement
from pptx.util import Inches, Pt

from .markdown import APPENDIX, animation_metadata, asset_path, image_node, nodes, pandoc, parse_task, plain, table_rows
from .preview import chrome_binary, contact_sheet, fit_picture, render_pdf, resolve_fonts, text
from .state import StateError, status, tree_hash
from .template import ROOT, NS, EMU, ensure_preset_reference, load_tokens, sha256, slots, validate_package

MATH_NS = "http://schemas.openxmlformats.org/officeDocument/2006/math"
MC_NS = "http://schemas.openxmlformats.org/markup-compatibility/2006"
DRAW_MATH_NS = "http://schemas.microsoft.com/office/drawing/2010/main"


def run(arguments, *, data=None, cwd=None):
    try:
        result = subprocess.run([str(a) for a in arguments], input=data, cwd=cwd,
                                text=True, encoding="utf-8", capture_output=True, timeout=120)
    except (OSError, subprocess.TimeoutExpired) as error:
        raise StateError(f"Renderer failed: {error}") from error
    if result.returncode:
        raise StateError(f"Renderer failed: {result.stderr[-2000:]}")
    return result.stdout


def font_path(profile, *, korean=False, code=False, bold=False):
    family = "Liberation Mono" if code else profile["korean" if korean else "latin"]["resolved"]
    if shutil.which("fc-match"):
        matched, value = run(["fc-match", "-f", "%{family}\n%{file}", family + (":style=Bold" if bold else "")]).strip().split("\n", 1)
        if family.casefold() not in matched.casefold().split(","):
            raise StateError(f"Missing fixed font: {family}")
        if Path(value).is_file():
            return value
    candidates = [family + ".ttf", family.replace(" ", "") + ".ttf"]
    for directory, filename in [(Path(os.environ.get("WINDIR", "C:/Windows")) / "Fonts", "LiberationMono-Regular.ttf" if code else "malgun.ttf" if korean else "arialbd.ttf" if bold else "arial.ttf"), (Path("/System/Library/Fonts/Supplemental"), "LiberationMono-Regular.ttf" if code else "Arial Bold.ttf" if bold else "Arial.ttf")]:
        if (directory / filename).is_file():
            candidates.insert(0, str(directory / filename))
    for candidate in candidates:
        try:
            return ImageFont.truetype(candidate, 20).path
        except OSError:
            continue
    raise StateError(f"Cannot measure font {family}; install the fonts in docs/setup.md")


def node_render(request):
    if not (ROOT / "node_modules/@resvg/resvg-js").is_dir():
        raise StateError("Node renderers are missing; run npm ci (see docs/setup.md)")
    return json.loads(run(["node", ROOT / "tools/rvppt/render.mjs"], data=json.dumps(request), cwd=ROOT))


def equation(tex, display, size, directory, profile):
    key = hashlib.sha256(f"{tex}:{display}:{size}".encode()).hexdigest()[:20]
    path = directory / f"math-{key}.png"
    if not path.exists():
        node_render({"mode": "math", "tex": tex, "display": display, "size": size,
                     "output": str(path), "svg": str(path.with_suffix('.svg')),
                     "font": profile["latin"]["resolved"]})
    return path


def inline_parts(inlines):
    for node in inlines:
        kind, content = node["t"], node.get("c")
        if kind == "Math":
            yield ("math", content)
        elif kind in ("Emph", "Strong", "Strikeout", "SmallCaps", "Superscript", "Subscript", "Underline"):
            yield from inline_parts(content)
        elif kind in ("Link", "Span", "Cite"):
            yield from inline_parts(content[1])
        elif kind == "Quoted":
            opening, closing = ("“", "”") if content[0]["t"] == "DoubleQuote" else ("‘", "’")
            yield ("text", opening)
            yield from inline_parts(content[1])
            yield ("text", closing)
        else:
            yield ("text", plain(node))


def paragraphs(block, depth=0, marker=None):
    if block["t"] in ("Para", "Plain"):
        yield block["c"], depth, False, marker
    elif block["t"] == "CodeBlock":
        for line in block["c"][1].splitlines():
            yield [{"t": "Str", "c": line or " "}], 0, True, None
    elif block["t"] in ("BulletList", "OrderedList"):
        items = block["c"] if block["t"] == "BulletList" else block["c"][1]
        start = block["c"][0][0] if block["t"] == "OrderedList" else 1
        for index, item in enumerate(items, start):
            for child in item:
                child_marker = f"{index}." if block["t"] == "OrderedList" else "•" if depth == 0 else "–"
                yield from paragraphs(child, depth + 1, child_marker)
    else:
        raise StateError(f"Cannot measure {block['t']}")


def compose(block, width, size, directory, profile, *, output=None):
    """Measure fixed-size text; rasterize math-bearing preview fragments at 300 DPI."""
    scale = 300
    # ponytail: 4% slack absorbs renderer glyph substitution (arrows, autospacing); per-glyph font routing if it still overflows.
    pixel_width = round(width * scale * .96)
    layouts = []
    y = round(profile["text_top_inset_pt"] / 72 * scale)
    for inlines, depth, code, marker in paragraphs(block):
        points = 16 if code else size - 2 if depth > 1 else size
        if len(inlines) == 1 and inlines[0]["t"] == "Math" and inlines[0]["c"][0]["t"] == "DisplayMath":
            points = 20
        latin = ImageFont.truetype(font_path(profile, code=code), round(points / 72 * scale))
        cjk = ImageFont.truetype(font_path(profile, korean=True), round(points / 72 * scale))
        indent = round(depth * .25 * scale)
        x = indent
        line = []
        line_h = round(points / 72 * scale * 1.25)
        previous = " "
        if depth:
            line.append((round((depth * .25 - .18) * scale), marker or "•", latin))
        for kind, value in inline_parts(inlines):
            if kind == "math":
                display = value[0]["t"] == "DisplayMath"
                path = equation(value[1], display, points if not display else 20, directory, profile)
                image = Image.open(path).convert("RGBA")
                parts = [(image, image.width, image.height, None)]
            else:
                parts = []
                for word in re.findall(r"\n|[^\S\n]+|[가-힣一-龥]|[^\s가-힣一-龥]+", value):
                    font = cjk if re.search(r"[가-힣一-龥]", word) else latin
                    advance = round(font.getlength(word))
                    # LibreOffice adds Asian–Latin autospacing (about a quarter em) between Hangul and letters/digits.
                    if re.match(r"[가-힣一-龥][A-Za-z0-9]|[A-Za-z0-9][가-힣一-龥]", previous[-1] + word[0]):
                        advance += round(points / 72 * scale / 4)
                    previous = word
                    parts.append((word, advance, round(points / 72 * scale * 1.25), font))
            for value, w, h, font in parts:
                if w > pixel_width - indent + 1:
                    raise StateError("Text token or equation exceeds the fixed content width")
                if isinstance(value, str) and value == "\n":
                    layouts.append((y, line_h, line)); y += line_h
                    x, line, line_h = indent, [], round(points / 72 * scale * 1.25)
                    continue
                if x + w > pixel_width and x > indent:
                    layouts.append((y, line_h, line)); y += line_h
                    x, line, line_h = indent, [], round(points / 72 * scale * 1.25)
                if isinstance(value, str) and value.isspace() and x == indent:
                    continue
                line.append((x, value, font)); x += w; line_h = max(line_h, h)
        layouts.append((y, line_h, line)); y += line_h + round((.14 if depth else .05) * scale)
    if output:
        canvas = Image.new("RGB", (round(width * scale), max(1, y)), "white")
        draw = ImageDraw.Draw(canvas)
        for top, height, line in layouts:
            for left, value, font in line:
                if isinstance(value, str):
                    # One baseline per line so Hangul and Latin fallback fonts line up.
                    draw.text((left, top + round(height * .8)), value, fill="black", font=font, anchor="ls")
                else:
                    canvas.paste(value, (left, round(top + (height - value.height) / 2)), value)
        canvas.save(output, dpi=(300, 300))
    return y / scale


def prepare_image(block, task, directory, box, tokens, profile):
    image = image_node(block)
    caption = plain(image).strip() if image else "Mermaid diagram"
    width = round(box[2] * tokens["limits"]["generated_image_dpi"])
    if image:
        source = asset_path(task, image["c"][2][0])
    else:
        key = hashlib.sha256(block["c"][1].encode()).hexdigest()[:16]
        source = directory / f"mermaid-{key}.svg"
        code = source.with_suffix(".mmd"); code.write_text(block["c"][1], encoding="utf-8")
        config = directory / "mermaid-config.json"
        config.write_text(json.dumps({"theme": "base", "securityLevel": "strict", "htmlLabels": False, "flowchart": {"htmlLabels": False}, "themeVariables": {"primaryColor": "#" + tokens["palette"]["secondary"], "primaryTextColor": "#000000", "primaryBorderColor": "#" + tokens["palette"]["primary"], "lineColor": "#" + tokens["palette"]["primary"], "fontFamily": profile["korean"]["resolved"]}}))
        args = ["node", ROOT / "node_modules/@mermaid-js/mermaid-cli/src/cli.js", "-i", code, "-o", source, "-c", config, "-b", "white"]
        if browser := chrome_binary():
            puppeteer = directory / "puppeteer-config.json"
            puppeteer.write_text(json.dumps({"executablePath": browser, "args": ["--no-sandbox"]}))
            args += ["-p", puppeteer]
        run(args, cwd=ROOT)
    suffix = source.suffix.lower()
    output = directory / (hashlib.sha256(str(source).encode()).hexdigest()[:20] + ".png")
    if suffix == ".svg":
        raw = source.read_text(encoding="utf-8")
        try:
            xml = etree.fromstring(raw.encode(), etree.XMLParser(resolve_entities=False, no_network=True))
        except etree.XMLSyntaxError as error:
            raise StateError(f"Invalid SVG: {source.name}") from error
        external = any(etree.QName(k).localname == "href" and not v.startswith(("#", "data:image/")) for e in xml.iter() for k, v in e.attrib.items())
        if "<!DOCTYPE" in raw or "@import" in raw or external or any(etree.QName(e).localname in ("script", "foreignObject") for e in xml.iter() if isinstance(e.tag, str)) or re.search(r"url\(\s*[^#]", raw, re.I):
            raise StateError(f"SVG external resources, scripts and foreignObject are forbidden: {source.name}")
        node_render({"mode": "svg", "input": str(source), "output": str(output), "width": width, "font": profile["korean"]["resolved"]})
    elif suffix == ".pdf":
        import pymupdf
        with pymupdf.open(source) as pdf:
            if len(pdf) != 1:
                raise StateError("Figure PDF must have exactly one page")
            pdf[0].get_pixmap(matrix=pymupdf.Matrix(width / pdf[0].rect.width, width / pdf[0].rect.width), alpha=False).save(output)
    else:
        output = source
    with Image.open(output) as picture:
        picture.load()
        # Never stretch below the DPI floor: small paper figures are placed smaller instead of blurry.
        floor = tokens["limits"]["image_min_effective_dpi"]
        w, h = min(box[2], picture.width / floor), min(box[3], picture.height / floor)
        position = fit_picture(picture.size, (box[0] + (box[2] - w) / 2, box[1] + (box[3] - h) / 2, w, h))
        dpi = min(picture.width / position[2], picture.height / position[3])
    return output, position, caption, round(dpi, 1)


def set_typography(shape, size, profile, *, code=False):
    for props in shape._element.iter(f"{{{NS['a']}}}bodyPr"):
        props.set("wrap", "square"); props.set("tIns", str(int(Pt(profile["text_top_inset_pt"]))))
        for attr in ("lIns", "rIns", "bIns"):
            props.set(attr, "0")
        for child in list(props):
            if etree.QName(child).localname in ("normAutofit", "spAutoFit"):
                props.remove(child)
        if props.find(f"{{{NS['a']}}}noAutofit") is None:
            etree.SubElement(props, f"{{{NS['a']}}}noAutofit")
    for p in shape._element.iter(f"{{{NS['a']}}}p"):
        ppr = p.find(f"{{{NS['a']}}}pPr")
        if ppr is None:
            ppr = OxmlElement("a:pPr"); p.insert(0, ppr)
        for name in ("lnSpc", "spcBef", "spcAft"):
            old = ppr.find(f"{{{NS['a']}}}{name}")
            if old is not None:
                ppr.remove(old)
        line = OxmlElement("a:lnSpc"); line.append(OxmlElement("a:spcPct")); line[0].set("val", "100000"); ppr.insert(0, line)
        space = OxmlElement("a:spcAft"); space.append(OxmlElement("a:spcPts")); space[0].set("val", "800" if ppr.find(f"{{{NS['a']}}}buChar") is not None else "0"); ppr.insert(1, space)
        default = ppr.find(f"{{{NS['a']}}}defRPr")
        if default is None:
            default = OxmlElement("a:defRPr"); ppr.append(default)
    for run in shape._element.iter(f"{{{MATH_NS}}}r"):
        if run.find(f"{{{NS['a']}}}rPr") is None:
            properties = OxmlElement("a:rPr")
            math_properties = run.find(f"{{{MATH_NS}}}rPr")
            run.insert(1 if math_properties is not None else 0, properties)
    for props in list(shape._element.iter(f"{{{NS['a']}}}rPr")) + list(shape._element.iter(f"{{{NS['a']}}}defRPr")) + list(shape._element.iter(f"{{{NS['a']}}}endParaRPr")):
        paragraph = next((a for a in props.iterancestors() if a.tag == f"{{{NS['a']}}}p"), None)
        ppr = paragraph.find(f"{{{NS['a']}}}pPr") if paragraph is not None else None
        points = size - 2 if ppr is not None and int(ppr.get("lvl", "0")) > 0 else size
        props.set("sz", str(round(points * 100)))
        for name, family in (("latin", "Liberation Mono" if code else profile["latin"]["resolved"]), ("ea", profile["korean"]["resolved"])):
            node = props.find(f"{{{NS['a']}}}{name}")
            if node is None:
                node = etree.SubElement(props, f"{{{NS['a']}}}{name}")
            node.set("typeface", "Cambria Math" if props.getparent().tag == f"{{{MATH_NS}}}r" else family)
        for child in list(props):
            if etree.QName(child).localname in ("solidFill", "gradFill", "noFill"):
                props.remove(child)
        fill = etree.Element(f"{{{NS['a']}}}solidFill"); props.insert(0, fill)
        etree.SubElement(fill, f"{{{NS['a']}}}srgbClr", val="000000")


def copy_fragment(shape, target, box, size, profile, block):
    element = deepcopy(shape._element)
    for node in element.iter():
        for attr, value in list(node.attrib.items()):
            if attr.startswith("{" + NS["r"] + "}"):
                relationship = shape.part.rels[value]
                if not relationship.is_external:
                    raise StateError("Unexpected internal content relationship in Pandoc fragment")
                node.set(attr, target.part.relate_to(relationship.target_ref, relationship.reltype, is_external=True))
    for prop in element.iter(f"{{{NS['p']}}}cNvPr"):
        prop.set("id", str(target.shapes._next_shape_id))
        prop.set("name", "RVLAB content")
    for ph in list(element.iter(f"{{{NS['p']}}}ph")):
        ph.getparent().remove(ph)
    if not shape.has_table:
        for p, (_, depth, _, marker) in zip(element.findall("p:txBody/a:p", NS), paragraphs(block)):
            ppr = p.find(f"{{{NS['a']}}}pPr")
            if ppr is None:
                ppr = OxmlElement("a:pPr"); p.insert(0, ppr)
            for child in list(ppr):
                if etree.QName(child).localname in ("buNone", "buChar", "buAutoNum"):
                    ppr.remove(child)
            ppr.set("algn", "l")
            if depth:
                # Automatic numbers ("1.") are wider than bullets and need the whole indent.
                number = .1 if marker and marker.endswith(".") else 0
                ppr.set("lvl", str(depth - 1)); ppr.set("marL", str(Inches(depth * .25 + number))); ppr.set("indent", str(-Inches(.18 + number * 1.7)))
                if marker and marker.endswith("."):
                    bullet = OxmlElement("a:buAutoNum"); bullet.set("type", "arabicPeriod"); bullet.set("startAt", marker[:-1])
                else:
                    bullet = OxmlElement("a:buChar"); bullet.set("char", marker or "•")
            else:
                bullet = OxmlElement("a:buNone")
            default = ppr.find(f"{{{NS['a']}}}defRPr")
            ppr.insert(ppr.index(default) if default is not None else len(ppr), bullet)
    target.shapes._spTree.insert_element_before(element, "p:extLst")
    added = target.shapes[-1]
    added.left, added.top, added.width, added.height = [Inches(v) for v in box]
    set_typography(added, size, profile, code=block["t"] == "CodeBlock")
    return added


def native_fragments(api, slides, reference, directory):
    fragments, blocks = [], []
    for slide in slides:
        if "slots" not in slide:
            continue
        for contents in slide["slots"]:
            for block in contents:
                if image_node(block) or (block["t"] == "CodeBlock" and block["c"][0][1] == ["mermaid"]):
                    continue
                fragments.append(block)
                blocks += [{"t": "Header", "c": [2, ["", [], []], [{"t": "Str", "c": f"F{len(fragments)}"}]]}, block]
    if not fragments:
        return {}
    path = directory / "pandoc-fragments.pptx"
    pandoc(["-f", "json", "-t", "pptx", "--slide-level=2", "--reference-doc", str(reference), "-o", str(path)], json.dumps({"pandoc-api-version": api, "meta": {}, "blocks": blocks}))
    presentation = Presentation(path)
    if len(presentation.slides) != len(fragments):
        raise StateError("Pandoc fragment count changed unexpectedly")
    result = {}
    for block, slide in zip(fragments, presentation.slides):
        # Unwrap for python-pptx editing; restore the Office math choice and image fallback before saving.
        for alternate in list(slide._element.iter(f"{{{MC_NS}}}AlternateContent")):
            choice = alternate.find(f"{{{MC_NS}}}Choice")
            if choice is None:
                raise StateError("Pandoc produced AlternateContent without a native choice")
            parent = alternate.getparent(); index = parent.index(alternate)
            for child in list(choice):
                parent.insert(index, child); index += 1
            parent.remove(alternate)
        title = slide.shapes.title
        shapes = [s for s in slide.shapes if (title is None or s._element is not title._element) and (s.has_table or s.has_text_frame and (s.text.strip() or list(s._element.iter(f"{{{MATH_NS}}}oMath"))))]
        if len(shapes) != 1:
            raise StateError(f"Pandoc block must yield one editable shape, got {len(shapes)}")
        result[id(block)] = shapes[0]
    return result


def add_text(slide, value, box, size, profile, *, center=False, bold=False, color="000000", bullets=False):
    shape = slide.shapes.add_textbox(*[Inches(v) for v in box])
    text(shape, value, size, color, profile, center=center, bold=bold, bullets=bullets)
    return shape


def box_of(shape):
    return [v / EMU for v in (shape.left, shape.top, shape.width, shape.height)]


def fill_template(slide, spec, tokens, page, records):
    """Cover, contents, section and closing keep the original placeholders and inherited styling."""
    layout = spec["layout"]
    if layout == "cover":
        values = {0: spec["title"], 1: spec["subtitle"], 2: spec["presenter"], 3: "\n".join(spec["affiliation"]), 4: spec["date_label"]}
    elif layout == "toc":
        values = {1: None}
    else:
        values = {0: spec["title"], 1: spec.get("subtitle", "")}
    for ph in list(slide.placeholders):
        idx = ph.placeholder_format.idx
        if idx not in values or values[idx] == "":
            slide.shapes._spTree.remove(ph._element)
            continue
        if layout == "toc":
            lines = [line for chapter, topics in spec["chapters"] for line in [(0, chapter)] + [(1, t) for t in topics]]
            frame = ph.text_frame
            for i, (level, value) in enumerate(lines):
                paragraph = frame.paragraphs[0] if i == 0 else frame.add_paragraph()
                paragraph.text, paragraph.level = value, level
                paragraph.runs[0].font.bold = level == 0
            expected = "\n".join(value for _, value in lines)
        else:
            ph.text_frame.text = expected = values[idx]
        if layout == "closing" and idx == 0:
            ph.left, ph.top, ph.width, ph.height = [Inches(v) for v in tokens["geometry_in"]["closing_title"]]
        records.append({"page": page, "slide_id": spec["id"], "role": f"{layout}_{idx}", "box": box_of(ph), "expected": expected, "max_lines": None if layout == "toc" or (layout == "cover" and idx == 3) else 1, "template": True})


def figure_request(slide, box, request, path, tokens, profile):
    """A visible, editable gap the researcher fills by saving the figure at the named path."""
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, *[Inches(v) for v in box])
    shape.fill.background()
    shape.line.color.rgb = RGBColor.from_string(tokens["palette"]["primary"])
    shape.line.dash_style = MSO_LINE.DASH
    shape.line.width = Pt(1.5)
    text(shape, f"그림 필요: {request}\n{path}", tokens["sizes_pt"]["caption"] + 2, tokens["palette"]["primary"], profile, center=True)
    shape.text_frame.vertical_anchor = MSO_ANCHOR.MIDDLE


def table_geometry(block, width, directory, tokens, profile):
    rows = table_rows(block)
    cell_width = width / len(rows[0])
    heights = [max(.42, max(compose({"t": "Para", "c": [{"t": "Str", "c": cell}]}, cell_width - .12, tokens["sizes_pt"]["table"], directory, profile) for cell in row) + .1) for row in rows]
    return rows, heights


def package_checks(output, tokens):
    validate_package(output)
    presentation = Presentation(output)
    expected_w = round(float(tokens["slide"]["width_in"]) * EMU)
    expected_h = round(float(tokens["slide"]["height_in"]) * EMU)
    if (abs(presentation.slide_width - expected_w) > 2000 or abs(presentation.slide_height - expected_h) > 2000 or len(presentation.slide_masters) != 1 or len(presentation.slide_layouts) != 13):
        raise StateError("PPTX dimensions, masters or layouts violate the reference")
    reference_path = ensure_preset_reference(tokens)
    with ZipFile(reference_path) as reference, ZipFile(output) as result:
        for name in reference.namelist():
            if name.startswith(("ppt/slideMasters/", "ppt/slideLayouts/", "ppt/theme/", "ppt/media/")) and not name.endswith(".rels"):
                before, after = reference.read(name), result.read(name)
                if name.endswith(".xml"):
                    before = etree.tostring(etree.fromstring(before), method="c14n")
                    after = etree.tostring(etree.fromstring(after), method="c14n")
                if before != after:
                    raise StateError(f"Reference branding or layout changed: {name}")
    for slide in presentation.slides:
        for shape in slide.shapes:
            if min(shape.left, shape.top) < 0 or min(shape.width, shape.height) <= 0 or shape.left + shape.width > presentation.slide_width + 1 or shape.top + shape.height > presentation.slide_height + 1:
                raise StateError("Shape exceeds slide boundaries")


def assemble(api, slides, tokens, profile, task, directory):
    reference = ensure_preset_reference(tokens)
    presentation = Presentation(reference)
    if len(presentation.slides):
        raise StateError("Reference must not contain slides")
    fragments = native_fragments(api, slides, reference, directory)
    assets = directory / "generated-assets"; assets.mkdir()
    records, fallbacks, images, missing = [], [], [], []
    layouts = {layout.name: layout for layout in presentation.slide_layouts}
    for page, spec in enumerate(slides, 1):
        layout = spec["layout"]
        slide = presentation.slides.add_slide(layouts[tokens["layouts"]["section" if layout == "closing" else layout]])
        if layout in ("cover", "toc", "section", "closing"):
            fill_template(slide, spec, tokens, page, records)
        else:
            # Content slides: short topic in the original top bar, ▪ headline, then indented content.
            for ph in list(slide.placeholders):
                if ph.placeholder_format.idx != 0:
                    slide.shapes._spTree.remove(ph._element)
            slide.shapes.title.text = spec["topic"]
            records.append({"page": page, "slide_id": spec["id"], "role": "title", "box": box_of(slide.shapes.title), "expected": spec["topic"], "max_lines": 1})
            x0, y0, w0, h0 = tokens["geometry_in"]["body"]
            indent = tokens["geometry_in"]["content_indent"]
            headline = {"t": "Para", "c": [{"t": "Str", "c": spec["headline"]}]}
            headline_box = [x0, y0, w0, compose(headline, w0 - indent, tokens["sizes_pt"]["headline"], assets, profile)]
            add_text(slide, spec["headline"], headline_box, tokens["sizes_pt"]["headline"], profile, bullets=True)
            records.append({"page": page, "slide_id": spec["id"], "role": "headline", "box": headline_box, "expected": spec["headline"], "max_lines": tokens["limits"]["headline_lines"]})
            top = y0 + headline_box[3] + tokens["geometry_in"]["gap"] / 2
            region = [x0 + indent, top, w0 - indent, y0 + h0 - top]
            count = len(spec["slots"])
            source = plain(spec["source"]).strip()
            if source:
                region[3] = 6.6 - region[1] - .08
                source_box = [region[0], 6.6, (x0 + w0 - region[0]), .42]
                add_text(slide, source, source_box, tokens["sizes_pt"]["source"], profile)
                records.append({"page": page, "slide_id": spec["id"], "role": "source", "box": source_box, "expected": source, "max_lines": 2})
            boxes = slots(tokens, count, region)
            for slot_index, (contents, base) in enumerate(zip(spec["slots"], boxes)):
                x, y, w, h = base
                points = tokens["sizes_pt"]["columns" if layout in ("columns", "comparison") else "body"]
                heights, picture_indices = [], []
                for i, block in enumerate(contents):
                    if image_node(block) or (block["t"] == "CodeBlock" and block["c"][0][1] == ["mermaid"]):
                        heights.append(0); picture_indices.append(i)
                    elif block["t"] == "Table":
                        heights.append(sum(table_geometry(block, w, assets, tokens, profile)[1]))
                    else:
                        heights.append(compose(block, w, points, assets, profile))
                gap = tokens["geometry_in"]["gap"]
                remaining = h - sum(heights) - gap * (len(contents) - 1)
                if remaining < -.01 or picture_indices and remaining < .8 * len(picture_indices):
                    raise StateError(f"Content overflow on {spec['id']}, column {slot_index + 1}; split the slide")
                for i in picture_indices:
                    heights[i] = remaining / len(picture_indices)
                for i, (block, height) in enumerate(zip(contents, heights)):
                    box = [x, y, w, height]
                    if i in picture_indices:
                        image_box = [x, y, w, height - tokens["geometry_in"]["caption_height"]]
                        image = image_node(block)
                        animation = None
                        if image and not asset_path(task, image["c"][2][0]).exists():
                            caption, dpi = plain(image).strip(), None
                            request = image["c"][2][1] or caption  # ![caption](figures/x.png "what to draw")
                            figure_request(slide, image_box, request, image["c"][2][0], tokens, profile)
                            missing.append({"slide_id": spec["id"], "path": image["c"][2][0], "request": request})
                        else:
                            path, position, caption, dpi = prepare_image(block, task, assets, image_box, tokens, profile)
                            picture = slide.shapes.add_picture(str(path), *[Inches(v) for v in position])
                            if path.suffix.lower() == ".gif":
                                animation = animation_metadata(task, path)
                                poster = assets / (hashlib.sha256(str(path).encode()).hexdigest()[:20] + "-poster.png")
                                shutil.copyfile(task / animation["poster"], poster)
                                records.append({"page": page, "slide_id": spec["id"], "role": "animation_image", "box": position,
                                                "shape_id": picture.shape_id, "preview_image": str(poster.relative_to(directory))})
                        caption = f"그림 {len(images) + 1}. {caption}"
                        caption_box = [x, y + height - tokens["geometry_in"]["caption_height"], w, tokens["geometry_in"]["caption_height"]]
                        add_text(slide, caption, caption_box, tokens["sizes_pt"]["caption"], profile, center=True)
                        records.append({"page": page, "slide_id": spec["id"], "role": "caption", "box": caption_box, "expected": caption, "max_lines": 1})
                        images.append({"slide_id": spec["id"], "caption": caption, "effective_dpi": dpi,
                                       **({"animation": animation} if animation else {})})
                    else:
                        display = block["t"] == "Para" and len(block["c"]) == 1 and block["c"][0]["t"] == "Math" and block["c"][0]["c"][0]["t"] == "DisplayMath"
                        size = tokens["sizes_pt"]["table"] if block["t"] == "Table" else tokens["sizes_pt"]["code"] if block["t"] == "CodeBlock" else tokens["sizes_pt"]["equation"] if display else points
                        shape = copy_fragment(fragments[id(block)], slide, box, size, profile, block)
                        maths = [n["c"] for n in nodes(block) if n["t"] == "Math"]
                        actual_math = len(list(shape._element.iter(f"{{{MATH_NS}}}oMath")))
                        preview_image = None
                        if maths:
                            preview_image = assets / f"preview-math-{page}-{slot_index}-{i}.png"
                            compose(block, w, points, assets, profile, output=preview_image)
                            if actual_math != len(maths):
                                slide.shapes._spTree.remove(shape._element)
                                shape = slide.shapes.add_picture(str(preview_image), *[Inches(v) for v in box])
                            for _, tex in maths:
                                fallbacks.append({"slide_id": spec["id"], "tex": tex, "scope": "preview" if actual_math == len(maths) else "final_and_preview", "reason": "LibreOffice cannot display native OMML" if actual_math == len(maths) else "Pandoc could not convert LaTeX to native OMML"})
                        if block["t"] == "Table":
                            rows, row_heights = table_geometry(block, w, assets, tokens, profile)
                            for column in shape.table.columns:
                                column.width = Inches(w / len(rows[0]))
                            top = y
                            for row_index, (row, row_h) in enumerate(zip(shape.table.rows, row_heights)):
                                row.height = Inches(row_h)
                                for col_index, cell in enumerate(row.cells):
                                    cell.margin_left = cell.margin_right = Inches(.06)
                                    cell.margin_top = Pt(4); cell.margin_bottom = 0
                                    cell.fill.solid(); cell.fill.fore_color.rgb = RGBColor.from_string(tokens["palette"]["primary"] if row_index == 0 else "FFFFFF")
                                    for p in cell.text_frame.paragraphs:
                                        p.alignment = PP_ALIGN.RIGHT if row_index > 0 and re.fullmatch(r"[-+\d.,%\s]+", rows[row_index][col_index]) else PP_ALIGN.LEFT
                                        for r in p.runs:
                                            r.font.color.rgb = RGBColor.from_string("FFFFFF" if row_index == 0 else "000000")
                                            if row_index == 0:
                                                r.font.bold = True
                                    properties = cell._tc.get_or_add_tcPr()
                                    for side in ("lnL", "lnR", "lnT", "lnB"):
                                        border = properties.find(f"{{{NS['a']}}}{side}")
                                        if border is None:
                                            border = OxmlElement(f"a:{side}"); properties.insert(0, border)
                                        border.clear()
                                        if side == "lnB" and row_index in (0, len(rows) - 1):
                                            border.set("w", "12700")
                                            fill = OxmlElement("a:solidFill"); color = OxmlElement("a:srgbClr"); color.set("val", tokens["palette"]["primary"]); fill.append(color); border.append(fill)
                                        else:
                                            border.append(OxmlElement("a:noFill"))
                                    records.append({"page": page, "slide_id": spec["id"], "role": "table_cell", "box": [x + col_index * w / len(rows[0]), top, w / len(rows[0]), row_h], "expected": rows[row_index][col_index]})
                                top += row_h
                        else:
                            records.append({"page": page, "slide_id": spec["id"], "role": "math_image" if preview_image else "text", "box": box, "expected": plain(block).strip(), "shape_id": shape.shape_id, "preview_image": str(preview_image.relative_to(directory)) if preview_image else None})
                    y += height + gap
        slide.notes_slide.notes_text_frame.text = plain(spec["notes"]).strip()
    output = directory / "presentation.pptx"; presentation.save(output)
    package_checks(output, tokens)
    preview = Presentation(output)
    compatible = Presentation(output) if fallbacks else None
    for record in records:
        if record.get("preview_image"):
            slide = preview.slides[record["page"] - 1]
            shape = next(s for s in slide.shapes if s.shape_id == record["shape_id"])
            if record["role"] == "animation_image":
                slide.part.drop_rel(shape._element.blip_rId)
            slide.shapes._spTree.remove(shape._element)
            slide.shapes.add_picture(str(directory / record["preview_image"]), *[Inches(v) for v in record["box"]])
            if record["role"] == "math_image":
                compatible_slide = compatible.slides[record["page"] - 1]
                compatible_shape = next(s for s in compatible_slide.shapes if s.shape_id == record["shape_id"])
                compatible_slide.shapes._spTree.remove(compatible_shape._element)
                compatible_slide.shapes.add_picture(str(directory / record["preview_image"]), *[Inches(v) for v in record["box"]])
                native_slide = presentation.slides[record["page"] - 1]
                native_shape = next(s for s in native_slide.shapes if s.shape_id == record["shape_id"])
                if list(native_shape._element.iter(f"{{{MATH_NS}}}oMath")):
                    tree = native_slide.shapes._spTree
                    index = tree.index(native_shape._element)
                    picture = native_slide.shapes.add_picture(str(directory / record["preview_image"]), *[Inches(v) for v in record["box"]])
                    alternate = etree.Element(f"{{{MC_NS}}}AlternateContent", nsmap={"mc": MC_NS, "a14": DRAW_MATH_NS})
                    etree.SubElement(alternate, f"{{{MC_NS}}}Choice", Requires="a14").append(native_shape._element)
                    etree.SubElement(alternate, f"{{{MC_NS}}}Fallback").append(picture._element)
                    tree.insert(index, alternate)
    preview.save(directory / "presentation-preview-copy.pptx")
    if compatible is not None:
        compatible.save(directory / "presentation-math-compatible.pptx")
    presentation.save(output)
    package_checks(output, tokens)
    return {"records": records, "math_fallbacks": fallbacks, "images": images, "missing_figures": missing,
            "slide_count": len(presentation.slides), "native_equations": sum(len(list(s._element.iter(f"{{{MATH_NS}}}oMath"))) for s in presentation.slides),
            "native_tables": sum(s.has_table for slide in presentation.slides for s in slide.shapes),
            "notes_slides": sum(bool(s.notes_slide.notes_text_frame.text) for s in presentation.slides)}


def visual_rows(lines):
    """PDF text lines split at font changes (e.g. Arial spaces between CJK fallback runs); count rows by centre."""
    centres = sorted((line["bbox"][1] + line["bbox"][3]) / 2 for line in lines)
    tolerance = min((line["bbox"][3] - line["bbox"][1] for line in lines), default=0) / 2
    return sum(1 for i, centre in enumerate(centres) if i == 0 or centre - centres[i - 1] > tolerance)


def render_and_check(directory, report):
    import pymupdf
    pdf = directory / "presentation.pdf"
    render_pdf(directory / "presentation-preview-copy.pptx", pdf)
    findings, paths = [], []
    def normalize(value):
        # Bullets and automatic list numbers are rendered, not part of the source text.
        return re.sub(r"[\s▪•●◆–]", "", re.sub(r"(?m)^\s*\d+\.(?!\d)", "", value))
    with pymupdf.open(pdf) as document:
        if len(document) != report["slide_count"]:
            raise StateError("Rendered page count differs from the PPTX")
        for record in report["records"]:
            if record["role"] in ("math_image", "animation_image"):
                continue
            page = document[record["page"] - 1]
            x, y, w, h = record["box"]
            box = pymupdf.Rect(x * 72, y * 72, (x + w) * 72, (y + h) * 72)
            clip = box + (-2, -2, 2, 2)
            actual = page.get_text(clip=clip)
            if normalize(record["expected"]) not in normalize(actual):
                findings.append({"slide_id": record["slide_id"], "role": record["role"], "issue": "Text missing, altered or clipped", "expected": record["expected"], "actual": actual.strip()})
            # A neighbour's descenders can touch this clip; a line belongs to the box holding its centre.
            lines = [line for block in page.get_text("dict", clip=clip)["blocks"] if "lines" in block for line in block["lines"] if box.y0 <= (line["bbox"][1] + line["bbox"][3]) / 2 <= box.y1]
            if record.get("max_lines") and visual_rows(lines) > record["max_lines"]:
                findings.append({"slide_id": record["slide_id"], "role": record["role"], "issue": "Too many rendered lines"})
            # Original template placeholders have tight boxes; their text presence and line count are checked instead.
            if not record.get("template") and any(not clip.contains(pymupdf.Rect(line["bbox"])) for line in lines):
                findings.append({"slide_id": record["slide_id"], "role": record["role"], "issue": "Rendered text exceeds its fixed box"})
        for index, page in enumerate(document, 1):
            path = directory / f"slide-{index:02}.png"
            page.get_pixmap(matrix=pymupdf.Matrix(1.8, 1.8), alpha=False).save(path)
            paths.append(path)
        report["rendered_fonts"] = sorted({font[3] for page in document for font in page.get_fonts()})
    contact_sheet(paths, [f"Slide {i}" for i in range(1, len(paths) + 1)], directory / "contact-sheet.png")
    return findings


def fingerprint(task, tokens):
    ref_path = ensure_preset_reference(tokens)
    result = {"slides.md": sha256(task / "slides.md"), "figures/": tree_hash(task / "figures"), "sources/": tree_hash(task / "sources"),
              "reference_sha256": sha256(ref_path), "design_sha256": sha256(ROOT / "DESIGN.md")}
    if tokens.get("preset_id", "rvlab") != "rvlab":
        result["preset_id"] = tokens["preset_id"]
    return result


def output_stem(deck):
    """Lab file naming, e.g. 20260831_학습루프개선_및_실험."""
    return deck["date"].replace("-", "") + "_" + re.sub(r'[\\/:*?"<>|\s]+', "_", deck["title"]).strip("_")


def _workspace(task):
    directory = task / ".build"
    if directory.is_symlink():
        raise StateError(".build/ symlinks are forbidden")
    directory.mkdir(exist_ok=True)
    return directory


def _last_report(build):
    path = build / "output/build-report.json"
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def publish(staging, task, outputs, *, math_compatible_name=None):
    """Swap .build/output, then copy the PPTX/PDF beside slides.md like Overleaf's output.pdf."""
    build = task / ".build"
    destination, previous = build / "output", build / ".previous"
    managed = _last_report(build).get("outputs", {})
    for name in outputs:
        path = task / name
        if path.is_symlink() or path.exists() and sha256(path) != managed.get(name):
            # Researchers may polish the PPTX by hand; never overwrite that work.
            raise StateError(f"{name} differs from the last build (edited by hand?); rename or move it, then rebuild")
    if destination.is_symlink() or previous.is_symlink():
        raise StateError("Output directory symlinks are forbidden")
    if previous.exists():
        if not (previous / "build-report.json").is_file():
            raise StateError("Existing .previous is not a managed build; refusing to remove it")
        if not destination.exists():
            previous.replace(destination)
        else:
            shutil.rmtree(previous)
    if destination.exists() and not (destination / "build-report.json").is_file():
        raise StateError("Existing .build/output is not a managed build; refusing to overwrite")
    if destination.exists():
        destination.replace(previous)
    try:
        staging.replace(destination)
    except OSError:
        if previous.exists():
            previous.replace(destination)
        raise
    if previous.exists():
        shutil.rmtree(previous, ignore_errors=True)
    for name in outputs:
        temporary = task / f".rvppt-{name}.tmp"
        source = "presentation-math-compatible.pptx" if name == math_compatible_name else "presentation" + Path(name).suffix
        shutil.copy2(destination / source, temporary)
        temporary.replace(task / name)
    for name, digest in managed.items():
        stale = task / name
        if name not in outputs and stale.is_file() and not stale.is_symlink() and sha256(stale) == digest:
            stale.unlink()  # Old title's output from a managed build.


def build(task):
    """Compile slides.md at any stage, like Overleaf's Recompile; the report records content approval."""
    api, slides, tokens = parse_task(task)
    if "source" in tokens and sha256(ROOT / tokens["source"]["path"]) != tokens["source"]["sha256"]:
        raise StateError("Original template checksum changed; restore the original")
    before = fingerprint(task, tokens)
    workspace = _workspace(task)
    lock = workspace / ".lock"
    try:
        descriptor = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError as error:
        raise StateError("Another build is active (.build/.lock); retry after it finishes") from error
    os.close(descriptor)
    try:
        with tempfile.TemporaryDirectory(prefix=".rvppt-", dir=workspace) as temporary:
            directory = Path(temporary)
            profile = dict(resolve_fonts(tokens), text_top_inset_pt=tokens["text_top_inset_pt"])
            report = assemble(api, slides, tokens, profile, task, directory)
            findings = render_and_check(directory, report)
            if findings:
                raise StateError("Render QA failed; previous build preserved: " + json.dumps(findings, ensure_ascii=False))
            if fingerprint(task, tokens) != before:
                raise StateError("Inputs or design changed during build; previous build preserved")
            stem = output_stem(slides[0])
            report.update(schema_version=1, task_id=task.name, preset=tokens.get("preset_id", "rvlab"),
                          aspect=tokens["slide"]["aspect"], fingerprint=before, fonts=profile,
                          content_approved=status(task)["content_approved"],
                          findings=findings, detected_overflows=0, powerpoint_editing="unverified",
                          preview_math="300 DPI raster in preview and math-compatible PPTX; native PPTX has OMML and AlternateContent image fallback",
                          preview_animation="Selected PNG posters only; PowerPoint GIF playback unverified")
            report["artifacts"] = {p.name: sha256(p) for p in directory.iterdir() if p.is_file() and p.suffix in (".pptx", ".pdf", ".png")}
            report["outputs"] = {f"{stem}.pptx": report["artifacts"]["presentation.pptx"], f"{stem}.pdf": report["artifacts"]["presentation.pdf"]}
            compatible_name = f"{stem}_수식호환.pptx" if (directory / "presentation-math-compatible.pptx").exists() else None
            if compatible_name:
                report["outputs"][compatible_name] = report["artifacts"]["presentation-math-compatible.pptx"]
            report["math_compatible_output"] = compatible_name
            requests = "".join(f"\n- {m['slide_id']}: {m['request']} → `{m['path']}`" for m in report["missing_figures"]) or " 없음"
            (directory / "build-report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
            (directory / "build-report.md").write_text(f"# Presentation build QA ({tokens.get('preset_id', 'rvlab')})\n\nTask: {task.name} · 내용 승인: {'완료' if report['content_approved'] else '미완료(초안 빌드)'}\n\nSlides: {report['slide_count']}; native tables: {report['native_tables']}; native equations: {report['native_equations']}; notes: {report['notes_slides']}.\n\n필요한 그림:{requests}\n\nDetected overflows: 0. PowerPoint editing: unverified. PDF/PNG use the separate math/animation preview copy. GIF playback: unverified.\n", encoding="utf-8")
            publish(directory, task, report["outputs"], math_compatible_name=compatible_name)
        return {"task_id": task.name, "preset": tokens.get("preset_id", "rvlab"), "aspect": tokens["slide"]["aspect"],
                "pptx": str(task / f"{stem}.pptx"), "pdf": str(task / f"{stem}.pdf"), "preview": str(workspace / "output/contact-sheet.png"),
                "slide_count": report["slide_count"], "content_approved": report["content_approved"], "missing_figures": report["missing_figures"],
                "warnings": deck_findings(slides), "detected_overflows": 0, "native_equations": report["native_equations"], "native_tables": report["native_tables"], "math_fallbacks": report["math_fallbacks"], "math_compatible_pptx": str(task / compatible_name) if compatible_name else None, "fonts": profile}
    finally:
        lock.unlink(missing_ok=True)


def requested_figures(task, slides):
    return [{"slide_id": s["id"], "path": n["c"][2][0], "request": n["c"][2][1] or plain(n).strip()}
            for s in slides for n in nodes(s.get("slots", [])) if n["t"] == "Image" and not asset_path(task, n["c"][2][0]).exists()]


def deck_findings(slides):
    """Advisory gaps the parser accepts: missing cover/section subtitles and content length hints."""
    findings = [] if slides[0]["subtitle"].strip() else [{"slide_id": "cover", "issue": "Cover subtitle is empty; RVLAB covers show a yellow subtitle under the title. Propose candidates and set deck.subtitle in slides.md"}]
    findings += [{"slide_id": s["id"], "issue": "Section has no subtitle; use '# 섹션 | 부제' (short description or English name) unless omitted on purpose"}
                 for s in slides if s["layout"] == "section" and not s["subtitle"] and s["title"] not in APPENDIX]
    findings += [{"slide_id": s["id"], "issue": w} for s in slides for w in s.get("warnings", [])]
    return findings


def lint(task):
    _, slides, tokens = parse_task(task)
    return {"task_id": task.name, "preset": tokens.get("preset_id", "rvlab"), "aspect": tokens["slide"]["aspect"], "slide_count": len(slides), "findings": deck_findings(slides), "missing_figures": requested_figures(task, slides), "scope": "Markdown structure, limits, paths and styling; rendered fit is checked by build"}


def preview(task):
    _, _, tokens = parse_task(task)
    directory = task / ".build/output"
    if directory.is_symlink():
        raise StateError("Output directory symlinks are forbidden")
    report_path = directory / "build-report.json"
    if not report_path.is_file():
        raise StateError("No successful build; run rvppt build TASK first")
    try:
        report = json.loads(report_path.read_text(encoding="utf-8"))
        if not isinstance(report["fingerprint"], dict) or not isinstance(report["artifacts"], dict) or not isinstance(report["outputs"], dict) or report["detected_overflows"] != 0:
            raise ValueError("Invalid report fields")
    except (ValueError, TypeError, KeyError) as error:
        raise StateError("Invalid build report; rebuild from slides.md") from error
    if report["fingerprint"] != fingerprint(task, tokens):
        raise StateError("Build is stale; slides.md, figures or design changed. Run rvppt build TASK")
    for name, expected in report["artifacts"].items():
        if not isinstance(name, str) or name != Path(name).name:
            raise StateError("Invalid build artifact path in report")
        path = directory / name
        if path.is_symlink() or not path.is_file() or sha256(path) != expected:
            raise StateError("Build artifact changed; rebuild from slides.md")
    # Successful builds already include render QA; this read-only command returns the verified preview.
    return {"task_id": task.name, "preset": report.get("preset", tokens.get("preset_id", "rvlab")), "outputs": [str(task / n) for n in report["outputs"]], "contact_sheet": str(directory / "contact-sheet.png"), "slides": [str(p) for p in sorted(directory.glob("slide-*.png"))], "content_approved": report.get("content_approved"), "missing_figures": report.get("missing_figures", []), "detected_overflows": report["detected_overflows"]}


def audit(task, zoom=4.0):
    """Anatomy-inspired 4x critic audit: render high-DPI close-ups of slide regions and measure clearance/contrast."""
    import pymupdf
    _, slides, tokens = parse_task(task)
    directory = task / ".build/output"
    report_path = directory / "build-report.json"
    if not report_path.is_file() or json.loads(report_path.read_text(encoding="utf-8")).get("fingerprint") != fingerprint(task, tokens):
        build(task)
    report = json.loads(report_path.read_text(encoding="utf-8"))
    pdf_path = directory / "presentation.pdf"
    crops_dir = directory / "crops"
    crops_dir.mkdir(exist_ok=True)
    for old in crops_dir.glob("*.png"):
        old.unlink()

    crop_records = []
    warnings = []
    crop_images = []
    crop_labels = []

    with pymupdf.open(pdf_path) as document:
        for idx, record in enumerate(report["records"], 1):
            if record["role"] == "table_cell":
                continue  # Individual table cells are audited via their slide/headline or full box
            page = document[record["page"] - 1]
            x, y, w, h = record["box"]
            rect = pymupdf.Rect(x * 72, y * 72, (x + w) * 72, (y + h) * 72)
            padded = (rect + (-4, -4, 4, 4)) & page.rect
            if padded.is_empty or padded.width < 2 or padded.height < 2:
                continue
            pix = page.get_pixmap(matrix=pymupdf.Matrix(zoom, zoom), clip=padded, alpha=False)
            crop_name = f"crop-p{record['page']:02}-{record['slide_id']}-{record['role']}-{idx:02}.png"
            crop_path = crops_dir / crop_name
            pix.save(crop_path)

            with Image.open(crop_path) as img:
                gray = img.convert("L")
                extrema = gray.getextrema()
                stat = ImageStat.Stat(gray)
                min_l, max_l = extrema if extrema else (255, 255)
                mean_l = round(stat.mean[0], 1)
                contrast = round((max_l + 12.75) / (min_l + 12.75), 2)

            lines = [
                line
                for block in page.get_text("dict", clip=rect)["blocks"]
                if "lines" in block
                for line in block["lines"]
                if rect.y0 <= (line["bbox"][1] + line["bbox"][3]) / 2 <= rect.y1
            ]
            min_clearance_pt = None
            if lines and not record.get("template"):
                clearances = [
                    min(
                        line["bbox"][0] - rect.x0,
                        rect.x1 - line["bbox"][2],
                        line["bbox"][1] - rect.y0,
                        rect.y1 - line["bbox"][3],
                    )
                    for line in lines
                ]
                min_clearance_pt = round(min(clearances), 2)
                if min_clearance_pt < -1.5:
                    warnings.append({
                        "slide_id": record["slide_id"],
                        "role": record["role"],
                        "issue": f"4x audit: text approaches or crosses box edge (clearance {min_clearance_pt} pt)",
                    })

            if contrast < 2.0 and record.get("expected", "").strip():
                warnings.append({
                    "slide_id": record["slide_id"],
                    "role": record["role"],
                    "issue": f"4x audit: low luminance contrast ({contrast}:1) in rendered region",
                })

            crop_records.append({
                "page": record["page"],
                "slide_id": record["slide_id"],
                "role": record["role"],
                "crop": str(crop_path.relative_to(task)),
                "zoom": zoom,
                "contrast_ratio": contrast,
                "mean_luminance": mean_l,
                "min_clearance_pt": min_clearance_pt,
            })
            if record["role"] in ("headline", "math_image", "animation_image", "caption", "source"):
                crop_images.append(crop_path)
                crop_labels.append(f"p{record['page']} {record['slide_id']} · {record['role']} ({zoom:.0f}x)")

    sheet_path = directory / "critic-crops-sheet.png"
    if crop_images:
        cols, tile_w, header_h = 2, 640, 28
        tile_h = 200
        sheet = Image.new("RGB", (tile_w * cols, max(1, (tile_h + header_h) * math.ceil(len(crop_images) / cols))), "#f1f5f9")
        draw = ImageDraw.Draw(sheet)
        for i, (cpath, label) in enumerate(zip(crop_images, crop_labels)):
            cx, cy = (i % cols) * tile_w, (i // cols) * (tile_h + header_h)
            draw.text((cx + 10, cy + 6), label, fill="#0f172a")
            with Image.open(cpath) as cimg:
                scale = min((tile_w - 16) / max(1, cimg.width), (tile_h - 12) / max(1, cimg.height))
                nw, nh = max(1, round(cimg.width * scale)), max(1, round(cimg.height * scale))
                sheet.paste(cimg.resize((nw, nh)), (cx + 8, cy + header_h + (tile_h - nh) // 2))
        sheet.save(sheet_path)

    result = {
        "ok": len(warnings) == 0,
        "task_id": task.name,
        "preset": tokens.get("preset_id", "rvlab"),
        "zoom": zoom,
        "crops_count": len(crop_records),
        "crops_dir": str(crops_dir),
        "critic_sheet": str(sheet_path) if crop_images else None,
        "warnings": warnings,
        "crops": crop_records,
    }
    (directory / "critic-audit.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    return result
