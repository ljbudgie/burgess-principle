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
    algorithm = "ML-DSA"
    module_name = "fake.mldsa"
    derive_public_key = None

    @staticmethod
    def generate_keypair():
        key = b"\x11" * 48
        return key, key

    @staticmethod
    def sign(private_key: bytes, message: bytes) -> bytes:
        return hashlib.sha256(private_key + message).digest()

    @staticmethod
    def verify(public_key: bytes, message: bytes, signature: bytes) -> bool:
        return signature == hashlib.sha256(public_key + message).digest()


def test_build_personal_profile_generates_signed_identity():
    profile = build_personal_profile(name="Lewis", handle="ljbudgie")

    assert profile["name"] == "Lewis"
    assert profile["handle"] == "ljbudgie"
    assert profile["preferred_signature_block"] == "Lewis [Burgess Principle]"
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
        name="Lewis",
        handle="ljbudgie",
        preferred_signature_block="Lewis / Burgess Principle",
    )

    saved = save_personal_profile(profile, "correct horse battery staple", root=tmp_path)
    loaded = load_personal_profile("correct horse battery staple", root=tmp_path)
    summary = load_personal_profile_summary(root=tmp_path)

    assert Path(saved["path"]).exists()
    assert loaded["signed_profile"] == profile["signed_profile"]
    assert loaded["profile_signature"] == profile["profile_signature"]
    assert summary == saved["profile"]
    assert summary["name"] == "Lewis"
    assert summary["key_fingerprint"] == profile["key_fingerprint"]


def test_load_personal_profile_rejects_wrong_passphrase(tmp_path):
    profile = build_personal_profile(name="Lewis")
    save_personal_profile(profile, "correct horse battery staple", root=tmp_path)

    with pytest.raises(CryptoError):
        load_personal_profile("wrong passphrase", root=tmp_path)


def test_verify_personal_profile_rejects_tampered_signature():
    profile = build_personal_profile(name="Lewis")

    assert (
        verify_personal_profile({**profile, "profile_signature": "00" * 64}) is False
    )


def test_helpers_expose_public_summary_defaults_and_storage_path(tmp_path):
    summary = summarize_personal_profile({})

    assert summary == {
        "name": "",
        "handle": "ljbudgie",
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
    assert profile_signature_block(" Lewis ", "  ") == ""
    assert mirror_mode_prompt("Lewis") == "Lewis — Mirror Mode active. The handshake continues on this device."
    assert mirror_mode_prompt("Lewis", greeting_style="warm_personal") == "Hello Lewis — Mirror Mode active. The handshake continues: your energy + my structure = sovereign record."
    assert mirror_mode_prompt("Lewis", greeting_style="minimal") == "Mirror Mode active."
    assert mirror_mode_prompt("Lewis", custom_greeting="Welcome back, Lewis.") == "Welcome back, Lewis."
    assert normalize_mirror_greeting_style("Warm & Personal") == "warm_personal"
    assert normalize_mirror_reflection_scope("all documents") == "all_documents"
    assert fingerprint_public_key("ab" * 32, length=8) == "9a2db2e2"
    assert profile_path(tmp_path) == tmp_path / ".sovereign-vault" / "personal-profile.json"


def test_build_personal_profile_can_use_hybrid_signatures(monkeypatch):
    monkeypatch.setattr(
        sovereign_profile._onchain_claims_module(),
        "_resolve_post_quantum_provider",
        lambda expected_algorithm=None: _FakePostQuantumProvider(),
    )

    profile = build_personal_profile(name="Lewis", post_quantum=True)

    assert profile["signature_mode"] == "hybrid"
    assert profile["post_quantum_algorithm"] == "ML-DSA"
    assert verify_personal_profile(profile) is True


def test_save_personal_profile_requires_passphrase(tmp_path):
    profile = build_personal_profile(name="Lewis")

    with pytest.raises(ValueError, match="vault_passphrase must be a non-empty string"):
        save_personal_profile(profile, "", root=tmp_path)


def test_save_personal_profile_rejects_invalid_signature(tmp_path):
    profile = build_personal_profile(name="Lewis")

    with pytest.raises(ValueError, match="profile signature verification failed"):
        save_personal_profile(
            {**profile, "profile_signature": "00" * 64},
            "correct horse battery staple",
            root=tmp_path,
        )


def test_load_personal_profile_requires_passphrase(tmp_path):
    profile = build_personal_profile(name="Lewis")
    save_personal_profile(profile, "correct horse battery staple", root=tmp_path)

    with pytest.raises(ValueError, match="vault_passphrase must be a non-empty string"):
        load_personal_profile("", root=tmp_path)


def test_load_personal_profile_rejects_tampered_signature_after_decryption(tmp_path):
    profile = build_personal_profile(name="Lewis")
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
        name="Lewis",
    )
    loaded = setup_personal_profile(
        vault_passphrase="correct horse battery staple",
        root=tmp_path,
        name="Ignored on reload",
    )

    assert created["created"] is True
    assert loaded["created"] is False
    assert loaded["profile"]["name"] == "Lewis"


def test_setup_personal_profile_can_enable_mirror_mode_for_existing_profile(tmp_path):
    setup_personal_profile(
        vault_passphrase="correct horse battery staple",
        root=tmp_path,
        name="Lewis",
    )

    updated = setup_personal_profile(
        vault_passphrase="correct horse battery staple",
        root=tmp_path,
        mirror_mode_enabled=True,
    )

    assert updated["created"] is False
    assert updated["profile"]["mirror_mode_enabled"] is True
    assert updated["profile"]["mirror_greeting"] == "Lewis — Mirror Mode active. The handshake continues on this device."
    loaded = load_personal_profile("correct horse battery staple", root=tmp_path)
    assert loaded["mirror_mode_enabled"] is True
    assert loaded["mirror_mode_activated_at"]


def test_setup_personal_profile_can_store_mirror_preferences(tmp_path):
    setup_personal_profile(
        vault_passphrase="correct horse battery staple",
        root=tmp_path,
        name="Lewis",
    )

    updated = setup_personal_profile(
        vault_passphrase="correct horse battery staple",
        root=tmp_path,
        mirror_mode_enabled=True,
        mirror_greeting_style="warm_personal",
        mirror_custom_greeting="Welcome back, Lewis.",
        mirror_reflection_scope="all_documents",
    )

    assert updated["profile"]["mirror_greeting_style"] == "warm_personal"
    assert updated["profile"]["mirror_custom_greeting"] == "Welcome back, Lewis."
    assert updated["profile"]["mirror_reflection_scope"] == "all_documents"
    assert updated["profile"]["mirror_greeting"] == "Welcome back, Lewis."


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
        name="Lewis",
    )
    raw_record = json.loads(Path(result["stored_path"]).read_text(encoding="utf-8"))

    payload = decrypt_profile_payload(
        raw_record["encrypted_payload"],
        "correct horse battery staple",
    )

    assert payload["name"] == "Lewis"
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
