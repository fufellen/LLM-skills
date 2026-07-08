param(
    [Parameter(Mandatory = $true, Position = 0)]
    [string]$Path,

    [int]$First = 24,

    [switch]$CheckLinks,

    [switch]$Strict,

    [string]$VaultRoot
)

$utf8NoBom = [System.Text.UTF8Encoding]::new($false)
$strictUtf8 = [System.Text.UTF8Encoding]::new($false, $true)
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

$item = Get-Item -LiteralPath $notePath
$bytes = [System.IO.File]::ReadAllBytes($item.FullName)

try {
    $text = $strictUtf8.GetString($bytes)
}
catch {
    throw "File is not valid UTF-8: $($item.FullName)"
}

if ($text.Length -gt 0 -and $text[0] -eq [char]0xFEFF) {
    $text = $text.Substring(1)
}

$lines = if ($text.Length -eq 0) { @() } else { $text -split "\r\n|\n|\r" }

Write-Output "[ok] UTF-8 decode succeeded"
Write-Output "Path: $($item.FullName)"
Write-Output "Size: $($item.Length) bytes"
Write-Output "Lines: $($lines.Count)"
Write-Output "LastWriteTime: $($item.LastWriteTime)"

$mojibakeRegex = [regex]'[\u00C2\u00D0\u00D1\uFFFD]|\u0420[\u00A0-\u00BF\u0400-\u040F\u0450-\u045F\u2010-\u203F]|\u0421[\u00A0-\u00BF\u0400-\u040F\u0450-\u045F\u2010-\u203F]'
$hits = $mojibakeRegex.Matches($text) |
    Select-Object -First 12 |
    ForEach-Object { $_.Value }

if ($hits) {
    Write-Warning ("Suspicious encoding fragments found: " + (($hits | Sort-Object -Unique) -join ", "))
    if ($Strict) {
        exit 2
    }
}
else {
    Write-Output "[ok] No common mojibake markers found"
}

$openCount = ([regex]::Matches($text, "\[\[")).Count
$closeCount = ([regex]::Matches($text, "\]\]")).Count
$linkMatches = [regex]::Matches($text, "\[\[([^\]]+)\]\]")
Write-Output "Obsidian links: $($linkMatches.Count)"

if ($openCount -ne $closeCount) {
    Write-Warning "Unbalanced Obsidian link brackets: [[=$openCount ]]=$closeCount"
    if ($Strict) {
        exit 3
    }
}
else {
    Write-Output "[ok] Obsidian link brackets are balanced"
}

if ($CheckLinks -and $linkMatches.Count -gt 0) {
    # Index every non-service file in the vault, not only .md, so attachment
    # links and embeds (PDF, PNG, canvas, ...) resolve the same way Obsidian does.
    $allFiles = Get-ChildItem -LiteralPath $VaultRoot -Recurse -File -ErrorAction SilentlyContinue |
        Where-Object {
            $_.FullName -notmatch "\\(\.git|\.trash|\.venv|\.obsidian|_\.obsidian)\\"
        }

    # PowerShell hashtables key case-insensitively, matching Obsidian link
    # resolution on Windows.
    $fullNameSet = @{}   # exact filename incl. extension: "figure.png", "paper.pdf", "Note.md"
    $baseNameSet = @{}   # filename without extension: "Note", "figure"
    foreach ($file in $allFiles) {
        $fullNameSet[$file.Name] = $true
        $baseNameSet[$file.BaseName] = $true
    }

    $missing = New-Object System.Collections.Generic.List[string]
    foreach ($match in $linkMatches) {
        $rawTarget = $match.Groups[1].Value
        $target = ($rawTarget -split "\|", 2)[0]
        $target = ($target -split "#", 2)[0].Trim()
        if (-not $target -or $target.StartsWith("http://") -or $target.StartsWith("https://")) {
            continue
        }

        $hasExt = $target -match "\.[A-Za-z0-9]+$"
        $found = $false

        if ($target -match "[/\\]") {
            # Path-qualified link/embed: try the exact path under the vault root,
            # append .md for an extensionless note path, then fall back to a
            # shortest-path filename match (as Obsidian does).
            $rel = $target -replace "/", "\"
            $found = Test-Path -LiteralPath (Join-Path $VaultRoot $rel) -PathType Leaf
            if (-not $found -and -not $hasExt) {
                $found = Test-Path -LiteralPath (Join-Path $VaultRoot ($rel + ".md")) -PathType Leaf
            }
            if (-not $found) {
                $leaf = Split-Path -Leaf $rel
                if ($leaf -match "\.[A-Za-z0-9]+$") {
                    $found = $fullNameSet.ContainsKey($leaf)
                }
                else {
                    $found = $baseNameSet.ContainsKey($leaf) -or $fullNameSet.ContainsKey($leaf + ".md")
                }
            }
        }
        elseif ($hasExt) {
            # Bare attachment filename (e.g. .pdf, .png): match the full name anywhere.
            $found = $fullNameSet.ContainsKey($target)
        }
        else {
            # Bare note name: resolves to <name>.md (or any file with that base name).
            $found = $baseNameSet.ContainsKey($target) -or $fullNameSet.ContainsKey($target + ".md")
        }

        if (-not $found) {
            $missing.Add($target)
        }
    }

    if ($missing.Count -gt 0) {
        Write-Warning "Missing Obsidian link targets:"
        $missing | Sort-Object -Unique | ForEach-Object { Write-Warning "  $_" }
        if ($Strict) {
            exit 4
        }
    }
    else {
        Write-Output "[ok] Obsidian link targets resolved"
    }
}

if ($First -gt 0) {
    Write-Output ""
    Write-Output "## First $First lines"
    $lines | Select-Object -First $First
}
