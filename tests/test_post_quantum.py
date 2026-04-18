"""Tests for real post-quantum (ML-DSA / SLH-DSA) signing paths.

These exercise the optional PQ branches of ``onchain_claims`` and
``iris.sovereign_profile`` end-to-end against the real ``pqcrypto``
package.  When ``pqcrypto`` is not installed the tests are skipped so the
core suite still runs in environments without the optional dependency.
"""

from __future__ import annotations

import os
import sys

import pytest

# Ensure the SDK is importable from the repo root.
sys.path.insert(
    0, os.path.join(os.path.dirname(__file__), "..", "onchain-protocol", "sdk")
)

pytest.importorskip("pqcrypto.sign.ml_dsa_65")

import onchain_claims  # noqa: E402

from onchain_claims import (  # noqa: E402
    PostQuantumProvider,
    _load_pqcrypto_provider,
    _normalise_algorithm_name,
    _resolve_post_quantum_provider,
    _select_first_string,
    build_signature_bundle,
    generate_onchain_claim,
    signature_mode_label,
    verify_onchain_receipt,
    verify_signature_bundle,
)

from iris import sovereign_profile  # noqa: E402
from iris.sovereign_profile import (  # noqa: E402
    build_personal_profile,
    setup_personal_profile,
    verify_personal_profile,
)


PRIVATE_KEY = "11" * 32
FIXED_TIMESTAMP = "2025-01-01T00:00:00Z"
FIXED_NONCE = "ab" * 32


@pytest.fixture(autouse=True)
def _clear_pq_provider_cache():
    """The PQ provider lookup is ``lru_cache``d; reset between tests."""
    _resolve_post_quantum_provider.cache_clear()
    yield
    _resolve_post_quantum_provider.cache_clear()


# ---------------------------------------------------------------------------
# _select_first_string + _normalise_algorithm_name (small private helpers
# used by the PQ resolution path)
# ---------------------------------------------------------------------------

class TestPrivateHelpers:
    def test_select_first_string_returns_first_non_empty(self):
        result = _select_first_string({"a": "", "b": "  hi  ", "c": "later"}, "a", "b", "c")
        assert result == "hi"

    def test_select_first_string_skips_none_values(self):
        result = _select_first_string({"a": None, "b": "value"}, "a", "b")
        assert result == "value"

    def test_select_first_string_returns_empty_when_no_match(self):
        assert _select_first_string({"a": "", "b": None}, "a", "b") == ""

    def test_select_first_string_handles_none_mapping(self):
        assert _select_first_string(None, "a", "b") == ""

    def test_normalise_algorithm_name_strips_punctuation_and_case(self):
        assert _normalise_algorithm_name("ML-DSA") == "mldsa"
        assert _normalise_algorithm_name("SLH_DSA-65") == "slhdsa65"
        assert _normalise_algorithm_name("") == ""


# ---------------------------------------------------------------------------
# _load_pqcrypto_provider
# ---------------------------------------------------------------------------

class TestLoadPqcryptoProvider:
    def test_returns_none_when_module_missing(self):
        assert (
            _load_pqcrypto_provider("ML-DSA", "definitely.not.a.real.module")
            is None
        )

    def test_returns_none_when_module_lacks_required_callables(self, monkeypatch):
        # Build a fake module that is importable but missing the API.
        import types

        fake = types.ModuleType("fake_pq_missing_api")
        fake.generate_keypair = "not callable"  # type: ignore[assignment]
        sys.modules["fake_pq_missing_api"] = fake
        try:
            assert _load_pqcrypto_provider("ML-DSA", "fake_pq_missing_api") is None
        finally:
            sys.modules.pop("fake_pq_missing_api", None)

    def test_loads_real_ml_dsa_module(self):
        provider = _load_pqcrypto_provider("ML-DSA", "pqcrypto.sign.ml_dsa_65")
        assert isinstance(provider, PostQuantumProvider)
        assert provider.algorithm == "ML-DSA"
        assert provider.module_name == "pqcrypto.sign.ml_dsa_65"

    def test_loaded_provider_round_trips(self):
        provider = _load_pqcrypto_provider("ML-DSA", "pqcrypto.sign.ml_dsa_65")
        assert provider is not None

        private_key, public_key = provider.generate_keypair()
        assert isinstance(private_key, bytes) and len(private_key) > 0
        assert isinstance(public_key, bytes) and len(public_key) > 0

        message = b"hybrid signing roundtrip"
        signature = provider.sign(private_key, message)
        assert isinstance(signature, bytes) and len(signature) > 0

        assert provider.verify(public_key, message, signature) is True
        # Wrong message fails verification.
        assert provider.verify(public_key, b"different", signature) is False

    def test_loaded_provider_verify_returns_false_on_exception(self):
        provider = _load_pqcrypto_provider("ML-DSA", "pqcrypto.sign.ml_dsa_65")
        assert provider is not None
        # Garbage public key triggers an exception inside the wrapper, which
        # the adapter must swallow and return False for.
        assert provider.verify(b"\x00" * 4, b"msg", b"\x00" * 4) is False


