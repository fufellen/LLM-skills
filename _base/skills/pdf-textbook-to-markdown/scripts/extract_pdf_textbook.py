#!/usr/bin/env python3
"""Extract page-anchored Markdown drafts from PDF textbooks."""

from __future__ import annotations

import argparse
import contextlib
import datetime as _dt
import json
import os
import re
import sys
from pathlib import Path
from typing import Iterable, Iterator


LIGATURES = {
    "\ufb00": "ff",
    "\ufb01": "fi",
    "\ufb02": "fl",
    "\ufb03": "ffi",
    "\ufb04": "ffl",
    "\ufb05": "st",
    "\ufb06": "st",
}


def import_fitz():
    try:
        import fitz  # type: ignore
    except ImportError:
        return None
    return fitz


def import_pymupdf4llm():
    try:
        import pymupdf4llm  # type: ignore
    except ImportError:
        return None
    return pymupdf4llm


def import_pdf_reader():
    try:
        from pypdf import PdfReader  # type: ignore

        return PdfReader
    except ImportError:
        try:
            from PyPDF2 import PdfReader  # type: ignore

            return PdfReader
        except ImportError:
            return None


def normalize_text(text: str) -> str:
    for old, new in LIGATURES.items():
        text = text.replace(old, new)
    text = text.replace("\u00ad", "")
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n{4,}", "\n\n\n", text)
    return text.strip()


def parse_pages(spec: str | None, total_pages: int) -> list[int]:
    if not spec:
        return list(range(total_pages))
    pages: set[int] = set()
    for chunk in spec.split(","):
        chunk = chunk.strip()
        if not chunk:
            continue
        if "-" in chunk:
            start_s, end_s = chunk.split("-", 1)
            start = int(start_s)
            end = int(end_s)
            if start > end:
                raise ValueError(f"Invalid page range: {chunk}")
            pages.update(range(start - 1, end))
        else:
            pages.add(int(chunk) - 1)
    bad = [p + 1 for p in pages if p < 0 or p >= total_pages]
    if bad:
        raise ValueError(f"Page(s) outside 1..{total_pages}: {bad}")
    return sorted(pages)


def markdown_relpath(target: Path, base_file: Path) -> str:
    try:
        rel = target.resolve().relative_to(base_file.resolve().parent)
    except ValueError:
        rel = target.resolve()
    return rel.as_posix()


def ensure_can_write(path: Path, overwrite: bool) -> None:
    if path.exists() and not overwrite:
        raise FileExistsError(f"{path} already exists; pass --overwrite to replace it")
    path.parent.mkdir(parents=True, exist_ok=True)


@contextlib.contextmanager
def working_directory(path: Path):
    previous = Path.cwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(previous)


def iter_pypdf_pages(pdf_path: Path) -> Iterator[str]:
    PdfReader = import_pdf_reader()
    if PdfReader is None:
        raise RuntimeError("Install pymupdf or pypdf for PDF extraction")
    reader = PdfReader(str(pdf_path))
    for page in reader.pages:
        yield normalize_text(page.extract_text() or "")


def inspect_with_fitz(pdf_path: Path) -> dict:
    fitz = import_fitz()
    if fitz is None:
        raise RuntimeError("PyMuPDF is unavailable")
    doc = fitz.open(pdf_path)
    page_stats = []
    low_text_pages = []
    for i, page in enumerate(doc):
        text = normalize_text(page.get_text("text") or "")
        chars = len(text)
        page_stats.append({"page": i + 1, "chars": chars})
        if chars < 80:
            low_text_pages.append(i + 1)
    outline = []
    try:
        for level, title, page_number in doc.get_toc(simple=True):
            outline.append({"level": level, "title": title, "page": page_number})
    except Exception:
        outline = []
    metadata = {k: v for k, v in (doc.metadata or {}).items() if v}
    total_chars = sum(item["chars"] for item in page_stats)
    return {
        "method": "pymupdf",
        "file": str(pdf_path),
        "pages": doc.page_count,
        "metadata": metadata,
        "total_text_chars": total_chars,
        "avg_chars_per_page": round(total_chars / max(doc.page_count, 1), 1),
        "low_text_pages": low_text_pages[:100],
        "low_text_page_count": len(low_text_pages),
        "outline_preview": outline[:40],
    }


