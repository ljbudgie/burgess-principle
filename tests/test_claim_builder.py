"""Tests for the sovereign Iris claim builder."""

from __future__ import annotations

from contextlib import contextmanager
import importlib.util
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import pytest
from nacl.exceptions import CryptoError
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
    }


def _assert_all_placeholders_resolved(text: str) -> None:
    assert claim_builder._PLACEHOLDER_RE.findall(text) == []


@contextmanager
def _fresh_scenario_rows_cache():
    claim_builder._scenario_rows.cache_clear()
    try:
        yield
    finally:
        claim_builder._scenario_rows.cache_clear()


def test_classify_scenario_reads_fast_match_table():
    scenario = claim_builder.classify_scenario(
        "I want to reference a hash, signature, receipt, or on-chain claim."
    )

    assert scenario["template"] == "CRYPTOGRAPHIC_PROOF_AND_ONCHAIN_NOTICE_WITH_BURGESS.md"
    assert scenario["situation"] == (
        "I want to reference a hash, signature, receipt, or on-chain claim"
    )
    assert scenario["score"] > 0


@pytest.mark.parametrize(
    ("reply_text", "expected"),
    [
        (
            "Our automated system incorporates human oversight and your matter was reviewed in line with policy.",
            "AMBIGUOUS",
        ),
        (
            "No individual human review took place because the case was handled automatically.",
            "NULL",
        ),
        (
            "Yes — your case officer personally reviewed the specific facts of your case before the decision was issued.",
            "SOVEREIGN",
        ),
    ],
)
def test_classify_institutional_reply_detects_working_states(reply_text, expected):
    assert claim_builder.classify_institutional_reply(reply_text) == expected


def test_classify_scenario_routes_weasel_word_follow_up():
    scenario = claim_builder.classify_scenario(
        "They replied saying decisions are subject to human review and handled in line with policy."
    )

    assert scenario["template"] == "FOLLOW_UP_WEASEL_RESPONSE.md"
    assert scenario["reply_classification"] == "AMBIGUOUS"
    assert scenario["score"] > 0


def test_classify_scenario_prioritizes_weasel_follow_up_over_domain_keywords():
    scenario = claim_builder.classify_scenario(
        "My exchange froze withdrawals and then replied that the decision was reviewed in line with policy and subject to human review."
    )

    assert scenario["template"] == "FOLLOW_UP_WEASEL_RESPONSE.md"
    assert scenario["reply_classification"] == "AMBIGUOUS"


def test_scenario_rows_ignore_table_rows_without_template_links(tmp_path):
    scenarios_path = tmp_path / "COMMON_SCENARIOS.md"
    scenarios_path.write_text(
        "\n".join(
            [
                "# Test scenarios",
                "## Fast match table",
                "| Situation | Template | Notes |",
                "| --- | --- | --- |",
                "| Broken row | REQUEST_FOR_HUMAN_REVIEW.md | ignored |",
                "| Good row | [`REQUEST_FOR_HUMAN_REVIEW.md`](./REQUEST_FOR_HUMAN_REVIEW.md) | kept |",
            ]
        ),
        encoding="utf-8",
    )

    with _fresh_scenario_rows_cache():
        with patch.object(claim_builder, "_SCENARIOS", scenarios_path):
            rows = claim_builder._scenario_rows()

    assert rows == (
        {
            "situation": "Good row",
            "template": "REQUEST_FOR_HUMAN_REVIEW.md",
        },
    )


def test_module_raises_import_error_when_spec_loader_is_missing():
    with patch.object(
        claim_builder.importlib.util,
        "spec_from_file_location",
        return_value=SimpleNamespace(loader=None),
    ):
        with pytest.raises(ImportError, match="Could not load on-chain claims module"):
            claim_builder._module()


