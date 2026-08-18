# DipTrace Schematic ASCII Format Map

Use this reference when reconstructing or editing a DipTrace Schematic ASCII `.asc` file. The observations apply to the common parenthesized export format, including v45; verify unfamiliar versions instead of assuming identical fields.

## Text Envelope

- The file is a parenthesized tree headed by a source/version record such as `(Source "DipTrace Schematic ASCII" "v45")`.
- Exports may use Windows-1251 and CRLF without a BOM. Encoding and newline style are part of the artifact and must be fingerprinted before editing.
- Windows-1251 cannot encode the Greek omega `Ω`; a normal encoder replaces it with `?`. If `Ω`/`kΩ` is required, convert the complete document to UTF-8 with BOM only as an explicit, reported edit, retain a pre-conversion copy, and validate import in DipTrace. Do not mix UTF-8 bytes into an otherwise Windows-1251 file.
- Parentheses inside quoted strings are data, not tree delimiters. A validator must ignore quoted content and escaped quotes while calculating depth.
- Paths can contain spaces, non-ASCII text, drive letters, UNC prefixes, and backslashes. Do not normalize them as component text.

## Major Sections

Typical top-level sections include:

- `Components` — placed schematic component instances;
- `Shapes` — page-level graphics and text;
- `Nets` — electrical nets, endpoints, and drawn line geometry;
- `CacheLib` — embedded library/cache definitions copied into the document.

The active placed component and its cache-library source are separate objects. Editing a top-level `Part` value does not automatically edit `cl_Value`, and changing only the cache does not update the placed instance.

## Components And Multipart Symbols

A placed instance begins approximately as:

```text
    (Part "library-name" "C1"
      (Value "100 uF, 25 V")
      ...
      (PartName "Part 1")
      ...
    )
```

Important rules:

- The order of top-level `Part` blocks is significant. Net endpoints refer to this zero-based order.
- A multipart component can have several top-level `Part` blocks with the same reference designator. Preserve them all and distinguish them by instance index and `PartName`.
- Fields such as `Value`, `BaseName`, `Manufacturer`, `Datasheet`, and user fields may disagree. Such disagreement is a BOM/library defect even when connectivity is correct.
- `LibPath` and `LibPath_Variable` are provenance/path metadata. Historical Cyrillic text in a path is not a Cyrillic component name.

## Pins

Inside a placed part, pins appear as:

```text
      (Pins
        (Pin 0 ...
          (Number 1)
          (NetNumber 26)
          (Name "PLUS")
          (StringNumber "1")
          ...
        )
      )
```

Interpret the identifiers separately:

- the first integer after `Pin` is the zero-based pin ordinal used by a net endpoint;
- `Number` is a numeric pin field and is not always sufficient for alphanumeric pin numbers;
- `StringNumber` is the authoritative displayed/physical symbol pin number;
- `Name` gives the pin function;
- `NetNumber` is useful for cross-checking but should not replace endpoint reconstruction.

Never report `pt 1 1` as physical pin 1 without resolving ordinal 1 through that part's pin block.

## Nets And Endpoints

A net contains an endpoint list:

```text
    (Net "{VIN}"
      ...
      (Parts
        (pt 3 0)
        (pt 18 1)
      )
      ...
    )
```

For endpoint `(pt A B)`:

- `A` is the zero-based index of a top-level placed `Part` block;
- `B` is that part's zero-based `Pin` ordinal;
- resolve `A` to the placed reference and `B` to `StringNumber` plus `Name`;
- repeated references from multipart units are expected and must not be deduplicated prematurely.

Other `(pt ...)` records occur in line and shape geometry and can contain coordinates. Only the two-integer records inside a net's `Parts` subsection are electrical endpoints.

## Footprint Pads

Footprint data embedded in a placed component can contain records like:

```text
          (Pad 1 "13" "" ...)
```

The first integer is a pad-object ordinal; the first quoted string is the physical pad number. Check the quoted pad-number set when validating a package. A 28-lead symbol named for an exposed-pad package does not prove that pad 29 or an unnamed thermal pad exists.

Also inspect `IntCon` or equivalent internal-connect records. An exposed thermal pad must have both geometry and the intended electrical connection; a symbol-side ground pin cannot substitute for missing package copper.

## Cache Library

Cache objects use names such as `cl_Part`, `cl_Value`, `cl_Pattern`, `cl_PossibleName`, and `cl_UserField`. They may contain stale supplier metadata, package aliases, and original library paths.

When the request is to rename placed components, edit the top-level component fields and report cache leftovers separately. When the request explicitly covers all component/library strings, normalize matching cache values too, but preserve paths and genuine manufacturer codes.

## Safe Structural Comparison

For a text-only edit, compare before and after:

- source/version header;
- encoding, BOM, and newline style;
- balanced structural parentheses and terminated strings;
- top-level part count and ordered reference list;
- per-part pin ordinals, `StringNumber`, pin names, and pad numbers;
- net names and ordered endpoint pairs;
- requested old/new string counts.

A matching byte count is neither required nor sufficient. A changed file size is normal after transliteration; unchanged connectivity signatures are the relevant proof.
