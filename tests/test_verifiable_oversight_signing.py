"""Tests for verifiable_oversight Phase 2 — Ed25519 record signing.

Covers key generation, signing, independent verification, tamper-evidence,
fingerprint stability, Verifier integration, and error handling.
"""

import builtins
import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from verifiable_oversight import (
    BinaryTest,
    DecisionRecord,
    RecordSigner,
    SigningError,
    Verifier,
    signing_message,
    verify_record_signature,
    SIGNING_CONTEXT,
)


def _null_record() -> DecisionRecord:
    return DecisionRecord.create(
        subject="Fourth response — circular referral",
        institution="EASS",
        binary_test=BinaryTest(context="No named individual across four responses."),
    )


def _sovereign_record() -> DecisionRecord:
    return DecisionRecord.create(
        subject="Named review confirmed",
        institution="LGO",
        binary_test=BinaryTest(
            named_person="Rebecca Hunt",
            role_and_authority="Investigator, authority to uphold or reject",
            specific_facts_considered="Reviewed the specific complaint file",
            pre_decision_timing="Reviewed before the decision letter issued",
            authority_to_differ="Could have reached a different conclusion",
        ),
    )


# ---------------------------------------------------------------------------
# Key generation and identity
# ---------------------------------------------------------------------------


def test_generate_produces_valid_hex_keys():
    signer = RecordSigner.generate()
    assert len(signer.private_key_hex) == 64
    assert len(signer.public_key_hex) == 64
    bytes.fromhex(signer.private_key_hex)
    bytes.fromhex(signer.public_key_hex)


def test_signer_reconstructed_from_private_key_matches_public_key():
    signer = RecordSigner.generate()
    same = RecordSigner(signer.private_key_hex)
    assert same.public_key_hex == signer.public_key_hex


def test_invalid_private_key_raises_signing_error():
    with pytest.raises(SigningError):
        RecordSigner("not-hex")
    with pytest.raises(SigningError):
        RecordSigner("ab")  # too short


# ---------------------------------------------------------------------------
# Signing behaviour
# ---------------------------------------------------------------------------


def test_sign_populates_signature_fields():
    record = _null_record()
    signer = RecordSigner.generate()
    returned = signer.sign(record)

    assert record.signature == returned
    assert len(record.signature) == 128
    assert record.public_key == signer.public_key_hex
    assert record.signed_at is not None
    assert record.is_signed is True


def test_signing_does_not_change_fingerprint():
    record = _null_record()
    fingerprint_before = record.fingerprint
    RecordSigner.generate().sign(record)
    assert record.fingerprint == fingerprint_before


def test_signing_an_unsealed_record_seals_it():
    record = DecisionRecord(
        subject="x",
        institution="y",
        binary_test=BinaryTest(context="z"),
        result=BinaryTest(context="z").assess(),
    )
    assert record.fingerprint is None
    RecordSigner.generate().sign(record)
    assert record.fingerprint is not None
    assert verify_record_signature(record) is True


def test_sign_unsealed_without_seal_flag_raises():
    record = DecisionRecord(
        subject="x",
        institution="y",
        binary_test=BinaryTest(context="z"),
        result=BinaryTest(context="z").assess(),
    )
    with pytest.raises(SigningError):
        RecordSigner.generate().sign(record, seal_if_needed=False)


# ---------------------------------------------------------------------------
# Verification
# ---------------------------------------------------------------------------


def test_valid_signature_verifies():
    record = _sovereign_record()
    RecordSigner.generate().sign(record)
    assert verify_record_signature(record) is True


def test_unsigned_record_does_not_verify():
    assert verify_record_signature(_null_record()) is False


def test_tampering_after_signing_breaks_verification():
    record = _null_record()
    RecordSigner.generate().sign(record)
    assert verify_record_signature(record) is True

    record.subject = "Altered after signing"
    assert record.verify_integrity() is False
    assert verify_record_signature(record) is False


def test_wrong_public_key_does_not_verify():
    record = _null_record()
    RecordSigner.generate().sign(record)
    record.public_key = RecordSigner.generate().public_key_hex
    assert verify_record_signature(record) is False


def test_swapped_signature_does_not_verify():
    a = _null_record()
    b = _sovereign_record()
    signer = RecordSigner.generate()
    signer.sign(a)
    signer.sign(b)
    # Move a's signature onto b (same key, different fingerprint).
    b.signature = a.signature
    assert verify_record_signature(b) is False


def test_malformed_signature_raises_signing_error():
    record = _null_record()
    RecordSigner.generate().sign(record)
    record.signature = "zz"  # invalid hex/length
    with pytest.raises(SigningError):
        verify_record_signature(record)


# ---------------------------------------------------------------------------
# signing_message helper
# ---------------------------------------------------------------------------


def test_signing_message_is_context_prefixed():
    record = _null_record()
    message = signing_message(record.fingerprint)
    assert message == SIGNING_CONTEXT + b":" + record.fingerprint.encode("ascii")


def test_signing_message_rejects_bad_fingerprint():
    with pytest.raises(SigningError):
        signing_message("")
    with pytest.raises(SigningError):
        signing_message("nothex")


# ---------------------------------------------------------------------------
# Verifier integration
# ---------------------------------------------------------------------------


def test_verifier_reports_signature_none_when_unsigned():
    report = Verifier().verify(_null_record())
    assert report.signature_ok is None
    assert report.is_valid is True


def test_verifier_reports_signature_ok_when_signed():
    record = _sovereign_record()
    RecordSigner.generate().sign(record)
    report = Verifier().verify(record)
    assert report.signature_ok is True
    assert report.is_valid is True
    assert "signature_ok" in report.to_dict()


def test_verifier_flags_bad_signature():
    record = _null_record()
    RecordSigner.generate().sign(record)
    record.public_key = RecordSigner.generate().public_key_hex
    report = Verifier().verify(record)
    assert report.signature_ok is False
    assert report.is_valid is False
    assert any("Signature verification failed" in i for i in report.issues)


# ---------------------------------------------------------------------------
# Serialisation
# ---------------------------------------------------------------------------


def test_to_dict_includes_signing_fields():
    record = _null_record()
    RecordSigner.generate().sign(record)
    data = record.to_dict()
    assert data["signature"] == record.signature
    assert data["public_key"] == record.public_key
    assert data["signed_at"] == record.signed_at


# ---------------------------------------------------------------------------
# PyNaCl absence
# ---------------------------------------------------------------------------


def test_signing_without_pynacl_raises_signing_error(monkeypatch):
    real_import = builtins.__import__

    def block_nacl(name, *args, **kwargs):
        if name == "nacl" or name.startswith("nacl."):
            raise ImportError("Mocked: no nacl")
        return real_import(name, *args, **kwargs)

    saved = {
        k: sys.modules.pop(k)
        for k in list(sys.modules)
        if k == "nacl" or k.startswith("nacl.")
    }
    try:
        monkeypatch.setattr(builtins, "__import__", block_nacl)
        with pytest.raises(SigningError, match="PyNaCl"):
            RecordSigner.generate()
    finally:
        sys.modules.update(saved)