def test_public_helpers_generate_and_encrypt_claim(tmp_path):
    profile = _build_profile(tmp_path)
    template = claim_builder.load_template(
        "CRYPTO_EXCHANGE_ACCOUNT_RESTRICTION_WITH_BURGESS.md"
    )
    filled = claim_builder.fill_placeholders(
        template,
        profile,
        {
            "date": "2026-04-11",
            "team_name": profile["team_name"],
            "target_entity": profile["institution_name"],
            "reference": profile["reference"],
            "query_summary": "The exchange froze my account.",
            "transaction_hashes": profile["transaction_hash"],
            "wallet_addresses": profile["wallet_address"],
            "full_name": profile["full_name"],
            "contact_details": f'{profile["email"]} | {profile["phone"]}',
        },
    )

    claim = claim_builder.generate_commitment(
        filled,
        profile,
        category="exchange",
        target_entity=profile["institution_name"],
    )
    assert verify_onchain_receipt(
        claim["commitment_hash"], claim["signature"], claim["public_key"]
    ).valid is True

    with patch.object(claim_builder, "_ROOT", tmp_path):
        vault = claim_builder.encrypt_to_vault(
            {"created_at": claim["timestamp"], "letter": filled, "onchain_claim": claim},
            profile,
            "CRYPTO_EXCHANGE_ACCOUNT_RESTRICTION_WITH_BURGESS.md",
        )
    raw_record = json.loads(Path(vault["path"]).read_text(encoding="utf-8"))
    payload = json.loads(
        claim_builder._decrypt_vault_payload(
            raw_record["encrypted_payload"], profile["vault_passphrase"]
        )
    )
    assert payload["letter"] == filled


def test_fill_placeholders_supports_banking_template_labels():
    profile = {
        "full_name": "Alex Example",
        "bank_building_society_name": "Example Bank",
        "account_number_sort_code_if_relevant": "12-34-56 / 12345678",
        "contact_email": "alex@example.com",
    }
    template = claim_builder.load_template("DIRECT_DEBIT_REFUND_WITH_BURGESS.md")
    filled = claim_builder.fill_placeholders(
        template,
        profile,
        {
            "date": "2026-04-11",
            "amount": "150.00",
            "company_organisation_name_or_reference": "Example Utilities Ltd",
            claim_builder._norm(
                "refused the refund / investigated itself and rejected my claim / reversed the refund / pushed me to the Financial Ombudsman"
            ): "refused the refund",
        },
    )

    assert "Dear Example Bank Complaints / Fraud / Customer Services Team," in filled
    assert "On 2026-04-11, a Direct Debit of £150.00 was taken" in filled
    assert "by Example Utilities Ltd." in filled
    assert "The bank has refused the refund." in filled
    assert "Alex Example" in filled
    assert "12-34-56 / 12345678" in filled
    assert "alex@example.com" in filled
    _assert_all_placeholders_resolved(filled)


def test_fill_placeholders_supports_crypto_exchange_template_context(tmp_path):
    profile = _build_profile(tmp_path)
    template = claim_builder.load_template(
        "CRYPTO_EXCHANGE_ACCOUNT_RESTRICTION_WITH_BURGESS.md"
    )
    context = {
        **claim_builder._context(
            "The exchange froze my account and blocked withdrawals.", profile
        ),
        "commitment_hash": "0xcommitment",
        "onchain_reference": "claim-123",
    }
    filled = claim_builder.fill_placeholders(template, profile, context)

    assert "**Date:**" in filled and context["date"] in filled
    assert profile["reference"] in filled
    assert profile["institution_name"] in filled
    assert "The exchange froze my account and blocked withdrawals." in filled
    assert profile["transaction_hash"] in filled
    assert profile["wallet_address"] in filled
    assert "0xcommitment" in filled
    assert "claim-123" in filled
    assert "Alex Example" in filled
    assert "alex@example.com | 07123 456789" in filled
    _assert_all_placeholders_resolved(filled)


def test_fill_placeholders_supports_cryptographic_proof_template_context(tmp_path):
    profile = _build_profile(tmp_path)
    template = claim_builder.load_template(
        "CRYPTOGRAPHIC_PROOF_AND_ONCHAIN_NOTICE_WITH_BURGESS.md"
    )
    context = {
        **claim_builder._context(
            "I need to share a verifiable proof for this frozen account review.",
            profile,
        ),
        "signature_reference": "signed-proof / public-key",
        "commitment_hash": "0xproof",
        "onchain_reference": "tx-789",
    }
    filled = claim_builder.fill_placeholders(template, profile, context)

    assert profile["reference"] in filled
    assert profile["institution_name"] in filled
    assert "I need to share a verifiable proof for this frozen account review." in filled
    assert "0xproof" in filled
    assert "signed-proof / public-key" in filled
    assert "tx-789" in filled
    assert "Alex Example" in filled
    assert "alex@example.com | 07123 456789" in filled
    _assert_all_placeholders_resolved(filled)


