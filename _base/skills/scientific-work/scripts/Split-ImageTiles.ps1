param(
  [Parameter(Mandatory=$true)][string]$Path,
  [int]$Cols = 3,
  [int]$Rows = 3,
  [double]$Overlap = 0.12,
  [double]$Zoom = 3.0,
  [string]$OutDir
)
Add-Type -AssemblyName System.Drawing
$img = [System.Drawing.Image]::FromFile($Path)
$base = [System.IO.Path]::GetFileNameWithoutExtension($Path)
if (-not $OutDir) { $OutDir = Join-Path ([System.IO.Path]::GetDirectoryName($Path)) ("_tiles\" + $base) }
New-Item -ItemType Directory -Force -Path $OutDir | Out-Null

$tw = [int]($img.Width / $Cols)
$th = [int]($img.Height / $Rows)
$ox = [int]($tw * $Overlap)
$oy = [int]($th * $Overlap)

for ($r = 0; $r -lt $Rows; $r++) {
  for ($c = 0; $c -lt $Cols; $c++) {
    $x = [Math]::Max(0, $c * $tw - $ox)
    $y = [Math]::Max(0, $r * $th - $oy)
    $w = [Math]::Min($img.Width - $x, $tw + 2 * $ox)
    $h = [Math]::Min($img.Height - $y, $th + 2 * $oy)
    $dw = [int]($w * $Zoom); $dh = [int]($h * $Zoom)
    $bmp = New-Object System.Drawing.Bitmap($dw, $dh)
    $g = [System.Drawing.Graphics]::FromImage($bmp)
    $g.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
    $g.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::HighQuality
    $g.PixelOffsetMode = [System.Drawing.Drawing2D.PixelOffsetMode]::HighQuality
    $rectDst = New-Object System.Drawing.Rectangle(0, 0, $dw, $dh)
    $rectSrc = New-Object System.Drawing.Rectangle($x, $y, $w, $h)
    $g.DrawImage($img, $rectDst, $rectSrc, [System.Drawing.GraphicsUnit]::Pixel)
    $g.Dispose()
    $name = "{0}_r{1}c{2}.png" -f $base, ($r + 1), ($c + 1)
    $bmp.Save((Join-Path $OutDir $name), [System.Drawing.Imaging.ImageFormat]::Png)
    $bmp.Dispose()
    "{0}  src=({1},{2},{3}x{4}) dst={5}x{6}" -f $name, $x, $y, $w, $h, $dw, $dh
  }
}
$img.Dispose()
