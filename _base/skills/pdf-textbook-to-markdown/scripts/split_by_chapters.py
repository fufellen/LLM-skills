#!/usr/bin/env python3
"""Split a polished PDF-derived Markdown file by its `## Chapter …` headings.

Reads <file.md>, splits at every `^## ` heading. Writes one file per chapter
into a sibling folder `<stem>/`. The original file becomes an index note
listing chapters as wiki-links, keeping its front-matter (title, source,
extraction stamp).

Filename convention: `NN — <sanitized title>.md` where NN is the chapter's
index in the outline (2-digit, zero-padded). Non-filename-safe chars
(`/\\?*|<>":`) are replaced with `-`.

Usage:
    python split_by_chapters.py <file.md>
"""
from __future__ import annotations
import re, sys
from pathlib import Path

FILENAME_UNSAFE = re.compile(r'[/\\?*|<>":]+')

def sanitize(name: str) -> str:
    name = FILENAME_UNSAFE.sub("-", name)
    name = re.sub(r"\s+", " ", name).strip()
    # Trim ellipsis or trailing dots
    name = name.rstrip(".…")
    # Cap length (Windows path safety)
    if len(name) > 80:
        name = name[:77] + "…"
    return name

def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    md = Path(sys.argv[1])
    text = md.read_text(encoding="utf-8")

    # Find every `## ` heading at line start.
    matches = list(re.finditer(r"^## (.+)$", text, flags=re.MULTILINE))
    if not matches:
        print("No `## ` headings found — nothing to split.")
        return 1

    # Preamble = everything before the first chapter (title, front-matter).
    preamble = text[:matches[0].start()].rstrip() + "\n"

    # Build chapter blocks.
    chapters: list[tuple[str, str]] = []
    for i, m in enumerate(matches):
        title = m.group(1).strip()
        start = m.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        # Skip the heading itself in the body — the heading becomes the file's # H1.
        body_start = m.end() + 1  # past the newline after the heading
        body = text[body_start:end].strip()
        chapters.append((title, body))

    out_dir = md.parent / md.stem
    out_dir.mkdir(exist_ok=True)

    index_lines = [preamble.rstrip(), "", "## Оглавление", ""]
    for i, (title, body) in enumerate(chapters, 1):
        safe = sanitize(title)
        fname = f"{i:02d} — {safe}.md"
        (out_dir / fname).write_text(f"# {title}\n\n{body}\n", encoding="utf-8")
        # Link back to source PDF in each chapter? Optional. Skip — index has it.
        # Index link uses wiki-link with display = plain title.
        index_lines.append(f"{i}. [[{out_dir.name}/{fname[:-3]}|{title}]]")

    md.write_text("\n".join(index_lines) + "\n", encoding="utf-8")

    print(f"split into {len(chapters)} chapters -> {out_dir}")
    print(f"index -> {md}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