def test_encrypt_to_vault_uses_default_sovereign_vault_directory(tmp_path):
    profile = _build_profile(tmp_path)
    profile["vault_path"] = "/etc/ignored-by-design"

    with patch.object(claim_builder, "_ROOT", tmp_path):
        claim_builder.encrypt_to_vault(
            {"created_at": "2026-04-11T00:00:00Z", "letter": "test", "onchain_claim": {}},
            profile,
            "REQUEST_FOR_HUMAN_REVIEW.md",
        )
    vault_files = list((tmp_path / ".sovereign-vault").glob("*.json"))
    assert len(vault_files) == 1


def test_generate_commitment_uses_supplied_signing_key(tmp_path):
    profile = _build_profile(tmp_path)
    claim = claim_builder.generate_commitment(
        "Human review request for my frozen exchange account.",
        profile,
        category="exchange",
        target_entity=profile["institution_name"],
    )

    assert claim["public_key"] == SigningKey(
        bytes.fromhex(profile["private_key_hex"])
    ).verify_key.encode().hex()
    assert claim["target_entity"] == profile["institution_name"]
    assert claim["category"] == "exchange"
    assert "generated_private_key_hex" not in claim
    assert verify_onchain_receipt(
        claim["commitment_hash"], claim["signature"], claim["public_key"]
    ).valid is True


def test_auto_generate_claim_can_include_mirror_reflection_block(tmp_path):
    profile = {
        **_build_profile(tmp_path),
        "name": "Alex Example",
        "key_fingerprint": "abc123def4567890",
        "mirror_mode_enabled": True,
        "mirror_reflection_scope": "all_documents",
    }

    with patch.object(claim_builder, "_ROOT", tmp_path):
        result = auto_generate_claim(
            "I need a calm first letter asking for human review.",
            profile,
        )

    assert result["mirror_reflection"]["enabled"] is True
    assert result["mirror_reflection"]["scope"] == "all_documents"
    assert "Mirror Reflection" in result["letter"]


def test_generate_commitment_raises_when_receipt_verification_fails(tmp_path):
    profile = _build_profile(tmp_path)

    with patch.object(
        claim_builder._ONCHAIN_CLAIMS,
        "verify_onchain_receipt",
        return_value=SimpleNamespace(valid=False),
    ):
        with pytest.raises(ValueError, match="Generated commitment failed verification"):
            claim_builder.generate_commitment(
                "Human review request for my frozen exchange account.",
                profile,
                category="exchange",
                target_entity=profile["institution_name"],
            )


def test_encrypt_to_vault_round_trips_payload_and_rejects_wrong_passphrase(tmp_path):
    profile = _build_profile(tmp_path)
    payload = {
        "created_at": "2026-04-11T12:00:00+00:00",
        "template": "CRYPTOGRAPHIC_PROOF_AND_ONCHAIN_NOTICE_WITH_BURGESS.md",
        "letter": "proof letter",
        "onchain_claim": {
            "commitment_hash": "0xproof",
            "public_key": "ab" * 32,
        },
    }

    with patch.object(claim_builder, "_ROOT", tmp_path):
        vault = claim_builder.encrypt_to_vault(
            payload,
            profile,
            "CRYPTOGRAPHIC_PROOF_AND_ONCHAIN_NOTICE_WITH_BURGESS.md",
        )

    raw_record = json.loads(Path(vault["path"]).read_text(encoding="utf-8"))
    assert raw_record["template"] == payload["template"]
    assert raw_record["created_at"] == payload["created_at"]
    assert raw_record["commitment_hash"] == "0xproof"
    assert raw_record["public_key"] == "ab" * 32
    assert payload["letter"] not in raw_record["encrypted_payload"]

    decrypted_payload = json.loads(
        claim_builder._decrypt_vault_payload(
            raw_record["encrypted_payload"], profile["vault_passphrase"]
        )
    )
    assert decrypted_payload == payload

    with pytest.raises(CryptoError):
        claim_builder._decrypt_vault_payload(
            raw_record["encrypted_payload"], "wrong passphrase"
        )


