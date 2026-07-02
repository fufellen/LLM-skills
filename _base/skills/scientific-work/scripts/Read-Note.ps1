param(
    [Parameter(Mandatory = $true, Position = 0)]
    [string]$Path,

    [int]$First = 0,

    [int]$Skip = 0,

    [switch]$Raw,

    [string]$VaultRoot
)

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

if ([System.IO.Path]::IsPathRooted($Path)) {
    $notePath = $Path
}
else {
    $notePath = Join-Path $VaultRoot $Path
}

if (-not (Test-Path -LiteralPath $notePath -PathType Leaf)) {
    throw "Note file not found: $notePath"
}

if ($Raw) {
    Get-Content -Encoding UTF8 -Raw -LiteralPath $notePath
    exit
}

$content = Get-Content -Encoding UTF8 -LiteralPath $notePath

if ($Skip -gt 0) {
    $content = $content | Select-Object -Skip $Skip
}

if ($First -gt 0) {
    $content = $content | Select-Object -First $First
}

$content
