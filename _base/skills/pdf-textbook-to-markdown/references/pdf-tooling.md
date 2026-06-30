# PDF Textbook Tooling

## Route Selection

Use this reference when a textbook PDF is scanned, math-heavy, table-heavy, multilingual, or difficult to extract cleanly.

| PDF condition | Preferred route | Notes |
| --- | --- | --- |
| Born-digital text layer, ordinary layout | `scripts/extract_pdf_textbook.py extract` | Start with page anchors and images, then clean structure. |
| Text layer exists but line breaks are poor | Try `pdftotext -layout`, then compare with the script output | Use whichever preserves paragraphs, lists, and equations better. |
| Scanned pages or low text coverage | OCR a copy with OCRmyPDF/Tesseract, then extract | Keep the original and OCR PDF separately. |
| Formula-heavy textbook | Use page images or a math-aware converter for formulas; manually verify KaTeX | Do not guess equations from noisy OCR. |
| Table-heavy textbook | Preserve simple tables as Markdown; use image fallback or HTML only when needed | Verify row/column alignment against the page image. |
| Two-column or marginal notes | Extract sample pages first and compare routes | Column mixing is common; avoid bulk cleanup before triage. |

## Useful Commands

Inspect text coverage and PDF outline:

```powershell
python ".\scripts\extract_pdf_textbook.py" inspect "input.pdf"
```

Extract a page-anchored draft:

```powershell
python ".\scripts\extract_pdf_textbook.py" extract "input.pdf" --output "book.md" --media-dir "book_media"
```

Extract selected pages:

```powershell
python ".\scripts\extract_pdf_textbook.py" extract "input.pdf" --pages "1-12,45,80-96" --output "sample.md"
```

Check image links and page anchors:

```powershell
python ".\scripts\extract_pdf_textbook.py" check "book.md"
```

OCR a scanned PDF when OCRmyPDF is available:

```powershell
ocrmypdf --language rus+eng --deskew --rotate-pages "input.pdf" "input.ocr.pdf"
```

Fallback line-preserving extraction when Poppler is available:

```powershell
pdftotext -layout -enc UTF-8 "input.pdf" "book.txt"
```

## Cleanup Checklist

- Compare the first pages, a middle chapter page, a figure page, a table page, and the last content page against the PDF.
- Remove repeated running headers and footers only after confirming the pattern across several pages.
- Join broken line wraps without merging list items, theorem labels, equations, captions, or examples.
- Repair hyphenation at line breaks only when the joined word is clear.
- Normalize common ligatures such as `fi`, `fl`, `ffi`, and soft hyphens.
- Keep `<!-- source-page: N -->` markers during cleanup; they are the audit trail.
- Mark uncertain OCR or formula conversions with a short HTML comment near the affected content.
- Keep extracted images even when captions are converted; they are useful for visual verification.

## Obsidian Split Pattern

For a full textbook, prefer:

```text
Book Title/
  Book Title.md
  01 - Chapter Title.md
  02 - Chapter Title.md
  Book Title_media/
```

The index note should include source metadata, chapter links, page ranges, and remaining review notes. Chapter notes should start with the chapter title and a short source line, then preserve local page markers inside the body.
