#!/usr/bin/env python3
"""Render CBAA module drafts (Word XML, .docx) and table files (.xlsx) as annotated text.

The drafts carry meaning in formatting, so the output keeps it as inline markup:

  «...»          red run: embedded variable
  [[...]]        blue run: referenced object
  {hl:...}       highlighted run: variation letter
  ~              paragraph whose text is mostly grey: optional or conditional clause
  ## ...         paragraph with a Heading style
  ⟨EN ...⟩       endnote text (variable id, name, population method)
  ⟨FN id: ...⟩   footnote text
  ⟪Cid: ...⟫     comment anchored in the preceding paragraph
  <table> | .. | Word table rows

Spreadsheets render one line per non-empty row (`rN: cell | cell`) plus cell comments.

Standard library only. Usage: cbaa_extract.py SOURCE... -o OUTDIR
"""
import argparse
import os
import re
import sys
import zipfile
import xml.etree.ElementTree as ET

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
W03 = "http://schemas.microsoft.com/office/word/2003/wordml"
AML = "http://schemas.microsoft.com/aml/2001/core"
PKG = "http://schemas.microsoft.com/office/2006/xmlPackage"

VARIABLE_COLOURS = {"EE0000", "FF0000"}
REFERENCE_COLOUR = "0000FF"
OPTIONAL_COLOUR = "808080"
OPTIONAL_THRESHOLD = 0.6


def q(tag):
    return f"{{{W}}}{tag}"


def plain(el):
    return "".join(t.text or "" for t in el.iter(q("t")))


def paragraphs_text(el, sep):
    return sep.join(x for x in (plain(p).strip() for p in el.iter(q("p"))) if x)


class WordDoc:
    """The parts of a Word document the renderer needs, independent of container format."""

    def __init__(self, document, footnotes=None, endnotes=None, comments=None, styles=None):
        self.body = document.find(q("body"))
        self.footnotes = footnotes or {}
        self.endnotes = endnotes or {}
        self.comments = comments or {}
        self.styles = styles or {}

    @classmethod
    def from_parts(cls, parts):
        def notes(name, tag):
            root = parts.get(name)
            if root is None:
                return {}
            return {n.get(q("id")): paragraphs_text(n, " ") for n in root.findall(q(tag))}

        comments = {}
        if (root := parts.get("word/comments.xml")) is not None:
            comments = {c.get(q("id")): paragraphs_text(c, " / ") for c in root.findall(q("comment"))}
        styles = {}
        if (root := parts.get("word/styles.xml")) is not None:
            for s in root.findall(q("style")):
                if (name := s.find(q("name"))) is not None:
                    styles[s.get(q("styleId"))] = name.get(q("val"))
        return cls(
            parts["word/document.xml"],
            footnotes=notes("word/footnotes.xml", "footnote"),
            endnotes=notes("word/endnotes.xml", "endnote"),
            comments=comments,
            styles=styles,
        )


WORD_PARTS = ("word/document.xml", "word/footnotes.xml", "word/endnotes.xml",
              "word/comments.xml", "word/styles.xml")


def load_flat_opc(path):
    root = ET.parse(path).getroot()
    parts = {}
    for part in root.findall(f"{{{PKG}}}part"):
        name = part.get(f"{{{PKG}}}name").lstrip("/")
        data = part.find(f"{{{PKG}}}xmlData")
        if name in WORD_PARTS and data is not None and len(data):
            parts[name] = data[0]
    return WordDoc.from_parts(parts)


def load_docx(path):
    with zipfile.ZipFile(path) as z:
        parts = {n: ET.fromstring(z.read(n)) for n in WORD_PARTS if n in z.namelist()}
    return WordDoc.from_parts(parts)


