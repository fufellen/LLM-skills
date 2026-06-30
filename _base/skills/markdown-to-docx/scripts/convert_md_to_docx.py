#!/usr/bin/env python3
"""Convert Markdown to DOCX with lightweight artifact sanitization.

Pandoc is preferred. A tiny stdlib-only DOCX writer exists as a fallback and
for smoke tests, so the skill can still validate its core artifact rule.
"""

from __future__ import annotations

import argparse
import html
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from datetime import datetime, timezone
from pathlib import Path


SUBSCRIPTS = {"0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "eff", "pi", "power"}
ARTIFACTS = [
    (re.compile(r"\\\s*\|"), "escaped Markdown pipe is visible"),
    (re.compile(r"\b(?:SiO|lambda|Lambda|k|n|L)_\{?(?:0|1|2|3|eff|pi|power)\}?"), "formula-like underscore is visible"),
    (re.compile(r"\$[^$\n]+\$"), "raw TeX inline math is visible"),
    (re.compile(r"!\[[^\]]*\]\([^)]+\)"), "raw Markdown image syntax is visible"),
]


def args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Convert Markdown to DOCX.")
    p.add_argument("input_md", nargs="?")
    p.add_argument("-o", "--output")
    p.add_argument("--reference-doc")
    p.add_argument("--method", choices=["auto", "pandoc", "basic"], default="auto")
    p.add_argument("--keep-sanitized", action="store_true")
    p.add_argument("--strict", action="store_true")
    p.add_argument("--no-subscript", action="store_true")
    p.add_argument("--self-test", action="store_true")
    return p.parse_args()


def sanitize_inline(text: str, subscript: bool = True) -> str:
    text = re.sub(r"\\\s*\|", " |", text)
    text = re.sub(r"\|\s*\\", "| ", text)
    text = re.sub(r" {2,}", " ", text)
    if not subscript:
        return text

    def repl(m: re.Match[str]) -> str:
        value = m.group(1).strip("{}")
        return f"<sub>{html.escape(value)}</sub>" if value in SUBSCRIPTS or value.isdigit() else m.group(0)

    return re.sub(r"(?<=[A-Za-z0-9)\]])_\{?([A-Za-z0-9]+)\}?", repl, text)


def sanitize_markdown(text: str, subscript: bool = True) -> str:
    lines = []
    in_code = False
    for line in text.splitlines():
        if line.lstrip().startswith("```"):
            in_code = not in_code
            lines.append(line)
        elif in_code:
            lines.append(line)
        else:
            lines.append(sanitize_inline(line, subscript=subscript))
    return "\n".join(lines) + ("\n" if text.endswith("\n") else "")


def scan_text(text: str) -> list[str]:
    return [message for pattern, message in ARTIFACTS if pattern.search(text)]


def has_pandoc() -> bool:
    return shutil.which("pandoc") is not None


def run_pandoc(md: Path, output: Path, reference_doc: str | None) -> None:
    cmd = [
        "pandoc",
        str(md),
        "--from",
        "gfm+raw_html",
        "--to",
        "docx",
        "--standalone",
        "--wrap=none",
        "--resource-path",
        os.pathsep.join([str(md.parent), os.getcwd()]),
        "--output",
        str(output),
    ]
    if reference_doc:
        cmd.extend(["--reference-doc", reference_doc])
    subprocess.run(cmd, check=True)


def w_t(text: str) -> str:
    space = ' xml:space="preserve"' if text.startswith(" ") or text.endswith(" ") else ""
    return f"<w:t{space}>{html.escape(text, quote=False)}</w:t>"


def w_r(text: str, *, sub: bool = False, mono: bool = False, bold: bool = False) -> str:
    props = []
    if mono:
        props.append('<w:rFonts w:ascii="Courier New" w:hAnsi="Courier New"/>')
    if bold:
        props.append("<w:b/>")
    if sub:
        props.append('<w:vertAlign w:val="subscript"/>')
    rpr = f"<w:rPr>{''.join(props)}</w:rPr>" if props else ""
    return f"<w:r>{rpr}{w_t(text)}</w:r>"


def runs(text: str, *, mono: bool = False, bold: bool = False) -> str:
    text = re.sub(r"!\[([^\]]*)\]\([^)]+\)", r"[Figure: \1]", text)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r"\1 (\2)", text)
    text = text.replace("**", "").replace("__", "")
    out = []
    pos = 0
    for m in re.finditer(r"<sub>(.*?)</sub>|(?<=[A-Za-z0-9)\]])_\{?([A-Za-z0-9]+)\}?", text):
        if m.start() > pos:
            out.append(w_r(text[pos:m.start()], mono=mono, bold=bold))
        value = html.unescape(m.group(1) if m.group(1) is not None else m.group(2))
        if m.group(1) is not None or value in SUBSCRIPTS or value.isdigit():
            out.append(w_r(value, sub=True, mono=mono, bold=bold))
        else:
            out.append(w_r(m.group(0), mono=mono, bold=bold))
        pos = m.end()
    if pos < len(text):
        out.append(w_r(text[pos:], mono=mono, bold=bold))
    return "".join(out) or w_r("")


