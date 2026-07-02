param(
    [Parameter(Mandatory = $true, Position = 0)]
    [string]$Term,

    [string[]]$Roots = @("PhD"),

    [switch]$AllVault,

    [int]$Context = 2,

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

if ($AllVault) {
    $Roots = @(".")
}

$targetPaths = foreach ($root in $Roots) {
    if ([System.IO.Path]::IsPathRooted($root)) {
        $candidate = $root
    }
    else {
        $candidate = Join-Path $VaultRoot $root
    }

    if (Test-Path -LiteralPath $candidate) {
        (Resolve-Path -LiteralPath $candidate).Path
    }
    else {
        Write-Warning "Search root not found: $candidate"
    }
}

if (-not $targetPaths) {
    throw "No valid search roots were provided."
}

Write-Output "## Matching note titles"

$titleMatches = foreach ($target in $targetPaths) {
    Get-ChildItem -LiteralPath $target -Recurse -File -Filter "*.md" -ErrorAction SilentlyContinue |
        Where-Object {
            $_.FullName -notmatch "\\(\.git|\.trash|\.venv|\.obsidian|_\.obsidian)\\" -and
            $_.BaseName -like "*$Term*"
        } |
        ForEach-Object {
            $_.FullName.Substring($VaultRoot.Length + 1)
        }
}

if ($titleMatches) {
    $titleMatches | Sort-Object -Unique
}
else {
    Write-Output "(none)"
}

Write-Output ""
Write-Output "## Content matches"

$searchScript = Join-Path $PSScriptRoot "Search-Vault.ps1"
& $searchScript -Query $Term -Roots $Roots -Context $Context -Literal -VaultRoot $VaultRoot
