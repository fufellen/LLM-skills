<#
.SYNOPSIS
Remove invisible characters that arrive by copy-paste from rendered web pages.

.DESCRIPTION
Zero-width spaces, word joiners, soft hyphens and directional marks survive
copy-paste, show the reader nothing, and break things silently: a U+200B inside
$...$ makes the formula stop matching any search, and one after a #### marker
breaks the [[#Heading]] anchors this vault relies on. The usual source is
copying a MathJax-rendered formula from a web page.

Deleted outright, because they carry no meaning in these notes:
  U+200B zero width space, U+200E/U+200F directional marks, U+2060 word joiner,
  U+00AD soft hyphen, and U+FEFF when it is NOT the leading byte-order mark.
Replaced by a newline: U+2028 line separator, U+2029 paragraph separator.

Deliberately NOT touched by default:
  U+200C/U+200D joiners, which are meaningful in emoji sequences and in some
  scripts, and the visible exotic spaces U+00A0, U+2009, U+202F, U+2007, since
  a non-breaking space can be intentional in Russian typography. Pass
  -NormalizeSpaces to fold those exotic spaces into ordinary spaces when the
  file is known to be paste garbage.

A leading byte-order mark, the file's CRLF/LF style and its trailing newline are
preserved, exactly as in Repair-NoteTables.ps1. Detection matches Test-Note.ps1,
so a repaired note passes `Test-Note.ps1 -Strict`.

Runs as a dry run by default and reports what it would change. Pass -Apply to
write files.

.EXAMPLE
.\Repair-NoteInvisibles.ps1 "PhD\Scientific_study\note.md"

.EXAMPLE
Get-ChildItem -Recurse -Filter *.md | .\Repair-NoteInvisibles.ps1 -Apply
#>
param(
    [Parameter(Mandatory = $true, Position = 0, ValueFromPipeline = $true, ValueFromPipelineByPropertyName = $true)]
    [Alias('FullName')]
    [string[]]$Path,

    [switch]$Apply,

    [switch]$NormalizeSpaces,

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

    $deleteNames = [ordered]@{
        ([char]0x200B) = 'ZERO WIDTH SPACE'
        ([char]0x200E) = 'LEFT-TO-RIGHT MARK'
        ([char]0x200F) = 'RIGHT-TO-LEFT MARK'
        ([char]0x2060) = 'WORD JOINER'
        ([char]0x00AD) = 'SOFT HYPHEN'
        ([char]0xFEFF) = 'ZERO WIDTH NO-BREAK SPACE'
    }
    $newlineNames = [ordered]@{
        ([char]0x2028) = 'LINE SEPARATOR'
        ([char]0x2029) = 'PARAGRAPH SEPARATOR'
    }
    $spaceNames = [ordered]@{
        ([char]0x00A0) = 'NO-BREAK SPACE'
        ([char]0x2009) = 'THIN SPACE'
        ([char]0x202F) = 'NARROW NO-BREAK SPACE'
        ([char]0x2007) = 'FIGURE SPACE'
    }

    $totalFiles = 0
    $totalFixes = 0
    $grandTally = @{}
    $queue = New-Object System.Collections.Generic.List[string]
}

process {
    # Collect only. The work runs in end{} because a script invoked as
    # `powershell -File script.ps1 -Path x` with stdin on the null device gets
    # an EMPTY pipeline, and PowerShell then skips process{} entirely - the
    # parameter is bound, but nothing happens and the run reports zero finds.
    # Collecting here and working in end{} makes both invocation styles behave
    # the same (found 2026-08-16, cost a debugging round).
    if ($Path) {
        foreach ($p in $Path) { $queue.Add($p) }
    }
}

end {
    if ($queue.Count -eq 0 -and $PSBoundParameters.ContainsKey('Path')) {
        foreach ($p in $Path) { $queue.Add($p) }
    }

    foreach ($p in $queue) {
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

        # A leading U+FEFF is the byte-order mark and is part of the encoding,
        # not a paste artifact. Split it off before scanning so the same code
        # point can be deleted safely everywhere else in the file.
        $hadBom = $false
        if ($text.Length -gt 0 -and $text[0] -eq [char]0xFEFF) {
            $hadBom = $true
            $text = $text.Substring(1)
        }

        $newline = if ($text -match "`r`n") { "`r`n" } else { "`n" }

        $tally = [ordered]@{}
        $sb = New-Object System.Text.StringBuilder
        foreach ($ch in $text.ToCharArray()) {
            if ($deleteNames.Contains($ch)) {
                $tally[$deleteNames[$ch]] = 1 + [int]$tally[$deleteNames[$ch]]
                continue
            }
            if ($newlineNames.Contains($ch)) {
                $tally[$newlineNames[$ch]] = 1 + [int]$tally[$newlineNames[$ch]]
                [void]$sb.Append($newline)
                continue
            }
            if ($NormalizeSpaces -and $spaceNames.Contains($ch)) {
                $tally[$spaceNames[$ch]] = 1 + [int]$tally[$spaceNames[$ch]]
                [void]$sb.Append(' ')
                continue
            }
            [void]$sb.Append($ch)
        }

        $fixes = 0
        foreach ($v in $tally.Values) { $fixes += $v }
        if ($fixes -eq 0) {
            continue
        }

        $totalFiles++
        $totalFixes += $fixes
        foreach ($k in $tally.Keys) { $grandTally[$k] = [int]$grandTally[$k] + $tally[$k] }

        $rel = $full
        if ($full.StartsWith($VaultRoot, [System.StringComparison]::OrdinalIgnoreCase)) {
            $rel = $full.Substring($VaultRoot.Length).TrimStart('\', '/')
        }
        $detail = ($tally.Keys | ForEach-Object { "$_ x$($tally[$_])" }) -join ', '
        $verb = if ($Apply) { "healed" } else { "would heal" }
        Write-Output ("{0,3} {1}  {2}  [{3}]" -f $fixes, $verb, $rel, $detail)

        if (-not $Apply) {
            continue
        }

        $result = $sb.ToString()
        if ($hadBom) { $result = [char]0xFEFF + $result }
        [System.IO.File]::WriteAllText($full, $result, $utf8NoBom)
    }

    Write-Output ""
    if ($grandTally.Count -gt 0) {
        $summary = ($grandTally.Keys | Sort-Object | ForEach-Object { "$_ x$($grandTally[$_])" }) -join ', '
        Write-Output "By kind: $summary"
    }
    $verb = if ($Apply) { "healed" } else { "healable" }
    Write-Output ("{0} characters {1} across {2} files" -f $totalFixes, $verb, $totalFiles)
    if (-not $Apply -and $totalFixes -gt 0) {
        Write-Output "Dry run only. Re-run with -Apply to write the files."
    }
}
