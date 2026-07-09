---
name: ru-language-purity
description: Keep Russian scientific prose natural and free of English calques (кальки), суржик, false friends, and invented compound words, and catch the mirror problem of Russian insider jargon leaking into English manuscripts. Use before writing or editing Russian научный текст, as a full pass over any Russian text translated from an English (AI-written) draft, and when checking an English version written from a Russian working draft. Shared source of truth for де-кальке rules, referenced by scientific-article-writing, nto-formatting, optics-spectroscopy-article, apede-ieee-conference-article, and any skill producing bilingual RU/EN technical text.
---

# RU/EN Language Purity (де-кальки)

## Purpose

Single shared discipline for natural bilingual scientific language, so the
де-кальке checklist lives in ONE place and every manuscript / report skill
references it instead of re-embedding its own copy. Two directions:

- **RU prose** must not inherit English calques (кальки), false friends,
  суржик, or invented compound words when it is written from - or translated
  from - an English draft, especially an AI-generated one.
- **EN prose** written from a Russian working draft must not carry insider
  Russian-lab calques and working-title jargon that mean nothing to an
  international reader (the mirror problem).

Written imperatively so any model, including weaker ones, can apply it
without judgment calls.

## When To Apply

- MANDATORY before writing or editing Russian manuscript / report prose.
- MANDATORY as a full pass over any Russian text that is, or descends from,
  a translation of an English draft.
- When producing or reviewing an English version written from a Russian
  working draft (the mirror check below).

## RU Direction - De-Calque

Read and apply `references/decalque-ru-en.md`. It is the single source of
truth for RU de-calque pairs and holds:

- the strategic rules (rewrite from facts, resolve sense against the source,
  existence test for coined words) - apply these FIRST, they beat
  word-by-word fixes;
- the verified replacement tables by defect class (false friends and
  wrong-sense translations, invented calque compounds, imported metaphors,
  суржик raw-English words);
- the deliberate keeps (do not over-correct established terms such as
  «метрики», «вытекающая мода», «отсечка»);
- the grep automation recipe and the count-asserted bulk-fix rule.

New caught calques are added to that file, not inlined here.

## EN Direction - Working-Vocabulary Leakage (mirror)

An English version written from a Russian working draft inherits insider
calques that mean nothing to an international reader. Watch for:

- "local" meaning "our in-house runs" ("local COMSOL data" -> "our /
  reference COMSOL runs");
- "referred to locally as" -> "known in the Russian-language literature as";
- working-title jargon that was never introduced ("failure atlas" -> spell
  out the meaning);
- compound shorthand ("COMSOL-side step" -> "a step on the FEM side");
- ML working jargon in physics prose ("hold-out FEM points" ->
  "confirmatory FEM checks");
- in-figure text (legends, captions) drifting from the manuscript's own
  terminology ("planar anchor" in the legend while the text says
  "planar reference") - figures follow the text's terms.

Also scan for British spellings (IEEE uses American English), "allows to /
possibility to / it is necessary to note", doubled words, and "data is".

## Allowed English In Russian Prose

English is allowed ONLY: (a) in parentheses when first defining a term or
abbreviation, (b) in established abbreviations (PCM, FEM, SPP, PML, COMSOL,
TM), (c) inside reference titles. Everything else is a defect. Register:
научный стиль уровня опытного ученого.

## Self-Improvement And Publishing

When language work reveals a durable, reusable calque, false-friend, or
суржик pair, use the `skill-learning` policy: add the pair to the matching
class table in `references/decalque-ru-en.md` (not as prose in this
SKILL.md) and keep the grep list there current. Do not store secrets,
credentials, unpublished manuscript content, referee correspondence,
copyrighted source text, generated logs, or one-off facts.

Before materially editing this skill, run the owning repository's freshness
check: fetch `origin main`, compare local `HEAD` with `origin/main`,
fast-forward if behind and clean, inspect dirty/ahead/diverged states first.

After materially updating this skill, validate the shared base and adapters
when feasible, then commit and push to the owning repository by default
unless the user says not to. Stage only relevant skill files; split commits
by semantic block; avoid vague rollups. If publishing hits remote changes or
merge conflicts, resolve them autonomously when the intended meaning is
determinable from files, history, and the user's instruction; otherwise stop
and report.

This skill is the source-of-truth safety copy and is also mirrored into a
downstream corporate skills repository so corporate skills can reference it.
Keep this copy; if corporate publishing, permissions, sync, or merge fails,
preserve and report this copy.
