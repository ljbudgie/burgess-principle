"""
Cryptographic signing — Ed25519 signatures for DecisionRecords (Phase 2).

The SHA-256 fingerprint on a DecisionRecord makes it *tamper-evident*: anyone
holding the record can recompute the fingerprint and detect a changed field.
It does not, on its own, prove *who* produced the record.

This module adds the missing half — *non-repudiation*. A `RecordSigner` holds
an Ed25519 private key and signs the record's fingerprint. The signature and the
corresponding public key are attached to the record, so any third party can
independently verify — offline, with no shared secret — that:

1. the record's content still matches its fingerprint (integrity), and
2. the fingerprint was signed by the holder of the published public key.

Design notes
------------
* The signature covers the fingerprint, not the raw content. Because the
  fingerprint already commits to every content field (see
  ``DecisionRecord._canonical_dict``), signing the fingerprint binds the
  signature to the exact content while keeping the signed message short and
  reproducible.
* A versioned, domain-separated context prefix (``SIGNING_CONTEXT``) is prepended
  to the fingerprint before signing, so a Burgess oversight signature can never
  be confused with a signature produced by another part of the ecosystem.
* Signatures live *outside* the canonical fingerprint (they are applied after
  sealing), so signing never changes a record's fingerprint and unsigned records
  behave exactly as before.
* Ed25519 is provided by PyNaCl, consistent with the rest of this repository
  (see ``onchain-protocol/sdk/onchain_claims.py`` and
  ``CRYPTOGRAPHIC_IDENTITY.md``). PyNaCl is an *optional* dependency: the stdlib
  core continues to work without it, and signing raises a clear error if it is
  missing.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover - import for type checkers only
    from .decision_record import DecisionRecord

__all__ = [
    "SIGNING_CONTEXT",
    "SigningError",
    "RecordSigner",
    "signing_message",
    "verify_record_signature",
]

# Domain-separation prefix. Bumping the version invalidates old-context
# signatures deliberately, so the meaning of a signature is unambiguous.
SIGNING_CONTEXT = b"burgess-oversight/decision-record/v1"

_PYNACL_HINT = (
    "The 'PyNaCl' package is required for Ed25519 signing/verification. "
    "Install it with:  pip install PyNaCl"
)


class SigningError(Exception):
    """Raised when a record cannot be signed or verified."""


def _require_signing_key():
    try:
        from nacl.signing import SigningKey
    except ImportError as exc:  # pragma: no cover - exercised only without PyNaCl
        raise SigningError(_PYNACL_HINT) from exc
    return SigningKey


def _require_verify_key():
    try:
        from nacl.exceptions import BadSignatureError
        from nacl.signing import VerifyKey
    except ImportError as exc:  # pragma: no cover - exercised only without PyNaCl
        raise SigningError(_PYNACL_HINT) from exc
    return VerifyKey, BadSignatureError


def _validate_hex(value: str, label: str, expected_length: int) -> None:
    if not isinstance(value, str) or len(value) != expected_length:
        raise SigningError(
            f"{label} must be a {expected_length}-character hex string."
        )
    try:
        bytes.fromhex(value)
    except ValueError as exc:
        raise SigningError(f"{label} must be valid hexadecimal.") from exc


def signing_message(fingerprint: str) -> bytes:
    """
    The exact byte string that gets signed for a given fingerprint.

    Exposed so independent verifiers can reproduce the signed message without
    importing the signing machinery: ``SIGNING_CONTEXT + b":" + fingerprint``.
    """
    if not fingerprint:
        raise SigningError("Cannot build a signing message from an empty fingerprint.")
    _validate_hex(fingerprint, "fingerprint", expected_length=64)
    return SIGNING_CONTEXT + b":" + fingerprint.encode("ascii")


class RecordSigner:
    """
    Signs DecisionRecords with an Ed25519 private key.

    Usage
    -----
        signer = RecordSigner.generate()          # or RecordSigner(private_key_hex)
        signer.sign(record)                        # populates record.signature etc.
        signer.public_key_hex                      # publish this for verification

    The private key never leaves this object. Only the signature and public key
    are attached to the record.
    """

    def __init__(self, private_key_hex: str) -> None:
        _validate_hex(private_key_hex, "private_key_hex", expected_length=64)
        SigningKey = _require_signing_key()
        self._signing_key = SigningKey(bytes.fromhex(private_key_hex))

    @classmethod
    def generate(cls) -> "RecordSigner":
        """Create a signer with a freshly generated Ed25519 key pair."""
        SigningKey = _require_signing_key()
        key = SigningKey.generate()
        return cls(key.encode().hex())

    @property
    def private_key_hex(self) -> str:
        """The 32-byte Ed25519 seed as hex. Keep this secret."""
        return self._signing_key.encode().hex()

    @property
    def public_key_hex(self) -> str:
        """The 32-byte Ed25519 public key as hex. Safe to publish."""
        return self._signing_key.verify_key.encode().hex()

    def sign(self, record: "DecisionRecord", *, seal_if_needed: bool = True) -> str:
        """
        Sign ``record`` and attach the signature, public key and timestamp.

        The record is sealed first if it has no fingerprint (or ``seal_if_needed``
        forces a reseal is *not* performed — an already-sealed record keeps its
        fingerprint so signing a tampered record is impossible without detection).

        Returns the signature as a hex string. Mutates the record in place.
        """
        if record.fingerprint is None:
            if not seal_if_needed:
                raise SigningError(
                    "Record is not sealed. Call record.seal() before signing, "
                    "or pass seal_if_needed=True."
                )
            record.seal()

        message = signing_message(record.fingerprint)
        signature_hex = self._signing_key.sign(message).signature.hex()

        record.signature = signature_hex
        record.public_key = self.public_key_hex
        record.signed_at = datetime.now(timezone.utc).isoformat()
        return signature_hex


def verify_record_signature(record: "DecisionRecord") -> bool:
    """
    Verify a signed DecisionRecord end to end.

    Returns True only if:
      * the record carries a signature and a public key,
      * the record's content still matches its fingerprint (integrity), and
      * the signature is a valid Ed25519 signature over the fingerprint by the
        attached public key.

    Returns False for an unsigned record, a tampered record, or a bad signature.
    A malformed signature/public key raises SigningError.
    """
    if not record.signature or not record.public_key:
        return False

    # A signature over a fingerprint is meaningless if the content no longer
    # matches that fingerprint — check integrity first.
    if not record.verify_integrity():
        return False

    VerifyKey, BadSignatureError = _require_verify_key()
    _validate_hex(record.signature, "signature", expected_length=128)
    _validate_hex(record.public_key, "public_key", expected_length=64)

    message = signing_message(record.fingerprint)
    try:
        VerifyKey(bytes.fromhex(record.public_key)).verify(
            message, bytes.fromhex(record.signature)
        )
    except BadSignatureError:
        return False
    return True
