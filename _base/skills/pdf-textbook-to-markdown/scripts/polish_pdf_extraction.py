#!/usr/bin/env python3
"""Polish a Markdown file extracted from a PDF into a clean, readable book.

Passes (in order):

1. **Mojibake fix**       — CP1251 bytes wrongly decoded as Latin-1
   ("×èñëî áðàêîâ" -> "Число браков"). Only tokens made entirely of
   Latin-1 accented chars are touched; ASCII prose is safe.
2. **PUA marker**         — custom-font glyphs (U+E000..U+F8FF) that Obsidian
   renders as replacement squares. Replaced with `⟨PUA U+XXXX⟩` so the user
   can spot and decide.
3. **Drop page images**   — remove auto-emitted `![Page N image](...)` embeds
   and the `### Page Images` sub-headings that group them. Extracted image
   files stay in `<stem>_media/`; the user can add specific embeds back.
4. **Mark broken tables** — long runs of very short lines (each PDF cell
   became a separate line) get an HTML-comment marker with page number and
   the original cell text saved to `<stem>.table-NNN.txt` sidecar.
5. **Strip running headers/footers** — any line that appears verbatim in
   many pages (chapter titles, book title, section labels) plus pure-number
   pagination lines are removed.
6. **Drop page markers**  — `## Page N` headings and `<!-- source-page: N -->`
   comments are removed once tables and headers no longer need them.
7. **Reflow paragraphs**  — join wrapped lines inside a paragraph into one
   line; unwrap soft hyphens ("слово-\\nостаток" -> "словоостаток") only
   when the tail starts with a lowercase letter, otherwise keep the dash.

Usage:
    python cleanup_pdf_extraction.py <file.md> [<source.pdf>]

If the source PDF is given, its top-level outline entries are inserted as
`## Chapter …` headings at the position of the matching page marker (which
happens BEFORE page markers are stripped). Downstream tools (e.g. a
chapter splitter) can then split by these headings.

Rewrites in place. Writes `<file.md>.cleanup.json` summary. Idempotent —
safe to re-run.
"""
from __future__ import annotations
import json, re, sys
from pathlib import Path

# --- 1. Mojibake ------------------------------------------------------------
# A token is a run of non-whitespace chars. It's a mojibake candidate iff
# every char is either an accented Latin-1 letter (0x80..0xFF) or ASCII
# punctuation typical to Russian text. Pure ASCII words are skipped.
LATIN1_ACCENT_RE = re.compile(r"[ -ÿ]")
_TOKEN_RE = re.compile(r"\S+")

# Chars we allow inside a mojibake candidate token besides Latin-1 diacritics.
_ALLOWED_PUNCT = set(",.;:!?()[]{}\"'—–-«»…/\\")

def _looks_like_mojibake(tok: str) -> bool:
    # need at least 2 Latin-1 accented chars
    accents = sum(1 for c in tok if 0x80 <= ord(c) <= 0xFF and not c.isspace())
    if accents < 2:
        return False
    for c in tok:
        o = ord(c)
        if 0x80 <= o <= 0xFF:
            continue
        if c in _ALLOWED_PUNCT or c.isdigit():
            continue
        return False
    return True

def _demojibake(tok: str) -> str | None:
    try:
        raw = tok.encode("latin-1")
    except UnicodeEncodeError:
        return None
    try:
        fixed = raw.decode("cp1251")
    except UnicodeDecodeError:
        return None
    # Sanity: fixed should have Cyrillic chars
    if not re.search(r"[Ѐ-ӿ]", fixed):
        return None
    return fixed

def fix_mojibake(text: str) -> tuple[str, int]:
    fixed_count = 0
    def repl(m: re.Match) -> str:
        nonlocal fixed_count
        tok = m.group(0)
        if not _looks_like_mojibake(tok):
            return tok
        f = _demojibake(tok)
        if f is None:
            return tok
        fixed_count += 1
        return f
    new_text = _TOKEN_RE.sub(repl, text)
    return new_text, fixed_count

# --- 2. Private Use Area ----------------------------------------------------
def mark_pua(text: str) -> tuple[str, dict[str, int]]:
    counts: dict[str, int] = {}
    def repl(m: re.Match) -> str:
        c = m.group(0)
        key = "U+{:04X}".format(ord(c))
        counts[key] = counts.get(key, 0) + 1
        return f"⟨PUA {key}⟩"
    new_text = re.sub(r"[-]", repl, text)
    return new_text, counts

