# PDF Textbook Lessons

Accumulated reusable lessons from real conversions. Add new entries at the end of the matching section; keep each lesson compact and source-agnostic.

## Word "Print To PDF" documents (theses, reports)

- Broken Word `REF` fields print as the literal artifact «Ошибка! Источник ссылки не найден.» throughout the PDF. Every in-text bibliography number is then unrecoverable from the PDF itself — recover citation numbers from the source `.doc`/`.docx` when available, and if not, state explicitly in the conversion note that reference numbers are lost; never invent them.
- PDF metadata `title` of such documents is often mojibake (cp1251/UTF mix from the Word filename). Harmless; do not treat it as an OCR-quality signal.
- Formula-heavy pages keep a full text layer, but equations extract as per-glyph vertical scatter (symbols split line by line). Do not transcribe formulas from the extracted text — use rendered page images as ground truth.

## Markdown-native open textbooks (GitHub, MkDocs)

- A GitHub/MkDocs textbook needs no extraction: clone it, verify the licence first (Apache-2.0/CC → translation and vault copy are permitted; keep LICENSE and attribution), then work directly on the chapter `.md` files. Check math delimiters — MkDocs sources often already use `$...$`/`$$...$$`, which Obsidian accepts as-is.
- For full translation, fan out one subagent per ≤~10k source words (split large chapters by file ranges; two agents may write into the same destination folder — different numeric prefixes never collide). Put the common rules (terminology policy, embed rewriting, footer line, file-naming rule) into ONE shared rules file and give each agent a two-line assignment pointing at it — prompts stay tiny and the rules stay consistent.
- Copy the book's shared `images/` once into `attachments/` with a unique per-book prefix (e.g. `mcsai-<name>.svg`), and have agents rewrite `![alt](../images/X.svg)` → `![[<prefix>-X.svg]]`. Verify afterwards by counting: total embeds in translation must equal total image links in source, and per-chapter counts must match; also check every embed filename exists.
- Agents killed by session limits or dropped connections usually leave whole files either complete (tail contains the footer/source line) or absent — the per-file footer line doubles as a completeness marker. Resume the same agent with a message («допиши файл X») instead of relaunching: its context (rules + source already read) survives, so the retry costs little.
- Expect ~13–14 output-tokens per source word end-to-end for EN→RU translation agents (rules reading included) — use this to size the fan-out before launching.

## Large documents (200+ pages)

- Render all pages to PNG early (`page.get_pixmap(dpi=170)`): the images serve simultaneously as formula-transcription ground truth, figure-crop source, and OCR fallback, and cost little time or disk.
- For chapter-level summarization or cleanup, fan out parallel subagents: give each agent the extracted-Markdown line range for its chapter, computed by grepping the `## Page N` anchors emitted by `extract_pdf_textbook.py`. Instruct agents to mark unreadable formulas as «[формула нечитаема]» rather than guessing; require per-chapter term lists with page anchors so the synthesizer can build term notes without re-reading the source.
- When the same work exists as PDF + source `.doc`/`.docx`, treat the pair as one source: prose and structure convert best from the DOCX route (`docx-to-markdown` skill), while the PDF supplies page anchors and rendered ground truth for formulas and figures.
- The PDF-only full-conversion route is proven viable when the DOC route fails (e.g. Word COM `SaveAs2` never completes): prose from the PDF text layer, every formula transcribed to LaTeX against the page render, figures cropped from the PDF with an iterative crop-verify loop (render `page.get_pixmap(clip=...)` → visually inspect the crop → adjust bbox; expect 1–2 re-crops per tricky multi-panel figure). A 214-page, ~450-formula dissertation converted this way with only one formula left as an image.
- Replace the broken-REF artifact «Ошибка! Источник ссылки не найден.» with one compact inline marker (e.g. `[лит.?]`), collapsing runs of consecutive artifacts into a single marker, and explain the convention once in the book/index note — not in every chapter note.
- Vault note validators aimed at authored term notes (e.g. a Strict rule "display formula must be followed by a `Где:` block") do not apply to full-text conversion notes, where the source's own prose explains notation. Validate conversions with the non-strict profile: UTF-8, headings, link balance/resolution, embed existence.
