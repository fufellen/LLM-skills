# Obsidian AI Integration

Use this reference when connecting Codex or another AI assistant to the user's Obsidian vault.

## Preferred Stack

The user's Google Drive vault is expected to be open in Obsidian on every working machine, so the Obsidian Local REST API should normally be available. Treat the API/MCP bridge as the primary live-vault interface for Codex when the task benefits from metadata, current Obsidian state, or compact reads/writes.

1. Use `Obsidian Local REST API` / MCP first for live-vault reads, writes, metadata checks, and compact automation.
2. Use native Obsidian capabilities when the user is working interactively in the app:
   - Search
   - Backlinks
   - Outgoing links
   - Graph view
   - Properties
   - Bases
3. Use local `scripts/` helpers from this shared-base skill as a filesystem fallback for UTF-8-safe note reads and exact search when Obsidian/API is unavailable or exact patch control is safer.

## Installed Bridge

The vault is prepared for the community plugin:

- Plugin id: `obsidian-local-rest-api`
- Name: `Local REST API with MCP`
- Target folder: `.obsidian/plugins/obsidian-local-rest-api`
- Default API/MCP base URL: `https://127.0.0.1:27124`
- MCP endpoint: `https://127.0.0.1:27124/mcp/`

The plugin release files are stored under `.obsidian/plugins`, so they can sync through Google Drive with the vault.

The plugin settings file `.obsidian/plugins/obsidian-local-rest-api/data.json` is also part of the synced vault. On a new machine, first assume the plugin configuration has synced; only regenerate or replace keys if the status check below shows authentication failure.

## Synced API Key

The user explicitly chose to keep the Obsidian Local REST API key in Google Drive for cross-PC convenience.

Standard synced config path:

```text
.codex/secrets/scientific-work/obsidian-local-rest-api.json
```

Older checkouts may still have `.codex/skills/scientific-work/secrets/obsidian-local-rest-api.json`; migrate that file to the standard path so the `scientific-work` adapter remains only a thin pointer.

Expected fields:

```json
{
  "base_url": "https://127.0.0.1:27124",
  "mcp_endpoint": "https://127.0.0.1:27124/mcp/",
  "api_key": "..."
}
```

When using Obsidian Local REST API or MCP, read the API key from the standard config path first. Do not print the full key in user-facing responses unless the user explicitly asks to inspect it.

## New Machine Setup Checklist

Use this checklist when setting up Codex/Obsidian API access on another computer:

1. Let Google Drive finish syncing the vault, including `.obsidian/plugins/obsidian-local-rest-api`, `.obsidian/community-plugins.json`, and `.codex/secrets/scientific-work/obsidian-local-rest-api.json`.
2. Open this synced vault in Obsidian and keep Obsidian running while Codex works with the vault.
3. In Obsidian, confirm Community Plugins are enabled and `Local REST API with MCP` is enabled. If the plugin files or enablement are missing, run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\.codex\skills\_base\skills\scientific-work\scripts\Install-ObsidianLocalRestApi.ps1" -Enable
```

4. Verify the synced API config without exposing the full key:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\.codex\skills\_base\skills\scientific-work\scripts\Get-ObsidianLocalRestApiConfig.ps1"
```

