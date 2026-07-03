param(
    [string]$VaultRoot,

    [switch]$RevealKey
)

$ErrorActionPreference = "Stop"
$utf8NoBom = [System.Text.UTF8Encoding]::new($false)
[Console]::OutputEncoding = $utf8NoBom
$OutputEncoding = $utf8NoBom

if (-not $VaultRoot) {
    $probe = $PSScriptRoot
    while ($probe -and -not (Test-Path -LiteralPath (Join-Path $probe ".obsidian") -PathType Container)) {
        $probe = Split-Path -Parent $probe
    }
    if ($probe) {
        $VaultRoot = $probe
    }
    else {
        $VaultRoot = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot "..\..\..\..")).Path
    }
}

$configPath = Join-Path $VaultRoot ".codex\secrets\scientific-work\obsidian-local-rest-api.json"
$legacyConfigPath = Join-Path $VaultRoot ".codex\skills\scientific-work\secrets\obsidian-local-rest-api.json"

if ((-not (Test-Path -LiteralPath $configPath -PathType Leaf)) -and (Test-Path -LiteralPath $legacyConfigPath -PathType Leaf)) {
    $configPath = $legacyConfigPath
}

if (-not (Test-Path -LiteralPath $configPath -PathType Leaf)) {
    throw "Obsidian Local REST API config not found: $configPath"
}

$config = Get-Content -Encoding UTF8 -Raw -LiteralPath $configPath | ConvertFrom-Json
$key = [string]$config.api_key
$placeholder = "PASTE_OBSIDIAN_LOCAL_REST_API_KEY_HERE"
$configured = -not [string]::IsNullOrWhiteSpace($key) -and $key -ne $placeholder

if ($RevealKey) {
    $keyOut = $key
}
elseif ($configured) {
    if ($key.Length -le 8) {
        $keyOut = "***"
    }
    else {
        $keyOut = "$($key.Substring(0, 4))...$($key.Substring($key.Length - 4))"
    }
}
else {
    $keyOut = "(not configured)"
}

[pscustomobject]@{
    config_path = $configPath
    base_url = $config.base_url
    mcp_endpoint = $config.mcp_endpoint
    api_key_configured = $configured
    api_key = $keyOut
}
