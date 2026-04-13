"""Burgess Claims Protocol — Python SDK.

Provides off-chain claim generation, commitment hashing, Ed25519 signing,
and verification utilities.  On-chain interaction helpers are included for
posting claims to an EVM-compatible chain via web3.py (optional dependency).

Usage::

    # From the repository root:
    #   cd onchain-protocol/sdk
    #   python
    from onchain_claims import generate_onchain_claim, verify_onchain_receipt

    claim = generate_onchain_claim(
        claim_details="My case was not reviewed by a human",
        target_entity="Example Council",
        category="enforcement",
        private_key_hex="<ed25519-private-key-hex>",
    )

    result = verify_onchain_receipt(
        commitment_hash=claim.commitment_hash,
        signature=claim.signature,
        public_key_hex=claim.public_key,
    )
    assert result.valid
"""

from __future__ import annotations

import hashlib
import importlib
import json
import os
from dataclasses import dataclass, field
from datetime import datetime, timezone
from functools import lru_cache
from typing import Any, Callable, Mapping


# ---------------------------------------------------------------------------
# Result types
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class OnchainClaim:
    """A Burgess Claim prepared for on-chain posting."""

    commitment_hash: str
    signature: str
    public_key: str
    target_entity: str
    category: str
    timestamp: str
    nonce: str
    signature_mode: str = "classical"
    signatures: dict[str, str] = field(default_factory=dict)
    public_keys: dict[str, str] = field(default_factory=dict)
    post_quantum_algorithm: str = ""
    generated_post_quantum_private_key_hex: str = ""

    def to_json(self) -> str:
        """Compact JSON suitable for on-chain posting scripts."""
        payload = {
            "commitmentHash": self.commitment_hash,
            "signature": self.signature,
            "publicKey": self.public_key,
            "target": self.target_entity,
            "category": self.category,
            "timestamp": self.timestamp,
            "nonce": self.nonce,
        }
        if self.signature_mode != "classical":
            payload["signatureMode"] = self.signature_mode
            payload["signatures"] = dict(self.signatures)
            payload["publicKeys"] = dict(self.public_keys)
            payload["postQuantumAlgorithm"] = self.post_quantum_algorithm
        return json.dumps(payload, separators=(",", ":"), sort_keys=True)

    def to_dict(self) -> dict[str, str]:
        """Plain dictionary representation."""
        payload = {
            "commitment_hash": self.commitment_hash,
            "signature": self.signature,
            "public_key": self.public_key,
            "target_entity": self.target_entity,
            "category": self.category,
            "timestamp": self.timestamp,
            "nonce": self.nonce,
        }
        if self.signature_mode != "classical":
            payload["signature_mode"] = self.signature_mode
            payload["signatures"] = dict(self.signatures)
            payload["public_keys"] = dict(self.public_keys)
            payload["post_quantum_algorithm"] = self.post_quantum_algorithm
        if self.generated_post_quantum_private_key_hex:
            payload["generated_post_quantum_private_key_hex"] = (
                self.generated_post_quantum_private_key_hex
            )
        return payload


@dataclass(frozen=True)
class VerificationResult:
    """Result of verifying an on-chain claim receipt."""

    valid: bool
    commitment_hash: str
    public_key: str
    details: str
    signature_mode: str = "classical"


@dataclass(frozen=True)
class PostQuantumProvider:
    """Optional post-quantum signing backend."""

    algorithm: str
    module_name: str
    generate_keypair: Callable[[], tuple[bytes, bytes]]
    sign: Callable[[bytes, bytes], bytes]
    verify: Callable[[bytes, bytes, bytes], bool]
    derive_public_key: Callable[[bytes], bytes] | None = None


# ---------------------------------------------------------------------------
# Allowed categories
# ---------------------------------------------------------------------------

VALID_CATEGORIES: frozenset[str] = frozenset(
    {
        "enforcement",
        "dispute",
        "oversight",
        "disclosure",
        "dao",
        "exchange",
    }
)

