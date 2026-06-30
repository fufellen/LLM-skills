param(
    [Parameter(Mandatory=$false)]
    [string[]]$Doi,

    [Parameter(Mandatory=$false)]
    [string]$DoiFile,

    [Parameter(Mandatory=$true)]
    [string]$OutputDir,

    [Parameter(Mandatory=$false)]
    [string]$ManifestPath
)

$ErrorActionPreference = "Stop"
$ProgressPreference = "SilentlyContinue"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

function Get-SafeFileName {
    param([string]$Value)
    $safe = $Value -replace '[\\/:*?"<>|]+', '_'
    $safe = $safe -replace '\s+', ' '
    $safe = $safe.Trim()
    if ($safe.Length -gt 140) {
        $safe = $safe.Substring(0, 140).Trim()
    }
    return $safe
}

function Invoke-JsonGet {
    param([string]$Url)
    $headers = @{
        "User-Agent" = "Codex scientific-work OA downloader"
        "Accept" = "application/json"
    }
    return Invoke-RestMethod -Uri $Url -Headers $headers -Method Get -TimeoutSec 45
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

function Save-PdfCandidate {
    param(
        [string]$Url,
        [string]$Path
    )
    $headers = @{
        "User-Agent" = "Mozilla/5.0"
        "Accept" = "application/pdf,*/*"
    }
    $tmp = "$Path.tmp"
    if (Test-Path -LiteralPath $tmp) {
        Remove-Item -LiteralPath $tmp -Force
    }
    Invoke-WebRequest -Uri $Url -Headers $headers -OutFile $tmp -TimeoutSec 120
    if (Test-PdfFile -Path $tmp) {
        Move-Item -LiteralPath $tmp -Destination $Path -Force
        return $true
    }
    Remove-Item -LiteralPath $tmp -Force -ErrorAction SilentlyContinue
    return $false
}

$doiList = @()
if ($Doi) {
    $doiList += $Doi
}
if ($DoiFile) {
    $doiList += Get-Content -LiteralPath $DoiFile -Encoding UTF8 |
        Where-Object { $_ -and $_.Trim() -and -not $_.Trim().StartsWith("#") }
}
$doiList = $doiList | ForEach-Object { $_.Trim() } | Where-Object { $_ } | Select-Object -Unique
if (-not $doiList -or $doiList.Count -eq 0) {
    throw "No DOI values provided. Use -Doi or -DoiFile."
}

New-Item -ItemType Directory -Force -Path $OutputDir | Out-Null
if (-not $ManifestPath) {
    $ManifestPath = Join-Path $OutputDir "download_manifest.json"
}

$results = @()
foreach ($doiValue in $doiList) {
    $encodedDoi = [System.Uri]::EscapeDataString($doiValue)
    $record = [ordered]@{
        doi = $doiValue
        title = $null
        status = "metadata lookup started"
        downloaded = $false
        file = $null
        pdf_url = $null
        landing_page_url = $null
        checked_urls = @()
        error = $null
    }

    try {
        $candidates = New-Object System.Collections.Generic.List[string]

        try {
            $openAlex = Invoke-JsonGet -Url "https://api.openalex.org/works/https://doi.org/$encodedDoi"
            $record.title = $openAlex.title
            foreach ($loc in @($openAlex.best_oa_location, $openAlex.primary_location)) {
                if ($null -ne $loc) {
                    if ($loc.pdf_url) {
                        [void]$candidates.Add([string]$loc.pdf_url)
                    }
                    if (-not $record.landing_page_url -and $loc.landing_page_url) {
                        $record.landing_page_url = [string]$loc.landing_page_url
                    }
                }
            }
        }
        catch {
            $record.error = "OpenAlex: $($_.Exception.Message)"
        }

        try {
            $crossref = Invoke-JsonGet -Url "https://api.crossref.org/works/$encodedDoi"
            if (-not $record.title -and $crossref.message.title) {
                $record.title = [string]$crossref.message.title[0]
            }
            foreach ($link in @($crossref.message.link)) {
                if ($link.URL -and ([string]$link.'content-type').ToLowerInvariant().Contains("pdf")) {
                    [void]$candidates.Add([string]$link.URL)
                }
            }
        }
        catch {
            if ($record.error) {
                $record.error += "; Crossref: $($_.Exception.Message)"
            }
            else {
                $record.error = "Crossref: $($_.Exception.Message)"
            }
        }

        $uniqueCandidates = $candidates | Where-Object { $_ } | Select-Object -Unique
        if (-not $uniqueCandidates -or $uniqueCandidates.Count -eq 0) {
            $record.status = "no direct open PDF URL found"
        }
        else {
            $record.status = "direct PDF candidates found"
            foreach ($url in $uniqueCandidates) {
                $record.checked_urls += $url
                if (-not $record.pdf_url) {
                    $record.pdf_url = $url
                }
                $safeDoi = Get-SafeFileName -Value ($doiValue -replace '/', '_')
                $titleForFile = $record.title
                if (-not $titleForFile) {
                    $titleForFile = "untitled"
                }
                $safeTitle = Get-SafeFileName -Value $titleForFile
                $fileName = "$safeDoi - $safeTitle.pdf"
                $outPath = Join-Path $OutputDir $fileName
                try {
                    if (Save-PdfCandidate -Url $url -Path $outPath) {
                        $record.status = "downloaded from open PDF URL"
                        $record.downloaded = $true
                        $record.file = $outPath
                        break
                    }
                    else {
                        $record.status = "candidate URL did not return a valid PDF"
                    }
                }
                catch {
                    $record.status = "download failed for candidate URL"
                    $record.error = "$($record.error); $url -> $($_.Exception.Message)"
                }
            }
            if (-not $record.downloaded -and $record.status -eq "direct PDF candidates found") {
                $record.status = "all direct PDF candidates failed"
            }
        }
    }
    catch {
        $record.status = "failed"
        $record.error = $_.Exception.Message
    }

    $results += [pscustomobject]$record
    $prefix = if ($record.downloaded) { "[downloaded]" } else { "[missing]" }
    Write-Host "$prefix $doiValue - $($record.status)"
}

$results | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $ManifestPath -Encoding UTF8
Write-Host "Manifest: $ManifestPath"
