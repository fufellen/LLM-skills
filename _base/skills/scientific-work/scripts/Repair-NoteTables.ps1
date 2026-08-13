<#
.SYNOPSIS
Insert the blank line a Markdown table needs in front of its header row.

.DESCRIPTION
A GFM table cannot interrupt a paragraph. A table glued to a lead-in line
(typically one ending with ":") is absorbed into that paragraph and Obsidian
renders raw "|" text, while the Markdown source still looks correct. This is
the single most common defect in notes produced by docx-to-markdown and
pdf-textbook-to-markdown conversions.

The repair is purely structural: one blank line is inserted before the header
row. No cell, heading, or prose text is modified. Detection matches
Test-Note.ps1, including its fenced-code-block handling, so a repaired note
passes `Test-Note.ps1 -Strict`.

Runs as a dry run by default and reports what it would change. Pass -Apply to
write files.

.EXAMPLE
.\Repair-NoteTables.ps1 "Работа\Лидар\note.md"

.EXAMPLE
Get-ChildItem -Recurse -Filter *.md | .\Repair-NoteTables.ps1 -Apply
#>
param(
    [Parameter(Mandatory = $true, Position = 0, ValueFromPipeline = $true, ValueFromPipelineByPropertyName = $true)]
    [Alias('FullName')]
    [string[]]$Path,

    [switch]$Apply,

    [string]$VaultRoot
)

begin {
    $utf8NoBom = [System.Text.UTF8Encoding]::new($false)
    $strictUtf8 = [System.Text.UTF8Encoding]::new($false, $true)
    [Console]::OutputEncoding = $utf8NoBom
    $OutputEncoding = $utf8NoBom

    if (-not $VaultRoot) {
        $probe = $PSScriptRoot
        while ($probe -and -not (Test-Path -LiteralPath (Join-Path $probe ".obsidian") -PathType Container)) {
            $probe = Split-Path -Parent $probe
        }
        $VaultRoot = if ($probe) { $probe } else { (Get-Location).Path }
    }

    $delimiterRegex = [regex]'^\s*\|?\s*:?-+:?\s*(?:\|\s*:?-+:?\s*)*\|?\s*$'
    $totalFiles = 0
    $totalFixes = 0
}

process {
    foreach ($p in $Path) {
        $full = if ([System.IO.Path]::IsPathRooted($p)) { $p } else { Join-Path $VaultRoot $p }
        if (-not (Test-Path -LiteralPath $full -PathType Leaf)) {
            Write-Warning "Not found: $full"
            continue
        }

        $bytes = [System.IO.File]::ReadAllBytes($full)
        try {
            $text = $strictUtf8.GetString($bytes)
        }
        catch {
            Write-Warning "Not valid UTF-8, skipped: $full"
            continue
        }

        $hadBom = $false
        if ($text.Length -gt 0 -and $text[0] -eq [char]0xFEFF) {
            $hadBom = $true
            $text = $text.Substring(1)
        }

        # Preserve the file's dominant newline style and its trailing newline.
        $newline = if ($text -match "`r`n") { "`r`n" } else { "`n" }
        $endsWithNewline = $text.EndsWith("`n")
        $lines = @($text -split "\r\n|\n|\r")
        if ($endsWithNewline -and $lines.Count -gt 0 -and $lines[-1] -eq '') {
            $lines = $lines[0..($lines.Count - 2)]
        }

        $insertBefore = New-Object System.Collections.Generic.List[int]
        $insideFence = $false
        for ($i = 0; $i -lt $lines.Count; $i++) {
            $line = $lines[$i]
            if ($line -match '^\s*(```|~~~)') {
                $insideFence = -not $insideFence
                continue
            }
            if ($insideFence -or $i -eq 0) {
                continue
            }
            if ($line -notmatch '^\s*\|') {
                continue
            }

            $nextLine = if ($i + 1 -lt $lines.Count) { $lines[$i + 1] } else { '' }
            if ($nextLine -notmatch '-' -or -not $delimiterRegex.IsMatch($nextLine)) {
                continue
            }

            $prevLine = $lines[$i - 1]
            if ($prevLine.Trim() -eq '') { continue }
            if ($prevLine -match '^#{1,6}[ \t]+') { continue }
            if ($prevLine -match '^\s*(```|~~~)') { continue }
            if ($prevLine.Trim() -eq '$$') { continue }
            if ($prevLine -match '^\s*\|') { continue }

            $insertBefore.Add($i)
        }

        if ($insertBefore.Count -eq 0) {
            continue
        }

        $totalFiles++
        $totalFixes += $insertBefore.Count
        $rel = $full
        if ($full.StartsWith($VaultRoot, [System.StringComparison]::OrdinalIgnoreCase)) {
            $rel = $full.Substring($VaultRoot.Length).TrimStart('\', '/')
        }
        $verb = if ($Apply) { "fixed" } else { "would fix" }
        Write-Output ("{0,3} {1}  {2}" -f $insertBefore.Count, $verb, $rel)

        if (-not $Apply) {
            continue
        }

        $out = New-Object System.Collections.Generic.List[string]
        $insertSet = @{}
        foreach ($idx in $insertBefore) { $insertSet[$idx] = $true }
        for ($i = 0; $i -lt $lines.Count; $i++) {
            if ($insertSet.ContainsKey($i)) { $out.Add('') }
            $out.Add($lines[$i])
        }

        $result = ($out -join $newline)
        if ($endsWithNewline) { $result += $newline }
        if ($hadBom) { $result = [char]0xFEFF + $result }
        [System.IO.File]::WriteAllText($full, $result, $utf8NoBom)
    }
}

end {
    Write-Output ""
    $verb = if ($Apply) { "repaired" } else { "repairable" }
    Write-Output ("{0} tables {1} across {2} files" -f $totalFixes, $verb, $totalFiles)
    if (-not $Apply -and $totalFixes -gt 0) {
        Write-Output "Dry run only. Re-run with -Apply to write the files."
    }
}