def inspect_with_pypdf(pdf_path: Path) -> dict:
    PdfReader = import_pdf_reader()
    if PdfReader is None:
        raise RuntimeError("Install pymupdf or pypdf for PDF inspection")
    reader = PdfReader(str(pdf_path))
    page_stats = []
    low_text_pages = []
    for i, page in enumerate(reader.pages):
        text = normalize_text(page.extract_text() or "")
        chars = len(text)
        page_stats.append({"page": i + 1, "chars": chars})
        if chars < 80:
            low_text_pages.append(i + 1)
    metadata = {}
    raw_metadata = getattr(reader, "metadata", None)
    if raw_metadata:
        metadata = {str(k).lstrip("/"): str(v) for k, v in raw_metadata.items() if v}
    total_chars = sum(item["chars"] for item in page_stats)
    return {
        "method": "pypdf",
        "file": str(pdf_path),
        "pages": len(reader.pages),
        "metadata": metadata,
        "total_text_chars": total_chars,
        "avg_chars_per_page": round(total_chars / max(len(reader.pages), 1), 1),
        "low_text_pages": low_text_pages[:100],
        "low_text_page_count": len(low_text_pages),
        "outline_preview": [],
    }


def cmd_inspect(args: argparse.Namespace) -> int:
    pdf_path = Path(args.pdf).expanduser()
    if not pdf_path.exists():
        raise FileNotFoundError(pdf_path)
    try:
        data = inspect_with_fitz(pdf_path)
    except RuntimeError:
        data = inspect_with_pypdf(pdf_path)
    print(json.dumps(data, ensure_ascii=False, indent=2))
    return 0


