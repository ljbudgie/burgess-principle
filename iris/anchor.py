"""Evidence anchoring helper — compute the canonical commitment to timestamp.

Local-first, pure standard library. Produces the SHA-256 commitment for an
evidence file (the findings ledger, a Witness attestation, the Attestor Registry
transparency log) — the exact digest you would anchor for proof-of-existence,
e.g. via OpenTimestamps to the Bitcoin chain. See
``onchain-protocol/bitcoin-anchoring.md``.

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


def build_anchor_manifest(paths: list[str | Path], *, now: datetime | None = None) -> dict:
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
    return {
        "algorithm": "sha256",
        "computed_at": when.isoformat(),
        "anchored": False,
        "anchor_method": "opentimestamps (submit separately)",
        "entries": entries,
        "disclaimer": DISCLAIMER,
    }


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
