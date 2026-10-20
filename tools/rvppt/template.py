"""Extract the original template and append fixed RVLAB/Pandoc or multi-preset layouts."""

import argparse
from copy import deepcopy
import hashlib
import json
import posixpath
from pathlib import Path
import re
import shutil
import tempfile
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

from lxml import etree
from pptx import Presentation
import yaml

ROOT = Path(__file__).resolve().parents[2]
NS = {
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "rel": "http://schemas.openxmlformats.org/package/2006/relationships",
    "ct": "http://schemas.openxmlformats.org/package/2006/content-types",
}
EMU = 914400
PRESET_ID_PATTERN = re.compile(r"[a-z0-9][a-z0-9-]{0,40}\Z")


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load_tokens(design=ROOT / "DESIGN.md", preset=None):
    if preset and preset != "rvlab" and Path(design).resolve() == (ROOT / "DESIGN.md").resolve():
        if not PRESET_ID_PATTERN.fullmatch(str(preset)):
            raise ValueError(f"Invalid preset ID: {preset}")
        preset_path = ROOT / "templates/presets" / f"{preset}.yaml"
        if not preset_path.is_file():
            raise ValueError(f"Unknown design preset: {preset} (run `pptgen presets` to list available presets)")
        tokens = yaml.safe_load(preset_path.read_text(encoding="utf-8"))
    else:
        text = Path(design).read_text(encoding="utf-8")
        raw = text.split("```yaml\n", 1)[1].split("```", 1)[0] if "```yaml\n" in text else text
        tokens = yaml.safe_load(raw)
    if not isinstance(tokens, dict) or tokens.get("schema_version") != 1:
        raise ValueError("Unsupported design token schema")
    tokens.setdefault("preset_id", preset or tokens.get("preset_id", "rvlab"))
    width_in = float(tokens["slide"]["width_in"])
    height_in = float(tokens["slide"]["height_in"])
    for key in ("title", "header_rule", "body"):
        x, y, w, h = tokens["geometry_in"][key]
        if min(x, y) < 0 or min(w, h) <= 0 or x + w > width_in + 1e-3 or y + h > height_in + 1e-3:
            raise ValueError(f"Invalid fixed geometry: {key}")
    return tokens


def semantic_palette(preset="rvlab"):
    """Return shared visual roles as #RRGGBB, derived from the preset tokens."""
    palette = load_tokens(preset=preset)["palette"]
    roles = {
        role: "#" + palette[key].lstrip("#").upper()
        for role, key in {
            "accent": "primary", "band": "band", "secondary": "secondary",
            "ink": "text", "section_accent": "section_accent", "background": "background",
        }.items()
    }

    def blend(color, factor):
        background = roles["background"]
        channels = (
            round(int(color[i:i + 2], 16) * (1 - factor) + int(background[i:i + 2], 16) * factor)
            for i in (1, 3, 5)
        )
        return "#" + "".join(f"{channel:02X}" for channel in channels)

    # These blends retain the original RVLAB chart tint and neutral exactly.
    roles["tint"] = blend(roles["secondary"], 0.8)
    roles["neutral"] = blend(roles["ink"], 0.65)
    return roles


def list_presets(root=ROOT):
    presets_dir = Path(root) / "templates/presets"
    items = []
    if presets_dir.is_dir():
        for path in sorted(presets_dir.glob("*.yaml")):
            data = yaml.safe_load(path.read_text(encoding="utf-8"))
            if not isinstance(data, dict):
                continue
            ref = Path(root) / data.get("reference", "")
            items.append({
                "preset_id": data.get("preset_id", path.stem),
                "name": data.get("name", path.stem),
                "description": data.get("description", ""),
                "mode": data.get("mode", "preset"),
                "aspect": data["slide"]["aspect"],
                "slide_in": [data["slide"]["width_in"], data["slide"]["height_in"]],
                "palette": data["palette"],
                "reference": data.get("reference"),
                "reference_ready": ref.is_file(),
            })
    return {"presets": items, "count": len(items)}


