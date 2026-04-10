# Iris Local — Windows installer
# Installs Python dependencies and downloads a small default model.
#
# Usage:
#   powershell -ExecutionPolicy Bypass -File scripts\install-windows.ps1
#
$ErrorActionPreference = "Stop"

Write-Host "=== Iris Local — Windows Setup ===" -ForegroundColor Cyan

# ── Python check ──────────────────────────────────────────────────────────
$python = $null
foreach ($cmd in @("python", "python3", "py")) {
    try {
        $ver = & $cmd --version 2>&1
        if ($ver -match "Python 3") {
            $python = $cmd
            break
        }
    } catch {}
}

if (-not $python) {
    Write-Host "Python 3 not found. Installing via winget..." -ForegroundColor Yellow
    winget install --id Python.Python.3.12 --accept-source-agreements --accept-package-agreements
    $python = "python"
    Write-Host "Please restart your terminal after Python installs, then re-run this script." -ForegroundColor Yellow
    exit 0
}

Write-Host "Using $(& $python --version)"

# ── pip dependencies ──────────────────────────────────────────────────────
Write-Host ""
Write-Host "Installing Python dependencies..."
& $python -m pip install --upgrade pip
& $python -m pip install llama-cpp-python fastapi uvicorn

# ── Default model download ────────────────────────────────────────────────
$modelDir = "models"
$modelFile = Join-Path $modelDir "model.gguf"

if (-not (Test-Path $modelFile)) {
    Write-Host ""
    Write-Host "No model found at $modelFile."
    Write-Host "Downloading Phi-3 Mini Q4 (~2.2 GB) — a small model that runs on most laptops..."
    if (-not (Test-Path $modelDir)) { New-Item -ItemType Directory -Path $modelDir | Out-Null }
    $url = "https://huggingface.co/microsoft/Phi-3-mini-4k-instruct-gguf/resolve/main/Phi-3-mini-4k-instruct-q4.gguf"
    Invoke-WebRequest -Uri $url -OutFile $modelFile
    Write-Host "Model downloaded to $modelFile"
} else {
    Write-Host "Model already present at $modelFile — skipping download."
}

Write-Host ""
Write-Host "=== Setup complete ===" -ForegroundColor Green
Write-Host "Start Iris Local with:  python iris-local.py"