def test_encrypt_to_vault_requires_passphrase(tmp_path):
    profile = _build_profile(tmp_path)
    profile.pop("vault_passphrase")

    with pytest.raises(
        ValueError,
        match="profile must include vault_passphrase to save an encrypted letter",
    ):
        claim_builder.encrypt_to_vault(
            {"created_at": "2026-04-11T12:00:00+00:00", "letter": "proof letter"},
            profile,
            "REQUEST_FOR_HUMAN_REVIEW.md",
        )


def test_queue_onchain_fingerprint_persists_minimal_package(tmp_path):
    with patch.object(claim_builder, "_ROOT", tmp_path):
        queued = claim_builder.queue_onchain_fingerprint(
            {
                "commitment_hash": "0xproof",
                "signature": "0xsig",
                "public_key": "ab" * 32,
                "target_entity": "Example Exchange",
                "category": "exchange",
            }
        )

    payload = json.loads(Path(queued["path"]).read_text(encoding="utf-8"))
    assert payload["version"] == "1.3.0"
    assert payload["queue_id"] == queued["queue_id"]
    assert payload["fingerprint"]["commitment_hash"] == "0xproof"
    assert payload["fingerprint"]["signature"] == "0xsig"
    assert payload["fingerprint"]["public_key"] == "ab" * 32
    assert payload["fingerprint"]["target_entity"] == "Example Exchange"


def test_queue_onchain_fingerprint_requires_core_fields(tmp_path):
    with patch.object(claim_builder, "_ROOT", tmp_path):
        with pytest.raises(
            ValueError,
            match="fingerprint must include commitment_hash, signature, and public_key",
        ):
            claim_builder.queue_onchain_fingerprint({"commitment_hash": "0xproof"})


class TestAutoGenerateClaim:
    @pytest.mark.parametrize(
        ("user_query", "profile"),
        [
            ("", {}),
            ("   ", {}),
            (None, {}),  # type: ignore[arg-type]
            ("Need a letter", None),  # type: ignore[arg-type]
        ],
    )
    def test_rejects_invalid_inputs(self, user_query, profile):
        with pytest.raises(
            ValueError,
            match="user_query must be a non-empty string and profile must be a dict",
        ):
            auto_generate_claim(user_query, profile)

    def test_crypto_exchange_flow_generates_signed_vault_record(self, tmp_path):
        profile = _build_profile(tmp_path)

        with patch.object(claim_builder, "_ROOT", tmp_path):
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

        with patch.object(claim_builder, "_ROOT", tmp_path):
            result = auto_generate_claim(
                "Please help me ask for a human review of this account decision.",
                profile,
            )

        assert result["scenario"]["template"] == "REQUEST_FOR_HUMAN_REVIEW.md"
        assert len(result["generated_private_key_hex"]) == 64
        assert "Example Exchange" in result["letter"]

    def test_cryptographic_proof_flow_generates_notice_and_vault_record(self, tmp_path):
        profile = _build_profile(tmp_path)
        profile["onchain_reference"] = "0xtxhash"

        with patch.object(claim_builder, "_ROOT", tmp_path):
            result = auto_generate_claim(
                "I need to reference a hash, signature, receipt, or on-chain claim.",
                profile,
            )

        assert result["scenario"]["template"] == (
            "CRYPTOGRAPHIC_PROOF_AND_ONCHAIN_NOTICE_WITH_BURGESS.md"
        )
        assert result["onchain_claim"]["target_entity"] == profile["institution_name"]
        assert result["commitment_hash"] in result["letter"]
        assert result["signature"] in result["letter"]
        assert profile["onchain_reference"] in result["letter"]
        assert result["commitment_hash"] in result["onchain_notice"]
        assert result["signature"] in result["onchain_notice"]
        assert result["unresolved_placeholders"] == []

        raw_record = json.loads(
            Path(result["vault_record"]["path"]).read_text(encoding="utf-8")
        )
        payload = json.loads(
            claim_builder._decrypt_vault_payload(
                raw_record["encrypted_payload"], profile["vault_passphrase"]
            )
        )
        assert payload["template"] == result["scenario"]["template"]
        assert payload["created_at"] == result["timestamp"]
        assert (
            datetime.fromisoformat(payload["created_at"]).tzinfo is timezone.utc
        )