def slots(tokens, count, body=None):
    if count not in (1, 2, 3, 4):
        raise ValueError("RVLAB supports 1/2/3/4 figure slots")
    x, y, w, h = body or tokens["geometry_in"]["body"]
    gap = tokens["geometry_in"]["gap"]
    columns, rows = (2, 2) if count == 4 else (count, 1)
    sw, sh = (w - gap * (columns - 1)) / columns, (h - gap * (rows - 1)) / rows
    return [(x + c * (sw + gap), y + r * (sh + gap), sw, sh)
            for r in range(rows) for c in range(columns)]


def parse(data):
    return etree.fromstring(data, etree.XMLParser(resolve_entities=False, no_network=True))


def xml(root):
    return etree.tostring(root, xml_declaration=True, encoding="UTF-8", standalone=True)


def extract_manifest(source):
    prs = Presentation(source)
    result = {
        "schema_version": 1,
        "source": {"path": f"templates/{Path(source).name}", "sha256": sha256(source)},
        "slide_emu": [prs.slide_width, prs.slide_height],
        "slide_inches": [prs.slide_width / EMU, prs.slide_height / EMU],
        "masters": len(prs.slide_masters), "specimen_slides": len(prs.slides),
        "layouts": [],
    }
    for layout in prs.slide_layouts:
        shapes = []
        for shape in layout.shapes:
            record = {"id": shape.shape_id, "name": shape.name,
                      "box_emu": [shape.left, shape.top, shape.width, shape.height]}
            if shape.is_placeholder:
                record["placeholder"] = {"idx": shape.placeholder_format.idx,
                                          "type": str(shape.placeholder_format.type)}
            if shape.has_text_frame:
                record["text"] = shape.text
            shapes.append(record)
        result["layouts"].append({"name": layout.name, "shapes": shapes})
    with ZipFile(source) as z:
        layouts = [parse(z.read(n)) for n in z.namelist() if n.startswith("ppt/slideLayouts/") and n.endswith(".xml")]
        result["layout_fonts"] = sorted({v for root in layouts for v in root.xpath(".//a:latin/@typeface | .//a:ea/@typeface", namespaces=NS)})
        result["layout_direct_colors"] = sorted({v for root in layouts for v in root.xpath(".//a:srgbClr/@val", namespaces=NS)})
        result["themes"] = {
            n: {etree.QName(e).localname: [dict(c.attrib) for c in e]
                for e in parse(z.read(n)).xpath(".//a:clrScheme/*", namespaces=NS)}
            for n in z.namelist() if n.startswith("ppt/theme/") and n.endswith(".xml")
        }
    return result


def set_box(shape, box):
    xfrm = shape.find("p:spPr/a:xfrm", NS)
    off, ext = xfrm.find("a:off", NS), xfrm.find("a:ext", NS)
    values = [str(round(v * EMU)) for v in box]
    off.set("x", values[0]); off.set("y", values[1])
    ext.set("cx", values[2]); ext.set("cy", values[3])


def placeholder(shape):
    return shape.find("p:nvSpPr/p:nvPr/p:ph", NS)


