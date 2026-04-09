"""The Burgess Principle Binary Test — SOVEREIGN / NULL verification.

Verifies whether reasoning text matches a known SHA-256 hash (the
'Sovereign Hash').  A match proves individual scrutiny was applied;
a mismatch signals bulk processing or information loss.

Usage as a library::

    from verify_scrutiny import verify_instrument

    result = verify_instrument("Specific reasoning text…", "<sha256-hex>")
    print(result.label, result.value)   # SOVEREIGN 1  /  NULL 0

Usage from the command line::

    python verify_scrutiny.py "Specific reasoning text…" "<sha256-hex>"
"""

import argparse
import hashlib
import hmac
import sys
from dataclasses import dataclass


# ---------------------------------------------------------------------------
# Result type
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class VerificationResult:
    """Immutable outcome of a Burgess Principle binary test."""

    value: int          # 1 = SOVEREIGN, 0 = NULL
    label: str          # Human-readable label
    description: str    # Explanation of the outcome

    def __bool__(self) -> bool:
        return self.value == 1


SOVEREIGN = VerificationResult(
    value=1,
    label="SOVEREIGN",
    description="Individual Scrutiny Verified.",
)

NULL = VerificationResult(
    value=0,
    label="NULL",
    description="Information Mismatch / Bulk Noise.",
)


# ---------------------------------------------------------------------------
# Core verification
# ---------------------------------------------------------------------------

def verify_instrument(
    reasoning_text: str,
    provided_hash: str,
) -> VerificationResult:
    """Run the Burgess Principle Binary Test.

    Parameters
    ----------
    reasoning_text:
        The text whose integrity is being verified.
    provided_hash:
        The expected SHA-256 hex-digest (the 'Sovereign Hash').

    Returns
    -------
    VerificationResult
        ``SOVEREIGN`` (1) when the hashes match, ``NULL`` (0) otherwise.

    Raises
    ------
    TypeError
        If *reasoning_text* or *provided_hash* is not a string.
    ValueError
        If *reasoning_text* is empty or *provided_hash* is not a valid
        64-character hexadecimal string.
    """
    # --- Input validation ------------------------------------------------
    # Reject non-string types early to provide clear error messages.
    if not isinstance(reasoning_text, str):
        raise TypeError(
            f"reasoning_text must be a string, got {type(reasoning_text).__name__}"
        )
    if not isinstance(provided_hash, str):
        raise TypeError(
            f"provided_hash must be a string, got {type(provided_hash).__name__}"
        )
    if not reasoning_text:
        raise ValueError("reasoning_text must not be empty")
    # SHA-256 digests are exactly 64 hex characters.
    if len(provided_hash) != 64 or not all(
        c in "0123456789abcdefABCDEF" for c in provided_hash
    ):
        raise ValueError(
            "provided_hash must be a 64-character hexadecimal string"
        )

    # Compute SHA-256 of the reasoning text for comparison against the
    # claimed Sovereign Hash.
    calculated_hash = hashlib.sha256(reasoning_text.encode()).hexdigest()

    # Constant-time comparison to prevent timing side-channel attacks.
    if hmac.compare_digest(calculated_hash, provided_hash.lower()):
        return SOVEREIGN
    return NULL


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    """Command-line interface for the Burgess Principle Binary Test."""
    parser = argparse.ArgumentParser(
        description="The Burgess Principle Binary Test — SOVEREIGN / NULL verification.",
    )
    parser.add_argument(
        "reasoning_text",
        help="The reasoning text to verify.",
    )
    parser.add_argument(
        "provided_hash",
        help="The expected SHA-256 hex-digest (Sovereign Hash).",
    )
    args = parser.parse_args(argv)

    try:
        result = verify_instrument(args.reasoning_text, args.provided_hash)
    except (TypeError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2

    icon = "✅" if result else "❌"
    print(f"{icon} RESULT: {result.label} ({result.value}) - {result.description}")
    return 0 if result else 1


if __name__ == "__main__":
    raise SystemExit(main())
