# PDF Textbook Lessons

Accumulated reusable lessons from real conversions. Add new entries at the end of the matching section; keep each lesson compact and source-agnostic.

## Post-extraction polish is a mandatory second pass

The raw output of `extract_pdf_textbook.py extract` is a debugging artifact, not a readable book: it carries `## Page N` breaks every page, per-page footer numbers, running headers repeated hundreds of times, broken hyphenation, mojibake, and each PDF text cell as its own line. Do not hand the raw file to the user as a "converted book" — always run `scripts/polish_pdf_extraction.py <file.md> [<file.pdf>]` afterwards. Passing the PDF path lets the polisher insert `## Chapter …` headings from the outline; without it the polisher falls back to detecting `^\s*ГЛАВА\s+\d+` in the body text. Polish is idempotent — safe to re-run.

## PyMuPDF text extraction artifacts (what the polisher fixes)

- **Mojibake `×èñëî áðàêîâ` = `Число браков`.** Cyrillic bytes in a CP1251 font glyph table decoded as Latin-1. Detected as tokens made entirely of `[\x80-\xff]` accented chars; round-tripped via `encode('latin-1').decode('cp1251')`. Only triggers on tokens with ≥2 such chars, so ASCII prose is untouched. On one 850-page devotional book: 4296 tokens fixed automatically.
- **Private-Use-Area glyphs `U+E000..U+F8FF`.** Custom-font glyphs Obsidian renders as replacement squares (□). Often decorative bullets/dingbats; occasionally lost letters. Polisher marks each as `⟨PUA U+XXXX⟩` so a human can scan and decide — do not silently strip.
- **Broken tables — each cell on its own line.** PyMuPDF reads text by layout coordinates; a numeric table with 20 columns × 10 rows produces 200 short lines in reading order. Detect as runs of ≥12 consecutive non-empty non-block lines ≤20 chars each; replace with an HTML-comment marker `<!-- TABLE #NNN — reconstruct from PDF p.N -->` and save original cell text to `<stem>.table-NNN.txt` sidecar. Do not try to auto-reconstruct — column boundaries are ambiguous from text alone; sidecar + PDF is a good tool for a human.
- **Running headers/footers.** Chapter title + book title + page number appear at the top/bottom of every page. Detect as lines appearing verbatim in ≥5 pages (uniquely per page); strip. But — this pass can eat legitimate chapter-start titles if the title itself is the running header (see next lesson).
- **Page markers `## Page N` and `<!-- source-page: N -->`.** Useful for locating tables and inserting chapter headings; strip after those passes are done. Never present them as content.
- **Hyphenation.** Words split across line boundaries as `слово-\nостаток`. Unwrap only when the tail starts with a lowercase letter; otherwise keep the dash (may be a real dash or a dialogue marker).

## Chapter splitting: order-of-operations matters

- **Insert chapter headings BEFORE stripping running headers**, when the PDF has an outline: outline entries index into `<!-- source-page: N -->` markers; insertion at each marker produces `## <Title>` at the right position. Sort outline entries by page ASCENDING and iterate in REVERSE order so later-page inserts don't shift earlier positions; for same-page groups, reverse the outline-index too so first-outline entry ends up first in text.
- **Fallback text-based detection runs AFTER running-header stripping**, when the PDF has no outline (Немцев/Winkler-style books): pattern `^\s*ГЛАВА\s+\d+.*` on line start. Running-header stripping usually removes the per-page repeats; the surviving occurrence is the true chapter start. But if the chapter title *is* the running header (repeats verbatim on every page), the stripper removes even the actual first occurrence, leaving only a shorter `ГЛАВА N` label somewhere else, and the auto-inserted heading loses its title. **Rename the chapter files manually from the book's own TOC in this case** — it takes 30 seconds and there is no cleaner automatic fix that doesn't risk missing real chapter starts.
- Split by `^## ` headings into per-chapter files via `scripts/split_by_chapters.py`. The big .md becomes an index with wiki-links to chapter files; original chapter body opens each file as `# <Title>`.

## Do not present a raw or half-polished extract as "converted"

Users see the raw extraction as a broken deliverable, not as "a first pass we'll clean later" — even if the docstring says so. Run polish + split + (if applicable) `spiritual-literature/scripts/resolve_bible_refs.py` in one pipeline; deliver the chapter folder and the index. If the user later wants raw page anchors, they're in the .cleanup.json report.



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