_ML_DSA_MODULES = (
    ("ML-DSA", "pqcrypto.sign.ml_dsa_65"),
    ("ML-DSA", "pqcrypto.sign.ml_dsa_87"),
    ("ML-DSA", "pqcrypto.sign.dilithium3"),
    ("ML-DSA", "pqcrypto.sign.dilithium5"),
)
_SLH_DSA_MODULES = (
    ("SLH-DSA", "pqcrypto.sign.sphincs_shake_256f_simple"),
    ("SLH-DSA", "pqcrypto.sign.sphincs_sha2_256f_simple"),
)
_PQ_PROVIDER_CACHE_SIZE = 3


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _compute_commitment(
    claim_details: str,
    timestamp: str,
    nonce: str,
    public_key_hex: str,
) -> str:
    """Compute a SHA-256 commitment over the canonical claim JSON payload."""
    canonical_json = _canonical_claim_json(
        claim_details,
        timestamp,
        nonce,
        public_key_hex,
    )
    return hashlib.sha256(canonical_json.encode("utf-8")).hexdigest()


def _compute_legacy_commitment(
    claim_details: str,
    timestamp: str,
    nonce: str,
    public_key_hex: str,
) -> str:
    """Compute the original concatenation-based commitment for legacy receipts."""
    preimage = claim_details + timestamp + nonce + public_key_hex
    return hashlib.sha256(preimage.encode("utf-8")).hexdigest()


def _canonical_claim_json(
    claim_details: str,
    timestamp: str,
    nonce: str,
    public_key_hex: str,
) -> str:
    """Canonical sorted-key JSON for deterministic hashing."""
    return json.dumps(
        {
            "claim_details": claim_details,
            "nonce": nonce,
            "public_key": public_key_hex,
            "timestamp": timestamp,
        },
        separators=(",", ":"),
        sort_keys=True,
    )


def _select_first_string(values: Mapping[str, Any] | None, *keys: str) -> str:
    for key in keys:
        if values is None:
            break
        value = values.get(key)
        if value not in (None, ""):
            return str(value).strip()
    return ""


def _normalise_algorithm_name(value: str) -> str:
    return "".join(ch for ch in str(value).lower() if ch.isalnum())


def _load_pqcrypto_provider(
    algorithm: str,
    module_name: str,
) -> PostQuantumProvider | None:
    try:
        module = importlib.import_module(module_name)
    except ImportError:
        return None

    generate_keypair = getattr(module, "generate_keypair", None)
    sign = getattr(module, "sign", None)
    verify = getattr(module, "verify", None)
    if not all(callable(func) for func in (generate_keypair, sign, verify)):
        return None

    def _generate() -> tuple[bytes, bytes]:
        public_key, private_key = generate_keypair()
        return bytes(private_key), bytes(public_key)

    def _sign(private_key: bytes, message: bytes) -> bytes:
        return bytes(sign(private_key, message))

    def _verify(public_key: bytes, message: bytes, signature: bytes) -> bool:
        try:
            result = verify(public_key, message, signature)
        except Exception:
            return False
        return True if result is None else bool(result)

    return PostQuantumProvider(
        algorithm=algorithm,
        module_name=module_name,
        generate_keypair=_generate,
        sign=_sign,
        verify=_verify,
    )


@lru_cache(maxsize=_PQ_PROVIDER_CACHE_SIZE)
def _resolve_post_quantum_provider(expected_algorithm: str | None = None) -> PostQuantumProvider:
    candidates = (_ML_DSA_MODULES, _SLH_DSA_MODULES)
    expected = _normalise_algorithm_name(expected_algorithm or "")
    if expected.startswith("slhdsa") or expected.startswith("sphincs"):
        candidates = (_SLH_DSA_MODULES, _ML_DSA_MODULES)
    for group in candidates:
        for algorithm, module_name in group:
            provider = _load_pqcrypto_provider(algorithm, module_name)
            if provider is None:
                continue
            if expected and _normalise_algorithm_name(provider.algorithm) != expected:
                continue
            return provider
    raise ImportError(
        "Post-quantum signing was requested but no optional ML-DSA or SLH-DSA "
        "provider was found. Install a lightweight wrapper such as pqcrypto or "
        "another pure-Python ML-DSA / SLH-DSA implementation."
    )


def signature_mode_label(post_quantum: bool = False) -> str:
    """Return the visible signature mode label for banners and receipts."""
    if not post_quantum:
        return "Classical (Ed25519)"
    provider = _resolve_post_quantum_provider()
    return f"Hybrid (Ed25519 + {provider.algorithm})"


