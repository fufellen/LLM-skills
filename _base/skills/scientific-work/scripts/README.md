# Scientific Work Scripts

Reusable UTF-8-safe helpers for searching and reading the Obsidian vault from PowerShell.

## Scripts

- `Read-Note.ps1` - read a Markdown note with explicit UTF-8 handling.
- `Search-Vault.ps1` - search the vault with `rg`, consistent exclusions, and UTF-8 output.
- `Find-Term.ps1` - look for matching note titles and nearby content matches for a scientific or technical term.
- `Find-ExistingPaperPdf.ps1` - search for already downloaded paper PDFs by DOI, DOI-safe fragment, DOI suffix, year, and stable title words before downloading duplicates.
- `Install-ObsidianLocalRestApi.ps1` - install/update Obsidian Local REST API release files into `.obsidian/plugins`.
- `Get-ObsidianLocalRestApiConfig.ps1` - read the synced Obsidian Local REST API config and report whether the API key is configured.
- `Test-ObsidianLocalRestApi.ps1` - check whether the local Obsidian REST/MCP endpoint is reachable.

## Examples

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\.codex\skills\scientific-work\scripts\Read-Note.ps1" "PhD\Кандидатский экзамен\1. Теория колебаний\11.md" -First 80
```

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\.codex\skills\scientific-work\scripts\Search-Vault.ps1" "показатель Ляпунова" -Roots PhD -Context 2 -Literal
```

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\.codex\skills\scientific-work\scripts\Find-Term.ps1" "показатель Ляпунова" -Roots PhD
```

Use `-AllVault` when the term may appear outside the default research area.

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\.codex\skills\scientific-work\scripts\Find-ExistingPaperPdf.ps1" -Doi "10.1063/5.0082094" -Year 2022 -Title "Ultra-compact nonvolatile plasmonic phase change modulators and switches with dual electrical-optical functionality" -Root "."
```

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\.codex\skills\scientific-work\scripts\Install-ObsidianLocalRestApi.ps1" -Enable
```

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\.codex\skills\scientific-work\scripts\Test-ObsidianLocalRestApi.ps1"
```

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\.codex\skills\scientific-work\scripts\Get-ObsidianLocalRestApiConfig.ps1"
```
