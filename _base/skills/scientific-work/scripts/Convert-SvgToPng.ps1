# Renders an SVG to PNG with headless Chrome, for visual QA of the reconstructed posters.
# Usage: powershell -NoProfile -ExecutionPolicy Bypass -File _render-svg.ps1 -Svg "<abs path>.svg" [-Width 1600] [-Height 1130]
param(
  [Parameter(Mandatory=$true)][string]$Svg,
  [int]$Width = 1600,
  [int]$Height = 1130,
  [string]$Out
)
$chrome = "C:\Program Files\Google\Chrome\Application\chrome.exe"
if (-not (Test-Path $chrome)) { $chrome = "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" }
if (-not (Test-Path $Svg)) { throw "SVG not found: $Svg" }
if (-not $Out) { $Out = [System.IO.Path]::ChangeExtension($Svg, ".png") }

$tmp = Join-Path $env:TEMP ("svgshot_" + [System.IO.Path]::GetRandomFileName())
New-Item -ItemType Directory -Force -Path $tmp | Out-Null

# file:// URL with percent-encoded path (vault paths contain spaces and Cyrillic)
$uri = ([System.Uri]$Svg).AbsoluteUri

& $chrome --headless=new --disable-gpu --no-sandbox --hide-scrollbars `
  --force-device-scale-factor=1 --default-background-color=FFFFFFFF `
  --user-data-dir="$tmp" --window-size="$Width,$Height" `
  --screenshot="$Out" $uri | Out-Null

Remove-Item -Recurse -Force $tmp -ErrorAction SilentlyContinue
if (Test-Path $Out) {
  $fi = Get-Item $Out
  "OK: {0} ({1} bytes)" -f $fi.FullName, $fi.Length
} else {
  throw "Render failed, no output at $Out"
}
