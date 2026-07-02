param(
    [string]$VaultRoot,

    [string]$Version = "latest",

    [switch]$Enable
)

$ErrorActionPreference = "Stop"
$ProgressPreference = "SilentlyContinue"
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

$repo = "coddingtonbear/obsidian-local-rest-api"
$pluginId = "obsidian-local-rest-api"
$pluginDir = Join-Path $VaultRoot ".obsidian\plugins\$pluginId"
$communityPluginsPath = Join-Path $VaultRoot ".obsidian\community-plugins.json"

if ($Version -eq "latest") {
    $release = Invoke-RestMethod -Uri "https://api.github.com/repos/$repo/releases/latest"
}
else {
    $release = Invoke-RestMethod -Uri "https://api.github.com/repos/$repo/releases/tags/$Version"
}

New-Item -ItemType Directory -Force -Path $pluginDir | Out-Null

$requiredAssets = @("main.js", "manifest.json", "styles.css")

foreach ($assetName in $requiredAssets) {
    $asset = $release.assets | Where-Object { $_.name -eq $assetName } | Select-Object -First 1
    if (-not $asset) {
        throw "Release $($release.tag_name) does not contain required asset: $assetName"
    }

    $target = Join-Path $pluginDir $assetName
    Invoke-WebRequest -Uri $asset.browser_download_url -OutFile $target

    if ($asset.digest -and $asset.digest.StartsWith("sha256:")) {
        $expected = $asset.digest.Substring("sha256:".Length).ToUpperInvariant()
        $actual = (Get-FileHash -Algorithm SHA256 -LiteralPath $target).Hash.ToUpperInvariant()
        if ($actual -ne $expected) {
            throw "SHA256 mismatch for $assetName. Expected $expected, got $actual"
        }
    }
}

if ($Enable) {
    if (Test-Path -LiteralPath $communityPluginsPath) {
        $enabled = Get-Content -Encoding UTF8 -Raw -LiteralPath $communityPluginsPath | ConvertFrom-Json
        $enabled = @($enabled)
    }
    else {
        $enabled = @()
    }

    if ($enabled -notcontains $pluginId) {
        $enabled += $pluginId
        $json = $enabled | ConvertTo-Json
        Set-Content -Encoding UTF8 -LiteralPath $communityPluginsPath -Value $json
    }
}

[pscustomobject]@{
    plugin = $pluginId
    version = $release.tag_name
    directory = $pluginDir
    enabled = if (Test-Path -LiteralPath $communityPluginsPath) {
        @((Get-Content -Encoding UTF8 -Raw -LiteralPath $communityPluginsPath | ConvertFrom-Json)) -contains $pluginId
    }
    else {
        $false
    }
    release = $release.html_url
}
