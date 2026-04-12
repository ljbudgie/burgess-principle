"""Tests for scripts/generate-vapid-keys.py."""

from __future__ import annotations

import builtins
import importlib.util
from pathlib import Path
import subprocess
import sys

import pytest


_MODULE_PATH = (
    Path(__file__).resolve().parents[1] / "scripts" / "generate-vapid-keys.py"
)
_SPEC = importlib.util.spec_from_file_location("generate_vapid_keys", _MODULE_PATH)
_MODULE = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(_MODULE)


def test_b64url_strips_padding():
    assert _MODULE._b64url(b"\xfb\xef\xff") == "--__"


def test_main_prints_vapid_environment_values(monkeypatch, capsys):
    public_bytes = b"\x04" + (b"\x01" * 64)
    private_value = 123456789

    class FakePrivateNumbers:
        def __init__(self, value):
            self.private_value = value

    class FakePublicKey:
        def public_bytes(self, encoding, public_format):
            assert encoding is _MODULE.Encoding.X962
            assert public_format is _MODULE.PublicFormat.UncompressedPoint
            return public_bytes

    class FakePrivateKey:
        def private_numbers(self):
            return FakePrivateNumbers(private_value)

        def public_key(self):
            return FakePublicKey()

    monkeypatch.setattr(
        _MODULE.ec,
        "generate_private_key",
        lambda curve: FakePrivateKey(),
    )

    _MODULE.main()

    output = capsys.readouterr().out
    assert "Add these to your .env or Vercel environment variables:" in output
    assert f"VAPID_PUBLIC_KEY={_MODULE._b64url(public_bytes)}" in output
    assert (
        "VAPID_PRIVATE_KEY="
        f"{_MODULE._b64url(private_value.to_bytes(32, byteorder='big'))}"
    ) in output
    assert "VAPID_EMAIL=mailto:your-contact@example.com" in output
    assert "safe to embed in the HTML" in output


def test_script_exits_with_helpful_error_when_cryptography_is_missing(monkeypatch, capsys):
    real_import = builtins.__import__

    def fake_import(name, *args, **kwargs):
        if name.startswith("cryptography.hazmat.primitives"):
            raise ImportError("cryptography unavailable")
        return real_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", fake_import)

    spec = importlib.util.spec_from_file_location("generate_vapid_keys_missing_crypto", _MODULE_PATH)
    module = importlib.util.module_from_spec(spec)

    with pytest.raises(SystemExit, match="1"):
        spec.loader.exec_module(module)

    error = capsys.readouterr().err
    assert "cryptography" in error
    assert "pip install cryptography" in error


def test_script_runs_as_cli_entrypoint():
    result = subprocess.run(
        [sys.executable, str(_MODULE_PATH)],
        check=True,
        capture_output=True,
        text=True,
    )

    assert "VAPID_PUBLIC_KEY=" in result.stdout
    assert "VAPID_PRIVATE_KEY=" in result.stdout
    assert "VAPID_EMAIL=mailto:your-contact@example.com" in result.stdout