def load_wordml_2003(path):
    """WordML 2003 mirrors the 2006 element names, so remap its namespace and lift the
    inline notes and comments out into the reference markers the renderer expects."""
    with open(path, encoding="utf-8") as fh:
        root = ET.fromstring(fh.read().replace(W03, W))
    parent = {child: p for p in root.iter() for child in p}

    def replace(el, marker, ident):
        par = parent[el]
        idx = list(par).index(el)
        par.remove(el)
        ref = ET.Element(q(marker))
        ref.set(q("id"), ident)
        par.insert(idx, ref)

    footnotes, endnotes, comments = {}, {}, {}
    for tag, marker, store in (("footnote", "footnoteReference", footnotes),
                               ("endnote", "endnoteReference", endnotes)):
        for i, note in enumerate(list(root.iter(q(tag)))):
            ident = f"{tag}{i}"
            store[ident] = paragraphs_text(note, " ")
            replace(note, marker, ident)
    for ann in list(root.iter(f"{{{AML}}}annotation")):
        if ann.get(q("type")) == "Word.Comment":
            ident = ann.get(f"{{{AML}}}id")
            comments[ident] = paragraphs_text(ann, " / ")
            replace(ann, "commentRangeStart", ident)
    return WordDoc(root, footnotes=footnotes, endnotes=endnotes, comments=comments)


def load_word(path):
    if path.lower().endswith(".docx"):
        return load_docx(path)
    with open(path, encoding="utf-8") as fh:
        head = fh.read(400)
    return load_wordml_2003(path) if "<w:wordDocument" in head else load_flat_opc(path)


def run_style(run):
    rpr = run.find(q("rPr"))
    if rpr is None:
        return "", None
    colour = rpr.find(q("color"))
    highlight = rpr.find(q("highlight"))
    return ((colour.get(q("val")) if colour is not None else "") or "").upper(), \
        highlight.get(q("val")) if highlight is not None else None


def run_text(run, doc):
    """Return the run's rendered text and the length of its own wording, which excludes
    inlined note text so notes do not skew the optional-clause (grey) ratio."""
    text, own = "", 0
    for ch in run:
        if ch.tag == q("t"):
            text += ch.text or ""
            own += len((ch.text or "").strip())
        elif ch.tag in (q("tab"), q("br")):
            text += " "
        elif ch.tag == q("footnoteReference"):
            ident = ch.get(q("id"))
            text += f"⟨FN {ident}: {doc.footnotes.get(ident, '')}⟩"
        elif ch.tag == q("endnoteReference"):
            text += f"⟨EN {doc.endnotes.get(ch.get(q('id')), '')}⟩"
    return text, own


def render_paragraph(p, doc):
    segments, grey, total, comment_ids = [], 0, 0, []
    for el in p.iter():
        if el.tag == q("commentRangeStart"):
            comment_ids.append(el.get(q("id")))
        elif el.tag == q("r"):
            text, n = run_text(el, doc)
            if not text:
                continue
            colour, highlight = run_style(el)
            total += n
            if colour == OPTIONAL_COLOUR:
                grey += n
            if highlight:
                text = f"{{hl:{text}}}"
            elif colour in VARIABLE_COLOURS:
                text = f"«{text}»"
            elif colour == REFERENCE_COLOUR:
                text = f"[[{text}]]"
            segments.append(text)
    text = "".join(segments).replace("»«", "").replace("]][[", "")
    text = re.sub(r"\s+", " ", text).strip()
    if not text and not comment_ids:
        return None
    prefix = "~ " if total and grey / total > OPTIONAL_THRESHOLD else ""
    ppr = p.find(q("pPr"))
    style_el = ppr.find(q("pStyle")) if ppr is not None else None
    if style_el is not None:
        style = doc.styles.get(style_el.get(q("val")), style_el.get(q("val")))
        if style.lower().startswith("heading"):
            prefix += "## "
    lines = [prefix + text]
    for ident in dict.fromkeys(comment_ids):
        if ident in doc.comments:
            lines.append(f"    ⟪C{ident}: {doc.comments[ident]}⟫")
    return "\n".join(lines)


CONTAINERS = {q("sdt"), q("sdtContent"), q("customXml"), q("sect"), q("sub-section"),
              "{http://schemas.microsoft.com/office/word/2003/auxHint}sect",
              "{http://schemas.microsoft.com/office/word/2003/auxHint}sub-section"}


def render_word(path):
    doc = load_word(path)
    out = []

    def walk(container):
        for el in container:
            if el.tag == q("p"):
                if (line := render_paragraph(el, doc)):
                    out.append(line)
            elif el.tag == q("tbl"):
                out.append("<table>")
                for tr in el.findall(q("tr")):
                    cells = []
                    for tc in tr.findall(q("tc")):
                        rendered = (render_paragraph(p, doc) for p in tc.iter(q("p")))
                        cells.append(" ".join(filter(None, rendered)).replace("\n", " "))
                    out.append("| " + " | ".join(cells) + " |")
                out.append("</table>")
            elif el.tag in CONTAINERS:
                walk(el)

    walk(doc.body)
    return "\n".join(out)


