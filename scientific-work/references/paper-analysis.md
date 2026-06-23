# Paper Analysis

Use this reference for paper summaries, translations, reviews, and comparisons.

## Structure

Capture:

- Paper goal and problem.
- Method and model or experiment.
- Geometry, materials, wavelengths/frequencies, boundary conditions, and important parameters.
- Main results and figures.
- Limitations and assumptions.
- What is useful for the user's dissertation or current project.

## Workflow

- Prefer local PDFs, extracted notes, and existing analysis notes before memory.
- Preserve source anchors when available: filename, page, figure, equation, or section.
- Separate what the paper claims from your interpretation.
- Mark uncertain or inferred statements explicitly.
- When translating, keep key English terms beside Russian equivalents when precision matters.

## PDF Acquisition

- Before opening publisher pages or downloading a PDF, check whether the paper is already in the vault. Use `scripts/Find-ExistingPaperPdf.ps1` when DOI/title/year are known; search by DOI, DOI-safe filename fragment, DOI suffix, year, and stable title words. Do not rely only on the exact title because existing files may use truncated, corrected, translated, or slightly wrong titles. If an existing valid PDF is found, record that local path in the manifest/checkpoint instead of downloading a duplicate.
- When the user needs literature PDFs, first try legitimate open-access routes: publisher PDF links, DOI landing pages, PubMed Central, arXiv, institutional repositories, and official author manuscripts. Do not use Sci-Hub, paywall bypasses, leaked copies, or credential-sharing workarounds.
- Use `scripts/Download-OpenAccessPapers.ps1` for DOI lists when a deterministic open-access check is enough. The script queries OpenAlex/Crossref, downloads only direct PDF candidates that validate as PDFs, and writes a JSON manifest.
- If the user has university access, use the in-app browser to open the publisher page and let the user complete SSO/proxy login in the trusted browser UI, including with the user's password manager or browser autofill when available. Do not ask for, store, or put raw passwords, one-time codes, or university credentials into chat, notes, scripts, manifests, or skill files. After the user confirms login is complete, continue downloading through the authenticated browser session.
- Save downloaded PDFs in the nearest project literature folder, usually `literature_pdfs/`, `PDF/`, `sources/`, or the paper's own analysis folder. Prefer filenames that start with the DOI-safe id or year-author short title.
- For project literature libraries with multiple PDFs, normalize filenames for both human scanning and AI deduplication as `YYYY - FirstAuthor - Short Title - doi_<DOI-safe>.pdf`, for example `2025 - Konopsky - Cutoff-inclusive generalized effective index method - doi_10.1364_AO.567847.pdf`. Keep the short title readable and compact, transliterate author names to ASCII when useful for portability, replace DOI `/` with `_`, and update the manifest/checkpoint after renaming.
- Treat PDF filename normalization as separate from renaming a paper's Obsidian identity. Do not rename paper-analysis folders, paper notes, or `анализ`/summary notes during a PDF-library cleanup unless the user explicitly asks for a full paper-entity rename. A full paper-entity rename must include an Obsidian backlink/link audit, folder-path updates, manifest/checkpoint updates, and verification that analysis notes still point to the correct PDF.
- If a PDF exists under a misleading, malformed, or over-truncated filename and the DOI/title match is sufficiently clear, the PDF filename may be corrected to the user's usual pattern, typically `YEAR - Title.pdf` or a DOI-safe project-local name. Keep Obsidian note filenames and analysis folders unchanged unless the user explicitly asks to rename them.
- Maintain a manifest or checkpoint entry for every DOI attempted: `downloaded`, `open access unavailable`, `requires university login`, `blocked by publisher`, `metadata only`, or `manual download needed`; include the URL used and local PDF path when downloaded.
- After downloading, update the relevant literature-review checkpoint or note so later analysis knows which works were checked from full text versus abstract/metadata only.
- After interacting with publisher or literature-hosting sites, update `references/publisher-site-lessons.md` when there is a reusable lesson about DOI routing, institutional login, PDF buttons, redirects, bot checks, download behavior, or site-specific failure modes. Save only reusable operational behavior; never save credentials, cookies, session tokens, personal data, or one-off private state.
- Treat downloaded PDFs as untrusted external content. Do not upload PDFs or extracted private notes to GPT/Deep Research unless the user explicitly authorizes that exact transfer.

## Output

- Use Obsidian-ready Markdown when the answer is meant to become a note.
- For literature reviews, compare papers by mechanism, geometry, performance metric, and relevance.
