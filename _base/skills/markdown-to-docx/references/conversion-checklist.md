# Markdown To DOCX Conversion Checklist

Use this checklist for publication/report-grade `.md` to `.docx` work.

## Preflight

- Identify the source `.md`, output `.docx`, and whether a Word reference/template document is required.
- Check for images and relative media paths. If images are required, prefer Pandoc and set an appropriate resource path.
- Check for display math, inline math, chemical formulas, layer stacks, and captions before conversion.
- For scientific or technical articles, keep the scientific/content skill active for prose quality and use this skill for conversion mechanics.

## Sanitization

- Unescape Markdown-only pipe escapes in prose and captions: `\|` and `\ |` must not appear in Word.
- Convert formula-like underscores to subscript formatting when the token is scientific text rather than code: examples include `SiO_2`, `lambda_0`, `k_0`, `n_eff`, `L_pi`, and `L_power`.
- Leave underscores untouched in code blocks, file names, URLs, and identifiers.
- Convert Markdown links to Word links with Pandoc, or to readable `label (url)` text in a lightweight fallback.
- Treat raw `$...$` math as a warning unless Pandoc or another converter is explicitly rendering equations.

## Layout Checks

- Ensure figure captions contain only caption text. Body lines that describe layer stacks, equations, or methods should not visually attach to the previous caption.
- Check that tables did not turn into plain pipe-delimited paragraphs.
- Check that bullets and numbered lists remain lists or at least visually stable list paragraphs.
- Check that headings map to Word heading styles rather than bold body text.
- For camera-ready papers, confirm page size, margins, columns, fonts, and reference style against the official template.

## DOCX QA

Inspect `word/document.xml` or extracted text for these patterns before delivery:

```text
\|
\ |
SiO_2
lambda_0
k_0
n_eff
L_pi
L_power
$...$
![...](...)
```

Finding one of these patterns is not automatically fatal, but it requires manual judgment. It is a defect when the pattern is visible prose that should have been rendered as Word text, subscript, equation, image, or caption formatting.