# --- 3. Repeating running headers / footers --------------------------------
# For each PDF page (between two `<!-- source-page: N -->` markers), split into
# non-empty stripped lines. Count how many *pages* each line appears in.
# Any line appearing in >= threshold pages is a running header/footer/pagenumber
# and gets stripped.

def strip_running_headers(text: str, page_threshold: int = 5) -> tuple[str, dict]:
    page_re = re.compile(r"<!--\s*source-page:\s*(\d+)\s*-->")
    pages: list[tuple[int, int, int]] = []  # (page_num, start_pos, end_pos)
    marks = list(page_re.finditer(text))
    for i, m in enumerate(marks):
        start = m.end()
        end = marks[i + 1].start() if i + 1 < len(marks) else len(text)
        pages.append((int(m.group(1)), start, end))

    # Count line occurrences across pages (uniquely per page).
    per_line_page_count: dict[str, int] = {}
    for _, start, end in pages:
        seen = set()
        for ln in text[start:end].split("\n"):
            s = ln.strip()
            if not s or len(s) > 120:
                continue
            if s.startswith("#") or s.startswith("<!--") or s.startswith(">"):
                continue
            if s in seen:
                continue
            seen.add(s)
            per_line_page_count[s] = per_line_page_count.get(s, 0) + 1

    running = {ln for ln, n in per_line_page_count.items() if n >= page_threshold}
    # Also strip pure-numeric "page number" lines (1-4 digits alone).
    def is_pagenum(s: str) -> bool:
        return bool(re.fullmatch(r"\d{1,4}", s))

    stripped = 0
    new_lines: list[str] = []
    for ln in text.split("\n"):
        s = ln.strip()
        if s and (s in running or is_pagenum(s)):
            stripped += 1
            continue
        new_lines.append(ln)
    return "\n".join(new_lines), {
        "stripped_lines": stripped,
        "running_headers_detected": sorted(running)[:50],
        "running_headers_total": len(running),
    }

# --- Drop auto-emitted page-image embeds -----------------------------------

def drop_page_images(text: str) -> tuple[str, int]:
    """Remove `### Page Images` sections and standalone `![Page N image](...)`
    embeds. Files in `<stem>_media/` are untouched — the user can re-add
    meaningful figures manually."""
    dropped = 0
    # Remove `### Page Images` heading + the run of `![Page N image](...)` lines that follow (until next heading/blank paragraph break with non-image content).
    def _sub_section(m: re.Match) -> str:
        nonlocal dropped
        block = m.group(0)
        # Count image lines in the block for reporting.
        dropped += len(re.findall(r"!\[Page \d+ image\]\([^)]*\)", block))
        return ""
    text = re.sub(
        r"### Page Images\n(?:!\[Page \d+ image\]\([^)]*\)\n?)+",
        _sub_section,
        text,
    )
    # Any leftover standalone image lines.
    def _sub_one(m: re.Match) -> str:
        nonlocal dropped
        dropped += 1
        return ""
    text = re.sub(r"^!\[Page \d+ image\]\([^)]*\)\n?", _sub_one, text, flags=re.MULTILINE)
    # Orphan `### Page Images` headings (no images followed) — drop them too.
    text = re.sub(r"^### Page Images\n?", "", text, flags=re.MULTILINE)
    # Placeholder comments from the extractor for pages without a text layer.
    text = re.sub(r"^<!-- No extractable text[^\n]*-->\n?", "", text, flags=re.MULTILINE)
    return text, dropped

# --- Broken tables ---------------------------------------------------------
# Detect a run of >= MIN_RUN consecutive non-empty lines, each with len <= MAX_LEN
# and no ##/### headings, no wiki-links (already-linkified). These are almost
# always PDF cells that flattened into a column.
MIN_RUN = 12
MAX_LEN = 20

def find_page_at(text: str, pos: int) -> int | None:
    """Nearest preceding <!-- source-page: N --> before pos."""
    last = None
    for m in re.finditer(r"<!--\s*source-page:\s*(\d+)\s*-->", text[:pos]):
        last = int(m.group(1))
    return last