def set_text_style(shape, size, color, tokens, *, center=False, bullets=False):
    body = shape.find("p:txBody", NS)
    body_pr = body.find("a:bodyPr", NS)
    body_pr.attrib.update({"lIns": "0", "rIns": "0", "tIns": str(round(tokens["text_top_inset_pt"] * 12700)), "bIns": "0", "anchor": "t", "wrap": "square"})
    for child in list(body_pr):
        body_pr.remove(child)
    etree.SubElement(body_pr, f"{{{NS['a']}}}noAutofit")
    style = body.find("a:lstStyle", NS)
    style.clear()
    for level in range(1, 10):
        p = etree.SubElement(style, f"{{{NS['a']}}}lvl{level}pPr", algn="ctr" if center else "l")
        if bullets:
            p.set("marL", str(228600 * min(level, 2)))
            p.set("indent", "-152400")
        spacing = etree.SubElement(p, f"{{{NS['a']}}}lnSpc")
        etree.SubElement(spacing, f"{{{NS['a']}}}spcPct", val="100000")
        if bullets:
            after = etree.SubElement(p, f"{{{NS['a']}}}spcAft")
            etree.SubElement(after, f"{{{NS['a']}}}spcPts", val="1000")
            etree.SubElement(p, f"{{{NS['a']}}}buChar", char="▪" if level == 1 else "•")
        else:
            etree.SubElement(p, f"{{{NS['a']}}}buNone")
        r = etree.SubElement(p, f"{{{NS['a']}}}defRPr", sz=str(int((size if level == 1 else min(size, tokens['sizes_pt']['secondary'])) * 100)))
        fill = etree.SubElement(r, f"{{{NS['a']}}}solidFill")
        etree.SubElement(fill, f"{{{NS['a']}}}srgbClr", val=color)
        etree.SubElement(r, f"{{{NS['a']}}}latin", typeface=tokens["fonts"]["latin"])
        etree.SubElement(r, f"{{{NS['a']}}}ea", typeface=tokens["fonts"]["korean"])
    for paragraph in body.findall("a:p", NS):
        body.remove(paragraph)
    etree.SubElement(body, f"{{{NS['a']}}}p")
    shape.find("p:nvSpPr/p:cNvSpPr", NS).attrib.pop("txBox", None)


def content_layout(base, name, count, tokens):
    root = deepcopy(base)
    root.set("type", "obj"); root.set("preserve", "1")
    root.find("p:cSld", NS).set("name", name)
    tree = root.find("p:cSld/p:spTree", NS)
    shapes = tree.findall("p:sp", NS)
    title = next(s for s in shapes if placeholder(s) is not None and placeholder(s).get("type") == "title")
    body = next(s for s in shapes if placeholder(s) is not None and placeholder(s).get("idx") == "1")
    # The white title box masks the rule behind it; RVLAB decks widen it to this fixed tab.
    set_box(title, tokens["geometry_in"]["title"])
    tree.remove(body)
    for idx, box in enumerate(slots(tokens, count), 1):
        cell = deepcopy(body)
        ph = placeholder(cell)
        ph.attrib.clear(); ph.set("idx", str(idx))
        # Pandoc recognizes object placeholders only when the type attribute is absent.
        props = cell.find("p:nvSpPr/p:cNvPr", NS)
        props.set("id", str(100 + idx)); props.set("name", f"RVLAB Content {idx}")
        set_box(cell, box)
        set_text_style(cell, tokens["sizes_pt"]["headline" if count == 1 else "columns"], tokens["palette"]["text"], tokens, bullets=True)
        tree.append(cell)
    if name == "Blank":
        for s in list(tree.findall("p:sp", NS)):
            if placeholder(s) is not None and placeholder(s).get("type") not in ("sldNum", "ftr"):
                tree.remove(s)
    return root


def validate_package(path):
    """Check internal relationships and XML before replacing a good reference."""
    with ZipFile(path) as z:
        names = set(z.namelist())
        if z.testzip() is not None:
            raise ValueError("Corrupt PPTX archive")
        for name in names:
            if name.endswith((".xml", ".rels")):
                root = parse(z.read(name))
                if name.endswith(".rels"):
                    base = posixpath.dirname(posixpath.dirname(name))
                    for rel in root:
                        if rel.get("TargetMode") == "External":
                            continue
                        target = rel.get("Target", "")
                        target = target.lstrip("/") if target.startswith("/") else posixpath.normpath(posixpath.join(base, target))
                        if target not in names:
                            raise ValueError(f"Missing PPTX relationship target: {name} → {target}")
        for override in parse(z.read("[Content_Types].xml")):
            if "PartName" in override.attrib and override.get("PartName").lstrip("/") not in names:
                raise ValueError("Missing content type part")
    return True


