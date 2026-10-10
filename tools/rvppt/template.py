"""Extract the original template and append fixed RVLAB/Pandoc layouts."""

import argparse
from copy import deepcopy
import hashlib
import json
import posixpath
from pathlib import Path
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


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load_tokens(design=ROOT / "DESIGN.md"):
    text = Path(design).read_text(encoding="utf-8")
    tokens = yaml.safe_load(text.split("```yaml\n", 1)[1].split("```", 1)[0])
    if tokens["schema_version"] != 1:
        raise ValueError("Unsupported design token schema")
    for key in ("title", "header_rule", "body"):
        x, y, w, h = tokens["geometry_in"][key]
        if min(x, y) < 0 or min(w, h) <= 0 or x + w > 10 or y + h > 7.5:
            raise ValueError(f"Invalid fixed geometry: {key}")
    return tokens


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
    parser.parse_args()
    tokens = load_tokens()
    manifest = build_reference(ROOT / tokens["source"]["path"], ROOT / tokens["reference"], tokens)
    target = ROOT / "docs/design/template-manifest.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Reference generated: {tokens['reference']} (1 master, 13 layouts, 0 specimen slides)")
    print(f"Original preserved: {manifest['source']['sha256']}")


if __name__ == "__main__":
    main()
