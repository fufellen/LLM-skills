param(
    [Parameter(Mandatory=$false)]
    [string]$Doi,

    [Parameter(Mandatory=$false)]
    [string]$Title,

    [Parameter(Mandatory=$false)]
    [string]$Year,

    [Parameter(Mandatory=$false)]
    [string]$Root = (Get-Location).Path,

    [Parameter(Mandatory=$false)]
    [int]$MinScore = 30,

    [switch]$AsJson
)

$ErrorActionPreference = "Stop"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

if (-not $Doi -and -not $Title -and -not $Year) {
    throw "Provide at least one of -Doi, -Title, or -Year."
}

function Normalize-Text {
    param([string]$Value)
    if (-not $Value) {
        return ""
    }
    $s = $Value.ToLowerInvariant()
    $s = $s -replace '<[^>]+>', ' '
    $s = $s -replace '&[a-z0-9#]+;', ' '
    $s = $s -replace '[^a-z0-9]+', ' '
    $s = $s -replace '\s+', ' '
    return $s.Trim()
}

function Get-TitleTokens {
    param([string]$Value)
    if (-not $Value) {
        return @()
    }
    $stop = @{
        "with"=$true; "from"=$true; "into"=$true; "using"=$true; "based"=$true
        "and"=$true; "the"=$true; "for"=$true; "their"=$true; "phase"=$false
    }
    $tokens = @(Normalize-Text $Value).Split(" ", [System.StringSplitOptions]::RemoveEmptyEntries)
    $out = New-Object System.Collections.Generic.List[string]
    foreach ($token in $tokens) {
        if ($token.Length -lt 4) {
            continue
        }
        if ($stop.ContainsKey($token) -and $stop[$token]) {
            continue
        }
        if (-not $out.Contains($token)) {
            [void]$out.Add($token)
        }
        if ($out.Count -ge 14) {
            break
        }
    }
    return @($out)
}

function Test-PdfFile {
    param([string]$Path)
    if (-not (Test-Path -LiteralPath $Path)) {
        return $false
    }
    $fs = [System.IO.File]::OpenRead((Resolve-Path -LiteralPath $Path))
    try {
        if ($fs.Length -lt 5) {
            return $false
        }
        $buf = New-Object byte[] 4
        [void]$fs.Read($buf, 0, 4)
        $sig = [System.Text.Encoding]::ASCII.GetString($buf)
        return $sig -eq "%PDF"
    }
    finally {
        $fs.Dispose()
    }
}

$resolvedRoot = (Resolve-Path -LiteralPath $Root).Path
$doiNorm = Normalize-Text ($Doi -replace '^https?://(dx\.)?doi\.org/', '')
$doiSafeNorm = Normalize-Text (($Doi -replace '^https?://(dx\.)?doi\.org/', '') -replace '/', '_')
$doiSuffixNorm = ""
if ($Doi -and $Doi.Contains("/")) {
    $doiSuffixNorm = Normalize-Text (($Doi -split '/', 2)[1])
}
$titleTokens = Get-TitleTokens $Title

$skipParts = @(
    [IO.Path]::DirectorySeparatorChar + ".git" + [IO.Path]::DirectorySeparatorChar,
    [IO.Path]::DirectorySeparatorChar + ".obsidian" + [IO.Path]::DirectorySeparatorChar,
    [IO.Path]::DirectorySeparatorChar + ".codex" + [IO.Path]::DirectorySeparatorChar,
    [IO.Path]::DirectorySeparatorChar + ".trash" + [IO.Path]::DirectorySeparatorChar,
    [IO.Path]::DirectorySeparatorChar + "node_modules" + [IO.Path]::DirectorySeparatorChar
)

$files = Get-ChildItem -LiteralPath $resolvedRoot -Recurse -File -Filter "*.pdf" -ErrorAction SilentlyContinue |
    Where-Object {
        $path = $_.FullName
        foreach ($part in $skipParts) {
            if ($path.Contains($part)) {
                return $false
            }
        }
        return $true
    }

$results = New-Object System.Collections.Generic.List[object]
foreach ($file in $files) {
    $norm = Normalize-Text $file.FullName
    $nameNorm = Normalize-Text $file.Name
    $parentNorm = Normalize-Text (Split-Path -Leaf $file.DirectoryName)
    $score = 0
    $reasons = New-Object System.Collections.Generic.List[string]
    $yearMatched = $false

    if ($doiSafeNorm -and $norm.Contains($doiSafeNorm)) {
        $score += 100
        [void]$reasons.Add("doi-safe")
    }
    elseif ($doiNorm -and $norm.Contains($doiNorm)) {
        $score += 90
        [void]$reasons.Add("doi")
    }

    if ($doiSuffixNorm -and $norm.Contains($doiSuffixNorm)) {
        $score += 70
        [void]$reasons.Add("doi-suffix")
    }

    if ($Year -and (($nameNorm.Contains((Normalize-Text $Year))) -or ($parentNorm.Contains((Normalize-Text $Year))))) {
        $score += 12
        $yearMatched = $true
        [void]$reasons.Add("year")
    }

    $matchedTokens = 0
    foreach ($token in $titleTokens) {
        if ($norm.Contains($token)) {
            $matchedTokens += 1
            $score += 8
        }
    }
    if ($matchedTokens -gt 0) {
        [void]$reasons.Add("title-tokens:$matchedTokens")
    }
    if ($titleTokens.Count -ge 4 -and $matchedTokens -ge [Math]::Min(4, $titleTokens.Count)) {
        $score += 20
        [void]$reasons.Add("title-cluster")
    }

    if ($score -ge $MinScore) {
        $confidence = "possible"
        if (($reasons -contains "doi-safe") -or ($reasons -contains "doi") -or ($reasons -contains "doi-suffix")) {
            $confidence = "strong-doi"
        }
        elseif ($yearMatched -and $matchedTokens -ge 5) {
            $confidence = "strong-title-year"
        }
        elseif ($matchedTokens -ge 4) {
            $confidence = "possible-title-only"
        }

        [void]$results.Add([pscustomobject]@{
            Score = $score
            Confidence = $confidence
            IsPdf = (Test-PdfFile -Path $file.FullName)
            Reason = ($reasons -join ",")
            SizeBytes = $file.Length
            LastWriteTime = $file.LastWriteTime
            Path = $file.FullName
        })
    }
}

$sorted = @($results | Sort-Object -Property Score, LastWriteTime -Descending)
if ($AsJson) {
    $sorted | ConvertTo-Json -Depth 4
}
else {
    $sorted | Format-Table -AutoSize Score, Confidence, IsPdf, Reason, SizeBytes, LastWriteTime, Path
}
