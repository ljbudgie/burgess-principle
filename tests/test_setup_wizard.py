"""Tests for setup-wizard.py."""

import importlib.util
import json
import os
from pathlib import Path

import pytest

MODULE_PATH = os.path.join(os.path.dirname(__file__), "..", "setup-wizard.py")
spec = importlib.util.spec_from_file_location("setup_wizard", MODULE_PATH)
setup_wizard_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(setup_wizard_module)


load_config = setup_wizard_module.load_config
save_config = setup_wizard_module.save_config
prompt_yes_no = setup_wizard_module.prompt_yes_no
prompt_choice = setup_wizard_module.prompt_choice
detect_ram_gb = setup_wizard_module.detect_ram_gb
detect_gpu_hint = setup_wizard_module.detect_gpu_hint
choose_context_size = setup_wizard_module.choose_context_size
download_model = setup_wizard_module.download_model
python_hint = setup_wizard_module.python_hint
main = setup_wizard_module.main
DEFAULT_CONFIG = setup_wizard_module.DEFAULT_CONFIG


def test_load_config_returns_defaults_when_file_missing(tmp_path, monkeypatch):
    monkeypatch.setattr(setup_wizard_module, "CONFIG_PATH", tmp_path / "iris-config.json")

    assert load_config() == DEFAULT_CONFIG


def test_load_config_merges_existing_values(tmp_path, monkeypatch):
    config_path = tmp_path / "iris-config.json"
    config_path.write_text(json.dumps({"port": 9000, "easy_mode": False}), encoding="utf-8")
    monkeypatch.setattr(setup_wizard_module, "CONFIG_PATH", config_path)

    config = load_config()

    assert config["port"] == 9000
    assert config["easy_mode"] is False
    assert config["model_path"] == DEFAULT_CONFIG["model_path"]


def test_load_config_falls_back_to_defaults_for_invalid_json(tmp_path, monkeypatch):
    config_path = tmp_path / "iris-config.json"
    config_path.write_text("{not valid json", encoding="utf-8")
    monkeypatch.setattr(setup_wizard_module, "CONFIG_PATH", config_path)

    assert load_config() == DEFAULT_CONFIG


def test_save_config_writes_indented_json_with_trailing_newline(tmp_path, monkeypatch):
    config_path = tmp_path / "iris-config.json"
    monkeypatch.setattr(setup_wizard_module, "CONFIG_PATH", config_path)

    save_config({"port": 8123})

    assert config_path.read_text(encoding="utf-8") == '{\n    "port": 8123\n}\n'


def test_prompt_yes_no_retries_until_valid_answer(monkeypatch, capsys):
    answers = iter(["maybe", "YeS"])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))

    assert prompt_yes_no("Continue?", default=False) is True
    assert "Please answer yes or no." in capsys.readouterr().out


def test_prompt_choice_retries_until_choice_is_valid(monkeypatch, capsys):
    choices = [
        {"label": "One", "size": "~1 GB", "best_for": "fast"},
        {"label": "Two", "size": "~2 GB", "best_for": "quality"},
    ]
    answers = iter(["0", "2"])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))

    selected = prompt_choice("Pick one", choices)

    assert selected == choices[1]
    assert "Please enter one of the numbers shown above." in capsys.readouterr().out


def test_detect_ram_gb_reads_linux_meminfo(monkeypatch):
    monkeypatch.setattr(setup_wizard_module.sys, "platform", "linux")
    monkeypatch.setattr(
        Path,
        "read_text",
        lambda self, encoding="utf-8": "MemTotal:       16777216 kB\n",
    )

    assert detect_ram_gb() == 16.0


def test_detect_ram_gb_returns_none_when_detection_fails(monkeypatch):
    def raising_run(*args, **kwargs):
        raise RuntimeError("sysctl unavailable")

    monkeypatch.setattr(setup_wizard_module.sys, "platform", "darwin")
    monkeypatch.setattr(setup_wizard_module.subprocess, "run", raising_run)

    assert detect_ram_gb() is None


