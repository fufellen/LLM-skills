#!/usr/bin/env python3
"""Render a DOCX (or PDF) to per-page PNG images for VISUAL review.

Parsing word/document.xml proves attributes; it does NOT show how the page
looks. After building a manuscript DOCX, render it and actually LOOK at the
pages (open the PNGs / read them as images) before calling the layout done.

Pipeline: DOCX -> PDF -> PNG per page.
  DOCX->PDF: LibreOffice `soffice --headless` if available, else MS Word COM
             (Windows). PDF input is passed straight through.
  PDF->PNG:  PyMuPDF (`pip install pymupdf`).

Usage:
  python render_docx_pages.py <file.docx|file.pdf> [out_dir] [--dpi 110]

Prints the saved PNG paths (one per line). Read each one and compare against
the venue template's own example figures/tables.
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


def docx_to_pdf(src: Path, out_dir: Path) -> Path:
    pdf = out_dir / (src.stem + ".pdf")
    soffice = shutil.which("soffice") or shutil.which("libreoffice")
    if soffice:
        subprocess.run(
            [soffice, "--headless", "--convert-to", "pdf", "--outdir",
             str(out_dir), str(src)],
            check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
        if pdf.exists():
            return pdf
    if sys.platform == "win32":
        # MS Word COM via PowerShell; ExportAsFixedFormat, 17 = wdFormatPDF.
        ps = (
            "$w = New-Object -ComObject Word.Application; $w.Visible=$false; "
            f"$d = $w.Documents.Open('{src}', $false, $true); "
            f"$d.ExportAsFixedFormat('{pdf}', 17); $d.Close($false); $w.Quit()"
        )
        subprocess.run(["powershell", "-NoProfile", "-Command", ps], check=True)
        if pdf.exists():
            return pdf
    raise RuntimeError(
        "No DOCX->PDF converter found (install LibreOffice, or use Windows "
        "with MS Word). PDF input works without a converter."
    )


def pdf_to_pngs(pdf: Path, out_dir: Path, dpi: int) -> list[Path]:
    import fitz  # PyMuPDF
    doc = fitz.open(pdf)
    paths = []
    for i, page in enumerate(doc, 1):
        pix = page.get_pixmap(dpi=dpi)
        out = out_dir / f"{pdf.stem}_p{i}.png"
        pix.save(out)
        paths.append(out)
    return paths


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("out_dir", nargs="?", default=None)
    ap.add_argument("--dpi", type=int, default=110)
    args = ap.parse_args()

    src = Path(args.src).resolve()
    out_dir = Path(args.out_dir).resolve() if args.out_dir else src.parent
    out_dir.mkdir(parents=True, exist_ok=True)

    pdf = src if src.suffix.lower() == ".pdf" else docx_to_pdf(src, out_dir)
    for p in pdf_to_pngs(pdf, out_dir, args.dpi):
        print(p)


if __name__ == "__main__":
    main()
