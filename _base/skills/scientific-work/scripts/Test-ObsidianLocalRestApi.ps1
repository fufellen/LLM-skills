param(
    [string]$BaseUrl = "https://127.0.0.1:27124",

    [string]$ApiKey,

    [string]$VaultRoot
)

$ErrorActionPreference = "Stop"
$ProgressPreference = "SilentlyContinue"
$utf8NoBom = [System.Text.UTF8Encoding]::new($false)
[Console]::OutputEncoding = $utf8NoBom
$OutputEncoding = $utf8NoBom

if (-not $VaultRoot) {
    $VaultRoot = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot "..\..\..\..")).Path
}

$configPath = Join-Path $VaultRoot ".codex\skills\scientific-work\secrets\obsidian-local-rest-api.json"

if ((-not $ApiKey) -and (Test-Path -LiteralPath $configPath -PathType Leaf)) {
    $config = Get-Content -Encoding UTF8 -Raw -LiteralPath $configPath | ConvertFrom-Json
    if ($config.base_url) {
        $BaseUrl = [string]$config.base_url
    }
    $candidateKey = [string]$config.api_key
    if ($candidateKey -and $candidateKey -ne "PASTE_OBSIDIAN_LOCAL_REST_API_KEY_HERE") {
        $ApiKey = $candidateKey
    }
}

$uri = [Uri]$BaseUrl
$hostName = $uri.Host
$port = $uri.Port

$tcp = Test-NetConnection -ComputerName $hostName -Port $port -InformationLevel Quiet -WarningAction SilentlyContinue

$result = [ordered]@{
    base_url = $BaseUrl
    tcp_port_open = $tcp
    api_key_source = if ($ApiKey) { $configPath } else { "not configured" }
    authenticated_request = "not attempted"
    mcp_endpoint = "$BaseUrl/mcp/"
}

if ($tcp -and $ApiKey) {
    [System.Net.ServicePointManager]::ServerCertificateValidationCallback = { $true }
    $headers = @{
        Authorization = "Bearer $ApiKey"
    }

    try {
        $response = Invoke-WebRequest -Uri "$BaseUrl/" -Headers $headers -UseBasicParsing
        $result.authenticated_request = "ok: HTTP $($response.StatusCode)"
    }
    catch {
        $curl = Get-Command curl.exe -ErrorAction SilentlyContinue
        if ($curl) {
            $status = & $curl.Source -k -s -o NUL -w "%{http_code}" -H "Authorization: Bearer $ApiKey" "$BaseUrl/"
            if ($LASTEXITCODE -eq 0 -and $status -match "^\d{3}$") {
                $result.authenticated_request = "ok: HTTP $status via curl.exe -k"
            }
            else {
                $result.authenticated_request = "failed: $($_.Exception.Message); curl fallback exit=$LASTEXITCODE status=$status"
            }
        }
        else {
            $result.authenticated_request = "failed: $($_.Exception.Message)"
        }
    }
}

[pscustomobject]$result
