"""Tests for the sovereign Iris claim builder."""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

from nacl.signing import SigningKey

from iris import claim_builder
from iris.claim_builder import auto_generate_claim

_ONCHAIN_CLAIMS_PATH = (
    Path(__file__).resolve().parents[1]
    / "onchain-protocol"
    / "sdk"
    / "onchain_claims.py"
)
_spec = importlib.util.spec_from_file_location("test_onchain_claims", _ONCHAIN_CLAIMS_PATH)
_onchain_claims = importlib.util.module_from_spec(_spec)
sys.modules[_spec.name] = _onchain_claims
_spec.loader.exec_module(_onchain_claims)
verify_onchain_receipt = _onchain_claims.verify_onchain_receipt


def _build_profile(tmp_path: Path) -> dict[str, str]:
    signing_key = SigningKey.generate()
    return {
        "full_name": "Alex Example",
        "email": "alex@example.com",
        "phone": "07123 456789",
        "institution_name": "Example Exchange",
        "team_name": "Compliance Team",
        "reference": "EX-12345",
        "wallet_address": "0x1234567890abcdef1234567890abcdef12345678",
        "transaction_hash": "0xabc123",
        "private_key_hex": signing_key.encode().hex(),
        "vault_passphrase": "correct horse battery staple",
        "vault_path": str(tmp_path / "vault"),
    }


class TestAutoGenerateClaim:
    def test_crypto_exchange_flow_generates_signed_vault_record(self, tmp_path):
        profile = _build_profile(tmp_path)

        result = auto_generate_claim(
            "A crypto exchange froze my account and blocked withdrawals.",
            profile,
        )

        assert result["scenario"]["template"] == (
            "CRYPTO_EXCHANGE_ACCOUNT_RESTRICTION_WITH_BURGESS.md"
        )
        assert "Alex Example" in result["letter"]
        assert "Example Exchange" in result["letter"]
        assert "0xabc123" in result["letter"]
        assert result["commitment_hash"] in result["onchain_notice"]
        assert result["unresolved_placeholders"] == []
        assert [action["label"] for action in result["ui_actions"]] == [
            "Save",
            "Generate Commitment",
            "Copy Letter",
            "On-Chain Notice",
        ]

        verification = verify_onchain_receipt(
            result["commitment_hash"],
            result["signature"],
            result["public_key"],
        )
        assert verification.valid is True

        vault_path = Path(result["vault_record"]["path"])
        assert vault_path.exists()
        raw_record = json.loads(vault_path.read_text(encoding="utf-8"))
        assert raw_record["commitment_hash"] == result["commitment_hash"]
        assert result["letter"] not in raw_record["encrypted_payload"]

        decrypted_payload = claim_builder._decrypt_vault_payload(
            raw_record["encrypted_payload"],
            profile["vault_passphrase"],
        )
        payload = json.loads(decrypted_payload)
        assert payload["letter"] == result["letter"]
        assert payload["onchain_claim"]["public_key"] == result["public_key"]

    def test_missing_private_key_generates_one(self, tmp_path):
        profile = _build_profile(tmp_path)
        profile.pop("private_key_hex")

        result = auto_generate_claim(
            "Please help me ask for a human review of this account decision.",
            profile,
        )

        assert result["scenario"]["template"] == "REQUEST_FOR_HUMAN_REVIEW.md"
        assert len(result["generated_private_key_hex"]) == 64
        assert "Example Exchange" in result["letter"]
