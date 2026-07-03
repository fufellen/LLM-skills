# Obsidian AI Integration

Use this reference when connecting Codex or another AI assistant to the user's Obsidian vault.

## Preferred Stack

1. Use native Obsidian capabilities first:
   - Search
   - Backlinks
   - Outgoing links
   - Graph view
   - Properties
   - Bases
2. Use local `scripts/` helpers from this shared-base skill as a filesystem fallback for UTF-8-safe note reads and exact search.
3. Use `Obsidian Local REST API` when an external agent needs live Obsidian access, metadata, or MCP.

## Installed Bridge

The vault is prepared for the community plugin:

- Plugin id: `obsidian-local-rest-api`
- Name: `Local REST API with MCP`
- Target folder: `.obsidian/plugins/obsidian-local-rest-api`
- Default API/MCP base URL: `https://127.0.0.1:27124`
- MCP endpoint: `https://127.0.0.1:27124/mcp/`

The plugin release files are stored under `.obsidian/plugins`, so they can sync through Google Drive with the vault.

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

## Helper Scripts

- `scripts/Install-ObsidianLocalRestApi.ps1` installs or updates the plugin from GitHub release assets. Use `-Enable` to add it to `.obsidian/community-plugins.json`.
- `scripts/Get-ObsidianLocalRestApiConfig.ps1` reads the synced config and reports whether the API key is configured, masking the key by default.
- `scripts/Test-ObsidianLocalRestApi.ps1` checks whether the local API port is open and uses the synced API key automatically when configured.
- The HTTPS endpoint uses a local self-signed certificate; if Windows PowerShell fails the authenticated request, the test script falls back to `curl.exe -k`.

Example install/update:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\.codex\skills\_base\skills\scientific-work\scripts\Install-ObsidianLocalRestApi.ps1" -Enable
```

Example status check without exposing secrets:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\.codex\skills\_base\skills\scientific-work\scripts\Test-ObsidianLocalRestApi.ps1"
```

If the plugin is enabled and Obsidian is running, but `api_key_configured` is false, ask the user to paste the key from Obsidian settings into the synced config path above.

## When To Use What

- Exact local text search: `Search-Vault.ps1` or Obsidian Search.
- Term-note workflow: `Find-Term.ps1` plus normal Markdown edits.
- Structured note lists/tables: Obsidian Bases first, Dataview if Bases is not enough.
- Semantic discovery: Smart Connections, if installed and configured by the user.
- External AI tool access to the live vault: Obsidian Local REST API / MCP.

## Safety

- Do not create additional copies of API keys, bearer tokens, or generated credentials outside the standard synced config path unless the user explicitly asks.
- Do not print the full synced API key in normal responses; report only whether it is configured.
- Do not mass-edit backlinks or term links without inspecting samples first.
- Prefer read-only API operations until the target note and intended edit are unambiguous.
- Keep filesystem scripts as fallback even when MCP is available, because they work without Obsidian running.
