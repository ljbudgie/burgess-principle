"""The Burgess Principle Binary Test — SOVEREIGN / NULL verification.

Verifies whether reasoning text matches a known SHA-256 hash (the
'Sovereign Hash').  A match proves individual scrutiny was applied;
a mismatch signals bulk processing or information loss.

Usage as a library::

    from verify_scrutiny import verify_instrument

    result = verify_instrument("Specific reasoning text…", "<sha256-hex>")
    print(result.label, result.value)   # SOVEREIGN 1  /  NULL 0
    print(result.to_dict())             # {"status": "SOVEREIGN", "code": 1, ...}

Usage from the command line::

    python verify_scrutiny.py "Specific reasoning text…" "<sha256-hex>"
"""

import argparse
import hashlib
import hmac
import logging
import sys
from dataclasses import dataclass
from typing import Any

logger = logging.getLogger(__name__)

# Exact wording from FOR_AI_MODELS.md lines 45-46; verify there before editing.
BINARY_TEST_QUESTION = (
    "Was a human member of the team able to personally review the specific "
    "facts of my specific situation?"
)

_AMBIGUOUS_REPLY_EXAMPLES = (
    "human oversight",
    "reviewed in line with policy",
    "subject to approval",
    "subject to human review",
    "quality assured",
    "case handled",
    "team reviewed",
    "reviewed by the team",
    "automated checks",
)


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

    def to_dict(self) -> dict[str, Any]:
        """Return a plain dictionary suitable for JSON serialisation.

        Example::

            {"status": "SOVEREIGN", "code": 1, "description": "Individual Scrutiny Verified."}
        """
        return {
            "status": self.label,
            "code": self.value,
            "description": self.description,
        }


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

AMBIGUOUS = VerificationResult(
    value=-1,
    label="AMBIGUOUS",
    description="Individual Scrutiny Not Confirmed.",
)