def _transform_xml_for_preset(root_el, tokens, sx, sy, *, strip_pics=True):
    palette = tokens["palette"]
    color_map = {
        "0070C0": palette["primary"].upper(),
        "053F95": palette["band"].upper(),
        "002060": palette["band"].upper(),
        "5B9BD5": palette["secondary"].upper(),
        "FFFF00": palette["section_accent"].upper(),
        "000000": palette["text"].upper(),
    }
    if strip_pics:
        for pic in list(root_el.xpath(".//p:pic", namespaces=NS)):
            parent = pic.getparent()
            if parent is not None:
                parent.remove(pic)
    if abs(sx - 1.0) > 1e-6 or abs(sy - 1.0) > 1e-6:
        for xfrm in root_el.xpath(".//p:sp/p:spPr/a:xfrm", namespaces=NS):
            off, ext = xfrm.find("a:off", NS), xfrm.find("a:ext", NS)
            if off is not None and "x" in off.attrib and "y" in off.attrib:
                off.set("x", str(round(int(off.get("x")) * sx)))
                off.set("y", str(round(int(off.get("y")) * sy)))
            if ext is not None and "cx" in ext.attrib and "cy" in ext.attrib:
                ext.set("cx", str(round(int(ext.get("cx")) * sx)))
                ext.set("cy", str(round(int(ext.get("cy")) * sy)))
    for clr in root_el.xpath(".//a:srgbClr", namespaces=NS):
        val = clr.get("val", "").upper()
        if val in color_map:
            clr.set("val", color_map[val])


