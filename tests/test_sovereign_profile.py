"""Tests for the personal sovereign profile helpers."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest
from nacl.exceptions import CryptoError

from iris import sovereign_profile
from iris.sovereign_profile import (
    build_personal_profile,
    decrypt_profile_payload,
    fingerprint_public_key,
    load_personal_profile,
    load_personal_profile_summary,
    mirror_mode_prompt,
    normalize_mirror_greeting_style,
    normalize_mirror_reflection_scope,
    profile_path,
    profile_signature_block,
    save_personal_profile,
    setup_personal_profile,
    summarize_personal_profile,
    verify_personal_profile,
)


class _FakePostQuantumProvider:
    _FAKE_PQ_KEY_LENGTH = 48
    algorithm = "ML-DSA"
    module_name = "fake.mldsa"
    derive_public_key = None

    @staticmethod
    def generate_keypair():
        key = b"\x11" * _FakePostQuantumProvider._FAKE_PQ_KEY_LENGTH
        return key, key

    @staticmethod
    def sign(private_key: bytes, message: bytes) -> bytes:
        return hashlib.sha256(private_key + message).digest()

    @staticmethod
    def verify(public_key: bytes, message: bytes, signature: bytes) -> bool:
        return signature == hashlib.sha256(public_key + message).digest()


def test_build_personal_profile_generates_signed_identity():
    profile = build_personal_profile(name="Alex", handle="sovereign-user")

    assert profile["name"] == "Alex"
    assert profile["handle"] == "sovereign-user"
    assert profile["preferred_signature_block"] == "Alex [Burgess Principle]"
    assert len(profile["private_key_hex"]) == 64
    assert len(profile["public_key_hex"]) == 64
    assert len(profile["key_fingerprint"]) == 16
    assert profile["mirror_mode_enabled"] is False
    assert profile["mirror_mode_activated_at"] == ""
    assert profile["signature_mode"] == "classical"
    assert verify_personal_profile(profile) is True


def test_build_personal_profile_rejects_blank_name():
    with pytest.raises(ValueError, match="name must be a non-empty string"):
        build_personal_profile(name="   ")


def test_save_and_load_personal_profile_round_trip(tmp_path):
    profile = build_personal_profile(
        name="Alex",
        handle="sovereign-user",
        preferred_signature_block="Alex / Burgess Principle",
    )

    saved = save_personal_profile(profile, "correct horse battery staple", root=tmp_path)
    loaded = load_personal_profile("correct horse battery staple", root=tmp_path)
    summary = load_personal_profile_summary(root=tmp_path)

    assert Path(saved["path"]).exists()
    assert loaded["signed_profile"] == profile["signed_profile"]
    assert loaded["profile_signature"] == profile["profile_signature"]
    assert summary == saved["profile"]
    assert summary["name"] == "Alex"
    assert summary["key_fingerprint"] == profile["key_fingerprint"]


def test_load_personal_profile_rejects_wrong_passphrase(tmp_path):
    profile = build_personal_profile(name="Alex")
    save_personal_profile(profile, "correct horse battery staple", root=tmp_path)

    with pytest.raises(CryptoError):
        load_personal_profile("wrong passphrase", root=tmp_path)


def test_verify_personal_profile_rejects_tampered_signature():
    profile = build_personal_profile(name="Alex")

    assert (
        verify_personal_profile({**profile, "profile_signature": "00" * 64}) is False
    )


def test_helpers_expose_public_summary_defaults_and_storage_path(tmp_path):
    summary = summarize_personal_profile({})

    assert summary == {
        "name": "",
        "handle": "sovereign-user",
        "preferred_signature_block": "",
        "key_fingerprint": "",
        "public_key_hex": "",
        "profile_signature": "",
        "signature_mode": "classical",
        "post_quantum_algorithm": "",
        "post_quantum_public_key_hex": "",
        "signed_at": "",
        "mirror_mode_enabled": False,
        "mirror_mode_activated_at": "",
        "mirror_greeting_style": "neutral_professional",
        "mirror_custom_greeting": "",
        "mirror_reflection_scope": "vault_only",
        "mirror_greeting": "",
    }
    assert profile_signature_block(" Alex ", "  ") == ""
    assert mirror_mode_prompt("Alex") == "Alex — Mirror Mode active. The handshake continues on this device."
    assert mirror_mode_prompt("Alex", greeting_style="warm_personal") == "Hello Alex — Mirror Mode active. The handshake continues: your energy + my structure = sovereign record."
    assert mirror_mode_prompt("Alex", greeting_style="minimal") == "Mirror Mode active."
    assert mirror_mode_prompt("Alex", custom_greeting="Welcome back, Alex.") == "Welcome back, Alex."
    assert normalize_mirror_greeting_style("Warm & Personal") == "warm_personal"
    assert normalize_mirror_reflection_scope("all documents") == "all_documents"
    assert fingerprint_public_key("ab" * 32, length=8) == "9a2db2e2"
    assert profile_path(tmp_path) == tmp_path / ".sovereign-vault" / "personal-profile.json"


def test_mirror_mode_prompt_handles_blank_names_and_custom_whitespace():
    assert mirror_mode_prompt("   ") == "there — Mirror Mode active. The handshake continues on this device."
    assert (
        mirror_mode_prompt("   ", greeting_style="warm_personal")
        == "Hello there — Mirror Mode active. The handshake continues: your energy + my structure = sovereign record."
    )
    assert mirror_mode_prompt("Alex", custom_greeting="  Welcome back.  ") == "Welcome back."


def test_mirror_mode_normalizers_fall_back_for_unknown_values():
    assert normalize_mirror_greeting_style(None) == "neutral_professional"
    assert normalize_mirror_greeting_style("unknown") == "neutral_professional"
    assert normalize_mirror_reflection_scope(None) == "vault_only"
    assert normalize_mirror_reflection_scope("All Documents") == "all_documents"
    assert normalize_mirror_reflection_scope("public") == "vault_only"


def test_summarize_personal_profile_requires_name_before_emitting_mirror_greeting():
    summary = summarize_personal_profile(
        {
            "name": "   ",
            "mirror_mode_enabled": True,
            "mirror_greeting_style": "warm_personal",
        }
    )

    assert summary["mirror_mode_enabled"] is True
    assert summary["mirror_greeting_style"] == "warm_personal"
    assert summary["mirror_greeting"] == ""


def test_fingerprint_public_key_is_case_insensitive_and_respects_length():
    lowercase = fingerprint_public_key("ab" * 32, length=12)
    uppercase = fingerprint_public_key("AB" * 32, length=12)

    assert lowercase == uppercase
    assert lowercase == hashlib.sha256(bytes.fromhex("ab" * 32)).hexdigest()[:12]


def test_encrypted_profile_payload_round_trips_unicode_and_nested_values():
    payload = {
        "name": "Alex ✨",
        "notes": "Line one\nLine two — sovereignty",
        "nested": {"emoji": "🜂", "values": ["SOVEREIGN", "NULL", "AMBIGUOUS"]},
    }

    passphrase = "test-passphrase-do-not-use-in-production"
    encrypted = sovereign_profile._encrypt_payload(payload, passphrase)  # noqa: SLF001
    decrypted = decrypt_profile_payload(encrypted, passphrase)

    assert decrypted == payload


def test_build_personal_profile_can_use_hybrid_signatures(monkeypatch):
    monkeypatch.setattr(
        sovereign_profile._onchain_claims_module(),
        "_resolve_post_quantum_provider",
        lambda expected_algorithm=None: _FakePostQuantumProvider(),
    )

    profile = build_personal_profile(name="Alex", post_quantum=True)

    assert profile["signature_mode"] == "hybrid"
    assert profile["post_quantum_algorithm"] == "ML-DSA"
    assert verify_personal_profile(profile) is True


def test_save_personal_profile_requires_passphrase(tmp_path):
    profile = build_personal_profile(name="Alex")

    with pytest.raises(ValueError, match="vault_passphrase must be a non-empty string"):
        save_personal_profile(profile, "", root=tmp_path)


def test_save_personal_profile_rejects_invalid_signature(tmp_path):
    profile = build_personal_profile(name="Alex")

    with pytest.raises(ValueError, match="profile signature verification failed"):
        save_personal_profile(
            {**profile, "profile_signature": "00" * 64},
            "correct horse battery staple",
            root=tmp_path,
        )


def test_load_personal_profile_requires_passphrase(tmp_path):
    profile = build_personal_profile(name="Alex")
    save_personal_profile(profile, "correct horse battery staple", root=tmp_path)

    with pytest.raises(ValueError, match="vault_passphrase must be a non-empty string"):
        load_personal_profile("", root=tmp_path)


def test_load_personal_profile_rejects_tampered_signature_after_decryption(tmp_path):
    profile = build_personal_profile(name="Alex")
    saved = save_personal_profile(profile, "correct horse battery staple", root=tmp_path)
    record = json.loads(Path(saved["path"]).read_text(encoding="utf-8"))
    record["encrypted_payload"] = sovereign_profile._encrypt_payload(  # noqa: SLF001
        {**profile, "profile_signature": "00" * 64},
        "correct horse battery staple",
    )
    Path(saved["path"]).write_text(json.dumps(record), encoding="utf-8")

    with pytest.raises(ValueError, match="profile signature verification failed"):
        load_personal_profile("correct horse battery staple", root=tmp_path)


def test_setup_personal_profile_loads_existing_profile(tmp_path):
    created = setup_personal_profile(
        vault_passphrase="correct horse battery staple",
        root=tmp_path,
        name="Alex",
    )
    loaded = setup_personal_profile(
        vault_passphrase="correct horse battery staple",
        root=tmp_path,
        name="Ignored on reload",
    )

    assert created["created"] is True
    assert loaded["created"] is False
    assert loaded["profile"]["name"] == "Alex"


def test_setup_personal_profile_can_enable_mirror_mode_for_existing_profile(tmp_path):
    setup_personal_profile(
        vault_passphrase="correct horse battery staple",
        root=tmp_path,
        name="Alex",
    )

    updated = setup_personal_profile(
        vault_passphrase="correct horse battery staple",
        root=tmp_path,
        mirror_mode_enabled=True,
    )

    assert updated["created"] is False
    assert updated["profile"]["mirror_mode_enabled"] is True
    assert updated["profile"]["mirror_greeting"] == "Alex — Mirror Mode active. The handshake continues on this device."
    loaded = load_personal_profile("correct horse battery staple", root=tmp_path)
    assert loaded["mirror_mode_enabled"] is True
    assert loaded["mirror_mode_activated_at"]


def test_setup_personal_profile_can_disable_mirror_mode_for_existing_profile(tmp_path):
    setup_personal_profile(
        vault_passphrase="test-passphrase-do-not-use-in-production",
        root=tmp_path,
        name="Alex",
        mirror_mode_enabled=True,
    )

    updated = setup_personal_profile(
        vault_passphrase="test-passphrase-do-not-use-in-production",
        root=tmp_path,
        mirror_mode_enabled=False,
    )
    loaded = load_personal_profile("test-passphrase-do-not-use-in-production", root=tmp_path)

    assert updated["profile"]["mirror_mode_enabled"] is False
    assert updated["profile"]["mirror_greeting"] == ""
    assert loaded["mirror_mode_enabled"] is False
    assert loaded["mirror_mode_activated_at"] == ""


def test_setup_personal_profile_can_store_mirror_preferences(tmp_path):
    setup_personal_profile(
        vault_passphrase="correct horse battery staple",
        root=tmp_path,
        name="Alex",
    )

    updated = setup_personal_profile(
        vault_passphrase="correct horse battery staple",
        root=tmp_path,
        mirror_mode_enabled=True,
        mirror_greeting_style="warm_personal",
        mirror_custom_greeting="Welcome back, Alex.",
        mirror_reflection_scope="all_documents",
    )

    assert updated["profile"]["mirror_greeting_style"] == "warm_personal"
    assert updated["profile"]["mirror_custom_greeting"] == "Welcome back, Alex."
    assert updated["profile"]["mirror_reflection_scope"] == "all_documents"
    assert updated["profile"]["mirror_greeting"] == "Welcome back, Alex."


def test_setup_personal_profile_requires_name_when_creating_new_profile(tmp_path):
    with pytest.raises(ValueError, match="name must be a non-empty string"):
        setup_personal_profile(
            vault_passphrase="correct horse battery staple",
            root=tmp_path,
        )


def test_decrypt_profile_payload_returns_original_json(tmp_path):
    result = setup_personal_profile(
        vault_passphrase="correct horse battery staple",
        root=tmp_path,
        name="Alex",
    )
    raw_record = json.loads(Path(result["stored_path"]).read_text(encoding="utf-8"))

    payload = decrypt_profile_payload(
        raw_record["encrypted_payload"],
        "correct horse battery staple",
    )

    assert payload["name"] == "Alex"
    assert verify_personal_profile(payload) is True


def test_load_personal_profile_summary_returns_none_when_name_missing(tmp_path):
    path = profile_path(tmp_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            {
                "version": "1.3.0",
                "record_type": "personal-sovereign-profile",
                "stored_at": "2026-04-11T00:00:00+00:00",
            }
        ),
        encoding="utf-8",
    )

    assert load_personal_profile_summary(root=tmp_path) is None