def _ed25519_public_key_hex(ed25519_private_key_hex: str) -> str:
    try:
        from nacl.signing import SigningKey
    except ImportError:
        raise ImportError(
            "The 'PyNaCl' package is required for Ed25519 signing. "
            "Install it with:  pip install PyNaCl"
        ) from None

    _validate_hex_string(ed25519_private_key_hex, "ed25519_private_key_hex", expected_length=64)
    return SigningKey(bytes.fromhex(ed25519_private_key_hex)).verify_key.encode().hex()


# Hybrid signature note:
# - SHA-256 commitments and the legacy Ed25519 receipt fields stay unchanged so
#   existing sovereign records continue to verify exactly as before.
# - When post_quantum=True we add a second signature with ML-DSA when available,
#   or SLH-DSA as the conservative fallback, so long-term scrutiny can require
#   both the classical and PQ proof without changing the offline commitment flow.
def build_signature_bundle(
    message: bytes,
    ed25519_private_key_hex: str,
    *,
    post_quantum: bool = False,
    post_quantum_private_key_hex: str | None = None,
    post_quantum_public_key_hex: str | None = None,
) -> dict[str, Any]:
    """Sign a payload with Ed25519 and optionally a post-quantum companion."""
    try:
        from nacl.signing import SigningKey
    except ImportError:
        raise ImportError(
            "The 'PyNaCl' package is required for Ed25519 signing. "
            "Install it with:  pip install PyNaCl"
        ) from None

    _validate_hex_string(ed25519_private_key_hex, "ed25519_private_key_hex", expected_length=64)
    signing_key = SigningKey(bytes.fromhex(ed25519_private_key_hex))
    signature_hex = signing_key.sign(message).signature.hex()
    public_key_hex = signing_key.verify_key.encode().hex()
    bundle: dict[str, Any] = {
        "signature": signature_hex,
        "public_key": public_key_hex,
        "signature_mode": "classical",
        "signatures": {},
        "public_keys": {},
        "post_quantum_algorithm": "",
        "generated_post_quantum_private_key_hex": "",
    }
    if not post_quantum:
        return bundle

    provider = _resolve_post_quantum_provider()
    private_key_hex = str(post_quantum_private_key_hex or "").strip()
    public_key_override = str(post_quantum_public_key_hex or "").strip()
    if private_key_hex:
        _validate_hex_string(private_key_hex, "post_quantum_private_key_hex")
        private_key = bytes.fromhex(private_key_hex)
        if public_key_override:
            _validate_hex_string(public_key_override, "post_quantum_public_key_hex")
            pq_public_key = bytes.fromhex(public_key_override)
        elif provider.derive_public_key is not None:
            pq_public_key = provider.derive_public_key(private_key)
            public_key_override = pq_public_key.hex()
        else:
            raise ValueError(
                "post_quantum_public_key_hex must be supplied when using a stored "
                "post-quantum private key with this provider."
            )
    else:
        private_key, pq_public_key = provider.generate_keypair()
        private_key_hex = private_key.hex()
        public_key_override = pq_public_key.hex()
        bundle["generated_post_quantum_private_key_hex"] = private_key_hex

    pq_signature_hex = provider.sign(private_key, message).hex()
    algorithm_key = provider.algorithm.lower()
    bundle["signature_mode"] = "hybrid"
    bundle["signatures"] = {
        "ed25519": signature_hex,
        algorithm_key: pq_signature_hex,
    }
    bundle["public_keys"] = {
        "ed25519": public_key_hex,
        algorithm_key: public_key_override,
    }
    bundle["post_quantum_algorithm"] = provider.algorithm
    return bundle


