# Iris Local — Windows installer
$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRoot = Resolve-Path (Join-Path $scriptDir "..")
$modelDir = Join-Path $repoRoot "models"
$modelFile = Join-Path $modelDir "phi-3-mini-4k-instruct-q4.gguf"
$modelUrl = "https://huggingface.co/microsoft/Phi-3-mini-4k-instruct-gguf/resolve/main/Phi-3-mini-4k-instruct-q4.gguf"

function Step([int]$Number, [string]$Message) {
    Write-Host ""
    Write-Host "[$Number/5] $Message" -ForegroundColor Cyan
}

function Stop-Setup([string]$Message) {
    Write-Host "Setup stopped: $Message" -ForegroundColor Red
    exit 1
}

Write-Host "=== Iris Local — Windows Setup ===" -ForegroundColor Cyan
Write-Host "This installs local dependencies and an easy starter model for Sovereign Local Mode."

Step 1 "Checking Python"
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
    Write-Host "Python was not found." -ForegroundColor Yellow
    if (Get-Command winget -ErrorAction SilentlyContinue) {
        Write-Host "Trying the standard Windows install for you..." -ForegroundColor Yellow
        winget install --id Python.Python.3.12 --accept-source-agreements --accept-package-agreements
        Write-Host "Python has been installed. Please open a new PowerShell window and run this script again." -ForegroundColor Yellow
        exit 0
    }
    Stop-Setup "Install Python 3.11+ from https://www.python.org/downloads/windows/ and then run this script again."
}

Write-Host "Using $(& $python --version)"

Step 2 "Checking download support"
if (-not (Get-Command Invoke-WebRequest -ErrorAction SilentlyContinue)) {
    Stop-Setup "PowerShell download support was not available. Please update PowerShell and run the script again."
}

Step 3 "Installing Python packages"
Push-Location $repoRoot
& $python -m pip install --upgrade pip
& $python -m pip install -e ".[local]"
Pop-Location

Step 4 "Checking for a starter model"
if (-not (Test-Path $modelDir)) {
    New-Item -ItemType Directory -Path $modelDir | Out-Null
}
if (Test-Path $modelFile) {
    Write-Host "Model already present: $modelFile"
} else {
    Write-Host "No local model was found."
    Write-Host "Downloading Phi-3 Mini 4K Instruct Q4 (~2.2 GB). This is the Easy Mode starter model..."
    try {
        Invoke-WebRequest -Uri $modelUrl -OutFile $modelFile
    } catch {
        if (Test-Path $modelFile) { Remove-Item $modelFile -Force }
        Stop-Setup "The model download did not complete. Please check your connection or try python setup-wizard.py for guided help."
    }
    Write-Host "Model saved to $modelFile"
}

Step 5 "Finishing up"
Write-Host "Setup complete." -ForegroundColor Green
Write-Host "Next steps:"
Write-Host "  1. Optional guided setup: python setup-wizard.py"
Write-Host "  2. Start Iris Local:      python iris-local.py"
Write-Host "If Windows Defender or another antivirus asks about a local download, review the file path and allow it if appropriate."
