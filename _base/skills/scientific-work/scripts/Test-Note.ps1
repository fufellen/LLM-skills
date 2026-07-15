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

# A single Cyrillic \u0420/\u0421 followed by punctuation from the suspicious ranges is
# legitimate Russian (\u00AB\u041D\u043E\u043A\u0434\u0430\u0443\u043D-\u0420\u00BB, \u00AB...\u0413\u041E\u0421\u0422 \u0420\u00BB, word ending in \u0421 before \u00BB).
# Genuine UTF-8-as-cp1251 mojibake is a dense run of such pairs, so require at
# least two consecutive pairs before flagging.
$mojibakeRegex = [regex]'[\u00C2\u00D0\u00D1\uFFFD]|(?:[\u0420\u0421][\u00A0-\u00BF\u0400-\u040F\u0450-\u045F\u2010-\u203F]){2}'
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

# Scientific and technical notes in this vault use the filename as the visible
# title and reserve #### for topical sections. Ignore fenced code examples so a
# Markdown snippet does not trigger a false positive.
$headingViolations = New-Object System.Collections.Generic.List[string]
$duplicateTitleViolations = New-Object System.Collections.Generic.List[string]
$insideFence = $false
for ($i = 0; $i -lt $lines.Count; $i++) {
    $line = $lines[$i]
    if ($line -match '^\s*(```|~~~)') {
        $insideFence = -not $insideFence
        continue
    }
    if (-not $insideFence -and $line -match '^(#{1,3})[ \t]+(.+)$') {
        $headingViolations.Add("line $($i + 1): $line")
    }
    if (-not $insideFence -and $line -match '^#{1,6}[ \t]+(.+?)[ \t]*$') {
        $headingText = $Matches[1] -replace '[ \t]+#+[ \t]*$', ''
        if ([string]::Equals($headingText.Trim(), $item.BaseName, [System.StringComparison]::OrdinalIgnoreCase)) {
            $duplicateTitleViolations.Add("line $($i + 1): $line")
        }
    }
}

$styleViolationFound = $false
if ($headingViolations.Count -gt 0) {
    Write-Warning "Heading levels # through ### are not allowed; use #### and do not repeat the filename as a heading:"
    $headingViolations | ForEach-Object { Write-Warning "  $_" }
    $styleViolationFound = $true
}
else {
    Write-Output "[ok] No heading levels # through ### found"
}

if ($duplicateTitleViolations.Count -gt 0) {
    Write-Warning "The note filename is already displayed by Obsidian and must not be repeated as a heading at any level:"
    $duplicateTitleViolations | ForEach-Object { Write-Warning "  $_" }
    $styleViolationFound = $true
}
else {
    Write-Output "[ok] Note filename is not repeated as a heading"
}

$formulaNotationViolations = New-Object System.Collections.Generic.List[string]
$whereLabel = -join @([char]0x0413, [char]0x0434, [char]0x0435, [char]0x003A)
$insideFence = $false
$insideDisplayMath = $false
$displayMathStartLine = 0
for ($i = 0; $i -lt $lines.Count; $i++) {
    $line = $lines[$i]
    $trimmed = $line.Trim()
    if ($line -match '^\s*(```|~~~)') {
        $insideFence = -not $insideFence
        continue
    }
    if ($insideFence) {
        continue
    }

    $isSingleLineDisplay = $trimmed.Length -gt 4 -and $trimmed.StartsWith('$$') -and $trimmed.EndsWith('$$')
    if ($isSingleLineDisplay) {
        $nextLine = if ($i + 1 -lt $lines.Count) { $lines[$i + 1] } else { '' }
        if ($nextLine -ne $whereLabel) {
            $formulaNotationViolations.Add("line $($i + 1): display formula is not followed immediately by the required notation label")
        }
        continue
    }

    if ($trimmed -eq '$$') {
        if (-not $insideDisplayMath) {
            $insideDisplayMath = $true
            $displayMathStartLine = $i + 1
        }
        else {
            $insideDisplayMath = $false
            $nextLine = if ($i + 1 -lt $lines.Count) { $lines[$i + 1] } else { '' }
            if ($nextLine -ne $whereLabel) {
                $formulaNotationViolations.Add("line $($i + 1): display formula is not followed immediately by the required notation label")
            }
        }
    }
}

if ($insideDisplayMath) {
    $formulaNotationViolations.Add(('line {0}: display formula has no closing $$ delimiter' -f $displayMathStartLine))
}

if ($formulaNotationViolations.Count -gt 0) {
    Write-Warning "Every display formula must be followed immediately by a locally complete notation block:"
    $formulaNotationViolations | ForEach-Object { Write-Warning "  $_" }
    $styleViolationFound = $true
}
else {
    Write-Output "[ok] Every display formula is followed immediately by the required notation block"
}

if ($Strict -and $styleViolationFound) {
    exit 5
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