def verify_signature_bundle(
    message: bytes,
    signature: str,
    public_key_hex: str,
    *,
    signatures: Mapping[str, str] | None = None,
    public_keys: Mapping[str, str] | None = None,
) -> VerificationResult:
    """Verify a classical signature and, when present, its PQ companion."""
    try:
        from nacl.exceptions import BadSignatureError
        from nacl.signing import VerifyKey
    except ImportError:
        raise ImportError(
            "The 'PyNaCl' package is required for Ed25519 verification. "
            "Install it with:  pip install PyNaCl"
        ) from None

    _validate_hex_string(signature, "signature", expected_length=128)
    _validate_hex_string(public_key_hex, "public_key_hex", expected_length=64)

    try:
        verify_key = VerifyKey(bytes.fromhex(public_key_hex))
        verify_key.verify(message, bytes.fromhex(signature))
    except BadSignatureError:
        return VerificationResult(
            valid=False,
            commitment_hash=message.hex(),
            public_key=public_key_hex,
            details="Signature verification failed — claim may be tampered.",
        )

    signature_map = dict(signatures or {})
    public_key_map = dict(public_keys or {})
    for algorithm, pq_signature in signature_map.items():
        if _normalise_algorithm_name(algorithm) == "ed25519":
            continue
        pq_public_key = public_key_map.get(algorithm) or public_key_map.get(algorithm.lower())
        if not pq_public_key:
            return VerificationResult(
                valid=False,
                commitment_hash=message.hex(),
                public_key=public_key_hex,
                details=f"{algorithm} public key missing from hybrid receipt.",
                signature_mode="hybrid",
            )
        _validate_hex_string(pq_signature, f"{algorithm} signature")
        _validate_hex_string(pq_public_key, f"{algorithm} public key")
        provider = _resolve_post_quantum_provider(algorithm)
        if not provider.verify(
            bytes.fromhex(pq_public_key),
            message,
            bytes.fromhex(pq_signature),
        ):
            return VerificationResult(
                valid=False,
                commitment_hash=message.hex(),
                public_key=public_key_hex,
                details=f"{provider.algorithm} verification failed — hybrid receipt is invalid.",
                signature_mode="hybrid",
            )
        return VerificationResult(
            valid=True,
            commitment_hash=message.hex(),
            public_key=public_key_hex,
            details=(
                f"Hybrid signature verified — Ed25519 and {provider.algorithm} proofs are valid."
            ),
            signature_mode="hybrid",
        )

    return VerificationResult(
        valid=True,
        commitment_hash=message.hex(),
        public_key=public_key_hex,
        details="Signature verified — claim is authentic.",
    )


# ---------------------------------------------------------------------------
# Input validation
# ---------------------------------------------------------------------------

def _validate_hex_string(value: str, name: str, expected_length: int | None = None) -> None:
    """Validate that a value is a non-empty hex string of the expected length."""
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a string, got {type(value).__name__}")
    if not value:
        raise ValueError(f"{name} must not be empty")
    try:
        bytes.fromhex(value)
    except ValueError:
        raise ValueError(f"{name} must be a valid hexadecimal string") from None
    if expected_length is not None and len(value) != expected_length:
        raise ValueError(
            f"{name} must be exactly {expected_length} hex characters, got {len(value)}"
        )


def _validate_non_empty_string(value: str, name: str) -> None:
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a string, got {type(value).__name__}")
    if not value.strip():
        raise ValueError(f"{name} must not be empty")


# ---------------------------------------------------------------------------
# Core API
# ---------------------------------------------------------------------------

