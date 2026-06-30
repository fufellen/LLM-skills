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
- After formulas that introduce or combine symbols, explain notation with a separate, non-indented `Где:` block followed immediately by non-indented bullet items, for example `Где:` then `- $\beta$ - ...` and `- $k_0$ - ...`. Do not indent `Где:` or its bullets under a previous list item, because Obsidian will render them as nested bullets.

## Links

- Use Obsidian links for local concepts: `[[FCS]]`, `[[CRC_32|CRC-32]]`.
- Use the shortest Obsidian link path that resolves unambiguously, matching Obsidian's "Shortest path when possible" behavior. Prefer `[[Note title]]` or `[[Note title|alias]]`; include folders only when needed to disambiguate duplicate note names, and avoid full vault-relative paths unless no shorter stable link works.
- When writing formula notation blocks such as `Где:`, check whether explained terms already have notes in the vault and link them in the bullet text; for example use `[[Propagation constant (постоянная распространения, продольное волновое число)|постоянная распространения]]` instead of plain "постоянная распространения".
- If a term has a common display alias, use `[[Note title|alias]]`.
- Do not put LaTeX or other math markup inside an aliased Obsidian wikilink display text, for example avoid `[[Note title|длина $\pi$-фазового сдвига]]`: Obsidian renders the alias as link text and the formula may remain literal. Put the formula outside the link, for example `$L_\pi$ - длина $\pi$-фазового сдвига, см. [[L_pi (длина pi-фазового сдвига)]]`.
- Do not put aliased Obsidian wikilinks `[[Note title|alias]]` inside Markdown table cells: the `|` can be parsed as a column separator and break the table. In tables, use plain text in the cell and add the Obsidian link in surrounding prose, or use an aliasless `[[Note title]]` link if the full title is acceptable.
- Do not duplicate standalone term-note explanations inside working notes, paper notes, method notes, or formula notation blocks. If a term already has a note, link it and keep only the local role needed for the current formula or argument.
- When a new term note was created because of a specific source note, link the term naturally from that source note if the location is obvious.
- Do not add meta-comments inside notes such as "to avoid duplication"; just link naturally.
- Linking direction: always add the specific→general link, since a specific note is naturally an instance of the broader concept (for example RC-цепь → `[[Теория цепей]]`); this reads as "частный случай ...". Add general→specific links only as a deliberate curated hub/list, not exhaustively by hand, because Obsidian backlinks already expose the children. When adding only one direction, prefer specific→general.

## Term Notes

- Start with a short definition.
- Add physical or engineering meaning.
- Add key formula, packet field, geometry, applicability, or limitation when relevant.
- Keep small standalone term notes focused; link out for deeper context.

## Mermaid Diagrams

- In Mermaid node labels for Obsidian, do not start text with Markdown list markers such as `1.`, `-`, or `*`: Obsidian/Mermaid may render the node as `Unsupported markdown: list`. Use wording such as `Шаг 1 - ...` instead of `1. ...`.

## Safety

- Do not move or rename notes unless explicitly asked.
- Do not create broad folder restructures during a focused answer.