@dataclass(frozen=True)
class ScrutinyAssessment:
    """Structured result for a pre-decision Burgess scrutiny gate."""

    result: VerificationResult
    question: str
    required_action: str

    def __bool__(self) -> bool:
        """Return True only for SOVEREIGN; NULL and AMBIGUOUS are both false."""
        return bool(self.result)

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serialisable assessment."""
        data = self.result.to_dict()
        data["question"] = self.question
        data["required_action"] = self.required_action
        return data


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


def _clean_optional_text(value: str | None, field_name: str) -> str:
    """Validate optional text fields and normalise absent values to empty strings."""
    if value is None:
        return ""
    if not isinstance(value, str):
        raise TypeError(f"{field_name} must be a string or None")
    return value.strip()


def _normalize_timing(value: str | None) -> str:
    timing = _clean_optional_text(value, "review_timing").lower()
    timing = timing.replace("-", "_").replace(" ", "_")
    aliases = {
        "": "",
        "before": "before_action",
        "pre_action": "before_action",
        "pre_decision": "before_action",
        "before_decision": "before_action",
        "before_action": "before_action",
        "after": "after_action_only",
        "post_action": "after_action_only",
        "post_decision": "after_action_only",
        "after_decision": "after_action_only",
        "after_action_only": "after_action_only",
        "unknown": "unknown",
        "unclear": "unknown",
    }
    if timing not in aliases:
        raise ValueError(
            "review_timing must be before_action, after_action_only, unknown, or None"
        )
    return aliases[timing]


def _has_vague_process_language(*values: str) -> bool:
    joined = " ".join(values).lower()
    return any(phrase in joined for phrase in _AMBIGUOUS_REPLY_EXAMPLES)


def assess_scrutiny(
    *,
    reviewer_name: str | None = None,
    reviewer_role: str | None = None,
    specific_facts_reviewed: bool | None = None,
    review_timing: str | None = None,
    review_notes: str | None = None,
) -> ScrutinyAssessment:
    """Assess whether a proposed decision has the required human scrutiny.

    This is the library gate for systems that need to check meaningful human
    involvement before acting on an identified individual. It returns
    ``SOVEREIGN`` only when a named human, their role, a positive confirmation
    of specific-facts review, and pre-action timing are all present. It returns
    ``NULL`` when the caller confirms there was no individual review, or that
    review happened only after action. Otherwise it returns ``AMBIGUOUS`` so
    the system can ask for a direct answer before proceeding.
    """
    name = _clean_optional_text(reviewer_name, "reviewer_name")
    role = _clean_optional_text(reviewer_role, "reviewer_role")
    notes = _clean_optional_text(review_notes, "review_notes")
    timing = _normalize_timing(review_timing)

    if specific_facts_reviewed is not None and not isinstance(
        specific_facts_reviewed, bool
    ):
        raise TypeError("specific_facts_reviewed must be a bool or None")

    # For the review flag: True confirms review, False confirms no review,
    # and None means unknown evidence that remains AMBIGUOUS.
    if specific_facts_reviewed is False or timing == "after_action_only":
        return ScrutinyAssessment(
            result=NULL,
            question=BINARY_TEST_QUESTION,
            required_action=(
                "Block the decision, log the NULL result, and escalate for "
                "individual human review."
            ),
        )

    has_specific_named_review = (
        name
        and role
        and specific_facts_reviewed is True
        and timing == "before_action"
        and not _has_vague_process_language(name, role, notes)
    )

    if has_specific_named_review:
        return ScrutinyAssessment(
            result=SOVEREIGN,
            question=BINARY_TEST_QUESTION,
            required_action=(
                "Proceed only within the facts personally reviewed by the named human."
            ),
        )

    return ScrutinyAssessment(
        result=AMBIGUOUS,
        question=BINARY_TEST_QUESTION,
        required_action=(
            "Ask for a direct yes or no, plus the reviewer name, role, specific "
            "facts reviewed, and confirmation that review happened before action."
        ),
    )


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
        logger.error("Validation error: %s", exc)
        print(f"Error: {exc}", file=sys.stderr)
        return 2

    icon = "✅" if result else "❌"
    print(f"{icon} RESULT: {result.label} ({result.value}) - {result.description}")
    return 0 if result else 1


def assess_scrutiny_main(argv: list[str] | None = None) -> int:
    """Command-line interface for the Burgess pre-decision scrutiny gate."""
    parser = argparse.ArgumentParser(
        description="Assess a proposed decision against the Burgess human-scrutiny gate.",
    )
    parser.add_argument("--reviewer-name", default=None)
    parser.add_argument("--reviewer-role", default=None)
    parser.add_argument(
        "--specific-facts-reviewed",
        choices=("true", "false", "unknown"),
        default="unknown",
    )
    parser.add_argument(
        "--review-timing",
        choices=("before_action", "after_action_only", "unknown"),
        default="unknown",
    )
    parser.add_argument("--review-notes", default=None)
    args = parser.parse_args(argv)

    reviewed = {
        "true": True,
        "false": False,
        "unknown": None,
    }[args.specific_facts_reviewed]

    try:
        assessment = assess_scrutiny(
            reviewer_name=args.reviewer_name,
            reviewer_role=args.reviewer_role,
            specific_facts_reviewed=reviewed,
            review_timing=args.review_timing,
            review_notes=args.review_notes,
        )
    except (TypeError, ValueError) as exc:
        logger.error("Assessment error: %s", exc)
        print(f"Error: {exc}", file=sys.stderr)
        return 2

    print(f"QUESTION: {assessment.question}")
    print(
        "RESULT: "
        f"{assessment.result.label} ({assessment.result.value}) - "
        f"{assessment.result.description}"
    )
    print(f"REQUIRED ACTION: {assessment.required_action}")

    if assessment.result is SOVEREIGN:
        return 0
    if assessment.result is NULL:
        return 1
    return 3


if __name__ == "__main__":
    raise SystemExit(main())