def para(text: str, style: str | None = None, *, center: bool = False, mono: bool = False, bold: bool = False) -> str:
    ppr = []
    if style:
        ppr.append(f'<w:pStyle w:val="{style}"/>')
    if center:
        ppr.append('<w:jc w:val="center"/>')
    return f"<w:p>{'<w:pPr>' + ''.join(ppr) + '</w:pPr>' if ppr else ''}{runs(text, mono=mono, bold=bold)}</w:p>"


def is_table_sep(line: str) -> bool:
    return bool(re.match(r"^\s*\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)+\|?\s*$", line))


def table(rows: list[list[str]]) -> str:
    borders = '<w:top w:val="single" w:sz="4" w:space="0" w:color="auto"/><w:left w:val="single" w:sz="4" w:space="0" w:color="auto"/><w:bottom w:val="single" w:sz="4" w:space="0" w:color="auto"/><w:right w:val="single" w:sz="4" w:space="0" w:color="auto"/><w:insideH w:val="single" w:sz="4" w:space="0" w:color="auto"/><w:insideV w:val="single" w:sz="4" w:space="0" w:color="auto"/>'
    parts = [f'<w:tbl><w:tblPr><w:tblW w:w="0" w:type="auto"/><w:tblBorders>{borders}</w:tblBorders></w:tblPr>']
    for i, row in enumerate(rows):
        parts.append("<w:tr>")
        for cell in row:
            parts.append(f'<w:tc><w:tcPr><w:tcW w:w="2400" w:type="dxa"/></w:tcPr>{para(cell, bold=i == 0)}</w:tc>')
        parts.append("</w:tr>")
    parts.append("</w:tbl>")
    return "".join(parts)


def blocks(md: str) -> list[str]:
    lines = md.splitlines()
    out: list[str] = []
    i = 0
    in_code = False
    code: list[str] = []
    while i < len(lines):
        raw = lines[i]
        s = raw.strip()
        if s.startswith("```"):
            if in_code:
                out.append(para("\n".join(code), "Code", mono=True))
                code = []
            in_code = not in_code
            i += 1
            continue
        if in_code:
            code.append(raw)
            i += 1
            continue
        if not s:
            i += 1
            continue
        if i + 1 < len(lines) and "|" in raw and is_table_sep(lines[i + 1]):
            rows = [[c.strip() for c in raw.strip().strip("|").split("|")]]
            i += 2
            while i < len(lines) and "|" in lines[i] and lines[i].strip():
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            out.append(table(rows))
            continue
        h = re.match(r"^(#{1,6})\s+(.+)$", s)
        if h:
            out.append(para(h.group(2), f"Heading{min(len(h.group(1)), 3)}"))
        elif re.match(r"^[-*+]\s+(.+)$", s):
            out.append(para(re.sub(r"^[-*+]\s+", "", s), "ListBullet"))
        elif re.match(r"^\d+[.)]\s+(.+)$", s):
            out.append(para(re.sub(r"^\d+[.)]\s+", "", s), "ListNumber"))
        elif re.match(r"^(Fig\.|Figure|Table)\s+\d+", s, re.I):
            out.append(para(s, "Caption", center=True))
        else:
            out.append(para(s))
        i += 1
    if code:
        out.append(para("\n".join(code), "Code", mono=True))
    return out


def styles() -> str:
    return """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/><w:qFormat/><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:sz w:val="20"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/><w:basedOn w:val="Normal"/><w:rPr><w:b/><w:sz w:val="28"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Heading2"><w:name w:val="heading 2"/><w:basedOn w:val="Normal"/><w:rPr><w:b/><w:sz w:val="24"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Heading3"><w:name w:val="heading 3"/><w:basedOn w:val="Normal"/><w:rPr><w:b/><w:sz w:val="22"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Caption"><w:name w:val="caption"/><w:basedOn w:val="Normal"/><w:rPr><w:i/><w:sz w:val="18"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="ListBullet"><w:name w:val="List Bullet"/><w:basedOn w:val="Normal"/><w:pPr><w:ind w:left="720" w:hanging="360"/></w:pPr></w:style>
<w:style w:type="paragraph" w:styleId="ListNumber"><w:name w:val="List Number"/><w:basedOn w:val="Normal"/><w:pPr><w:ind w:left="720" w:hanging="360"/></w:pPr></w:style>
<w:style w:type="paragraph" w:styleId="Code"><w:name w:val="Code"/><w:basedOn w:val="Normal"/><w:rPr><w:rFonts w:ascii="Courier New" w:hAnsi="Courier New"/><w:sz w:val="18"/></w:rPr></w:style>
</w:styles>"""


