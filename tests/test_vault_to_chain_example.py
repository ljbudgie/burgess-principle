"""Tests for the vault-to-chain example script."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock

ROOT = Path(__file__).resolve().parent.parent
MODULE_PATH = ROOT / "onchain-protocol" / "examples" / "vault_to_chain.py"


def _load_module(name: str):
    spec = importlib.util.spec_from_file_location(name, MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class _FakeVerifyKey:
    def encode(self) -> bytes:
        return bytes.fromhex("22" * 32)


class _FakeSigningKey:
    verify_key = _FakeVerifyKey()

    def encode(self) -> bytes:
        return bytes.fromhex("11" * 32)


class _FakeClaim:
    commitment_hash = "aa" * 32
    signature = "bb" * 64
    target_entity = "Example Borough Council"
    category = "enforcement"
    timestamp = "2026-04-12T20:00:00+00:00"
    nonce = "cc" * 32
    public_key = "22" * 32

    def to_json(self) -> str:
        return '{"commitmentHash":"%s"}' % self.commitment_hash


def test_main_prints_successful_flow(monkeypatch, capsys):
    module = _load_module("vault_to_chain_success")
    fake_claim = _FakeClaim()
    generate_onchain_claim = Mock(return_value=fake_claim)
    verify_onchain_receipt = Mock(
        return_value=SimpleNamespace(valid=True, details="Signature verified.")
    )
    verify_commitment = Mock(return_value=True)

    monkeypatch.setattr(module, "generate_onchain_claim", generate_onchain_claim)
    monkeypatch.setattr(module, "verify_onchain_receipt", verify_onchain_receipt)
    monkeypatch.setattr(module, "verify_commitment", verify_commitment)
    monkeypatch.setattr(module.SigningKey, "generate", lambda: _FakeSigningKey())

    module.main()

    output = capsys.readouterr().out
    assert "=== Burgess Claims Protocol — End-to-End Example ===" in output
    assert "--- Claim Generated ---" in output
    assert "✅ Signature verified." in output
    assert "✅ Commitment matches the disclosed details." in output
    generate_onchain_claim.assert_called_once_with(
        claim_details="My council tax was sent to enforcement without any human review of the specific facts.",
        target_entity="Example Borough Council",
        category="enforcement",
        private_key_hex="11" * 32,
    )
    verify_onchain_receipt.assert_called_once_with(
        commitment_hash=fake_claim.commitment_hash,
        signature=fake_claim.signature,
        public_key_hex=fake_claim.public_key,
    )
    verify_commitment.assert_called_once_with(
        claim_details="My council tax was sent to enforcement without any human review of the specific facts.",
        timestamp=fake_claim.timestamp,
        nonce=fake_claim.nonce,
        public_key_hex=fake_claim.public_key,
        expected_hash=fake_claim.commitment_hash,
    )


def test_main_prints_failure_icons(monkeypatch, capsys):
    module = _load_module("vault_to_chain_failure")

    monkeypatch.setattr(module, "generate_onchain_claim", Mock(return_value=_FakeClaim()))
    monkeypatch.setattr(
        module,
        "verify_onchain_receipt",
        Mock(return_value=SimpleNamespace(valid=False, details="Signature verification failed.")),
    )
    monkeypatch.setattr(module, "verify_commitment", Mock(return_value=False))
    monkeypatch.setattr(module.SigningKey, "generate", lambda: _FakeSigningKey())

    module.main()

    output = capsys.readouterr().out
    assert "❌ Signature verification failed." in output
    assert "❌ Commitment does not match the disclosed details." in output
