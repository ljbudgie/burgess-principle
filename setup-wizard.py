#!/usr/bin/env python3
"""Guided first-run setup for Iris Sovereign Local Mode."""

from __future__ import annotations

import json
import os
import platform
import shutil
import subprocess
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CONFIG_PATH = ROOT / "iris-config.json"
MODELS_DIR = ROOT / "models"

MODEL_CATALOG = [
    {
        "id": "phi3-mini",
        "label": "Phi-3 Mini 4K Instruct Q4",
        "size": "~2.2 GB",
        "best_for": "Easy Mode on most laptops",
        "filename": "phi-3-mini-4k-instruct-q4.gguf",
        "url": "https://huggingface.co/microsoft/Phi-3-mini-4k-instruct-gguf/resolve/main/Phi-3-mini-4k-instruct-q4.gguf",
    },
    {
        "id": "gemma-2b",
        "label": "Gemma 2 2B Instruct Q4",
        "size": "~1.7 GB",
        "best_for": "Lower-memory systems",
        "filename": "gemma-2-2b-it-q4_k_m.gguf",
        "url": "https://huggingface.co/bartowski/gemma-2-2b-it-GGUF/resolve/main/gemma-2-2b-it-Q4_K_M.gguf",
    },
    {
        "id": "mistral-7b",
        "label": "Mistral 7B Instruct Q4",
        "size": "~4.1 GB",
        "best_for": "Higher quality if you have more RAM",
        "filename": "mistral-7b-instruct-v0.3-q4_k_m.gguf",
        "url": "https://huggingface.co/bartowski/Mistral-7B-Instruct-v0.3-GGUF/resolve/main/Mistral-7B-Instruct-v0.3-Q4_K_M.gguf",
    },
]

DEFAULT_CONFIG = {
    "model_path": "models/phi-3-mini-4k-instruct-q4.gguf",
    "context_size": 2048,
    "port": 8000,
    "gpu_acceleration": False,
    "easy_mode": True,
    "easy_mode_model": {
        "name": "Phi-3 Mini 4K Instruct Q4",
        "filename": "phi-3-mini-4k-instruct-q4.gguf",
        "url": MODEL_CATALOG[0]["url"],
    },
    "mirror_greeting_style": "neutral_professional",
    "mirror_custom_greeting": "",
    "mirror_reflection_scope": "vault_only",
}


def load_config() -> dict:
    if not CONFIG_PATH.exists():
        return dict(DEFAULT_CONFIG)
    try:
        config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return dict(DEFAULT_CONFIG)
    merged = dict(DEFAULT_CONFIG)
    merged.update(config)
    return merged


def save_config(config: dict) -> None:
    CONFIG_PATH.write_text(json.dumps(config, indent=4) + "\n", encoding="utf-8")


def print_step(number: int, message: str) -> None:
    print(f"\n[{number}/5] {message}")


def prompt_yes_no(message: str, *, default: bool = True) -> bool:
    suffix = "Y/n" if default else "y/N"
    while True:
        answer = input(f"{message} [{suffix}] ").strip().lower()
        if not answer:
            return default
        if answer in {"y", "yes"}:
            return True
        if answer in {"n", "no"}:
            return False
        print("Please answer yes or no.")


def prompt_choice(message: str, choices: list[dict]) -> dict:
    print(message)
    for idx, choice in enumerate(choices, start=1):
        print(
            f"  {idx}. {choice['label']} ({choice['size']}) — {choice['best_for']}"
        )
    while True:
        answer = input("Choose a number: ").strip()
        if answer.isdigit() and 1 <= int(answer) <= len(choices):
            return choices[int(answer) - 1]
        print("Please enter one of the numbers shown above.")


def detect_ram_gb() -> float | None:
    try:
        if sys.platform.startswith("linux"):
            for line in Path("/proc/meminfo").read_text(encoding="utf-8").splitlines():
                if line.startswith("MemTotal:"):
                    return round(int(line.split()[1]) / 1024 / 1024, 1)
        if sys.platform == "darwin":
            result = subprocess.run(
                ["sysctl", "-n", "hw.memsize"],
                check=True,
                capture_output=True,
                text=True,
            )
            return round(int(result.stdout.strip()) / 1024 / 1024 / 1024, 1)
        if os.name == "nt":
            import ctypes

            class MemoryStatus(ctypes.Structure):
                _fields_ = [
                    ("length", ctypes.c_ulong),
                    ("memory_load", ctypes.c_ulong),
                    ("total_phys", ctypes.c_ulonglong),
                    ("avail_phys", ctypes.c_ulonglong),
                    ("total_page_file", ctypes.c_ulonglong),
                    ("avail_page_file", ctypes.c_ulonglong),
                    ("total_virtual", ctypes.c_ulonglong),
                    ("avail_virtual", ctypes.c_ulonglong),
                    ("avail_extended_virtual", ctypes.c_ulonglong),
                ]

            status = MemoryStatus()
            status.length = ctypes.sizeof(status)
            ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(status))
            return round(status.total_phys / 1024 / 1024 / 1024, 1)
    except Exception:
        return None
    return None


