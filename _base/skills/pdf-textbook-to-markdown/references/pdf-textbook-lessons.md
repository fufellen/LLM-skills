# PDF Textbook Lessons

Accumulated reusable lessons from real conversions. Add new entries at the end of the matching section; keep each lesson compact and source-agnostic.

## Word "Print To PDF" documents (theses, reports)

- Broken Word `REF` fields print as the literal artifact «Ошибка! Источник ссылки не найден.» throughout the PDF. Every in-text bibliography number is then unrecoverable from the PDF itself — recover citation numbers from the source `.doc`/`.docx` when available, and if not, state explicitly in the conversion note that reference numbers are lost; never invent them.
- PDF metadata `title` of such documents is often mojibake (cp1251/UTF mix from the Word filename). Harmless; do not treat it as an OCR-quality signal.
- Formula-heavy pages keep a full text layer, but equations extract as per-glyph vertical scatter (symbols split line by line). Do not transcribe formulas from the extracted text — use rendered page images as ground truth.

## Large documents (200+ pages)

- Render all pages to PNG early (`page.get_pixmap(dpi=170)`): the images serve simultaneously as formula-transcription ground truth, figure-crop source, and OCR fallback, and cost little time or disk.
- For chapter-level summarization or cleanup, fan out parallel subagents: give each agent the extracted-Markdown line range for its chapter, computed by grepping the `## Page N` anchors emitted by `extract_pdf_textbook.py`. Instruct agents to mark unreadable formulas as «[формула нечитаема]» rather than guessing; require per-chapter term lists with page anchors so the synthesizer can build term notes without re-reading the source.
- When the same work exists as PDF + source `.doc`/`.docx`, treat the pair as one source: prose and structure convert best from the DOCX route (`docx-to-markdown` skill), while the PDF supplies page anchors and rendered ground truth for formulas and figures.
