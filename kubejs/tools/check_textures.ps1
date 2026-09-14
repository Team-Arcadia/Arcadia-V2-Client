# Author: vyrriox
# Run from any working directory with Windows PowerShell.
$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Drawing
$kubeRoot = Split-Path $PSScriptRoot -Parent
$assets = Join-Path $kubeRoot 'assets'
$textureRoot = Join-Path $assets 'arcadia/textures'
$failures = [System.Collections.Generic.List[string]]::new()
$items = @(Get-ChildItem (Join-Path $textureRoot 'item') -Filter '*.png')
foreach ($file in $items) {
    $bitmap = [System.Drawing.Bitmap]::new($file.FullName)
    try {
        $isNewSprite = $bitmap.Width -eq 32 -and $bitmap.Height -eq 32
        if (!$isNewSprite) { $failures.Add("$($file.Name): expected 32x32 item texture") }
        $opaque = 0
        $soft = 0
        $border = 0
        $scanWidth = [Math]::Min(32, $bitmap.Width)
        $scanHeight = [Math]::Min(32, $bitmap.Height)
        for ($y=0; $y -lt $scanHeight; $y++) {
            for ($x=0; $x -lt $scanWidth; $x++) {
                $alpha = $bitmap.GetPixel($x,$y).A
                if ($alpha -gt 0) { $opaque++ }
                if ($alpha -gt 0 -and $alpha -lt 255) { $soft++ }
                if (($x -eq 0 -or $y -eq 0 -or $x -eq 31 -or $y -eq 31) -and $alpha -gt 0) { $border++ }
            }
        }
        if ($isNewSprite) {
            if ($opaque -lt 24 -or $opaque -eq 1024) { $failures.Add("$($file.Name): invalid silhouette") }
            if ($soft -gt 0) { $failures.Add("$($file.Name): semitransparent edge pixels") }
            if ($border -gt 0) { $failures.Add("$($file.Name): missing transparent margin") }
        }
    } finally { $bitmap.Dispose() }
}
$references = 0
Get-ChildItem (Join-Path $kubeRoot 'startup_scripts') -Recurse -Filter '*.js' | ForEach-Object {
    $source = Get-Content -LiteralPath $_.FullName -Raw
    foreach ($match in [regex]::Matches($source, "\.texture\('arcadia:([^']+)'\)")) {
        $references++
        $path = Join-Path $textureRoot ($match.Groups[1].Value + '.png')
        if (!(Test-Path -LiteralPath $path)) { $failures.Add("Missing texture: $($match.Groups[1].Value)") }
    }
}
$discs = @($items | Where-Object Name -Like 'music_disc_*.png')
foreach ($disc in $discs) {
    $hash = (Get-FileHash -LiteralPath $disc.FullName -Algorithm SHA256).Hash
    foreach ($directory in @('arcadia/textures/block/music_discs','amendments/textures/block/music_discs/arcadia')) {
        $copy = Join-Path (Join-Path $assets $directory) $disc.Name
        if (!(Test-Path -LiteralPath $copy) -or (Get-FileHash -LiteralPath $copy -Algorithm SHA256).Hash -ne $hash) {
            $failures.Add("Disc renderer copy differs: $directory/$($disc.Name)")
        }
    }
}
foreach ($name in @('atm','magnet_jammer')) {
    $bitmap = [System.Drawing.Bitmap]::new((Join-Path $textureRoot "block/$name.png"))
    try {
        if ($bitmap.Width -ne 32 -or $bitmap.Height -ne 32) { $failures.Add("$name block: expected 32x32 texture") }
        for ($y=0; $y -lt $bitmap.Height; $y++) {
            for ($x=0; $x -lt $bitmap.Width; $x++) {
                if ($bitmap.GetPixel($x,$y).A -ne 255) { $failures.Add("$name block: nonopaque pixel at $x,$y") }
            }
        }
    } finally { $bitmap.Dispose() }
}
foreach ($file in Get-ChildItem (Join-Path $textureRoot 'models/armor') -Filter '*.png') {
    $bitmap = [System.Drawing.Bitmap]::new($file.FullName)
    try {
        if ($bitmap.Width -ne 64 -or $bitmap.Height -ne 32) { $failures.Add("$($file.Name): armor UV dimensions changed") }
    } finally { $bitmap.Dispose() }
}
if ($failures.Count) {
    $failures | ForEach-Object { Write-Output "FAIL: $_" }
    exit 1
}
Write-Output "PASS: $($items.Count) item sprites, $references direct registry references, $($discs.Count * 2) disc copies, 2 block faces and armor UV dimensions."
Write-Output 'Visual review and a Minecraft resource reload are separate checks.'