5. Test the live API:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\.codex\skills\_base\skills\scientific-work\scripts\Test-ObsidianLocalRestApi.ps1"
```

The healthy result is `tcp_port_open: True` and `authenticated_request: ok: HTTP 200` (plain `Invoke-WebRequest` or `curl.exe -k` fallback are both acceptable). If the port is closed, Obsidian is not running, the wrong vault is open, or the plugin is disabled. If authentication fails, copy the current plugin API key from Obsidian's Local REST API settings into `.codex/secrets/scientific-work/obsidian-local-rest-api.json`.

## Helper Scripts

- `scripts/Install-ObsidianLocalRestApi.ps1` installs or updates the plugin from GitHub release assets. Use `-Enable` to add it to `.obsidian/community-plugins.json`.
- `scripts/Get-ObsidianLocalRestApiConfig.ps1` reads the synced config and reports whether the API key is configured, masking the key by default.
- `scripts/Test-ObsidianLocalRestApi.ps1` checks whether the local API port is open and uses the synced API key automatically when configured.
- `scripts/Invoke-ObsidianLocalRestApi.ps1` is a generic wrapper for authenticated API calls. Prefer it over ad hoc `curl` when Codex needs a compact live-vault read/write.
- The HTTPS endpoint uses a local self-signed certificate; if Windows PowerShell fails the authenticated request, the test script falls back to `curl.exe -k`.

Example install/update:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\.codex\skills\_base\skills\scientific-work\scripts\Install-ObsidianLocalRestApi.ps1" -Enable
```

Example status check without exposing secrets:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\.codex\skills\_base\skills\scientific-work\scripts\Test-ObsidianLocalRestApi.ps1"
```

Example compact note read through the API:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\.codex\skills\_base\skills\scientific-work\scripts\Invoke-ObsidianLocalRestApi.ps1" -Method GET -VaultPath "PhD\Термины\Электродинамика\RC цепь.md"
```

If the plugin is enabled and Obsidian is running, but `api_key_configured` is false, ask the user to paste the key from Obsidian settings into the synced config path above.

## When To Use What

- Exact local text search: `Search-Vault.ps1` or Obsidian Search.
- Term-note workflow: use scripts/API to gather candidate notes, existing definitions, backlinks, and target paths; spend model tokens on synthesis and the final diff, not on repeated manual filesystem plumbing.
- For term-note search, exclude `*.excalidraw.md` and `*.excalidraw.restored.md` on the first pass unless the task explicitly concerns diagrams; Excalidraw compressed JSON can dominate results and waste context, while useful diagram labels can be searched in a second targeted pass.
- Structured note lists/tables: Obsidian Bases first, Dataview if Bases is not enough.
- Semantic discovery: Smart Connections, if installed and configured by the user.
- External AI tool access to the live vault: Obsidian Local REST API / MCP by default, because Obsidian should be open with the synced vault on each machine.

## Token And Time Saving Rule

For recurring Obsidian tasks, prefer a two-layer workflow: small deterministic scripts or Local REST API calls perform search/read/write/validation, and Codex only decides the content and checks the resulting diff. Avoid dumping large note bodies into context when a script can return titles, paths, headings, link status, or short snippets first. Fall back to direct filesystem edits only when Obsidian is not running, the API is unavailable, or exact patch control is safer.

## Self-Learning

Before nontrivial Obsidian API/MCP work, read `references/obsidian-ai-integration-lessons.md` together with this file. After the task, if a reusable lesson appears, update the skill before finishing:

- Add durable workflow rules, endpoint behavior, search heuristics, failure modes, and validation checks to `references/obsidian-ai-integration-lessons.md`.
- Promote repeated command sequences, wrappers, parsers, validators, or safe edit flows into `scripts/` instead of leaving them as chat-only shell history.
- Update this reference when the lesson changes the default decision rule, setup checklist, safety policy, or cross-PC expectation.
- Do not save API keys, tokens, private note contents, raw confidential material, generated logs, or one-off facts in the skill.
- Validate changed scripts or references when feasible, then commit and push the relevant skill files under the `skill-learning` / `skill-management` publishing rules.

## Safety

- Do not create additional copies of API keys, bearer tokens, or generated credentials outside the standard synced config path unless the user explicitly asks.
- Do not print the full synced API key in normal responses; report only whether it is configured.
- Do not mass-edit backlinks or term links without inspecting samples first.
- Prefer read-only API operations until the target note and intended edit are unambiguous.
- Keep filesystem scripts as fallback even when MCP is available, because they work without Obsidian running.