# ---------------------------------------------------------------------------
# _resolve_post_quantum_provider
# ---------------------------------------------------------------------------

class TestResolvePostQuantumProvider:
    def test_default_resolution_returns_ml_dsa(self):
        provider = _resolve_post_quantum_provider()
        assert provider.algorithm == "ML-DSA"

    def test_algorithm_hint_for_slh_dsa_prefers_sphincs(self):
        provider = _resolve_post_quantum_provider("SLH-DSA")
        assert provider.algorithm == "SLH-DSA"

    def test_algorithm_hint_with_sphincs_alias(self):
        # Hints starting with "sphincs" reorder the candidate groups even
        # though the providers themselves still report the bucket name
        # "SLH-DSA".
        provider = _resolve_post_quantum_provider("slh-dsa")
        assert provider.algorithm == "SLH-DSA"

    def test_unknown_hint_raises_when_no_provider_matches(self):
        # An unrecognised hint is normalised and compared against every
        # candidate provider's algorithm name; if nothing matches the
        # resolver raises ImportError.
        with pytest.raises(ImportError):
            _resolve_post_quantum_provider("rainbow-bird-9000")

    def test_raises_when_no_provider_available(self, monkeypatch):
        monkeypatch.setattr(
            onchain_claims, "_load_pqcrypto_provider", lambda *args, **kwargs: None
        )
        _resolve_post_quantum_provider.cache_clear()
        with pytest.raises(ImportError, match="Post-quantum signing was requested"):
            _resolve_post_quantum_provider()


# ---------------------------------------------------------------------------
# signature_mode_label
# ---------------------------------------------------------------------------

class TestSignatureModeLabel:
    def test_classical_label(self):
        assert signature_mode_label() == "Classical (Ed25519)"
        assert signature_mode_label(post_quantum=False) == "Classical (Ed25519)"

    def test_post_quantum_label_with_real_provider(self):
        label = signature_mode_label(post_quantum=True)
        assert label.startswith("Hybrid (Ed25519 + ")
        assert "ML-DSA" in label or "SLH-DSA" in label

    def test_post_quantum_label_raises_when_provider_missing(self, monkeypatch):
        monkeypatch.setattr(
            onchain_claims, "_load_pqcrypto_provider", lambda *args, **kwargs: None
        )
        _resolve_post_quantum_provider.cache_clear()
        with pytest.raises(ImportError):
            signature_mode_label(post_quantum=True)


# ---------------------------------------------------------------------------
# build_signature_bundle / verify_signature_bundle round-trip with real PQ
# ---------------------------------------------------------------------------