@pytest.mark.parametrize(
    ("responses", "expected"),
    [
        ([{"stdout": "NVIDIA-SMI 555"}], "NVIDIA GPU detected"),
        ([RuntimeError(), {"stdout": "Apple Metal"}], "Apple graphics detected"),
        (
            [RuntimeError(), RuntimeError(), {"stdout": "00:02.0 VGA compatible controller"}],
            "PCI graphics devices listed",
        ),
        ([RuntimeError(), RuntimeError(), RuntimeError()], "No obvious GPU acceleration hint detected"),
    ],
)
def test_detect_gpu_hint_reports_detected_hardware(monkeypatch, responses, expected):
    queue = list(responses)

    def fake_run(*args, **kwargs):
        result = queue.pop(0)
        if isinstance(result, Exception):
            raise result
        return type("Completed", (), result)()

    monkeypatch.setattr(setup_wizard_module.subprocess, "run", fake_run)

    assert detect_gpu_hint() == expected


@pytest.mark.parametrize(
    ("ram_gb", "expected"),
    [(None, 2048), (4.0, 1024), (8.0, 2048), (32.0, 4096)],
)
def test_choose_context_size_uses_memory_thresholds(ram_gb, expected):
    assert choose_context_size(ram_gb) == expected


def test_download_model_reports_progress_and_writes_file(tmp_path, monkeypatch, capsys):
    destination = tmp_path / "models" / "demo.gguf"

    def fake_urlretrieve(url, path, reporthook):
        assert url == "https://example.com/demo.gguf"
        reporthook(1, 50, 100)
        reporthook(2, 50, 100)
        Path(path).write_text("model-bytes", encoding="utf-8")

    monkeypatch.setattr(setup_wizard_module.urllib.request, "urlretrieve", fake_urlretrieve)

    download_model(
        {"label": "Demo Model", "url": "https://example.com/demo.gguf"},
        destination,
    )

    assert destination.read_text(encoding="utf-8") == "model-bytes"
    output = capsys.readouterr().out
    assert "Downloading Demo Model" in output
    assert "Progress: 100%" in output


def test_download_model_wraps_network_errors(tmp_path, monkeypatch):
    def fake_urlretrieve(*args, **kwargs):
        raise OSError("offline")

    monkeypatch.setattr(setup_wizard_module.urllib.request, "urlretrieve", fake_urlretrieve)

    with pytest.raises(RuntimeError, match="download the GGUF file manually"):
        download_model(
            {"label": "Demo Model", "url": "https://example.com/demo.gguf"},
            tmp_path / "models" / "demo.gguf",
        )


def test_python_hint_prefers_python3_when_available(monkeypatch):
    def fake_which(name):
        return {"python3": "/usr/bin/python3", "python": "/usr/bin/python"}.get(name)

    monkeypatch.setattr(setup_wizard_module.shutil, "which", fake_which)
    monkeypatch.setattr(setup_wizard_module.platform, "python_version", lambda: "3.12.3")
    monkeypatch.setattr(setup_wizard_module.sys, "executable", "/fallback/python")

    assert python_hint() == "/usr/bin/python3 (Python 3.12.3)"


