#!/usr/bin/env bash
# Iris Local — Linux installer
# Installs Python dependencies and downloads a small default model.
#
# Usage:
#   bash scripts/install-linux.sh
#
set -euo pipefail

echo "=== Iris Local — Linux Setup ==="

# ── Python check ──────────────────────────────────────────────────────────
if ! command -v python3 &>/dev/null; then
    echo "Python 3 not found. Installing via apt..."
    sudo apt update && sudo apt install -y python3 python3-pip python3-venv
fi

PYTHON="python3"
echo "Using $($PYTHON --version)"

# ── pip dependencies ──────────────────────────────────────────────────────
echo ""
echo "Installing Python dependencies..."
$PYTHON -m pip install --upgrade pip
$PYTHON -m pip install llama-cpp-python fastapi uvicorn

# ── Default model download ────────────────────────────────────────────────
MODEL_DIR="models"
MODEL_FILE="$MODEL_DIR/model.gguf"

if [ ! -f "$MODEL_FILE" ]; then
    echo ""
    echo "No model found at $MODEL_FILE."
    echo "Downloading Phi-3 Mini Q4 (~2.2 GB) — a small model that runs on most laptops..."
    mkdir -p "$MODEL_DIR"
    curl -L -o "$MODEL_FILE" \
        "https://huggingface.co/microsoft/Phi-3-mini-4k-instruct-gguf/resolve/main/Phi-3-mini-4k-instruct-q4.gguf"
    echo "Model downloaded to $MODEL_FILE"
else
    echo "Model already present at $MODEL_FILE — skipping download."
fi

echo ""
echo "=== Setup complete ==="
echo "Start Iris Local with:  python3 iris-local.py"
