"""Tests for the Burgess Claims Protocol on-chain SDK.

Tests cover claim generation, commitment hashing, Ed25519 signing,
verification, and the full roundtrip (generate → verify).
"""

import hashlib
import json
import os
import sys

import pytest

# Ensure the SDK is importable from the repo root.
sys.path.insert(
    0, os.path.join(os.path.dirname(__file__), "..", "onchain-protocol", "sdk")
)

from onchain_claims import (
    VALID_CATEGORIES,
    OnchainClaim,
    VerificationResult,
    _canonical_claim_json,
    _compute_commitment,
    _validate_hex_string,
    _validate_non_empty_string,
    generate_onchain_claim,
    verify_commitment,
    verify_onchain_receipt,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_keypair():
    """Generate a fresh Ed25519 keypair using PyNaCl."""
    from nacl.signing import SigningKey

    sk = SigningKey.generate()
    return sk.encode().hex(), sk.verify_key.encode().hex()


PRIVATE_KEY, PUBLIC_KEY = _make_keypair()
FIXED_NONCE = os.urandom(32).hex()
FIXED_TIMESTAMP = "2026-04-10T12:00:00+00:00"


# ---------------------------------------------------------------------------
# generate_onchain_claim — happy path
# ---------------------------------------------------------------------------

class TestGenerateOnchainClaim:
    def test_returns_onchain_claim(self):
        claim = generate_onchain_claim(
            claim_details="Test claim",
            target_entity="Test Org",
            category="dispute",
            private_key_hex=PRIVATE_KEY,
            timestamp=FIXED_TIMESTAMP,
            nonce=FIXED_NONCE,
        )
        assert isinstance(claim, OnchainClaim)

    def test_commitment_hash_is_64_hex(self):
        claim = generate_onchain_claim(
            claim_details="Test",
            target_entity="Org",
            category="enforcement",
            private_key_hex=PRIVATE_KEY,
        )
        assert len(claim.commitment_hash) == 64
        int(claim.commitment_hash, 16)  # Ensure valid hex

    def test_signature_is_128_hex(self):
        claim = generate_onchain_claim(
            claim_details="Test",
            target_entity="Org",
            category="enforcement",
            private_key_hex=PRIVATE_KEY,
        )
        assert len(claim.signature) == 128
        int(claim.signature, 16)

    def test_public_key_derived_correctly(self):
        claim = generate_onchain_claim(
            claim_details="Test",
            target_entity="Org",
            category="enforcement",
            private_key_hex=PRIVATE_KEY,
        )
        assert claim.public_key == PUBLIC_KEY

    def test_category_preserved(self):
        claim = generate_onchain_claim(
            claim_details="Test",
            target_entity="Org",
            category="oversight",
            private_key_hex=PRIVATE_KEY,
        )
        assert claim.category == "oversight"

    def test_target_entity_preserved(self):
        claim = generate_onchain_claim(
            claim_details="Test",
            target_entity="My Council",
            category="enforcement",
            private_key_hex=PRIVATE_KEY,
        )
        assert claim.target_entity == "My Council"

    def test_custom_timestamp_preserved(self):
        claim = generate_onchain_claim(
            claim_details="Test",
            target_entity="Org",
            category="enforcement",
            private_key_hex=PRIVATE_KEY,
            timestamp=FIXED_TIMESTAMP,
        )
        assert claim.timestamp == FIXED_TIMESTAMP

    def test_custom_nonce_preserved(self):
        claim = generate_onchain_claim(
            claim_details="Test",
            target_entity="Org",
            category="enforcement",
            private_key_hex=PRIVATE_KEY,
            nonce=FIXED_NONCE,
        )
        assert claim.nonce == FIXED_NONCE

    def test_auto_timestamp_is_iso(self):
        claim = generate_onchain_claim(
            claim_details="Test",
            target_entity="Org",
            category="enforcement",
            private_key_hex=PRIVATE_KEY,
        )
        # Should parse without error
        from datetime import datetime

        datetime.fromisoformat(claim.timestamp)

    def test_auto_nonce_is_64_hex(self):
        claim = generate_onchain_claim(
            claim_details="Test",
            target_entity="Org",
            category="enforcement",
            private_key_hex=PRIVATE_KEY,
        )
        assert len(claim.nonce) == 64
        int(claim.nonce, 16)

    def test_different_claims_produce_different_commitments(self):
        c1 = generate_onchain_claim(
            claim_details="Claim A",
            target_entity="Org",
            category="enforcement",
            private_key_hex=PRIVATE_KEY,
        )
        c2 = generate_onchain_claim(
            claim_details="Claim B",
            target_entity="Org",
            category="enforcement",
            private_key_hex=PRIVATE_KEY,
        )
        assert c1.commitment_hash != c2.commitment_hash

    def test_same_inputs_same_commitment(self):
        kwargs = dict(
            claim_details="Same",
            target_entity="Org",
            category="enforcement",
            private_key_hex=PRIVATE_KEY,
            timestamp=FIXED_TIMESTAMP,
            nonce=FIXED_NONCE,
        )
        c1 = generate_onchain_claim(**kwargs)
        c2 = generate_onchain_claim(**kwargs)
        assert c1.commitment_hash == c2.commitment_hash

    def test_all_valid_categories_accepted(self):
        for cat in VALID_CATEGORIES:
            claim = generate_onchain_claim(
                claim_details="Test",
                target_entity="Org",
                category=cat,
                private_key_hex=PRIVATE_KEY,
            )
            assert claim.category == cat


# ---------------------------------------------------------------------------
# generate_onchain_claim — validation
# ---------------------------------------------------------------------------

class TestGenerateValidation:
    def test_empty_claim_details_raises(self):
        with pytest.raises(ValueError, match="claim_details"):
            generate_onchain_claim(
                claim_details="",
                target_entity="Org",
                category="enforcement",
                private_key_hex=PRIVATE_KEY,
            )

    def test_empty_target_entity_raises(self):
        with pytest.raises(ValueError, match="target_entity"):
            generate_onchain_claim(
                claim_details="Test",
                target_entity="",
                category="enforcement",
                private_key_hex=PRIVATE_KEY,
            )

    def test_invalid_category_raises(self):
        with pytest.raises(ValueError, match="category"):
            generate_onchain_claim(
                claim_details="Test",
                target_entity="Org",
                category="invalid",
                private_key_hex=PRIVATE_KEY,
            )

    def test_invalid_private_key_hex_raises(self):
        with pytest.raises(ValueError, match="private_key_hex"):
            generate_onchain_claim(
                claim_details="Test",
                target_entity="Org",
                category="enforcement",
                private_key_hex="not-hex",
            )

    def test_short_private_key_raises(self):
        with pytest.raises(ValueError, match="private_key_hex"):
            generate_onchain_claim(
                claim_details="Test",
                target_entity="Org",
                category="enforcement",
                private_key_hex="aa" * 16,
            )

    def test_non_string_claim_details_raises(self):
        with pytest.raises(TypeError, match="claim_details"):
            generate_onchain_claim(
                claim_details=123,  # type: ignore[arg-type]
                target_entity="Org",
                category="enforcement",
                private_key_hex=PRIVATE_KEY,
            )

    def test_whitespace_only_claim_details_raises(self):
        with pytest.raises(ValueError, match="claim_details"):
            generate_onchain_claim(
                claim_details="   ",
                target_entity="Org",
                category="enforcement",
                private_key_hex=PRIVATE_KEY,
            )


# ---------------------------------------------------------------------------
# OnchainClaim serialisation
# ---------------------------------------------------------------------------

class TestOnchainClaimSerialisation:
    def test_to_json_is_valid_json(self):
        claim = generate_onchain_claim(
            claim_details="Test",
            target_entity="Org",
            category="enforcement",
            private_key_hex=PRIVATE_KEY,
            timestamp=FIXED_TIMESTAMP,
            nonce=FIXED_NONCE,
        )
        data = json.loads(claim.to_json())
        assert data["commitmentHash"] == claim.commitment_hash
        assert data["target"] == "Org"

    def test_to_json_sorted_keys(self):
        claim = generate_onchain_claim(
            claim_details="Test",
            target_entity="Org",
            category="enforcement",
            private_key_hex=PRIVATE_KEY,
        )
        data = json.loads(claim.to_json())
        keys = list(data.keys())
        assert keys == sorted(keys)

    def test_to_dict_returns_all_fields(self):
        claim = generate_onchain_claim(
            claim_details="Test",
            target_entity="Org",
            category="enforcement",
            private_key_hex=PRIVATE_KEY,
        )
        d = claim.to_dict()
        expected_keys = {
            "commitment_hash",
            "signature",
            "public_key",
            "target_entity",
            "category",
            "timestamp",
            "nonce",
        }
        assert set(d.keys()) == expected_keys

    def test_to_dict_returns_new_dict_each_call(self):
        claim = generate_onchain_claim(
            claim_details="Test",
            target_entity="Org",
            category="enforcement",
            private_key_hex=PRIVATE_KEY,
        )
        d1 = claim.to_dict()
        d2 = claim.to_dict()
        assert d1 == d2
        assert d1 is not d2


# ---------------------------------------------------------------------------
# verify_onchain_receipt — roundtrip
# ---------------------------------------------------------------------------

class TestVerifyOnchainReceipt:
    def test_valid_signature_returns_true(self):
        claim = generate_onchain_claim(
            claim_details="Roundtrip test",
            target_entity="Org",
            category="enforcement",
            private_key_hex=PRIVATE_KEY,
        )
        result = verify_onchain_receipt(
            commitment_hash=claim.commitment_hash,
            signature=claim.signature,
            public_key_hex=claim.public_key,
        )
        assert result.valid is True
        assert "verified" in result.details.lower()

    def test_wrong_signature_returns_false(self):
        claim = generate_onchain_claim(
            claim_details="Test",
            target_entity="Org",
            category="enforcement",
            private_key_hex=PRIVATE_KEY,
        )
        bad_sig = "aa" * 64
        result = verify_onchain_receipt(
            commitment_hash=claim.commitment_hash,
            signature=bad_sig,
            public_key_hex=claim.public_key,
        )
        assert result.valid is False
        assert "failed" in result.details.lower()

    def test_wrong_public_key_returns_false(self):
        claim = generate_onchain_claim(
            claim_details="Test",
            target_entity="Org",
            category="enforcement",
            private_key_hex=PRIVATE_KEY,
        )
        other_priv, other_pub = _make_keypair()
        result = verify_onchain_receipt(
            commitment_hash=claim.commitment_hash,
            signature=claim.signature,
            public_key_hex=other_pub,
        )
        assert result.valid is False

    def test_tampered_hash_returns_false(self):
        claim = generate_onchain_claim(
            claim_details="Test",
            target_entity="Org",
            category="enforcement",
            private_key_hex=PRIVATE_KEY,
        )
        tampered = "bb" * 32
        result = verify_onchain_receipt(
            commitment_hash=tampered,
            signature=claim.signature,
            public_key_hex=claim.public_key,
        )
        assert result.valid is False

    def test_result_contains_hash_and_key(self):
        claim = generate_onchain_claim(
            claim_details="Test",
            target_entity="Org",
            category="enforcement",
            private_key_hex=PRIVATE_KEY,
        )
        result = verify_onchain_receipt(
            commitment_hash=claim.commitment_hash,
            signature=claim.signature,
            public_key_hex=claim.public_key,
        )
        assert result.commitment_hash == claim.commitment_hash
        assert result.public_key == claim.public_key


# ---------------------------------------------------------------------------
# verify_onchain_receipt — validation
# ---------------------------------------------------------------------------

class TestVerifyReceiptValidation:
    def test_invalid_commitment_hash_raises(self):
        with pytest.raises(ValueError, match="commitment_hash"):
            verify_onchain_receipt(
                commitment_hash="not-hex",
                signature="aa" * 64,
                public_key_hex=PUBLIC_KEY,
            )

    def test_invalid_signature_raises(self):
        with pytest.raises(ValueError, match="signature"):
            verify_onchain_receipt(
                commitment_hash="aa" * 32,
                signature="not-hex",
                public_key_hex=PUBLIC_KEY,
            )

    def test_invalid_public_key_raises(self):
        with pytest.raises(ValueError, match="public_key_hex"):
            verify_onchain_receipt(
                commitment_hash="aa" * 32,
                signature="aa" * 64,
                public_key_hex="short",
            )


# ---------------------------------------------------------------------------
# verify_commitment — selective disclosure
# ---------------------------------------------------------------------------

class TestVerifyCommitment:
    def test_matching_preimage_returns_true(self):
        claim = generate_onchain_claim(
            claim_details="Disclosure test",
            target_entity="Org",
            category="disclosure",
            private_key_hex=PRIVATE_KEY,
            timestamp=FIXED_TIMESTAMP,
            nonce=FIXED_NONCE,
        )
        assert verify_commitment(
            claim_details="Disclosure test",
            timestamp=FIXED_TIMESTAMP,
            nonce=FIXED_NONCE,
            public_key_hex=claim.public_key,
            expected_hash=claim.commitment_hash,
        )

    def test_tampered_details_returns_false(self):
        claim = generate_onchain_claim(
            claim_details="Original",
            target_entity="Org",
            category="enforcement",
            private_key_hex=PRIVATE_KEY,
            timestamp=FIXED_TIMESTAMP,
            nonce=FIXED_NONCE,
        )
        assert not verify_commitment(
            claim_details="Tampered",
            timestamp=FIXED_TIMESTAMP,
            nonce=FIXED_NONCE,
            public_key_hex=claim.public_key,
            expected_hash=claim.commitment_hash,
        )

    def test_wrong_nonce_returns_false(self):
        claim = generate_onchain_claim(
            claim_details="Test",
            target_entity="Org",
            category="enforcement",
            private_key_hex=PRIVATE_KEY,
            timestamp=FIXED_TIMESTAMP,
            nonce=FIXED_NONCE,
        )
        wrong_nonce = os.urandom(32).hex()
        assert not verify_commitment(
            claim_details="Test",
            timestamp=FIXED_TIMESTAMP,
            nonce=wrong_nonce,
            public_key_hex=claim.public_key,
            expected_hash=claim.commitment_hash,
        )

    def test_case_insensitive_hash_comparison(self):
        claim = generate_onchain_claim(
            claim_details="Case test",
            target_entity="Org",
            category="enforcement",
            private_key_hex=PRIVATE_KEY,
            timestamp=FIXED_TIMESTAMP,
            nonce=FIXED_NONCE,
        )
        assert verify_commitment(
            claim_details="Case test",
            timestamp=FIXED_TIMESTAMP,
            nonce=FIXED_NONCE,
            public_key_hex=claim.public_key,
            expected_hash=claim.commitment_hash.upper(),
        )


# ---------------------------------------------------------------------------
# _compute_commitment — deterministic
# ---------------------------------------------------------------------------

class TestComputeCommitment:
    def test_deterministic(self):
        h1 = _compute_commitment("a", "b", "cc" * 32, "dd" * 32)
        h2 = _compute_commitment("a", "b", "cc" * 32, "dd" * 32)
        assert h1 == h2

    def test_different_inputs_different_hashes(self):
        h1 = _compute_commitment("a", "b", "cc" * 32, "dd" * 32)
        h2 = _compute_commitment("x", "b", "cc" * 32, "dd" * 32)
        assert h1 != h2

    def test_hash_is_64_hex_chars(self):
        h = _compute_commitment("test", "ts", "aa" * 32, "bb" * 32)
        assert len(h) == 64
        int(h, 16)


# ---------------------------------------------------------------------------
# Full roundtrip: generate → verify signature → verify commitment
# ---------------------------------------------------------------------------

class TestFullRoundtrip:
    def test_end_to_end(self):
        """Generate a claim, verify the signature, then verify the commitment."""
        claim = generate_onchain_claim(
            claim_details="My council tax was sent to enforcement without review",
            target_entity="Example Council",
            category="enforcement",
            private_key_hex=PRIVATE_KEY,
            timestamp=FIXED_TIMESTAMP,
            nonce=FIXED_NONCE,
        )

        # Step 1: Verify the Ed25519 signature
        sig_result = verify_onchain_receipt(
            commitment_hash=claim.commitment_hash,
            signature=claim.signature,
            public_key_hex=claim.public_key,
        )
        assert sig_result.valid

        # Step 2: Verify the commitment (selective disclosure)
        assert verify_commitment(
            claim_details="My council tax was sent to enforcement without review",
            timestamp=FIXED_TIMESTAMP,
            nonce=FIXED_NONCE,
            public_key_hex=claim.public_key,
            expected_hash=claim.commitment_hash,
        )

    def test_roundtrip_with_auto_defaults(self):
        """Roundtrip with auto-generated timestamp and nonce."""
        claim = generate_onchain_claim(
            claim_details="Auto defaults test",
            target_entity="Org",
            category="oversight",
            private_key_hex=PRIVATE_KEY,
        )

        result = verify_onchain_receipt(
            commitment_hash=claim.commitment_hash,
            signature=claim.signature,
            public_key_hex=claim.public_key,
        )
        assert result.valid

        assert verify_commitment(
            claim_details="Auto defaults test",
            timestamp=claim.timestamp,
            nonce=claim.nonce,
            public_key_hex=claim.public_key,
            expected_hash=claim.commitment_hash,
        )


# ---------------------------------------------------------------------------
# _canonical_claim_json
# ---------------------------------------------------------------------------

class TestCanonicalClaimJson:
    def test_returns_valid_json(self):
        result = _canonical_claim_json("details", "2026-01-01T00:00:00Z", "aa" * 32, "bb" * 32)
        data = json.loads(result)
        assert isinstance(data, dict)

    def test_contains_expected_keys(self):
        result = _canonical_claim_json("my claim", "ts", "aa" * 32, "bb" * 32)
        data = json.loads(result)
        assert set(data.keys()) == {"claim_details", "nonce", "public_key", "timestamp"}

    def test_values_preserved(self):
        result = _canonical_claim_json("hello", "2026-01-01", "cc" * 32, "dd" * 32)
        data = json.loads(result)
        assert data["claim_details"] == "hello"
        assert data["timestamp"] == "2026-01-01"
        assert data["nonce"] == "cc" * 32
        assert data["public_key"] == "dd" * 32

    def test_keys_are_sorted(self):
        result = _canonical_claim_json("x", "y", "aa" * 32, "bb" * 32)
        data = json.loads(result)
        keys = list(data.keys())
        assert keys == sorted(keys)

    def test_compact_separators(self):
        result = _canonical_claim_json("x", "y", "aa" * 32, "bb" * 32)
        # Compact JSON should not have spaces after : or ,
        assert ": " not in result
        assert ", " not in result

    def test_deterministic(self):
        r1 = _canonical_claim_json("a", "b", "cc" * 32, "dd" * 32)
        r2 = _canonical_claim_json("a", "b", "cc" * 32, "dd" * 32)
        assert r1 == r2

    def test_different_inputs_produce_different_json(self):
        r1 = _canonical_claim_json("a", "b", "cc" * 32, "dd" * 32)
        r2 = _canonical_claim_json("x", "b", "cc" * 32, "dd" * 32)
        assert r1 != r2


# ---------------------------------------------------------------------------
# _validate_hex_string
# ---------------------------------------------------------------------------

class TestValidateHexString:
    def test_valid_hex_passes(self):
        _validate_hex_string("aabb", "test")

    def test_valid_hex_with_expected_length(self):
        _validate_hex_string("aa" * 32, "test", expected_length=64)

    def test_non_string_raises_type_error(self):
        with pytest.raises(TypeError, match="test must be a string"):
            _validate_hex_string(123, "test")  # type: ignore[arg-type]

    def test_none_raises_type_error(self):
        with pytest.raises(TypeError, match="test must be a string"):
            _validate_hex_string(None, "test")  # type: ignore[arg-type]

    def test_empty_string_raises_value_error(self):
        with pytest.raises(ValueError, match="test must not be empty"):
            _validate_hex_string("", "test")

    def test_non_hex_raises_value_error(self):
        with pytest.raises(ValueError, match="valid hexadecimal"):
            _validate_hex_string("not-hex!", "test")

    def test_wrong_length_raises_value_error(self):
        with pytest.raises(ValueError, match="exactly 64"):
            _validate_hex_string("aa" * 16, "test", expected_length=64)

    def test_no_length_check_when_none(self):
        # Should pass for any valid hex string regardless of length
        _validate_hex_string("aabb", "test", expected_length=None)
        _validate_hex_string("aa" * 100, "test", expected_length=None)

    def test_error_includes_field_name(self):
        with pytest.raises(TypeError, match="my_field"):
            _validate_hex_string(42, "my_field")  # type: ignore[arg-type]

    def test_bytes_raises_type_error(self):
        with pytest.raises(TypeError, match="must be a string"):
            _validate_hex_string(b"aabb", "test")  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# _validate_non_empty_string
# ---------------------------------------------------------------------------

class TestValidateNonEmptyString:
    def test_valid_string_passes(self):
        _validate_non_empty_string("hello", "test")

    def test_non_string_raises_type_error(self):
        with pytest.raises(TypeError, match="test must be a string"):
            _validate_non_empty_string(123, "test")  # type: ignore[arg-type]

    def test_empty_string_raises_value_error(self):
        with pytest.raises(ValueError, match="test must not be empty"):
            _validate_non_empty_string("", "test")

    def test_whitespace_only_raises_value_error(self):
        with pytest.raises(ValueError, match="test must not be empty"):
            _validate_non_empty_string("   ", "test")

    def test_tabs_only_raises_value_error(self):
        with pytest.raises(ValueError, match="must not be empty"):
            _validate_non_empty_string("\t\t", "test")

    def test_none_raises_type_error(self):
        with pytest.raises(TypeError, match="must be a string"):
            _validate_non_empty_string(None, "test")  # type: ignore[arg-type]

    def test_list_raises_type_error(self):
        with pytest.raises(TypeError, match="must be a string"):
            _validate_non_empty_string(["text"], "test")  # type: ignore[arg-type]

    def test_error_includes_field_name(self):
        with pytest.raises(TypeError, match="my_field"):
            _validate_non_empty_string(42, "my_field")  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# verify_commitment — validation edge cases
# ---------------------------------------------------------------------------

class TestVerifyCommitmentValidation:
    def test_empty_claim_details_raises(self):
        with pytest.raises(ValueError, match="claim_details"):
            verify_commitment(
                claim_details="",
                timestamp="2026-01-01",
                nonce="aa" * 32,
                public_key_hex="bb" * 32,
                expected_hash="cc" * 32,
            )

    def test_empty_timestamp_raises(self):
        with pytest.raises(ValueError, match="timestamp"):
            verify_commitment(
                claim_details="test",
                timestamp="",
                nonce="aa" * 32,
                public_key_hex="bb" * 32,
                expected_hash="cc" * 32,
            )

    def test_invalid_nonce_raises(self):
        with pytest.raises(ValueError, match="nonce"):
            verify_commitment(
                claim_details="test",
                timestamp="2026-01-01",
                nonce="not-hex",
                public_key_hex="bb" * 32,
                expected_hash="cc" * 32,
            )

    def test_invalid_public_key_raises(self):
        with pytest.raises(ValueError, match="public_key_hex"):
            verify_commitment(
                claim_details="test",
                timestamp="2026-01-01",
                nonce="aa" * 32,
                public_key_hex="short",
                expected_hash="cc" * 32,
            )

    def test_invalid_expected_hash_raises(self):
        with pytest.raises(ValueError, match="expected_hash"):
            verify_commitment(
                claim_details="test",
                timestamp="2026-01-01",
                nonce="aa" * 32,
                public_key_hex="bb" * 32,
                expected_hash="not-hex",
            )

    def test_non_string_claim_details_raises(self):
        with pytest.raises(TypeError, match="claim_details"):
            verify_commitment(
                claim_details=123,  # type: ignore[arg-type]
                timestamp="2026-01-01",
                nonce="aa" * 32,
                public_key_hex="bb" * 32,
                expected_hash="cc" * 32,
            )


# ---------------------------------------------------------------------------
# OnchainClaim — immutability
# ---------------------------------------------------------------------------

class TestOnchainClaimImmutability:
    def test_frozen_dataclass(self):
        claim = generate_onchain_claim(
            claim_details="Test",
            target_entity="Org",
            category="enforcement",
            private_key_hex=PRIVATE_KEY,
        )
        with pytest.raises(AttributeError):
            claim.commitment_hash = "tampered"  # type: ignore[misc]

    def test_frozen_signature(self):
        claim = generate_onchain_claim(
            claim_details="Test",
            target_entity="Org",
            category="enforcement",
            private_key_hex=PRIVATE_KEY,
        )
        with pytest.raises(AttributeError):
            claim.signature = "tampered"  # type: ignore[misc]


# ---------------------------------------------------------------------------
# VerificationResult — attributes
# ---------------------------------------------------------------------------

class TestVerificationResultAttributes:
    def test_valid_true_result(self):
        r = VerificationResult(valid=True, commitment_hash="aa" * 32, public_key="bb" * 32, details="ok")
        assert r.valid is True
        assert r.details == "ok"

    def test_valid_false_result(self):
        r = VerificationResult(valid=False, commitment_hash="aa" * 32, public_key="bb" * 32, details="bad")
        assert r.valid is False

    def test_frozen(self):
        r = VerificationResult(valid=True, commitment_hash="aa" * 32, public_key="bb" * 32, details="ok")
        with pytest.raises(AttributeError):
            r.valid = False  # type: ignore[misc]


# ---------------------------------------------------------------------------
# VALID_CATEGORIES
# ---------------------------------------------------------------------------

class TestValidCategories:
    def test_is_frozenset(self):
        assert isinstance(VALID_CATEGORIES, frozenset)

    def test_contains_expected_categories(self):
        expected = {"enforcement", "dispute", "oversight", "disclosure", "dao", "exchange"}
        assert VALID_CATEGORIES == expected

    def test_immutable(self):
        with pytest.raises(AttributeError):
            VALID_CATEGORIES.add("new")  # type: ignore[attr-defined]


# ---------------------------------------------------------------------------
# PyNaCl ImportError paths
# ---------------------------------------------------------------------------

class TestPyNaClImportError:
    """Verify friendly errors when PyNaCl is not installed."""

    def test_generate_raises_import_error_without_nacl(self):
        """generate_onchain_claim raises ImportError when nacl is unavailable."""
        import builtins

        real_import = builtins.__import__

        def block_nacl(name, *args, **kwargs):
            if "nacl" in name:
                raise ImportError("Mocked: no nacl")
            return real_import(name, *args, **kwargs)

        # Remove cached nacl modules so the lazy import fires again
        saved = {k: sys.modules.pop(k) for k in list(sys.modules) if k == "nacl" or k.startswith("nacl.")}
        try:
            with pytest.raises(ImportError, match="PyNaCl"):
                builtins.__import__ = block_nacl
                generate_onchain_claim(
                    claim_details="test",
                    target_entity="entity",
                    category="enforcement",
                    private_key_hex="aa" * 32,
                )
        finally:
            builtins.__import__ = real_import
            sys.modules.update(saved)

    def test_verify_raises_import_error_without_nacl(self):
        """verify_onchain_receipt raises ImportError when nacl is unavailable."""
        import builtins

        real_import = builtins.__import__

        def block_nacl(name, *args, **kwargs):
            if "nacl" in name:
                raise ImportError("Mocked: no nacl")
            return real_import(name, *args, **kwargs)

        saved = {k: sys.modules.pop(k) for k in list(sys.modules) if k == "nacl" or k.startswith("nacl.")}
        try:
            with pytest.raises(ImportError, match="PyNaCl"):
                builtins.__import__ = block_nacl
                verify_onchain_receipt(
                    commitment_hash="aa" * 32,
                    signature="bb" * 64,
                    public_key_hex="cc" * 32,
                )
        finally:
            builtins.__import__ = real_import
            sys.modules.update(saved)