def test_main_saves_config_and_skips_download_when_model_exists(tmp_path, monkeypatch, capsys):
    config_path = tmp_path / "iris-config.json"
    config_path.write_text(
        json.dumps({"mirror_greeting_style": "warm", "mirror_reflection_scope": "full"}),
        encoding="utf-8",
    )
    monkeypatch.setattr(setup_wizard_module, "ROOT", tmp_path)
    monkeypatch.setattr(setup_wizard_module, "CONFIG_PATH", config_path)
    monkeypatch.setattr(setup_wizard_module, "MODEL_CATALOG", [dict(setup_wizard_module.MODEL_CATALOG[0])])
    monkeypatch.setattr(setup_wizard_module, "python_hint", lambda: "/usr/bin/python3 (Python 3.12.3)")
    monkeypatch.setattr(setup_wizard_module, "detect_ram_gb", lambda: 32.0)
    monkeypatch.setattr(setup_wizard_module, "detect_gpu_hint", lambda: "NVIDIA GPU detected")
    monkeypatch.setattr(setup_wizard_module, "prompt_yes_no", lambda *args, **kwargs: True)
    monkeypatch.setattr(
        setup_wizard_module,
        "prompt_choice",
        lambda *args, **kwargs: setup_wizard_module.MODEL_CATALOG[0],
    )
    model_path = tmp_path / "models" / setup_wizard_module.MODEL_CATALOG[0]["filename"]
    model_path.parent.mkdir(parents=True, exist_ok=True)
    model_path.write_text("present", encoding="utf-8")

    assert main() == 0

    saved = json.loads(config_path.read_text(encoding="utf-8"))
    assert saved["model_path"] == f"models/{setup_wizard_module.MODEL_CATALOG[0]['filename']}"
    assert saved["context_size"] == 4096
    assert saved["gpu_acceleration"] is True
    assert saved["mirror_greeting_style"] == "warm"
    assert saved["mirror_reflection_scope"] == "full"
    output = capsys.readouterr().out
    assert "Model already present" in output


def test_main_downloads_model_when_requested(tmp_path, monkeypatch):
    monkeypatch.setattr(setup_wizard_module, "ROOT", tmp_path)
    monkeypatch.setattr(setup_wizard_module, "CONFIG_PATH", tmp_path / "iris-config.json")
    monkeypatch.setattr(setup_wizard_module, "MODEL_CATALOG", [dict(setup_wizard_module.MODEL_CATALOG[0])])
    monkeypatch.setattr(setup_wizard_module, "python_hint", lambda: "python3")
    monkeypatch.setattr(setup_wizard_module, "detect_ram_gb", lambda: 8.0)
    monkeypatch.setattr(
        setup_wizard_module,
        "detect_gpu_hint",
        lambda: "No obvious GPU acceleration hint detected",
    )
    answers = iter([True, False, True])
    monkeypatch.setattr(setup_wizard_module, "prompt_yes_no", lambda *args, **kwargs: next(answers))
    monkeypatch.setattr(
        setup_wizard_module,
        "prompt_choice",
        lambda *args, **kwargs: setup_wizard_module.MODEL_CATALOG[0],
    )
    calls = []
    monkeypatch.setattr(
        setup_wizard_module,
        "download_model",
        lambda model, destination: calls.append((model["id"], destination)),
    )

    assert main() == 0
    assert calls == [
        ("phi3-mini", tmp_path / "models" / setup_wizard_module.MODEL_CATALOG[0]["filename"])
    ]


def test_main_prints_manual_download_instructions_when_easy_mode_is_disabled(tmp_path, monkeypatch, capsys):
    chosen_model = dict(setup_wizard_module.MODEL_CATALOG[1])
    monkeypatch.setattr(setup_wizard_module, "ROOT", tmp_path)
    monkeypatch.setattr(setup_wizard_module, "CONFIG_PATH", tmp_path / "iris-config.json")
    monkeypatch.setattr(setup_wizard_module, "MODEL_CATALOG", [chosen_model])
    monkeypatch.setattr(setup_wizard_module, "python_hint", lambda: "python3")
    monkeypatch.setattr(setup_wizard_module, "detect_ram_gb", lambda: None)
    monkeypatch.setattr(
        setup_wizard_module,
        "detect_gpu_hint",
        lambda: "No obvious GPU acceleration hint detected",
    )
    answers = iter([False, False])
    monkeypatch.setattr(setup_wizard_module, "prompt_yes_no", lambda *args, **kwargs: next(answers))
    monkeypatch.setattr(setup_wizard_module, "prompt_choice", lambda *args, **kwargs: chosen_model)

    assert main() == 0

    output = capsys.readouterr().out
    assert "No model downloaded yet." in output
    assert str(tmp_path / "models" / chosen_model["filename"]) in output