def detect_gpu_hint() -> str:
    checks = [
        (["nvidia-smi"], "NVIDIA GPU tools detected"),
        (["system_profiler", "SPDisplaysDataType"], "Apple graphics information available"),
        (["lspci"], "PCI graphics devices listed"),
    ]
    for command, label in checks:
        try:
            result = subprocess.run(
                command,
                check=True,
                capture_output=True,
                text=True,
            )
        except Exception:
            continue
        output = result.stdout.lower()
        if "nvidia" in output:
            return "NVIDIA GPU detected"
        if "apple" in output or "metal" in output:
            return "Apple graphics detected"
        if "vga" in output or "3d controller" in output:
            return label
    return "No obvious GPU acceleration hint detected"


def choose_context_size(ram_gb: float | None) -> int:
    if ram_gb is None:
        return 2048
    if ram_gb < 8:
        return 1024
    if ram_gb < 16:
        return 2048
    return 4096


def download_model(model: dict, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    print(f"Downloading {model['label']} to {destination} ...")

    def report(block_count: int, block_size: int, total_size: int) -> None:
        if total_size <= 0:
            return
        downloaded = min(block_count * block_size, total_size)
        percent = int(downloaded * 100 / total_size)
        print(f"\rProgress: {percent:3d}%", end="", flush=True)

    try:
        urllib.request.urlretrieve(model["url"], destination, reporthook=report)
    except Exception as exc:  # pragma: no cover - network dependent
        print("\nThe model download did not complete.")
        raise RuntimeError(
            f"Please try again later or download the GGUF file manually: {exc}"
        ) from exc
    print("\rProgress: 100%")


def python_hint() -> str:
    executable = shutil.which("python3") or shutil.which("python") or sys.executable
    version = platform.python_version()
    return f"{executable} (Python {version})"


def main() -> int:
    print("Iris Sovereign Local Mode — Setup Wizard")
    print("This wizard keeps everything local and writes a simple first-run config for you.")

    print_step(1, "Checking your system")
    print(f"Python: {python_hint()}")
    ram_gb = detect_ram_gb()
    print(f"Estimated memory: {ram_gb} GB" if ram_gb is not None else "Estimated memory: not detected")
    print(f"Graphics hint: {detect_gpu_hint()}")

    print_step(2, "Choosing a starter model")
    easy_mode = prompt_yes_no(
        "Would you like Easy Mode to auto-download a lightweight starter model if one is missing?",
        default=True,
    )
    model = prompt_choice(
        "Recommended local models:",
        MODEL_CATALOG,
    )

    print_step(3, "Choosing local performance defaults")
    suggested_context = choose_context_size(ram_gb)
    use_gpu = prompt_yes_no(
        "Should Iris try GPU acceleration when your llama.cpp build supports it?",
        default=False,
    )
    print(f"Suggested context size: {suggested_context} tokens")

    print_step(4, "Saving your local config")
    config = load_config()
    config.update(
        {
            "model_path": f"models/{model['filename']}",
            "context_size": suggested_context,
            "gpu_acceleration": use_gpu,
            "easy_mode": easy_mode,
            "easy_mode_model": {
                "name": model["label"],
                "filename": model["filename"],
                "url": model["url"],
            },
            "mirror_greeting_style": config.get("mirror_greeting_style", "neutral_professional"),
            "mirror_custom_greeting": config.get("mirror_custom_greeting", ""),
            "mirror_reflection_scope": config.get("mirror_reflection_scope", "vault_only"),
        }
    )
    save_config(config)
    print(f"Saved {CONFIG_PATH}")

    print_step(5, "Checking your model file")
    model_path = ROOT / config["model_path"]
    if model_path.exists():
        print(f"Model already present: {model_path}")
    elif easy_mode and prompt_yes_no(
        f"Download {model['label']} now? This is about {model['size']}.",
        default=True,
    ):
        download_model(model, model_path)
    else:
        print("No model downloaded yet.")
        print(f"When you are ready, place a GGUF model at: {model_path}")

    print("\nNext steps")
    print("1. Install Python dependencies if you have not already:")
    print('   python -m pip install -e ".[local]"')
    print("2. Start Iris locally:")
    print("   python iris-local.py")
    print("3. If you prefer the hosted path first, start with the PWA and move to local when ready.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