def build_preset_reference(tokens, destination=None, base_source=ROOT / "templates/RVLAB_PPT양식.pptx"):
    """Build a reference PPTX for any 16:9 or 4:3 preset or custom registered template."""
    destination = Path(destination or (ROOT / tokens["reference"]))
    if tokens.get("preset_id", "rvlab") == "rvlab" and tokens.get("source", {}).get("path") == "templates/RVLAB_PPT양식.pptx":
        return build_reference(ROOT / tokens["source"]["path"], destination, tokens)
    base_source = Path(base_source)
    width_in = float(tokens["slide"]["width_in"])
    height_in = float(tokens["slide"]["height_in"])
    sx, sy = width_in / 10.0, height_in / 7.5
    with ZipFile(base_source) as z:
        parts = {
            n: z.read(n)
            for n in z.namelist()
            if not n.startswith(("ppt/slides/", "ppt/notesSlides/", "ppt/media/")) and n != "ppt/metadata"
        }
    presentation = parse(parts["ppt/presentation.xml"])
    for e in presentation.findall("p:sldIdLst", NS):
        presentation.remove(e)
    sld_sz = presentation.find("p:sldSz", NS)
    if sld_sz is not None:
        sld_sz.set("cx", str(round(width_in * EMU)))
        sld_sz.set("cy", str(round(height_in * EMU)))
        if tokens["slide"].get("aspect") == "16:9":
            sld_sz.set("type", "screen16x9")
        elif tokens["slide"].get("aspect") == "4:3":
            sld_sz.set("type", "screen4x3")
        else:
            sld_sz.attrib.pop("type", None)
    parts["ppt/presentation.xml"] = xml(presentation)
    relationships = parse(parts["ppt/_rels/presentation.xml.rels"])
    for rel in list(relationships):
        if rel.get("Type", "").endswith(("/slide", "/presentationmetadata")):
            relationships.remove(rel)
    parts["ppt/_rels/presentation.xml.rels"] = xml(relationships)
    parts["docProps/core.xml"] = xml(etree.Element("{http://schemas.openxmlformats.org/package/2006/metadata/core-properties}coreProperties", nsmap={"cp": "http://schemas.openxmlformats.org/package/2006/metadata/core-properties"}))
    for name in list(parts):
        if name.endswith(".rels") and name.startswith(("ppt/slideLayouts/_rels/", "ppt/slideMasters/_rels/")):
            rels_root = parse(parts[name])
            for rel in list(rels_root):
                if rel.get("Type", "").endswith("/image"):
                    rels_root.remove(rel)
            parts[name] = xml(rels_root)
    master_path = "ppt/slideMasters/slideMaster1.xml"
    master = parse(parts[master_path])
    _transform_xml_for_preset(master, tokens, sx, sy, strip_pics=True)
    for theme_name in [n for n in parts if n.startswith("ppt/theme/") and n.endswith(".xml")]:
        theme_root = parse(parts[theme_name])
        _transform_xml_for_preset(theme_root, tokens, 1.0, 1.0, strip_pics=False)
        parts[theme_name] = xml(theme_root)
    ids = master.find("p:sldLayoutIdLst", NS)
    next_id = max(int(i.get("id")) for i in ids) + 1
    relpath = "ppt/slideMasters/_rels/slideMaster1.xml.rels"
    master_rels = parse(parts[relpath])
    existing_ids = {r.get("Id") for r in master_rels}
    originals = {}
    for i in range(1, 5):
        layout_name = f"ppt/slideLayouts/slideLayout{i}.xml"
        layout_root = parse(parts[layout_name])
        _transform_xml_for_preset(layout_root, tokens, sx, sy, strip_pics=True)
        parts[layout_name] = xml(layout_root)
        originals[i] = layout_root
    derivatives = []
    for src, name, typ in [(1, "Title Slide", "title"), (3, "Section Header", "secHead")]:
        layout = deepcopy(originals[src]); layout.set("type", typ); layout.set("preserve", "1")
        layout.find("p:cSld", NS).set("name", name)
        for shape in layout.findall("p:cSld/p:spTree/p:sp", NS):
            ph = placeholder(shape)
            if ph is not None and ph.get("type") == "ctrTitle" and src == 3:
                ph.set("type", "title")
        derivatives.append((src, layout))
    for name, count in [("Title and Content", 1), ("Two Content", 2), ("Comparison", 2), ("Content with Caption", 1), ("Blank", 1), ("RVLAB Figure Grid 3", 3), ("RVLAB Figure Grid 4", 4)]:
        derivatives.append((4, content_layout(originals[4], name, count, tokens)))
    types = parse(parts["[Content_Types].xml"])
    for idx, (src, layout) in enumerate(derivatives, 5):
        name = f"ppt/slideLayouts/slideLayout{idx}.xml"
        parts[name] = xml(layout)
        parts[f"ppt/slideLayouts/_rels/slideLayout{idx}.xml.rels"] = parts[f"ppt/slideLayouts/_rels/slideLayout{src}.xml.rels"]
        rid = f"rvlabLayout{idx}"
        if rid in existing_ids:
            raise ValueError("Duplicate relationship ID")
        etree.SubElement(master_rels, f"{{{NS['rel']}}}Relationship", Id=rid, Type=NS["r"] + "/slideLayout", Target=f"../slideLayouts/slideLayout{idx}.xml")
        etree.SubElement(ids, f"{{{NS['p']}}}sldLayoutId", id=str(next_id + idx - 5), attrib={f"{{{NS['r']}}}id": rid})
        etree.SubElement(types, f"{{{NS['ct']}}}Override", PartName="/" + name, ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml")
    for t in list(types):
        if t.get("PartName", "").lstrip("/") not in parts and t.get("PartName"):
            types.remove(t)
    parts[master_path] = xml(master)
    parts[relpath] = xml(master_rels)
    parts["[Content_Types].xml"] = xml(types)
    destination.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=destination.parent, suffix=".pptx", delete=False) as f:
        temporary = Path(f.name)
    try:
        with ZipFile(temporary, "w", ZIP_DEFLATED) as z:
            for name, data in sorted(parts.items()):
                info = ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
                info.compress_type = ZIP_DEFLATED
                z.writestr(info, data)
        validate_package(temporary)
        prs = Presentation(temporary)
        if len(prs.slides) != 0 or len(prs.slide_masters) != 1 or len(prs.slide_layouts) != 13:
            raise ValueError("Invalid derived reference structure")
        temporary.replace(destination)
    finally:
        temporary.unlink(missing_ok=True)
    return {"preset_id": tokens.get("preset_id"), "reference": str(destination.relative_to(ROOT) if destination.is_relative_to(ROOT) else destination), "slide_inches": [width_in, height_in]}


