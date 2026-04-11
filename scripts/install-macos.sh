#!/usr/bin/env bash
# Iris Local — macOS installer
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd -- "$SCRIPT_DIR/.." && pwd)"
MODEL_DIR="$REPO_ROOT/models"
MODEL_FILE="$MODEL_DIR/phi-3-mini-4k-instruct-q4.gguf"
MODEL_URL="https://huggingface.co/microsoft/Phi-3-mini-4k-instruct-gguf/resolve/main/Phi-3-mini-4k-instruct-q4.gguf"

step() {
    echo ""
    echo "[$1/5] $2"
}

die() {
    echo "Setup stopped: $1" >&2
    exit 1
}

echo "=== Iris Local — macOS Setup ==="
echo "This keeps Iris local to your Mac and downloads an easy starter model if needed."

step 1 "Checking Python"
if ! command -v python3 >/dev/null 2>&1; then
    echo "Python was not found."
    if ! command -v brew >/dev/null 2>&1; then
        die "Install Homebrew from https://brew.sh or install Python 3.11+ manually, then run this script again."
    fi
    echo "Installing Python with Homebrew..."
    brew install python
fi
PYTHON="python3"
echo "Using $($PYTHON --version)"

step 2 "Checking download support"
if ! command -v curl >/dev/null 2>&1; then
    if command -v brew >/dev/null 2>&1; then
        echo "curl was not found. Installing it with Homebrew..."
        brew install curl
    else
        die "curl was not found. Please install curl and run this script again."
    fi
fi

step 3 "Installing Python packages"
cd "$REPO_ROOT"
$PYTHON -m pip install --upgrade pip
$PYTHON -m pip install -e ".[local]"

step 4 "Checking for a starter model"
mkdir -p "$MODEL_DIR"
if [ -f "$MODEL_FILE" ]; then
    echo "Model already present: $MODEL_FILE"
else
    echo "No local model was found."
    echo "Downloading Phi-3 Mini 4K Instruct Q4 (~2.2 GB). This is the Easy Mode starter model."
    if ! curl --fail --location --progress-bar --output "$MODEL_FILE" "$MODEL_URL"; then
        rm -f "$MODEL_FILE"
        die "The model download did not complete. Please check your connection or try setup-wizard.py for guided help."
    fi
    echo "Model saved to $MODEL_FILE"
fi

step 5 "Finishing up"
echo "Setup complete."
echo "Next steps:"
echo "  1. Optional guided setup: python3 setup-wizard.py"
echo "  2. Start Iris Local:      python3 iris-local.py"
echo "If macOS blocks a download or Python build step, open System Settings and review any security prompts, then re-run."
