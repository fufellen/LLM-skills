param(
    [Parameter(Mandatory = $true, Position = 0)]
    [Alias("Pattern")]
    [string]$Query,

    [Alias("Path")]
    [string[]]$Roots = @("PhD"),

    [switch]$AllVault,

    [int]$Context = 0,

    [switch]$Literal,

    [switch]$CaseSensitive,

    [switch]$FilesOnly,

    [string[]]$Glob = @("*.md"),

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

$excludedGlobs = @(
    "!**/.git/**",
    "!**/.trash/**",
    "!**/.venv/**",
    "!**/.obsidian/**",
    "!**/_.obsidian/**"
)

if ($AllVault) {
    $Roots = @(".")
}
else {
    $Roots = @(
        foreach ($root in $Roots) {
            foreach ($part in ($root -split ",")) {
                $trimmed = $part.Trim()
                if ($trimmed) {
                    $trimmed
                }
            }
        }
    )
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

$rg = Get-Command rg -ErrorAction SilentlyContinue

if ($rg) {
    $rgArgs = @(
        "--line-number",
        "--color", "never"
    )

    if ($Context -gt 0) {
        $rgArgs += @("--context", "$Context")
    }

    if ($Literal) {
        $rgArgs += "--fixed-strings"
    }

    if (-not $CaseSensitive) {
        $rgArgs += "--smart-case"
    }

    if ($FilesOnly) {
        $rgArgs += "--files-with-matches"
    }

    foreach ($g in $Glob) {
        $rgArgs += @("--glob", $g)
    }

    foreach ($g in $excludedGlobs) {
        $rgArgs += @("--glob", $g)
    }

    $rgArgs += "--"
    $rgArgs += $Query
    $rgArgs += $targetPaths

    & $rg.Source @rgArgs
    exit $LASTEXITCODE
}

Write-Warning "ripgrep (rg) was not found; falling back to Select-String."

$files = foreach ($target in $targetPaths) {
    Get-ChildItem -LiteralPath $target -Recurse -File -Include $Glob -ErrorAction SilentlyContinue |
        Where-Object {
            $_.FullName -notmatch "\\(\.git|\.trash|\.venv|\.obsidian|_\.obsidian)\\"
        }
}

if (-not $files) {
    exit 0
}

# LiteralPath, not Path: vault filenames contain [] () and other wildcard
# characters, and Select-String -Path fails on them with WildcardPatternException.
$selectArgs = @{
    LiteralPath = $files.FullName
    Pattern = $Query
    Encoding = "UTF8"
}

if ($Literal) {
    $selectArgs.SimpleMatch = $true
}

if ($CaseSensitive) {
    $selectArgs.CaseSensitive = $true
}

if ($FilesOnly) {
    Select-String @selectArgs | Select-Object -ExpandProperty Path -Unique
}
else {
    Select-String @selectArgs
}