class TestRealHybridRoundtrip:
    def test_generated_key_roundtrip(self):
        message = b"on-chain commitment payload"
        bundle = build_signature_bundle(
            message,
            PRIVATE_KEY,
            post_quantum=True,
        )
        assert bundle["signature_mode"] == "hybrid"
        assert bundle["post_quantum_algorithm"] in {"ML-DSA", "SLH-DSA"}
        algo_key = bundle["post_quantum_algorithm"].lower()
        assert algo_key in bundle["signatures"]
        assert algo_key in bundle["public_keys"]
        assert bundle["generated_post_quantum_private_key_hex"]

        result = verify_signature_bundle(
            message,
            bundle["signature"],
            bundle["public_keys"]["ed25519"],
            signatures=bundle["signatures"],
            public_keys=bundle["public_keys"],
        )
        assert result.valid is True
        assert result.signature_mode == "hybrid"

    def test_supplied_private_key_with_derived_public_key(self):
        # First call generates and exposes the PQ private key.
        message = b"second roundtrip"
        bootstrap = build_signature_bundle(message, PRIVATE_KEY, post_quantum=True)
        pq_private_hex = bootstrap["generated_post_quantum_private_key_hex"]
        assert pq_private_hex

        algo_key = bootstrap["post_quantum_algorithm"].lower()
        pq_public_hex = bootstrap["public_keys"][algo_key]

        # Re-sign supplying the stored PQ private key + matching public key.
        bundle = build_signature_bundle(
            message,
            PRIVATE_KEY,
            post_quantum=True,
            post_quantum_private_key_hex=pq_private_hex,
            post_quantum_public_key_hex=pq_public_hex,
        )
        # When a private key is supplied, the helper does not regenerate one.
        assert bundle["generated_post_quantum_private_key_hex"] == ""
        assert bundle["public_keys"][algo_key] == pq_public_hex

        result = verify_signature_bundle(
            message,
            bundle["signature"],
            bundle["public_keys"]["ed25519"],
            signatures=bundle["signatures"],
            public_keys=bundle["public_keys"],
        )
        assert result.valid is True

    def test_supplied_private_key_without_public_key_raises(self, monkeypatch):
        # Force the resolved provider to lack ``derive_public_key``.
        provider = _resolve_post_quantum_provider()
        stripped = PostQuantumProvider(
            algorithm=provider.algorithm,
            module_name=provider.module_name,
            generate_keypair=provider.generate_keypair,
            sign=provider.sign,
            verify=provider.verify,
            derive_public_key=None,
        )
        monkeypatch.setattr(
            onchain_claims, "_resolve_post_quantum_provider", lambda hint=None: stripped
        )
        # Use any valid hex blob as a stand-in private key — the call must
        # fail before the key is actually used.
        with pytest.raises(ValueError, match="post_quantum_public_key_hex must be supplied"):
            build_signature_bundle(
                b"msg",
                PRIVATE_KEY,
                post_quantum=True,
                post_quantum_private_key_hex="ab" * 32,
            )

    def test_supplied_private_key_uses_derive_public_key_when_available(self, monkeypatch):
        # Build a provider that exposes ``derive_public_key`` so the
        # corresponding branch in build_signature_bundle is exercised.
        base = _resolve_post_quantum_provider()
        captured = {}

        def _generate():
            private_key, public_key = base.generate_keypair()
            captured["private"] = private_key
            captured["public"] = public_key
            return private_key, public_key

        def _derive(private_key):
            # Only valid for the keypair we just generated; sufficient for
            # the test because the same private key is fed back in below.
            assert private_key == captured["private"]
            return captured["public"]

        with_derive = PostQuantumProvider(
            algorithm=base.algorithm,
            module_name=base.module_name,
            generate_keypair=_generate,
            sign=base.sign,
            verify=base.verify,
            derive_public_key=_derive,
        )
        monkeypatch.setattr(
            onchain_claims,
            "_resolve_post_quantum_provider",
            lambda hint=None: with_derive,
        )

        # First call uses ``generate_keypair`` and exposes the private key.
        bootstrap = build_signature_bundle(b"msg", PRIVATE_KEY, post_quantum=True)
        pq_private_hex = bootstrap["generated_post_quantum_private_key_hex"]
        assert pq_private_hex

        # Second call supplies the private key without a public key — the
        # ``derive_public_key`` branch (lines 349-350) must populate it.
        bundle = build_signature_bundle(
            b"msg",
            PRIVATE_KEY,
            post_quantum=True,
            post_quantum_private_key_hex=pq_private_hex,
        )
        algo_key = bundle["post_quantum_algorithm"].lower()
        assert bundle["public_keys"][algo_key] == captured["public"].hex()

    def test_verify_rejects_hybrid_receipt_missing_pq_public_key(self):
        message = b"missing public key path"
        bundle = build_signature_bundle(message, PRIVATE_KEY, post_quantum=True)
        algo_key = bundle["post_quantum_algorithm"].lower()

        # Drop the PQ public key from the receipt to trigger the missing-key
        # branch in verify_signature_bundle (line 416).
        public_keys = {k: v for k, v in bundle["public_keys"].items() if k != algo_key}
        result = verify_signature_bundle(
            message,
            bundle["signature"],
            bundle["public_keys"]["ed25519"],
            signatures=bundle["signatures"],
            public_keys=public_keys,
        )
        assert result.valid is False
        assert result.signature_mode == "hybrid"
        assert "public key missing" in result.details

    def test_verify_rejects_hybrid_receipt_with_bad_pq_signature(self):
        message = b"bad pq signature path"
        bundle = build_signature_bundle(message, PRIVATE_KEY, post_quantum=True)
        algo_key = bundle["post_quantum_algorithm"].lower()

        # Replace the PQ signature with an obviously wrong (but well-formed
        # hex) value so provider.verify returns False (line 431).
        bad_sigs = dict(bundle["signatures"])
        original = bad_sigs[algo_key]
        bad_sigs[algo_key] = "00" * (len(original) // 2)

        result = verify_signature_bundle(
            message,
            bundle["signature"],
            bundle["public_keys"]["ed25519"],
            signatures=bad_sigs,
            public_keys=bundle["public_keys"],
        )
        assert result.valid is False
        assert result.signature_mode == "hybrid"
        assert "verification failed" in result.details.lower()


# ---------------------------------------------------------------------------
# generate_onchain_claim + verify_onchain_receipt — full hybrid roundtrip
# ---------------------------------------------------------------------------

class TestRealHybridClaimRoundtrip:
    def test_full_hybrid_claim_verifies(self):
        claim = generate_onchain_claim(
            claim_details="My case was not reviewed by a human",
            target_entity="Example Council",
            category="enforcement",
            private_key_hex=PRIVATE_KEY,
            timestamp=FIXED_TIMESTAMP,
            nonce=FIXED_NONCE,
            post_quantum=True,
        )
        assert claim.signature_mode == "hybrid"
        assert claim.post_quantum_algorithm in {"ML-DSA", "SLH-DSA"}

        # to_json should round-trip through json.loads and include hybrid metadata.
        import json as _json

        payload = _json.loads(claim.to_json())
        assert payload["signatureMode"] == "hybrid"
        assert payload["postQuantumAlgorithm"] == claim.post_quantum_algorithm
        assert "signatures" in payload and "publicKeys" in payload

        result = verify_onchain_receipt(
            commitment_hash=claim.commitment_hash,
            signature=claim.signature,
            public_key_hex=claim.public_key,
            signatures=claim.signatures,
            public_keys=claim.public_keys,
        )
        assert result.valid is True
        assert result.signature_mode == "hybrid"


# ---------------------------------------------------------------------------
# iris.sovereign_profile hybrid paths (real PQ)
# ---------------------------------------------------------------------------

class TestSovereignProfileHybridReal:
    def test_build_personal_profile_hybrid_real_roundtrip(self):
        profile = build_personal_profile(name="Alex", post_quantum=True)
        assert profile["signature_mode"] == "hybrid"
        assert profile["post_quantum_algorithm"] in {"ML-DSA", "SLH-DSA"}
        # The generated PQ private key should have been captured.
        assert profile["post_quantum_private_key_hex"]
        assert verify_personal_profile(profile) is True

    def test_apply_profile_signatures_uses_supplied_private_key(self):
        # First create a profile to obtain real PQ key material.
        baseline = build_personal_profile(name="Alex", post_quantum=True)
        pq_private_hex = baseline["post_quantum_private_key_hex"]
        pq_public_hex = baseline["post_quantum_public_key_hex"]
        assert pq_private_hex and pq_public_hex

        # Now build a fresh profile, supplying the existing PQ keys.  This
        # exercises the ``elif post_quantum_private_key_hex`` branch in
        # ``_apply_profile_signatures`` (lines 191-192).
        profile = build_personal_profile(
            name="Alex",
            post_quantum=True,
            post_quantum_private_key_hex=pq_private_hex,
            post_quantum_public_key_hex=pq_public_hex,
        )
        assert profile["post_quantum_private_key_hex"] == pq_private_hex
        assert profile["post_quantum_public_key_hex"] == pq_public_hex
        assert verify_personal_profile(profile) is True

    def test_setup_personal_profile_can_toggle_post_quantum(self, tmp_path):
        # Create a classical profile first.
        setup_personal_profile(
            vault_passphrase="correct horse battery staple",
            root=tmp_path,
            name="Alex",
        )

        # Toggle PQ on for the existing profile — exercises lines 418-427 of
        # iris/sovereign_profile.py (the ``post_quantum is not None`` branch
        # of ``setup_personal_profile``).
        result = setup_personal_profile(
            vault_passphrase="correct horse battery staple",
            root=tmp_path,
            post_quantum=True,
        )
        assert result["created"] is False
        summary = result["profile"]
        assert summary["signature_mode"] == "hybrid"
        assert summary["post_quantum_algorithm"] in {"ML-DSA", "SLH-DSA"}
        assert summary["post_quantum_public_key_hex"]

        # The persisted record should still verify after the toggle.
        from iris.sovereign_profile import load_personal_profile

        loaded = load_personal_profile(
            "correct horse battery staple", root=tmp_path
        )
        assert loaded["signature_mode"] == "hybrid"
        assert verify_personal_profile(loaded) is True
