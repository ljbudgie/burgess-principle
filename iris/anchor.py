"""Evidence anchoring helper — compute the canonical commitment to timestamp.

Local-first, pure standard library. Produces the SHA-256 commitment for an
evidence file (the findings ledger, a Witness attestation, the Attestor Registry
transparency log) — the exact digest you would anchor for proof-of-existence,
e.g. via OpenTimestamps to the Bitcoin chain. See
``onchain-protocol/bitcoin-anchoring.md``.

It can also build a deterministic DID-controlled signing payload for that digest.
The signing itself is deliberately outside the stdlib core: an Ed25519, WebAuthn,
or hardware-backed signer can sign the returned payload hash without this helper
taking custody of private keys.

Honest scope (load-bearing):

* **Computes, does not submit.** This builds and packages the commitment to be
  anchored. It does NOT itself submit to Bitcoin or any chain — that step needs a
  network notary (OpenTimestamps) and is deliberately a separate, later wrapper.
* **Existence, not truth.** A timestamp proves a record existed, unaltered, at a
  point in time. It does not prove the record's contents are true, that an
  institution did wrong, or that any human reviewed anything.
* **Hashes only — never facts.** Only the digest is ever anchored; the underlying
  evidence stays local. The chain sees a hash, nothing more.
* **No token.** Anchoring uses public infrastructure as a neutral notary, nothing
  else. There is no coin and no payment.
"""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

__all__ = [
    "sha256_file",
    "canonical_json_sha256",
    "build_did_signing_payload",
    "build_anchor_manifest",
    "DISCLAIMER",
]

DISCLAIMER = (
    "Commitment only. This digest is what you would anchor for proof-of-existence; "
    "it has NOT been submitted to Bitcoin or any chain here. A timestamp proves a "
    "record existed unaltered at a time — not that its contents are true. Only "
    "hashes are ever anchored, never the underlying facts. No token is involved."
)


def sha256_file(path: str | Path) -> str:
    """SHA-256 hex digest of a file's raw bytes."""
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def canonical_json_sha256(obj: Any) -> str:
    """SHA-256 of an object serialised as canonical sorted-key JSON.

    Matches the protocol's canonicalisation (sorted keys, no whitespace) so the
    commitment is deterministic and order-independent.
    """
    canonical = json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def _default_verification_method(controller: str) -> str:
    if controller.startswith("did:key:") and "#" not in controller:
        key_id = controller.removeprefix("did:key:")
        return f"{controller}#{key_id}"
    return controller


def _assert_sha256_hex(commitment_hash: str) -> None:
    if len(commitment_hash) != 64:
        raise ValueError("commitment_hash must be a 64-character SHA-256 hex digest")
    try:
        int(commitment_hash, 16)
    except ValueError as exc:
        raise ValueError("commitment_hash must be a 64-character SHA-256 hex digest") from exc


def build_did_signing_payload(
    commitment_hash: str,
    *,
    controller: str,
    verification_method: str | None = None,
    proof_purpose: str = "assertionMethod",
    now: datetime | None = None,
    context: dict[str, Any] | None = None,
) -> dict:
    """Build the canonical payload a DID-controlled key should sign.

    ``commitment_hash`` is the SHA-256 hex digest being anchored or recorded.
    The returned object is intentionally plain JSON. Compute
    ``canonical_json_sha256(payload)`` and sign that digest with the
    DID-controlled Ed25519 key, WebAuthn ceremony, or external hardware signer.
    """
    _assert_sha256_hex(commitment_hash)
    if not controller:
        raise ValueError("controller is required")

    when = (now or datetime.now(timezone.utc)).astimezone(timezone.utc)
    payload: dict[str, Any] = {
        "@context": [
            "https://www.w3.org/ns/did/v1",
            "https://w3id.org/security/suites/ed25519-2020/v1",
        ],
        "type": "BurgessDIDCommitment",
        "controller": controller,
        "verificationMethod": verification_method or _default_verification_method(controller),
        "proofPurpose": proof_purpose,
        "commitmentHash": f"sha256:{commitment_hash}",
        "created": when.isoformat(),
    }
    if context:
        payload["context"] = context
    return payload


def build_anchor_manifest(
    paths: list[str | Path],
    *,
    now: datetime | None = None,
    did_controller: str | None = None,
    verification_method: str | None = None,
) -> dict:
    """Build the manifest of commitments to anchor for the given evidence files.

    Returns a plain dict (JSON-serialisable). ``now`` may be supplied for
    deterministic output; otherwise the current UTC time is used.
    """
    when = (now or datetime.now(timezone.utc)).astimezone(timezone.utc)
    entries = []
    for p in paths:
        path = Path(p)
        data = path.read_bytes()
        entries.append({"path": str(path), "sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)})
    manifest = {
        "algorithm": "sha256",
        "computed_at": when.isoformat(),
        "anchored": False,
        "anchor_method": "opentimestamps (submit separately)",
        "entries": entries,
        "disclaimer": DISCLAIMER,
    }
    if did_controller:
        manifest_hash = canonical_json_sha256(
            {
                "algorithm": manifest["algorithm"],
                "computed_at": manifest["computed_at"],
                "entries": manifest["entries"],
            }
        )
        manifest["did_signing"] = build_did_signing_payload(
            manifest_hash,
            controller=did_controller,
            verification_method=verification_method,
            now=when,
            context={"scope": "anchor_manifest"},
        )
    return manifest


def main() -> None:
    """Print the anchor manifest (JSON) for files given as CLI arguments."""
    import sys

    paths = sys.argv[1:]
    if not paths:
        print("usage: python -m iris.anchor <file> [<file> ...]", file=sys.stderr)
        raise SystemExit(2)
    print(json.dumps(build_anchor_manifest(paths), indent=2))


if __name__ == "__main__":
    main()