def extract_with_fitz(
    pdf_path: Path,
    output_path: Path,
    media_dir: Path | None,
    pages: list[int],
    title: str,
    overwrite: bool,
    extract_images: bool,
) -> None:
    fitz = import_fitz()
    if fitz is None:
        raise RuntimeError("PyMuPDF is unavailable")
    ensure_can_write(output_path, overwrite)
    if media_dir:
        media_dir.mkdir(parents=True, exist_ok=True)

    doc = fitz.open(pdf_path)
    lines: list[str] = [
        f"# {title}",
        "",
        f"> Source: [[{Path(pdf_path).name}]]",
        f"> Extracted: {_dt.date.today().isoformat()}",
        "> Method: PyMuPDF page text extraction",
        "",
    ]
    seen_xrefs: set[int] = set()
    for page_index in pages:
        page_number = page_index + 1
        page = doc[page_index]
        text = normalize_text(page.get_text("text") or "")
        lines.extend([f"## Page {page_number}", "", f"<!-- source-page: {page_number} -->", ""])
        lines.append(text if text else "<!-- No extractable text on this page. OCR or manual review may be required. -->")
        lines.append("")

        if extract_images and media_dir:
            page_images = []
            for image_number, img in enumerate(page.get_images(full=True), start=1):
                xref = int(img[0])
                if xref in seen_xrefs:
                    continue
                seen_xrefs.add(xref)
                try:
                    extracted = doc.extract_image(xref)
                except Exception:
                    continue
                ext = extracted.get("ext", "png")
                image_bytes = extracted.get("image")
                if not image_bytes:
                    continue
                image_path = media_dir / f"page-{page_number:04d}-img-{image_number:02d}.{ext}"
                image_path.write_bytes(image_bytes)
                page_images.append(image_path)
            if page_images:
                lines.extend(["### Page Images", ""])
                for image_path in page_images:
                    rel = markdown_relpath(image_path, output_path)
                    lines.append(f"![Page {page_number} image]({rel})")
                lines.append("")

    output_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def extract_with_pypdf(
    pdf_path: Path,
    output_path: Path,
    pages: list[int],
    title: str,
    overwrite: bool,
) -> None:
    ensure_can_write(output_path, overwrite)
    all_text = list(iter_pypdf_pages(pdf_path))
    lines: list[str] = [
        f"# {title}",
        "",
        f"> Source: [[{Path(pdf_path).name}]]",
        f"> Extracted: {_dt.date.today().isoformat()}",
        "> Method: pypdf text extraction",
        "",
    ]
    for page_index in pages:
        page_number = page_index + 1
        text = all_text[page_index]
        lines.extend([f"## Page {page_number}", "", f"<!-- source-page: {page_number} -->", ""])
        lines.append(text if text else "<!-- No extractable text on this page. OCR or manual review may be required. -->")
        lines.append("")
    output_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def extract_with_pymupdf4llm(
    pdf_path: Path,
    output_path: Path,
    media_dir: Path | None,
    pages: list[int],
    title: str,
    overwrite: bool,
    extract_images: bool,
) -> None:
    pymupdf4llm = import_pymupdf4llm()
    if pymupdf4llm is None:
        raise RuntimeError(
            "PyMuPDF4LLM is unavailable; install pymupdf4llm or use --engine pymupdf"
        )
    ensure_can_write(output_path, overwrite)
    output_path = output_path.resolve()
    pdf_path = pdf_path.resolve()
    if extract_images:
        if media_dir is None:
            raise RuntimeError("A media directory is required when image extraction is enabled")
        media_dir = media_dir.resolve()
        if media_dir.parent != output_path.parent:
            raise ValueError(
                "With --engine pymupdf4llm, --media-dir must be a direct sibling "
                "of the output Markdown file"
            )
        media_dir.mkdir(parents=True, exist_ok=True)

    kwargs = {
        "pages": pages,
        "page_chunks": True,
        "page_separators": False,
        "write_images": extract_images,
        "show_progress": True,
    }
    if extract_images and media_dir is not None:
        kwargs.update(
            {
                "image_path": media_dir.name,
                "image_format": "png",
                "dpi": 160,
            }
        )

    # A short relative image_path avoids a PyMuPDF4LLM path-normalization
    # failure observed on Windows with absolute paths containing spaces or Cyrillic.
    with working_directory(output_path.parent):
        chunks = pymupdf4llm.to_markdown(str(pdf_path), **kwargs)

    lines: list[str] = [
        f"# {title}",
        "",
        f"> Source: [[{pdf_path.name}]]",
        f"> Extracted: {_dt.date.today().isoformat()}",
        "> Method: PyMuPDF4LLM layout-aware extraction",
        "",
    ]
    for fallback_page_index, chunk in zip(pages, chunks):
        metadata = chunk.get("metadata") or {}
        page_number = int(metadata.get("page_number") or fallback_page_index + 1)
        text = normalize_text(chunk.get("text") or "")
        lines.extend([f"## Page {page_number}", "", f"<!-- source-page: {page_number} -->", ""])
        lines.append(
            text
            if text
            else "<!-- No extractable text on this page. OCR or manual review may be required. -->"
        )
        lines.append("")

    output_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def cmd_extract(args: argparse.Namespace) -> int:
    pdf_path = Path(args.pdf).expanduser()
    if not pdf_path.exists():
        raise FileNotFoundError(pdf_path)
    output_path = Path(args.output or pdf_path.with_suffix(".md")).expanduser()
    title = args.title or pdf_path.stem

    total_pages = None
    fitz = import_fitz()
    if fitz is not None:
        doc = fitz.open(pdf_path)
        total_pages = doc.page_count
        doc.close()
    else:
        PdfReader = import_pdf_reader()
        if PdfReader is None:
            raise RuntimeError("Install pymupdf or pypdf for PDF extraction")
        reader = PdfReader(str(pdf_path))
        total_pages = len(reader.pages)

    pages = parse_pages(args.pages, total_pages)
    media_dir = Path(args.media_dir).expanduser() if args.media_dir else output_path.with_name(f"{output_path.stem}_media")

    if args.engine == "pymupdf4llm":
        extract_with_pymupdf4llm(
            pdf_path=pdf_path,
            output_path=output_path,
            media_dir=media_dir,
            pages=pages,
            title=title,
            overwrite=args.overwrite,
            extract_images=not args.no_images,
        )
    elif args.engine in {"auto", "pymupdf"} and fitz is not None:
        extract_with_fitz(
            pdf_path=pdf_path,
            output_path=output_path,
            media_dir=media_dir,
            pages=pages,
            title=title,
            overwrite=args.overwrite,
            extract_images=not args.no_images,
        )
    elif args.engine in {"auto", "pypdf"}:
        if not args.no_images:
            print("PyMuPDF is unavailable; falling back to text-only extraction.", file=sys.stderr)
        extract_with_pypdf(pdf_path, output_path, pages, title, args.overwrite)
    else:
        raise RuntimeError(f"Requested extraction engine is unavailable: {args.engine}")

    print(f"Wrote {output_path}")
    return 0