def local(tag):
    return tag.rsplit("}", 1)[-1]


def children(el, name):
    return [c for c in el if local(c.tag) == name]


def cell_text(el):
    return "".join(x.text or "" for x in el.iter() if local(x.tag) == "t")


def cell_position(ref):
    letters, row = re.match(r"([A-Z]+)(\d+)", ref).groups()
    col = 0
    for ch in letters:
        col = col * 26 + ord(ch) - 64
    return int(row), col


THREADED_BOILERPLATE = re.compile(r"^\[Threaded comment\].*?Comment:\s*", re.S)


def render_xlsx(path):
    """Parse sheet XML directly. The CBAA workbooks use a namespace variant that openpyxl
    does not load, so element names are matched without namespaces."""
    out = []
    with zipfile.ZipFile(path) as z:
        names = set(z.namelist())
        shared = []
        if "xl/sharedStrings.xml" in names:
            shared = [cell_text(si) for si in children(ET.fromstring(z.read("xl/sharedStrings.xml")), "si")]
        rels = {r.get("Id"): r.get("Target") for r in ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))}
        workbook = ET.fromstring(z.read("xl/workbook.xml"))
        for sheet in (e for e in workbook.iter() if local(e.tag) == "sheet"):
            rid = next(v for k, v in sheet.attrib.items() if local(k) == "id")
            target = rels[rid].lstrip("/")
            target = target if target.startswith("xl/") else "xl/" + target
            out.append(f"### sheet: {sheet.get('name')}")
            rows = {}
            for c in ET.fromstring(z.read(target)).iter():
                if local(c.tag) != "c":
                    continue
                v, inline = children(c, "v"), children(c, "is")
                if c.get("t") == "s" and v:
                    value = shared[int(v[0].text)]
                elif inline:
                    value = cell_text(inline[0])
                elif v:
                    value = v[0].text
                else:
                    continue
                if value:
                    row, col = cell_position(c.get("r"))
                    rows.setdefault(row, {})[col] = value.replace("\n", " / ")
            for row in sorted(rows):
                out.append(f"r{row}: " + " | ".join(rows[row][c] for c in sorted(rows[row])))
            sheet_rels = target.replace("worksheets/", "worksheets/_rels/") + ".rels"
            if sheet_rels in names:
                for rel in ET.fromstring(z.read(sheet_rels)):
                    if "comments" not in rel.get("Target", ""):
                        continue
                    part = os.path.normpath(os.path.join(os.path.dirname(target), rel.get("Target")))
                    if part not in names:
                        continue
                    for cm in ET.fromstring(z.read(part)).iter():
                        if local(cm.tag) == "comment":
                            text = THREADED_BOILERPLATE.sub("", cell_text(cm).strip())
                            text = re.sub(r"\s+", " ", text)
                            out.append(f"  ⟪{cm.get('ref')}: {text}⟫")
    return "\n".join(out)


RENDERERS = {".xml": render_word, ".docx": render_word, ".xlsx": render_xlsx}


def sources(paths):
    for path in paths:
        if os.path.isdir(path):
            for name in sorted(os.listdir(path)):
                yield os.path.join(path, name)
        else:
            yield path


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("sources", nargs="+", help="files or directories")
    parser.add_argument("-o", "--out", required=True, help="output directory")
    args = parser.parse_args(argv)
    os.makedirs(args.out, exist_ok=True)
    failed = 0
    for path in sources(args.sources):
        render = RENDERERS.get(os.path.splitext(path)[1].lower())
        if render is None:
            continue
        name = os.path.basename(path)
        try:
            text = render(path)
        except Exception as exc:
            failed += 1
            print(f"FAILED  {name}: {exc}", file=sys.stderr)
            continue
        with open(os.path.join(args.out, name + ".txt"), "w", encoding="utf-8") as fh:
            fh.write(text)
        print(f"{len(text):>8}  {name}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
