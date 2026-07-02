# Obsidian Style

Use this reference before creating or editing Obsidian notes.

## Writing

- Write in Russian by default.
- Keep English technical terms next to Russian terms when useful.
- Use concise Markdown that is useful as a note, not chat transcript prose.
- Do not add a top-level heading that duplicates the note filename; Obsidian already shows the file title, and repeating it as `# ...` reads as a duplicate title.
- After a short label line ending with `:`, place the following paragraph, list, or code block on the next line without an empty line. Example: `Полезные ключи:` followed immediately by `- ...`.
- Prefer `####` subsections inside existing structured notes.
- Do not leave an empty line after a heading; place the following paragraph, list, or code block on the next line directly under the heading, the same as after a label line.
- Use LaTeX math syntax for formulas, not fenced code blocks. Obsidian renders it with MathJax, so the engine is not KaTeX; write plain LaTeX math.
- For inline formulas in Obsidian notes, use `$...$`, not `\(...\)`: in this vault `\(...\)` can remain visible in rendered text instead of displaying as math. Use `$$...$$` for display equations.
- Do not embed bare math operators like `$\le$`, `$\ge$`, `$\sim$` glued into prose (e.g. `($\le$400 нм)` or `$P\ge$half-max`) - such fragments render unreliably in Obsidian (user-confirmed). Either use the Unicode character in plain text (`(≤400 нм)`, `P ≥ half-max`) or put the whole expression inside one inline formula (`$\lambda \le 400$ нм`).
- After formulas that introduce or combine symbols, explain notation with a separate, non-indented `Где:` block followed immediately by non-indented bullet items, for example `Где:` then `- $\beta$ - ...` and `- $k_0$ - ...`. Do not indent `Где:` or its bullets under a previous list item, because Obsidian will render them as nested bullets.
- Never fold formula notation into an inline prose sentence such as "где $X$ — ..., $Y$ — ...". Always use the `Где:` block with exactly one symbol per bullet, even for just two or three symbols, in the form `- $symbol$ - description` (symbol, space-hyphen-space, then the meaning). Link every symbol that has a term note, for example `- $\mathbf{P}$ - [[материальная поляризация среды (P)]]` and `- $\varepsilon_0$ - [[диэлектрическая проницаемость свободного пространства (вакуума)]]`.

## Links

- Use Obsidian links for local concepts: `[[FCS]]`, `[[CRC_32|CRC-32]]`.
- Use the shortest Obsidian link path that resolves unambiguously, matching Obsidian's "Shortest path when possible" behavior. Prefer `[[Note title]]` or `[[Note title|alias]]`; include folders only when needed to disambiguate duplicate note names, and avoid full vault-relative paths unless no shorter stable link works.
- The same shortest-path rule covers attachment embeds (images, PDFs): prefer a bare `![[file.png]]` when the filename is unique in the vault, and add the minimal folder path only to disambiguate a duplicate name. Never use parent-relative `../` paths in links or embeds — under Obsidian's default "Shortest path when possible" link format they resolve unreliably, so the embed silently breaks (shows a broken-image placeholder) even though the file exists on disk.
- When writing formula notation blocks such as `Где:`, check whether explained terms already have notes in the vault and link them in the bullet text; for example use `[[Propagation constant (постоянная распространения, продольное волновое число)|постоянная распространения]]` instead of plain "постоянная распространения".
- If a term has a common display alias, use `[[Note title|alias]]`.
- Do not put LaTeX or other math markup inside an aliased Obsidian wikilink display text, for example avoid `[[Note title|длина $\pi$-фазового сдвига]]`: Obsidian renders the alias as link text and the formula may remain literal. Put the formula outside the link, for example `$L_\pi$ - длина $\pi$-фазового сдвига, см. [[L_pi (длина pi-фазового сдвига)]]`.
- Do not put aliased Obsidian wikilinks `[[Note title|alias]]` inside Markdown table cells: the `|` can be parsed as a column separator and break the table. In tables, use plain text in the cell and add the Obsidian link in surrounding prose, or use an aliasless `[[Note title]]` link if the full title is acceptable.
- Do not duplicate standalone term-note explanations inside working notes, paper notes, method notes, or formula notation blocks. If a term already has a note, link it and keep only the local role needed for the current formula or argument.
- When a new term note was created because of a specific source note, link the term naturally from that source note if the location is obvious.
- Do not add meta-comments inside notes such as "to avoid duplication"; just link naturally.
- Linking direction (one-line rule): a specific note always links up to its broader concept with exactly one inline link (for example RC-цепь → `[[Теория цепей]]`, reading as "частный случай ..."); a general note links down to specific notes only when it genuinely acts as a hub/MOC and the list is curated deliberately, never exhaustively by hand, because Obsidian backlinks already expose the children. When adding only one direction, prefer specific→general.
- Distinguish three link roles so direction is unambiguous: hierarchical (specific→general, "частный случай"), structural (hub/MOC → its curated children), and contextual/definition (a note that *uses* a term links to that term's standalone term-note). A definition link is usage→definition (lateral), not a taxonomic up-link: linking `[[Реактивное сопротивление]]` from RC-цепь means RC-цепь uses the term, not that it is a kind of it. This realizes single source of truth — the definition lives once in the term-note and everything else links to it, while backlinks collect the usages.
- When a term with a standalone term note appears multiple times in the same note's running prose, link every occurrence, not only the first. Do not apply a "link once per note is enough" convention: repeat `[[Note title|alias]]` (or the bare term as an alias, e.g. `[[Локализованный поверхностный плазмонный резонанс (LSPR)|ЛППР]]`) at each place the term's word or abbreviation appears, even ten times in one note. This was an explicit user correction after an abbreviation (`ЛППР`) was left unlinked on a later occurrence in a note that had already linked it once earlier.

## Term Notes

- Start with a short definition.
- Add physical or engineering meaning.
- Add key formula, packet field, geometry, applicability, or limitation when relevant.
- Keep small standalone term notes focused; link out for deeper context.

## Paper Notes

- In notes that analyze or reproduce a paper, never cite the paper's internals bare: "формула (1)", "рис. 2", "п. 3" must say whose they are - "формула (1) статьи [[paper-note]]", "рис. 2 статьи" - because the note has its own figures/formulas and bare numbers are ambiguous. Referencing the source paper's own formulas, paragraphs, and headings is allowed and encouraged; when the note reproduces that formula in its own section, also point to that section ("воспроизведена в п. 2.1").
- Reproduction/method notes need a geometry/model schematic per modeling level (what exactly is being solved: layers, periods, sizes, incidence) - a reader should not have to reconstruct the solved structure from prose; generate a simple matplotlib scheme into the note's media folder if the source has none.

## Mermaid Diagrams

- In Mermaid node labels for Obsidian, do not start text with Markdown list markers such as `1.`, `-`, or `*`: Obsidian/Mermaid may render the node as `Unsupported markdown: list`. Use wording such as `Шаг 1 - ...` instead of `1. ...`.

## Safety

- Do not move or rename notes unless explicitly asked.
- Do not create broad folder restructures during a focused answer.
