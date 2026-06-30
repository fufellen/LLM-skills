# Obsidian Canvas Patterns

## Canvas JSON Basics

An Obsidian `.canvas` file is JSON with two top-level arrays:

- `nodes`: visual items.
- `edges`: links between nodes.

Common text node fields:

```json
{
  "id": "stable-node-id",
  "type": "text",
  "text": "Markdown content",
  "x": 0,
  "y": 0,
  "width": 400,
  "height": 220,
  "color": "1"
}
```

Common edge fields:

```json
{
  "id": "edge-parent-child",
  "fromNode": "parent-id",
  "fromSide": "bottom",
  "toNode": "child-id",
  "toSide": "top",
  "label": "optional label"
}
```

Use `toEnd: "arrow"` only when the file or user's style already relies on explicit arrowheads. Obsidian can render edges without it.

## Horizontal Main Split, Detail Below

Use this when the user asks for a tree where the main decomposition is horizontal and lower rows contain more detail.

Layout recipe:

1. Put the root at the top center.
2. Put primary branches on the same `y` row, spaced horizontally.
3. Put each branch's children below that branch.
4. Put leaves below their direct parent, not in the main split row.
5. Put formulas, legends, and notes to the side as reference cards.

For a binary/protocol/packet structure, a good level model is:

- Level 0: whole packet or object.
- Level 1: main sections, such as `Header`, `Body`, `Tail`.
- Level 2: grouped fields or repeated structures.
- Level 3: individual fields or leaf details.

Suggested spacing:

- horizontal gap between primary branches: at least 500 px;
- horizontal gap between sibling detail cards: at least 60 px;
- vertical gap between levels: at least 120 px beyond the tallest card in the previous level;
- keep `width` stable for sibling cards when possible.

## Top-Down Tree

Use this for a direct hierarchy or decision tree:

- parent above child;
- sibling nodes share the same `y`;
- parent-to-child edges use `fromSide: bottom` and `toSide: top`;
- avoid chaining sibling details unless the data itself is sequential.

## Left-To-Right Flow

Use this for temporal processes, pipelines, and packet byte order when the user asks for a flow:

- put stages on the same `y` row;
- use `fromSide: right` and `toSide: left`;
- place annotations above or below the stage they explain.

## Edge Conventions

- Tree hierarchy: `bottom -> top`.
- Lateral reference: `right -> left` or `left -> right`.
- Avoid connecting every related concept. Prefer the few edges that make the intended reading path obvious.
- Edge IDs should be stable and descriptive: `edge-root-header`, `edge-body-point`, `edge-echo-distance`.

## Text Node Conventions

- Use a heading that names the concept.
- Put byte ranges, formulas, or critical constants near the top of the node.
- Keep leaf nodes specific and short.
- Preserve source-language terminology from the user.
- Use code formatting for field names, constants, filenames, and formulas.

## Common Repair Checklist

Before finishing:

- JSON parses successfully.
- Every node has a unique `id`.
- Every edge references existing `fromNode` and `toNode` IDs.
- Edge sides match the visual direction.
- Main branches are aligned on the same row when the layout is hierarchical.
- Child details are lower than their parent in top-down trees.
- No important nodes overlap.