def ensure_preset_reference(tokens):
    ref_path = ROOT / tokens["reference"]
    if not ref_path.is_file():
        if tokens.get("preset_id", "rvlab") == "rvlab":
            raise ValueError("Reference missing: uv run python -m rvppt.template")
        build_preset_reference(tokens, ref_path)
    return ref_path


def register_template(source_pptx, preset_id, *, name=None, description=None, root=ROOT):
    """Inspect a user-supplied .pptx file and register it as a reusable design preset."""
    if not PRESET_ID_PATTERN.fullmatch(str(preset_id)) or preset_id == "rvlab":
        raise ValueError("Preset ID must be lowercase alphanumeric/hyphens and cannot overwrite 'rvlab'")
    source_path = Path(source_pptx).resolve()
    if not source_path.is_file() or source_path.suffix.lower() != ".pptx":
        raise ValueError(f"Template must be an existing .pptx file: {source_pptx}")
    manifest = extract_manifest(source_path)
    w_in = round(manifest["slide_inches"][0], 3)
    h_in = round(manifest["slide_inches"][1], 3)
    ratio = w_in / h_in
    aspect = "16:9" if abs(ratio - 16 / 9) < 0.05 else "4:3" if abs(ratio - 4 / 3) < 0.05 else f"{w_in}:{h_in}"
    custom_dir = Path(root) / "templates/custom"
    custom_dir.mkdir(parents=True, exist_ok=True)
    stored_pptx = custom_dir / f"{preset_id}.pptx"
    if source_path != stored_pptx.resolve():
        shutil.copy2(source_path, stored_pptx)
    manifest["source"] = {"path": f"templates/custom/{preset_id}.pptx", "sha256": sha256(stored_pptx)}
    (custom_dir / f"{preset_id}-manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")

    # Extract theme accent colors if present, falling back to clean defaults
    theme_colors = []
    for theme in manifest.get("themes", {}).values():
        for key in ("accent1", "dk2", "accent2", "accent3"):
            for item in theme.get(key, []):
                val = item.get("val", "")
                if re.fullmatch(r"[0-9A-Fa-f]{6}", val) and val.upper() not in ("FFFFFF", "000000"):
                    theme_colors.append(val.upper())
    for c in manifest.get("layout_direct_colors", []):
        if re.fullmatch(r"[0-9A-Fa-f]{6}", c) and c.upper() not in ("FFFFFF", "000000") and c.upper() not in theme_colors:
            theme_colors.append(c.upper())
    primary = theme_colors[0] if len(theme_colors) >= 1 else "1D4ED8"
    band = theme_colors[1] if len(theme_colors) >= 2 else primary
    secondary = theme_colors[2] if len(theme_colors) >= 3 else "60A5FA"

    base_tokens = load_tokens(preset="modern-16x9" if aspect == "16:9" else "minimal-4x3")
    sx, sy = w_in / base_tokens["slide"]["width_in"], h_in / base_tokens["slide"]["height_in"]
    tokens = deepcopy(base_tokens)
    tokens.update({
        "preset_id": preset_id,
        "name": name or f"Custom Template ({preset_id})",
        "description": description or f"Registered from {source_path.name} ({aspect}, {w_in}x{h_in} in)",
        "mode": "custom_template",
        "custom_source": manifest["source"],
        "reference": f"templates/presets/{preset_id}_reference.pptx",
        "slide": {"width_in": w_in, "height_in": h_in, "aspect": aspect, "masters": 1, "original_layouts": 4},
        "palette": {
            "primary": primary,
            "band": band,
            "secondary": secondary,
            "section_accent": "FACC15",
            "text": "0F172A",
            "background": "FFFFFF",
        },
        "geometry_in": {
            "title": [round(base_tokens["geometry_in"]["title"][0] * sx, 2), round(base_tokens["geometry_in"]["title"][1] * sy, 2), round(base_tokens["geometry_in"]["title"][2] * sx, 2), round(base_tokens["geometry_in"]["title"][3] * sy, 2)],
            "header_rule": [round(base_tokens["geometry_in"]["header_rule"][0] * sx, 2), round(base_tokens["geometry_in"]["header_rule"][1] * sy, 2), round(base_tokens["geometry_in"]["header_rule"][2] * sx, 2), round(base_tokens["geometry_in"]["header_rule"][3] * sy, 2)],
            "body": [round(base_tokens["geometry_in"]["body"][0] * sx, 2), round(base_tokens["geometry_in"]["body"][1] * sy, 2), round(base_tokens["geometry_in"]["body"][2] * sx, 2), round(base_tokens["geometry_in"]["body"][3] * sy, 2)],
            "content_indent": 0.25,
            "closing_title": [round(base_tokens["geometry_in"]["closing_title"][0] * sx, 2), round(base_tokens["geometry_in"]["closing_title"][1] * sy, 2), round(base_tokens["geometry_in"]["closing_title"][2] * sx, 2), round(base_tokens["geometry_in"]["closing_title"][3] * sy, 2)],
            "gap": base_tokens["geometry_in"]["gap"],
            "caption_height": base_tokens["geometry_in"]["caption_height"],
        },
    })
    preset_yaml = Path(root) / "templates/presets" / f"{preset_id}.yaml"
    preset_yaml.parent.mkdir(parents=True, exist_ok=True)
    preset_yaml.write_text(yaml.safe_dump(tokens, allow_unicode=True, sort_keys=False), encoding="utf-8", newline="\n")
    ref_path = Path(root) / tokens["reference"]
    build_preset_reference(tokens, ref_path, base_source=Path(root) / "templates/RVLAB_PPT양식.pptx")
    return {
        "preset_id": preset_id,
        "preset_yaml": str(preset_yaml),
        "reference": str(ref_path),
        "manifest": str(custom_dir / f"{preset_id}-manifest.json"),
        "slide_inches": [w_in, h_in],
        "aspect": aspect,
        "palette": tokens["palette"],
    }