def mark_tables(text: str, sidecar_dir: Path, sidecar_stem: str) -> tuple[str, list[dict]]:
    lines = text.split("\n")
    out_lines: list[str] = []
    i = 0
    table_id = 0
    tables: list[dict] = []
    while i < len(lines):
        # try to start a run at line i
        j = i
        while j < len(lines):
            ln = lines[j]
            stripped = ln.strip()
            if not stripped:
                break
            if stripped.startswith("#") or stripped.startswith("<!--") or stripped.startswith(">"):
                break
            if "[[" in stripped or "![" in stripped:
                break
            if len(stripped) > MAX_LEN:
                break
            j += 1
        run_len = j - i
        if run_len >= MIN_RUN:
            table_id += 1
            # save sidecar
            sidecar = sidecar_dir / f"{sidecar_stem}.table-{table_id:03d}.txt"
            sidecar.write_text("\n".join(lines[i:j]), encoding="utf-8")
            # figure out page
            pos = sum(len(l) + 1 for l in out_lines) + sum(len(l) + 1 for l in lines[:i])
            pg = find_page_at(text, pos)
            marker = (
                f"<!-- TABLE #{table_id:03d} — {run_len} cells collapsed into a column"
                f"{f' on PDF p.{pg}' if pg else ''}."
                f" Original cell text saved to `{sidecar.name}`. Reconstruct manually. -->"
            )
            out_lines.append(marker)
            tables.append({
                "id": table_id,
                "page": pg,
                "cell_count": run_len,
                "sidecar": sidecar.name,
            })
            i = j
        else:
            out_lines.append(lines[i])
            i += 1
    return "\n".join(out_lines), tables

# --- Insert chapter headings ----------------------------------------------

def _pdf_outline_chapters(pdf_path: Path) -> list[tuple[int, str, int]]:
    """Return list of (level, title, page) from the PDF outline, or []."""
    try:
        import pymupdf  # type: ignore
    except ImportError:
        try:
            import fitz as pymupdf  # type: ignore
        except ImportError:
            return []
    doc = pymupdf.open(str(pdf_path))
    toc = doc.get_toc(simple=True)
    doc.close()
    return toc

def insert_chapters_from_pdf(text: str, pdf_path: Path) -> tuple[str, int]:
    """Insert `## <title>` headings from the PDF outline (levels 1 and 2).

    Sorts by page ASCENDING then original outline index, iterates in reverse
    so later-page insertions do not shift positions of earlier-page inserts.
    Within a same-page group, reverse-index insertion preserves outline order
    (first-outline entry ends up first in text). Idempotent.
    """
    toc = _pdf_outline_chapters(pdf_path)
    if not toc:
        return text, 0
    indexed = [
        (i, lv, re.sub(r"\s+", " ", t.strip()), p)
        for i, (lv, t, p) in enumerate(toc)
        if 1 <= lv <= 2 and t.strip()
    ]
    # Process in reverse page order (and reverse outline index within a page).
    indexed.sort(key=lambda x: (x[3], x[0]))
    inserted = 0
    for _idx, _lv, title, page in reversed(indexed):
        heading = f"## {title}"
        if heading in text:
            continue
        marker = f"<!-- source-page: {page} -->"
        pos = text.find(marker)
        if pos < 0:
            continue
        insert_at = pos + len(marker)
        text = text[:insert_at] + f"\n\n{heading}\n" + text[insert_at:]
        inserted += 1
    return text, inserted


def insert_chapters_from_text(text: str) -> tuple[str, int]:
    """Fallback for PDFs without an outline. Insert `## <title>` before every
    all-caps `ГЛАВА N ...` line in the body (typical Russian typeset books).

    Must run AFTER strip_running_headers so the pattern is not matched on
    per-page running headers (which repeat 100+ times). Idempotent — checks
    the running text state for each insertion.
    """
    lines = text.split("\n")
    out: list[str] = []
    inserted = 0
    i = 0
    while i < len(lines):
        ln = lines[i]
        m = re.match(r"^\s*ГЛАВА\s+\d+", ln)
        if m:
            title = re.sub(r"\s+", " ", ln.strip())
            # Skip TOC-style lines that end with a page number.
            if not re.search(r"\.\s*\d+\s*$", title):
                heading = f"## {title}"
                if heading not in "\n".join(out):
                    out.append(heading)
                    out.append("")
                    inserted += 1
        out.append(ln)
        i += 1
    return "\n".join(out), inserted


# --- Drop page markers -----------------------------------------------------

def drop_page_markers(text: str) -> tuple[str, int]:
    """Remove `## Page N` headings and `<!-- source-page: N -->` markers.

    Also drops the extractor's header block (`> Source:`, `> Extracted:`,
    `> Method:`) if present at the top — the top-level `# Title` stays.
    """
    dropped = 0
    def sub(m: re.Match) -> str:
        nonlocal dropped
        dropped += 1
        return ""
    text = re.sub(r"^## Page \d+\n?", sub, text, flags=re.MULTILINE)
    text = re.sub(r"^<!--\s*source-page:\s*\d+\s*-->\n?", sub, text, flags=re.MULTILINE)
    # Collapse runs of 3+ blank lines to 2 (paragraph break).
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text, dropped


