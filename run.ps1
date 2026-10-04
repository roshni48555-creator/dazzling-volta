$OutputEncoding = [System.Text.Encoding]::UTF8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$env:PYTHONIOENCODING = "utf-8"
$env:PYTHONUTF8 = "1"

# Always run from the game folder
if ($PSScriptRoot) {
    Set-Location $PSScriptRoot
}

$uvPath = "$HOME\.local\bin\uv.exe"

if (Get-Command uv -ErrorAction SilentlyContinue) {
    uv run python -X utf8 tarot.py
} elseif (Test-Path $uvPath) {
    & $uvPath run python -X utf8 tarot.py
} elseif (Get-Command python -ErrorAction SilentlyContinue) {
    python -X utf8 tarot.py
} else {
    Write-Host "[ERROR] Python or uv could not be located." -ForegroundColor Red
}