def build_reference(source, destination, tokens):
    source, destination = Path(source), Path(destination)
    if source.resolve() == destination.resolve():
        raise ValueError("The original template cannot be overwritten")
    if sha256(source) != tokens["source"]["sha256"]:
        raise ValueError("Original template hash differs from DESIGN.md")
    manifest = extract_manifest(source)
    if manifest["slide_inches"] != [10, 7.5] or manifest["masters"] != 1 or len(manifest["layouts"]) != 4:
        raise ValueError("Unexpected original template structure")
    with ZipFile(source) as z:
        parts = {n: z.read(n) for n in z.namelist() if not n.startswith(("ppt/slides/", "ppt/notesSlides/")) and n != "ppt/metadata"}
    presentation = parse(parts["ppt/presentation.xml"])
    for e in presentation.findall("p:sldIdLst", NS):
        presentation.remove(e)
    parts["ppt/presentation.xml"] = xml(presentation)
    relationships = parse(parts["ppt/_rels/presentation.xml.rels"])
    for rel in list(relationships):
        if rel.get("Type", "").endswith(("/slide", "/presentationmetadata")):
            relationships.remove(rel)
    parts["ppt/_rels/presentation.xml.rels"] = xml(relationships)
    parts["docProps/core.xml"] = xml(etree.Element("{http://schemas.openxmlformats.org/package/2006/metadata/core-properties}coreProperties", nsmap={"cp": "http://schemas.openxmlformats.org/package/2006/metadata/core-properties"}))
    types = parse(parts["[Content_Types].xml"])
    for t in list(types):
        if t.get("PartName", "").lstrip("/") not in parts and t.get("PartName"):
            types.remove(t)
    master_path = "ppt/slideMasters/slideMaster1.xml"
    master = parse(parts[master_path])
    ids = master.find("p:sldLayoutIdLst", NS)
    next_id = max(int(i.get("id")) for i in ids) + 1
    relpath = "ppt/slideMasters/_rels/slideMaster1.xml.rels"
    master_rels = parse(parts[relpath])
    existing_ids = {r.get("Id") for r in master_rels}
    originals = {i: parse(parts[f"ppt/slideLayouts/slideLayout{i}.xml"]) for i in range(1, 5)}
    derivatives = []
    for src, name, typ in [(1, "Title Slide", "title"), (3, "Section Header", "secHead")]:
        layout = deepcopy(originals[src]); layout.set("type", typ); layout.set("preserve", "1")
        layout.find("p:cSld", NS).set("name", name)
        for shape in layout.findall("p:cSld/p:spTree/p:sp", NS):
            ph = placeholder(shape)
            if ph is not None and ph.get("type") == "ctrTitle" and src == 3:
                ph.set("type", "title")
        derivatives.append((src, layout))
    for name, count in [("Title and Content", 1), ("Two Content", 2), ("Comparison", 2), ("Content with Caption", 1), ("Blank", 1), ("RVLAB Figure Grid 3", 3), ("RVLAB Figure Grid 4", 4)]:
        derivatives.append((4, content_layout(originals[4], name, count, tokens)))
    for idx, (src, layout) in enumerate(derivatives, 5):
        name = f"ppt/slideLayouts/slideLayout{idx}.xml"
        parts[name] = xml(layout)
        parts[f"ppt/slideLayouts/_rels/slideLayout{idx}.xml.rels"] = parts[f"ppt/slideLayouts/_rels/slideLayout{src}.xml.rels"]
        rid = f"rvlabLayout{idx}"
        if rid in existing_ids:
            raise ValueError("Duplicate relationship ID")
        etree.SubElement(master_rels, f"{{{NS['rel']}}}Relationship", Id=rid, Type=NS["r"] + "/slideLayout", Target=f"../slideLayouts/slideLayout{idx}.xml")
        etree.SubElement(ids, f"{{{NS['p']}}}sldLayoutId", id=str(next_id + idx - 5), attrib={f"{{{NS['r']}}}id": rid})
        etree.SubElement(types, f"{{{NS['ct']}}}Override", PartName="/" + name, ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml")
    parts[master_path] = xml(master)
    parts[relpath] = xml(master_rels)
    parts["[Content_Types].xml"] = xml(types)
    destination.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=destination.parent, suffix=".pptx", delete=False) as f:
        temporary = Path(f.name)
    try:
        with ZipFile(temporary, "w", ZIP_DEFLATED) as z:
            for name, data in sorted(parts.items()):
                # Stable zip timestamps make regeneration byte reproducible.
                info = ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
                info.compress_type = ZIP_DEFLATED
                z.writestr(info, data)
        validate_package(temporary)
        prs = Presentation(temporary)
        if len(prs.slides) != 0 or len(prs.slide_masters) != 1 or len(prs.slide_layouts) != 13:
            raise ValueError("Invalid derived reference structure")
        temporary.replace(destination)
    finally:
        temporary.unlink(missing_ok=True)
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--preset", help="Optional preset ID to generate reference for (default: all presets)")
    args = parser.parse_args()
    tokens = load_tokens()
    manifest = build_reference(ROOT / tokens["source"]["path"], ROOT / tokens["reference"], tokens)
    target = ROOT / "docs/design/template-manifest.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(f"Reference generated: {tokens['reference']} (1 master, 13 layouts, 0 specimen slides)")
    print(f"Original preserved: {manifest['source']['sha256']}")
    for item in list_presets()["presets"]:
        pid = item["preset_id"]
        if pid == "rvlab":
            continue
        if args.preset and args.preset != pid:
            continue
        ptokens = load_tokens(preset=pid)
        build_preset_reference(ptokens)
        print(f"Preset reference generated: {ptokens['reference']} ({ptokens['slide']['aspect']})")


if __name__ == "__main__":
    main()
