"""Tests for scripts/generate-vapid-keys.py."""

from __future__ import annotations

import importlib.util
from pathlib import Path


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
