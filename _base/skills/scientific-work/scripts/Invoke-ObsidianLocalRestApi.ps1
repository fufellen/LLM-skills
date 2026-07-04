param(
    [ValidateSet("GET", "POST", "PUT", "PATCH", "DELETE")]
    [string]$Method = "GET",

    [string]$Endpoint,

    [string]$VaultPath,

    [string]$Body,

    [string]$InputFile,

    [string]$OutputFile,

    [string]$ContentType = "application/json"
)

$ErrorActionPreference = "Stop"

function Find-VaultRoot {
    $probe = $PSScriptRoot
    while ($probe -and -not (Test-Path -LiteralPath (Join-Path $probe ".obsidian") -PathType Container)) {
        $parent = Split-Path -Parent $probe
        if ($parent -eq $probe) {
            break
        }
        $probe = $parent
    }
    if (-not $probe -or -not (Test-Path -LiteralPath (Join-Path $probe ".obsidian") -PathType Container)) {
        throw "Could not find vault root by walking up from $PSScriptRoot"
    }
    return $probe
}

function ConvertTo-EncodedVaultPath([string]$Path) {
    $normalized = $Path.TrimStart("\", "/") -replace "\\", "/"
    $segments = $normalized -split "/" | Where-Object { $_ -ne "" }
    $encoded = $segments | ForEach-Object { [System.Uri]::EscapeDataString($_) }
    return ($encoded -join "/")
}

if ($Endpoint -and $VaultPath) {
    throw "Use either -Endpoint or -VaultPath, not both."
}

if (-not $Endpoint -and -not $VaultPath) {
    throw "Provide -Endpoint for a raw API path or -VaultPath for a note path under /vault/."
}

if ($Body -and $InputFile) {
    throw "Use either -Body or -InputFile, not both."
}

$vaultRoot = Find-VaultRoot
$configPath = Join-Path $vaultRoot ".codex\secrets\scientific-work\obsidian-local-rest-api.json"
$legacyConfigPath = Join-Path $vaultRoot ".codex\skills\scientific-work\secrets\obsidian-local-rest-api.json"

if (-not (Test-Path -LiteralPath $configPath -PathType Leaf) -and (Test-Path -LiteralPath $legacyConfigPath -PathType Leaf)) {
    $configPath = $legacyConfigPath
}

if (-not (Test-Path -LiteralPath $configPath -PathType Leaf)) {
    throw "Obsidian Local REST API config not found: $configPath"
}

$config = Get-Content -Raw -Encoding UTF8 -LiteralPath $configPath | ConvertFrom-Json
if (-not $config.base_url -or -not $config.api_key) {
    throw "Config must contain base_url and api_key: $configPath"
}

$baseUrl = [string]$config.base_url
$baseUrl = $baseUrl.TrimEnd("/")

if ($VaultPath) {
    $apiPath = "/vault/" + (ConvertTo-EncodedVaultPath $VaultPath)
}
else {
    $apiPath = $Endpoint
    if (-not $apiPath.StartsWith("/")) {
        $apiPath = "/" + $apiPath
    }
}

$url = $baseUrl + $apiPath
$responseFile = [System.IO.Path]::GetTempFileName()

try {
    $curlArgs = @(
        "-k",
        "-sS",
        "-X", $Method,
        "-H", "Authorization: Bearer $($config.api_key)",
        "-H", "Content-Type: $ContentType",
        "-w", "%{http_code}",
        "-o", $responseFile
    )

    if ($InputFile) {
        if (-not (Test-Path -LiteralPath $InputFile -PathType Leaf)) {
            throw "Input file not found: $InputFile"
        }
        $curlArgs += @("--data-binary", "@$InputFile")
    }
    elseif ($PSBoundParameters.ContainsKey("Body")) {
        $curlArgs += @("--data-binary", $Body)
    }

    $curlArgs += $url
    $statusCode = & curl.exe @curlArgs
    if ($LASTEXITCODE -ne 0) {
        throw "curl.exe failed with exit code $LASTEXITCODE"
    }

    $responseText = Get-Content -Raw -Encoding UTF8 -LiteralPath $responseFile
    $statusNumber = [int]$statusCode

    if ($statusNumber -lt 200 -or $statusNumber -ge 300) {
        Write-Error "HTTP $statusNumber from $apiPath`n$responseText"
        exit 1
    }

    if ($OutputFile) {
        Copy-Item -LiteralPath $responseFile -Destination $OutputFile -Force
        Write-Output "HTTP $statusNumber; wrote $OutputFile"
    }
    else {
        $responseText
    }
}
finally {
    if (Test-Path -LiteralPath $responseFile -PathType Leaf) {
        Remove-Item -LiteralPath $responseFile -Force
    }
}
