# Crops an arbitrary rectangle from a normalized poster photo and upscales it for OCR reading.
# Usage: powershell -NoProfile -ExecutionPolicy Bypass -File _crop.ps1 -Path "<abs jpg>" -X 100 -Y 200 -W 300 -H 200 -Zoom 6 -Out "<abs png>"
param(
  [Parameter(Mandatory=$true)][string]$Path,
  [Parameter(Mandatory=$true)][int]$X,
  [Parameter(Mandatory=$true)][int]$Y,
  [Parameter(Mandatory=$true)][int]$W,
  [Parameter(Mandatory=$true)][int]$H,
  [double]$Zoom = 6.0,
  [Parameter(Mandatory=$true)][string]$Out,
  [switch]$Sharpen
)
Add-Type -AssemblyName System.Drawing
$img = [System.Drawing.Image]::FromFile($Path)
$X = [Math]::Max(0, [Math]::Min($X, $img.Width - 1))
$Y = [Math]::Max(0, [Math]::Min($Y, $img.Height - 1))
$W = [Math]::Min($W, $img.Width - $X)
$H = [Math]::Min($H, $img.Height - $Y)
$dw = [int]($W * $Zoom); $dh = [int]($H * $Zoom)
$bmp = New-Object System.Drawing.Bitmap($dw, $dh)
$g = [System.Drawing.Graphics]::FromImage($bmp)
$g.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
$g.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::HighQuality
$g.PixelOffsetMode = [System.Drawing.Drawing2D.PixelOffsetMode]::HighQuality
$rectDst = New-Object System.Drawing.Rectangle(0, 0, $dw, $dh)
$rectSrc = New-Object System.Drawing.Rectangle($X, $Y, $W, $H)
$g.DrawImage($img, $rectDst, $rectSrc, [System.Drawing.GraphicsUnit]::Pixel)
$g.Dispose()

if ($Sharpen) {
  # simple contrast/greyscale boost to help reading faded print
  $ia = New-Object System.Drawing.Imaging.ImageAttributes
  $cm = New-Object System.Drawing.Imaging.ColorMatrix
  $c = 1.7; $t = (1.0 - $c) / 2.0
  $cm.Matrix00 = $c; $cm.Matrix11 = $c; $cm.Matrix22 = $c
  $cm.Matrix40 = $t; $cm.Matrix41 = $t; $cm.Matrix42 = $t
  $ia.SetColorMatrix($cm)
  $bmp2 = New-Object System.Drawing.Bitmap($dw, $dh)
  $g2 = [System.Drawing.Graphics]::FromImage($bmp2)
  $g2.DrawImage($bmp, $rectDst, 0, 0, $dw, $dh, [System.Drawing.GraphicsUnit]::Pixel, $ia)
  $g2.Dispose(); $bmp.Dispose(); $bmp = $bmp2
}

$bmp.Save($Out, [System.Drawing.Imaging.ImageFormat]::Png)
"OK: {0}  src=({1},{2},{3}x{4}) -> {5}x{6}" -f $Out, $X, $Y, $W, $H, $dw, $dh
$bmp.Dispose(); $img.Dispose()
