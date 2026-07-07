# PowerPoint File Workflow

Use this reference when reading, editing, validating, or creating `.pptx` decks directly.

## Safe File Handling

- Treat an existing user deck as the original artifact. Create a copy before edits unless the user explicitly permits direct modification.
- Use clear suffixes such as `_copy`, `_kopiya_s_dopolneniyami`, `_reviewed`, or a dated version when that matches the user's language and folder style.
- On Windows, verify resolved absolute paths before recursive moves/deletes. Delete only files or folders created for this task.
- When passing Cyrillic paths or text from PowerShell into Python, prefer environment variables or UTF-8 files over inline stdin literals if encoding corruption appears.

## Inspection

- Use `python-pptx` when available to read slide count, page size, shapes, text boxes, notes, and media metadata.
- Iterate over `slide.shapes` directly; avoid brittle assumptions about shape order beyond what you have inspected.
- Extract slide text before edits and again after edits. Keep the before/after mapping for changed slides.
- If `python-pptx` cannot parse a file, inspect the `.pptx` ZIP parts (`ppt/slides/slide*.xml`, relationships, media) with structured XML parsing.

## Editing

- Preserve existing theme, image backgrounds, typography, and layout rhythm for targeted improvements.
- When replacing text, preserve or deliberately reset font family, size, bold, color, and paragraph breaks. Reduce font size or shorten text when adding lines to a constrained text box.
- Prefer adding content into existing placeholders or duplicated design patterns. Avoid adding visually unrelated boxes, colors, or fonts.
- Use structured APIs for slides, shapes, relationships, and media. Avoid raw search/replace across XML unless no safer path exists and the change is tightly scoped.
- If a deck needs substantial reconstruction and programmatic editing is too fragile, create a new deck in the requested tool or make a copy and document the manual/GUI step that remains.
- For illustrated or photo-based slides, treat faces, bodies, gestures, key objects, symbolic animals, and focal action as protected visual areas. In group scenes, protect foreground people as a set, especially children, including partially visible figures in reeds, crowds, doorways, or background action. Protect the whole visible extent of important subjects, not only the face; covering a rooster's tail, a child's hairline, a disciple's head edge, a staff, a hand, or a key object with a translucent card still counts as overlap. Text cards may overlap low-importance texture or background, but should not cover the main person, group, animal, or object even when the card is translucent.
- Keep text readable after layout fixes. If avoiding overlap requires making body text tiny, shorten the visible slide text, move secondary quotes or teacher support into speaker notes, or choose/regenerate a composition with more open space.

## Validation

- Validate `.pptx` integrity as a ZIP (`testzip`) and load it with `Presentation(...)` when using `python-pptx`.
- Re-extract changed slide text to confirm Cyrillic, punctuation, scripture references, and line breaks survived.
- Check slide count, target deck path, and original deck timestamp/size when preservation matters.
- Render or open the deck in PowerPoint, LibreOffice, Google Slides, or the browser when available, especially after layout-heavy edits.
- Look for text overflow, unreadable contrast, broken images, missing fonts, accidental removal of speaker notes or media, visible presenter-only cues that belong in speaker notes, oversized empty text panels, and overlays that hide the main visual subject.

## Handoff Note

For nontrivial work, leave or report:

- created/updated file path;
- source deck path when a copy was used;
- changed slide numbers and short reasons;
- local notes, images, prompts, and external URLs used;
- validation performed and any checks that could not be run.
