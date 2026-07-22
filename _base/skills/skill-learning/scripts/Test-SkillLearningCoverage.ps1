[CmdletBinding()]
param(
    [string]$RepositoryRoot
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

if ([string]::IsNullOrWhiteSpace($RepositoryRoot)) {
    $RepositoryRoot = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '..\..\..\..')).Path
}

$resolvedRoot = (Resolve-Path -LiteralPath $RepositoryRoot).Path
$baseRoots = Get-ChildItem -LiteralPath $resolvedRoot -Directory -Recurse -Force |
    Where-Object {
        $_.Name -eq 'skills' -and
        $_.Parent.Name -eq '_base' -and
        $_.FullName -notmatch '[\\/]\.git[\\/]'
    } |
    Sort-Object -Property FullName -Unique

if (-not $baseRoots) {
    throw "No _base/skills directories found under $resolvedRoot"
}

$skillFiles = foreach ($baseRoot in $baseRoots) {
    Get-ChildItem -LiteralPath $baseRoot.FullName -Directory | ForEach-Object {
        $skillPath = Join-Path $_.FullName 'SKILL.md'
        if (Test-Path -LiteralPath $skillPath) {
            Get-Item -LiteralPath $skillPath
        }
    }
}

$results = foreach ($skillFile in ($skillFiles | Sort-Object -Property FullName -Unique)) {
    $content = Get-Content -Raw -Encoding UTF8 -LiteralPath $skillFile.FullName
    $hasSharedPolicy = $content -match '(?i)skill-learning'
    $hasLearningHeading = $content -match '(?im)^##\s+(Self-Improvement(?:\s+And\s+Publishing)?|Self-Learning(?:\s+Rule)?|Learning)\s*$'
    $hasDurableLanguage = $content -match '(?i)durable|reusable|lesson|nuance'
    $covered = $hasSharedPolicy -or ($hasLearningHeading -and $hasDurableLanguage)
    $relativePath = $skillFile.FullName.Substring($resolvedRoot.Length).TrimStart([char[]]'\/')

    [pscustomobject]@{
        Status = if ($covered) { 'PASS' } else { 'FAIL' }
        Skill = $skillFile.Directory.Name
        Policy = if ($hasSharedPolicy) { 'skill-learning' } elseif ($hasLearningHeading) { 'local section' } else { 'missing' }
        Path = $relativePath
    }
}

$results | Format-Table -AutoSize

$failed = @($results | Where-Object { $_.Status -eq 'FAIL' })
Write-Output "Checked $($results.Count) canonical shared-base skills; failures: $($failed.Count)."

if ($failed.Count -gt 0) {
    exit 1
}