IMAGE_LINK_RE = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")
OBSIDIAN_IMAGE_RE = re.compile(r"!\[\[([^\]|#]+)(?:[|#][^\]]*)?\]\]")
SOURCE_PAGE_RE = re.compile(r"<!--\s*source-page:\s*(\d+)\s*-->")


def iter_image_links(markdown: str) -> Iterable[str]:
    for match in IMAGE_LINK_RE.finditer(markdown):
        link = match.group(1).strip()
        if "://" in link or link.startswith("#"):
            continue
        yield link


def cmd_check(args: argparse.Namespace) -> int:
    md_path = Path(args.markdown).expanduser()
    if not md_path.exists():
        raise FileNotFoundError(md_path)
    text = md_path.read_text(encoding="utf-8")
    missing = []
    ambiguous = []
    for link in iter_image_links(text):
        clean = link.split("#", 1)[0].replace("%20", " ")
        target = (md_path.parent / clean).resolve()
        if not target.exists():
            missing.append(link)
    for match in OBSIDIAN_IMAGE_RE.finditer(text):
        link = match.group(1).strip()
        direct = (md_path.parent / link).resolve()
        if direct.exists():
            continue
        candidates = list(md_path.parent.rglob(Path(link).name))
        if not candidates:
            missing.append(link)
        elif len(candidates) > 1:
            ambiguous.append(link)
    pages = SOURCE_PAGE_RE.findall(text)
    print(
        json.dumps(
            {
                "file": str(md_path),
                "source_page_markers": len(pages),
                "missing_image_links": missing,
                "ambiguous_obsidian_image_links": ambiguous,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 1 if missing or ambiguous else 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Extract page-anchored Markdown drafts from PDF textbooks")
    subparsers = parser.add_subparsers(dest="command", required=True)

    inspect_parser = subparsers.add_parser("inspect", help="Inspect PDF metadata and text-layer coverage")
    inspect_parser.add_argument("pdf", help="Input PDF")
    inspect_parser.set_defaults(func=cmd_inspect)

    extract_parser = subparsers.add_parser("extract", help="Extract a page-anchored Markdown draft")
    extract_parser.add_argument("pdf", help="Input PDF")
    extract_parser.add_argument("-o", "--output", help="Output Markdown path")
    extract_parser.add_argument("--media-dir", help="Directory for extracted images")
    extract_parser.add_argument("--pages", help="1-based pages or ranges, for example 1-12,45,80-96")
    extract_parser.add_argument("--title", help="Markdown H1 title")
    extract_parser.add_argument(
        "--engine",
        choices=("auto", "pymupdf", "pymupdf4llm", "pypdf"),
        default="auto",
        help="Extraction engine; use pymupdf4llm for a layout-aware comparison",
    )
    extract_parser.add_argument("--no-images", action="store_true", help="Skip embedded image extraction")
    extract_parser.add_argument("--overwrite", action="store_true", help="Replace an existing output file")
    extract_parser.set_defaults(func=cmd_extract)

    check_parser = subparsers.add_parser("check", help="Check Markdown image links and page anchors")
    check_parser.add_argument("markdown", help="Markdown file to check")
    check_parser.set_defaults(func=cmd_check)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return int(args.func(args))
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
