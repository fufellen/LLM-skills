# Obsidian API Integration Lessons

Use this file for compact reusable lessons learned while using Obsidian Local REST API, MCP, and related helper scripts with the synced vault. Keep it operational: short rules, failure modes, command patterns, validation checks, and pointers to scripts. Do not store secrets, API keys, private note contents, raw confidential material, generated logs, or one-off project facts.

## Current Lessons

- Treat Obsidian Local REST API / MCP as the primary live-vault interface when Obsidian is expected to be open with the synced Google Drive vault. Verify with `scripts/Test-ObsidianLocalRestApi.ps1` before relying on it.
- Use `scripts/Invoke-ObsidianLocalRestApi.ps1 -OutputFile <temp>` for compact reads when downstream PowerShell processing is needed. Piping raw API output directly into selectors can create noisy or misleading command behavior.
- For term-note search, exclude `*.excalidraw.md` and `*.excalidraw.restored.md` on the first pass unless the task explicitly concerns diagrams. Search diagram files separately when labels inside drawings are likely to matter.
- API write operations are good for creating or replacing a whole note, but they do not provide a visible diff by themselves. For larger edits, keep a before/after temp copy or use patch/diff control before writing back.
- API access is a transport, not semantic search. Good recall still requires synonym queries, title checks, content checks, and targeted reads of candidate notes.
- After creating or materially editing notes through the API, run `scripts/Test-Note.ps1 <path> -First 24 -CheckLinks` on the created/changed notes.

## Learning Triggers

Append a new compact lesson here when any of these happens:

- an endpoint behaves differently from expectation;
- a search pattern produces repeated noise or misses relevant notes;
- an API edit flow needs a safer before/after or validation step;
- a repeated command sequence should become a script;
- a cross-PC setup detail affects reliability;
- an Obsidian plugin, MCP behavior, or vault indexing behavior changes the preferred workflow.

When a lesson becomes a general decision rule or setup requirement, move or copy the distilled rule into `references/obsidian-ai-integration.md` and keep this file as the operational history.