def generate_onchain_claim(
    claim_details: str,
    target_entity: str,
    category: str,
    private_key_hex: str,
    *,
    timestamp: str | None = None,
    nonce: str | None = None,
    post_quantum: bool = False,
    post_quantum_private_key_hex: str | None = None,
    post_quantum_public_key_hex: str | None = None,
) -> OnchainClaim:
    """Generate a Burgess Claim ready for on-chain posting.

    Parameters
    ----------
    claim_details:
        Free-text description of the claim.
    target_entity:
        The institution or system being addressed.
    category:
        Claim category — must be one of the values in ``VALID_CATEGORIES``.
    private_key_hex:
        Ed25519 private key as a 64-character hex string (32 bytes).
    timestamp:
        ISO 8601 timestamp.  Defaults to the current UTC time.
    nonce:
        Random nonce as a 64-character hex string (32 bytes).
        Defaults to a cryptographically random value.

    Returns
    -------
    OnchainClaim
        The claim with commitment hash, signature, and metadata.

    Raises
    ------
    ImportError
        If the ``nacl`` (PyNaCl) library is not installed.
    TypeError
        If any argument is not a string.
    ValueError
        If any argument fails validation.
    """
    # --- Validate inputs ---
    _validate_non_empty_string(claim_details, "claim_details")
    _validate_non_empty_string(target_entity, "target_entity")
    _validate_non_empty_string(category, "category")
    if category not in VALID_CATEGORIES:
        raise ValueError(
            f"category must be one of {sorted(VALID_CATEGORIES)}, got {category!r}"
        )
    _validate_hex_string(private_key_hex, "private_key_hex", expected_length=64)

    # --- Defaults ---
    if timestamp is None:
        timestamp = datetime.now(timezone.utc).isoformat()
    if nonce is None:
        nonce = os.urandom(32).hex()

    _validate_hex_string(nonce, "nonce", expected_length=64)

    public_key_hex = _ed25519_public_key_hex(private_key_hex)

    # --- Compute commitment ---
    commitment_hash = _compute_commitment(
        claim_details, timestamp, nonce, public_key_hex
    )

    signature_bundle = build_signature_bundle(
        bytes.fromhex(commitment_hash),
        private_key_hex,
        post_quantum=post_quantum,
        post_quantum_private_key_hex=post_quantum_private_key_hex,
        post_quantum_public_key_hex=post_quantum_public_key_hex,
    )

    return OnchainClaim(
        commitment_hash=commitment_hash,
        signature=signature_bundle["signature"],
        public_key=signature_bundle["public_key"],
        target_entity=target_entity,
        category=category,
        timestamp=timestamp,
        nonce=nonce,
        signature_mode=signature_bundle["signature_mode"],
        signatures=signature_bundle["signatures"],
        public_keys=signature_bundle["public_keys"],
        post_quantum_algorithm=signature_bundle["post_quantum_algorithm"],
        generated_post_quantum_private_key_hex=signature_bundle[
            "generated_post_quantum_private_key_hex"
        ],
    )


def verify_onchain_receipt(
    commitment_hash: str,
    signature: str,
    public_key_hex: str,
    *,
    signatures: Mapping[str, str] | None = None,
    public_keys: Mapping[str, str] | None = None,
) -> VerificationResult:
    """Verify an on-chain Burgess Claim receipt.

    Checks that the Ed25519 ``signature`` over ``commitment_hash`` is
    valid for the given ``public_key_hex``.

    Parameters
    ----------
    commitment_hash:
        The SHA-256 commitment hash (64 hex chars).
    signature:
        The Ed25519 signature (128 hex chars / 64 bytes).
    public_key_hex:
        The claimant's Ed25519 public key (64 hex chars / 32 bytes).

    Returns
    -------
    VerificationResult
        Contains ``valid=True`` if the signature checks out.
    """
    _validate_hex_string(commitment_hash, "commitment_hash", expected_length=64)
    result = verify_signature_bundle(
        bytes.fromhex(commitment_hash),
        signature,
        public_key_hex,
        signatures=signatures,
        public_keys=public_keys,
    )
    return VerificationResult(
        valid=result.valid,
        commitment_hash=commitment_hash,
        public_key=public_key_hex,
        details=result.details,
        signature_mode=result.signature_mode,
    )


def verify_commitment(
    claim_details: str,
    timestamp: str,
    nonce: str,
    public_key_hex: str,
    expected_hash: str,
) -> bool:
    """Re-compute a commitment hash and compare with the expected value.

    This is used for selective disclosure: the claimant reveals the
    pre-image fields and the verifier checks that they produce the
    commitment hash stored on-chain.

    New claims use canonical sorted-key JSON before hashing. For
    backwards compatibility, verification also accepts the original
    concatenation-based preimage format used by early draft claims.

    Returns ``True`` if the hashes match, ``False`` otherwise.
    """
    _validate_non_empty_string(claim_details, "claim_details")
    _validate_non_empty_string(timestamp, "timestamp")
    _validate_hex_string(nonce, "nonce", expected_length=64)
    _validate_hex_string(public_key_hex, "public_key_hex", expected_length=64)
    _validate_hex_string(expected_hash, "expected_hash", expected_length=64)

    computed = _compute_commitment(claim_details, timestamp, nonce, public_key_hex)
    # Constant-time comparison to prevent timing attacks.
    import hmac as _hmac

    normalized_expected_hash = expected_hash.lower()
    if _hmac.compare_digest(
        computed,
        normalized_expected_hash,
    ):
        return True

    legacy = _compute_legacy_commitment(
        claim_details,
        timestamp,
        nonce,
        public_key_hex,
    )
    return _hmac.compare_digest(legacy, normalized_expected_hash)
