"""Burgess Claims Protocol — Python SDK.

Provides off-chain claim generation, commitment hashing, Ed25519 signing,
and verification utilities.  On-chain interaction helpers are included for
posting claims to an EVM-compatible chain via web3.py (optional dependency).

Usage::

    from onchain_protocol.sdk.onchain_claims import (
        generate_onchain_claim,
        verify_onchain_receipt,
    )

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
import json
import os
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


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

    def to_json(self) -> str:
        """Compact JSON suitable for on-chain posting scripts."""
        return json.dumps(
            {
                "commitmentHash": self.commitment_hash,
                "signature": self.signature,
                "publicKey": self.public_key,
                "target": self.target_entity,
                "category": self.category,
                "timestamp": self.timestamp,
                "nonce": self.nonce,
            },
            separators=(",", ":"),
            sort_keys=True,
        )

    def to_dict(self) -> dict[str, str]:
        """Plain dictionary representation."""
        return {
            "commitment_hash": self.commitment_hash,
            "signature": self.signature,
            "public_key": self.public_key,
            "target_entity": self.target_entity,
            "category": self.category,
            "timestamp": self.timestamp,
            "nonce": self.nonce,
        }


@dataclass(frozen=True)
class VerificationResult:
    """Result of verifying an on-chain claim receipt."""

    valid: bool
    commitment_hash: str
    public_key: str
    details: str


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


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _compute_commitment(
    claim_details: str,
    timestamp: str,
    nonce: str,
    public_key_hex: str,
) -> str:
    """Compute SHA-256 commitment: ``hash(details || timestamp || nonce || pubkey)``."""
    preimage = claim_details + timestamp + nonce + public_key_hex
    return hashlib.sha256(preimage.encode()).hexdigest()


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
    # Lazy import — Ed25519 signing requires PyNaCl.
    try:
        from nacl.signing import SigningKey
    except ImportError:
        raise ImportError(
            "The 'PyNaCl' package is required for Ed25519 signing. "
            "Install it with:  pip install PyNaCl"
        ) from None

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

    # --- Derive public key ---
    signing_key = SigningKey(bytes.fromhex(private_key_hex))
    public_key_hex = signing_key.verify_key.encode().hex()

    # --- Compute commitment ---
    commitment_hash = _compute_commitment(
        claim_details, timestamp, nonce, public_key_hex
    )

    # --- Sign commitment hash ---
    signed = signing_key.sign(bytes.fromhex(commitment_hash))
    signature_hex = signed.signature.hex()

    return OnchainClaim(
        commitment_hash=commitment_hash,
        signature=signature_hex,
        public_key=public_key_hex,
        target_entity=target_entity,
        category=category,
        timestamp=timestamp,
        nonce=nonce,
    )


def verify_onchain_receipt(
    commitment_hash: str,
    signature: str,
    public_key_hex: str,
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
    try:
        from nacl.signing import VerifyKey
        from nacl.exceptions import BadSignatureError
    except ImportError:
        raise ImportError(
            "The 'PyNaCl' package is required for Ed25519 verification. "
            "Install it with:  pip install PyNaCl"
        ) from None

    _validate_hex_string(commitment_hash, "commitment_hash", expected_length=64)
    _validate_hex_string(signature, "signature", expected_length=128)
    _validate_hex_string(public_key_hex, "public_key_hex", expected_length=64)

    try:
        verify_key = VerifyKey(bytes.fromhex(public_key_hex))
        verify_key.verify(
            bytes.fromhex(commitment_hash),
            bytes.fromhex(signature),
        )
        return VerificationResult(
            valid=True,
            commitment_hash=commitment_hash,
            public_key=public_key_hex,
            details="Signature verified — claim is authentic.",
        )
    except BadSignatureError:
        return VerificationResult(
            valid=False,
            commitment_hash=commitment_hash,
            public_key=public_key_hex,
            details="Signature verification failed — claim may be tampered.",
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

    return _hmac.compare_digest(computed, expected_hash.lower())