def basic_docx(md: str, output: Path) -> None:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    body = "".join(blocks(md))
    files = {
        "[Content_Types].xml": '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/><Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/><Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/></Types>',
        "_rels/.rels": '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/><Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/></Relationships>',
        "word/_rels/document.xml.rels": '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"/>',
        "word/styles.xml": styles(),
        "word/document.xml": f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:body>{body}<w:sectPr><w:pgSz w:w="11906" w:h="16838"/><w:pgMar w:top="1080" w:right="1080" w:bottom="1080" w:left="1080" w:header="720" w:footer="720" w:gutter="0"/></w:sectPr></w:body></w:document>',
        "docProps/core.xml": f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><dc:creator>markdown-to-docx</dc:creator><cp:lastModifiedBy>markdown-to-docx</cp:lastModifiedBy><dcterms:created xsi:type="dcterms:W3CDTF">{now}</dcterms:created><dcterms:modified xsi:type="dcterms:W3CDTF">{now}</dcterms:modified></cp:coreProperties>',
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as z:
        for name, data in files.items():
            z.writestr(name, data.encode("utf-8"))


def scan_docx(path: Path) -> list[str]:
    try:
        with zipfile.ZipFile(path) as z:
            xml = z.read("word/document.xml").decode("utf-8", errors="replace")
    except Exception as exc:
        return [f"could not inspect DOCX: {exc}"]
    return scan_text(xml)


def convert(ns: argparse.Namespace) -> int:
    if not ns.input_md:
        raise SystemExit("input_md is required unless --self-test is used")
    src = Path(ns.input_md)
    out = Path(ns.output) if ns.output else src.with_suffix(".docx")
    original = src.read_text(encoding="utf-8")
    sanitized = sanitize_markdown(original, subscript=not ns.no_subscript)
    if ns.keep_sanitized:
        out.with_suffix(".sanitized.md").write_text(sanitized, encoding="utf-8")
    warnings = scan_text(original)
    if warnings:
        print("Preflight warnings:")
        for warning in warnings:
            print(f"- {warning}")
    use_pandoc = ns.method == "pandoc" or (ns.method == "auto" and has_pandoc())
    if use_pandoc:
        if not has_pandoc():
            raise SystemExit("Pandoc was not found on PATH")
        with tempfile.TemporaryDirectory(prefix="md_to_docx_") as tmp:
            tmp_md = Path(tmp) / src.name
            tmp_md.write_text(sanitized, encoding="utf-8")
            run_pandoc(tmp_md, out, ns.reference_doc)
    else:
        if ns.reference_doc:
            print("Warning: --reference-doc is ignored by --method basic", file=sys.stderr)
        basic_docx(sanitized, out)
    docx_warnings = scan_docx(out)
    if docx_warnings:
        print("DOCX QA warnings:")
        for warning in docx_warnings:
            print(f"- {warning}")
        return 2 if ns.strict else 0
    print(f"Wrote {out}")
    return 0


def self_test() -> int:
    sample = "# Test\n\nair\\ |\\ PCM\\ |\\ SiO_2,\n\nFig. 1. Two-step workflow.\n\n| Metric | Value |\n| --- | --- |\n| L_pi | 1.2 |\n"
    with tempfile.TemporaryDirectory(prefix="md_to_docx_selftest_") as tmp:
        md = Path(tmp) / "sample.md"
        docx = Path(tmp) / "sample.docx"
        md.write_text(sample, encoding="utf-8")
        code = convert(argparse.Namespace(input_md=str(md), output=str(docx), reference_doc=None, method="basic", keep_sanitized=True, strict=True, no_subscript=False))
        if code:
            return code
        with zipfile.ZipFile(docx) as z:
            xml = z.read("word/document.xml").decode("utf-8")
        if r"\ |" in xml or "SiO_2" in xml or 'w:val="subscript"' not in xml:
            print("Self-test failed: artifact survived in document.xml", file=sys.stderr)
            return 2
    print("Self-test passed")
    return 0


def main() -> int:
    ns = args()
    return self_test() if ns.self_test else convert(ns)


if __name__ == "__main__":
    raise SystemExit(main())