# --- Reflow paragraphs -----------------------------------------------------

def reflow_paragraphs(text: str) -> tuple[str, dict]:
    """Join wrapped lines inside a paragraph. A paragraph is a run of
    non-empty lines. Between paragraphs, blank lines are preserved.

    - Block-level lines are left alone: headings (`#`), block quotes (`>`),
      HTML comments (`<!--`), list items (`- `, `* `, `1.`), and lines that
      already contain block-level markdown like a wiki-embed `![[...]]`.
    - Soft hyphen unwrap: `word-\n` + `лоwercase` → `wordлоwercase`
      (Cyrillic or Latin lowercase). Otherwise the dash is preserved (it may
      be a real dash / dialogue marker).
    """
    paragraphs = re.split(r"\n{2,}", text)
    joined_paragraphs = 0
    unhyphenated = 0
    out: list[str] = []
    for para in paragraphs:
        lines = para.split("\n")
        if len(lines) <= 1:
            out.append(para)
            continue
        # Skip reflow if paragraph is a block: heading, quote, comment, list, table marker.
        first = lines[0].lstrip()
        if (first.startswith(("#", ">", "<!--", "- ", "* ", "|", "```"))
                or re.match(r"^\d+\.\s", first)):
            out.append(para)
            continue
        # If the block starts with a bracketed heading label ("### ..."), skip.
        # Join lines with soft-hyphen handling.
        buf = lines[0].rstrip()
        for ln in lines[1:]:
            s = ln.rstrip()
            if not s:
                continue
            if buf.endswith("-") and s[:1] and s[:1].isalpha() and s[:1].islower():
                buf = buf[:-1] + s.lstrip()
                unhyphenated += 1
            else:
                buf = buf + " " + s.lstrip()
        joined_paragraphs += 1
        out.append(buf)
    return "\n\n".join(out), {
        "paragraphs_joined": joined_paragraphs,
        "soft_hyphens_unwrapped": unhyphenated,
    }


# --- driver -----------------------------------------------------------------
def main() -> int:
    if len(sys.argv) not in (2, 3):
        print(__doc__)
        return 2
    md = Path(sys.argv[1])
    pdf = Path(sys.argv[2]) if len(sys.argv) == 3 else None
    text = md.read_text(encoding="utf-8")

    # Order matters — see module docstring.
    text2, mojibake_fixed = fix_mojibake(text)
    text3, pua_counts = mark_pua(text2)
    text4, images_dropped = drop_page_images(text3)
    chapters_from_pdf = 0
    if pdf is not None:
        text4, chapters_from_pdf = insert_chapters_from_pdf(text4, pdf)
    text5, tables = mark_tables(text4, md.parent, md.stem)
    text6, header_stats = strip_running_headers(text5)
    # Text-based chapter fallback runs AFTER header stripping so it does not
    # match per-page running-header repeats. Contributes only if PDF outline
    # missed the chapter (skips headings that are already present).
    text6, chapters_from_text = insert_chapters_from_text(text6)
    text7, pagemarkers_dropped = drop_page_markers(text6)
    text8, reflow_stats = reflow_paragraphs(text7)
    chapters_inserted = chapters_from_pdf + chapters_from_text

    md.write_text(text8, encoding="utf-8")

    summary = {
        "input": str(md),
        "mojibake_tokens_fixed": mojibake_fixed,
        "pua_chars_marked_by_codepoint": pua_counts,
        "pua_chars_total": sum(pua_counts.values()),
        "page_images_dropped": images_dropped,
        "chapter_headings_inserted": chapters_inserted,
        "tables_marked": len(tables),
        "running_headers": header_stats,
        "page_markers_dropped": pagemarkers_dropped,
        "paragraph_reflow": reflow_stats,
        "tables": tables,
    }
    report = md.with_suffix(md.suffix + ".cleanup.json")
    report.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"mojibake fixed: {mojibake_fixed}")
    print(f"PUA chars marked: {sum(pua_counts.values())} across {len(pua_counts)} codepoints")
    print(f"page images dropped: {images_dropped}")
    print(f"tables marked: {len(tables)}")
    print(f"running headers stripped: {header_stats['stripped_lines']} lines ({header_stats['running_headers_total']} distinct)")
    print(f"page markers dropped: {pagemarkers_dropped}")
    print(f"paragraphs joined: {reflow_stats['paragraphs_joined']} (soft-hyphens: {reflow_stats['soft_hyphens_unwrapped']})")
    print(f"report: {report}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
