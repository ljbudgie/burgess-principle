"""Tests for the personal sovereign profile helpers."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from nacl.exceptions import CryptoError

from iris.sovereign_profile import (
    build_personal_profile,
    decrypt_profile_payload,
    load_personal_profile,
    load_personal_profile_summary,
    save_personal_profile,
    setup_personal_profile,
    verify_personal_profile,
)


def test_build_personal_profile_generates_signed_identity():
    profile = build_personal_profile(name="Lewis", handle="ljbudgie")

    assert profile["name"] == "Lewis"
    assert profile["handle"] == "ljbudgie"
    assert profile["preferred_signature_block"] == "Lewis [Burgess Principle]"
    assert len(profile["private_key_hex"]) == 64
    assert len(profile["public_key_hex"]) == 64
    assert len(profile["key_fingerprint"]) == 16
    assert verify_personal_profile(profile) is True


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
