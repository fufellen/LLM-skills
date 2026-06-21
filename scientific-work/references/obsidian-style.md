# Obsidian Style

Use this reference before creating or editing Obsidian notes.

## Writing

- Write in Russian by default.
- Keep English technical terms next to Russian terms when useful.
- Use concise Markdown that is useful as a note, not chat transcript prose.
- Do not add a top-level heading that duplicates the note filename; Obsidian already shows the file title, and repeating it as `# ...` reads as a duplicate title.
- After a short label line ending with `:`, place the following paragraph, list, or code block on the next line without an empty line. Example: `Полезные ключи:` followed immediately by `- ...`.
- Prefer `####` subsections inside existing structured notes.
- Use KaTeX for formulas, not fenced code blocks.
- For inline formulas in Obsidian notes, use `$...$`, not `\(...\)`: in this vault `\(...\)` can remain visible in rendered text instead of displaying as math. Use `$$...$$` for display equations.
- After formulas that introduce or combine symbols, explain notation with a separate, non-indented `Где:` block followed immediately by non-indented bullet items, for example `Где:` then `- $\beta$ - ...` and `- $k_0$ - ...`. Do not indent `Где:` or its bullets under a previous list item, because Obsidian will render them as nested bullets.

## Links

- Use Obsidian links for local concepts: `[[FCS]]`, `[[CRC_32|CRC-32]]`.
- If a term has a common display alias, use `[[Note title|alias]]`.
- When a new term note was created because of a specific source note, link the term naturally from that source note if the location is obvious.
- Do not add meta-comments inside notes such as "to avoid duplication"; just link naturally.

## Term Notes

- Start with a short definition.
- Add physical or engineering meaning.
- Add key formula, packet field, geometry, applicability, or limitation when relevant.
- Keep small standalone term notes focused; link out for deeper context.

## Safety

- Do not move or rename notes unless explicitly asked.
- Do not create broad folder restructures during a focused answer.
