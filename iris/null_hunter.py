"""NULL Hunter — local-first, advisory Burgess-Test signal scanner.

Scans the text of an institutional reply (an email, a decision letter, a portal
message) for language patterns associated with the three Burgess classifications
and suggests the next Burgess step.

Design principles (deliberate, and load-bearing):

* **Advisory only.** This is a heuristic aid, not a verdict. The tool that hunts
  NULLs must not itself *be* a NULL: every result carries
  ``requires_human_confirmation = True`` and a plain-language disclaimer. A human
  makes the classification; the scanner only surfaces signals and a suggestion.
* **Local-first.** Pure standard library. No network, no model download, no data
  leaving the device.
* **Transparent.** Every result lists the exact phrases that triggered it, so the
  user can check the reasoning rather than trust a black box.

The scanner never returns SOVEREIGN/NULL/AMBIGUOUS as a finding of fact — it
returns a *provisional* signal for a human to confirm.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field

__all__ = ["scan", "ScanResult", "DISCLAIMER"]

DISCLAIMER = (
    "Provisional signal only. The NULL Hunter is a heuristic aid, not a "
    "determination. A human must confirm the classification before it is "
    "recorded or relied upon."
)

# --- Signal patterns -------------------------------------------------------
# Each tuple is (label, compiled pattern). Patterns are intentionally simple and
# readable; precision is traded for transparency, and the human gate covers the
# residual error.

def _c(pattern: str) -> re.Pattern[str]:
    return re.compile(pattern, re.IGNORECASE)


# Explicit absence of individual human review → leans NULL.
_NULL_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("automated/automatic processing", _c(r"\bautomat(?:ed|ic|ically)\b")),
    ("system- or computer-generated", _c(r"\b(?:system|computer)[-\s]generated\b")),
    ("auto-acknowledgement / do-not-reply", _c(r"\b(?:auto[-\s]?acknowledg|do[-\s]?not[-\s]?reply|noreply)\w*")),
    ("bulk / batch / en bloc processing", _c(r"\b(?:bulk|batch|en\s+bloc|mass)\b")),
    ("explicit 'no individual review'", _c(r"\bno\s+(?:individual|specific|personal|human)\s+(?:review|consideration|assessment)\b")),
    ("processed by system logic", _c(r"\bprocessed\s+(?:by|through|using)\s+(?:our\s+)?(?:system|systems|software|algorithm)")),
]

# Process / weasel language that does not confirm a named human → leans AMBIGUOUS.
_AMBIGUOUS_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("'subject to human oversight'", _c(r"\bsubject\s+to\s+human\s+(?:oversight|review)\b")),
    ("'human review layer'", _c(r"\bhuman\s+(?:review|oversight)\s+(?:layer|process|step)\b")),
    ("'in line with policy/procedure'", _c(r"\bin\s+(?:line|accordance)\s+with\s+(?:our\s+)?(?:policy|policies|procedure|process)")),
    ("'robust/appropriate processes'", _c(r"\b(?:robust|appropriate|rigorous|established)\s+(?:process|processes|procedures|checks|controls)\b")),
    ("'our processes/systems ensure'", _c(r"\bour\s+(?:processes|systems|procedures)\s+ensure\b")),
    ("'quality assurance / QA'", _c(r"\b(?:quality\s+assurance|quality[-\s]checked|QA)\b")),
    ("'reviewed by the team' (unnamed)", _c(r"\b(?:reviewed|assessed|considered)\s+by\s+(?:our|the)\s+(?:team|department|relevant\s+team)\b")),
]

# A named individual described as having personally reviewed → leans SOVEREIGN.
_NAME = r"[A-Z][a-z]+(?:\s+[A-Z][a-z]+)+"
_PERSONAL = r"(?:personally|individually|in\s+person)"
_REVIEWVERB = r"(?:review|reviewed|consider|considered|assess|assessed|handle|handled|looked\s+at)"
_SOVEREIGN_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("'I, <Name>, personally reviewed'", _c(rf"\bI,?\s+{_NAME},?\s+{_PERSONAL}\s+{_REVIEWVERB}")),
    ("'reviewed by <Name>'", _c(rf"\b{_REVIEWVERB}\s+by\s+{_NAME}\b")),
    ("named person + personal review (name first)", _c(rf"\b{_NAME}\b[^.\n]{{0,60}}?{_PERSONAL}\s+\w*\s*{_REVIEWVERB}")),
    ("named person + personal review (verb first)", _c(rf"\b{_NAME}\b[^.\n]{{0,60}}?{_REVIEWVERB}[^.\n]{{0,30}}?{_PERSONAL}")),
    ("'<Name> personally handled your case'", _c(rf"\b{_NAME}\b[^.\n]{{0,60}}?(?:handled|dealt\s+with)\b[^.\n]{{0,30}}?{_PERSONAL}")),
]

_NEXT_STEP = {
    "NULL": (
        "Record the NULL. Preserve this reply as evidence (it admits no individual "
        "human review), then escalate for individual human review. Templates: "
        "templates/GENERAL_DISPUTE_WITH_BURGESS_PRINCIPLE.md or "
        "templates/NOTICE_OF_NULLITY_ADVANCED.md."
    ),
    "AMBIGUOUS": (
        "Process language without a named reviewer. Send the weasel-word follow-up "
        "asking for a direct YES/NO plus the reviewer's name and role. Template: "
        "templates/FOLLOW_UP_WEASEL_RESPONSE.md."
    ),
    "SOVEREIGN": (
        "Looks SOVEREIGN — a named human is described as having reviewed your "
        "specific facts. Confirm in writing who reviewed it and what they reviewed, "
        "and record the positive result."
    ),
    "INSUFFICIENT": (
        "No clear signal either way. Ask the binary question in writing. Template: "
        "templates/REQUEST_FOR_HUMAN_REVIEW.md."
    ),
}


@dataclass
class ScanResult:
    """The provisional output of a NULL Hunter scan."""

    classification: str  # SOVEREIGN | NULL | AMBIGUOUS | INSUFFICIENT (provisional)
    matched: dict[str, list[str]] = field(default_factory=dict)
    suggested_next_step: str = ""
    requires_human_confirmation: bool = True
    disclaimer: str = DISCLAIMER

    def as_dict(self) -> dict:
        return {
            "classification": self.classification,
            "provisional": True,
            "matched": self.matched,
            "suggested_next_step": self.suggested_next_step,
            "requires_human_confirmation": self.requires_human_confirmation,
            "disclaimer": self.disclaimer,
        }


def _hits(text: str, patterns: list[tuple[str, re.Pattern[str]]]) -> list[str]:
    return [label for label, pat in patterns if pat.search(text)]


def scan(text: str) -> ScanResult:
    """Scan institutional reply ``text`` for Burgess-Test signals.

    Returns a :class:`ScanResult` with a *provisional* classification that always
    requires human confirmation. Classification precedence is conservative:

    * explicit NULL admission outweighs everything;
    * a clean named-reviewer signal (with no muddying process language) → SOVEREIGN;
    * a named reviewer mixed with weasel language → AMBIGUOUS (the named-but-
      unconfirmed trap), needing the follow-up question;
    * process language alone → AMBIGUOUS;
    * nothing recognised → INSUFFICIENT (ask the binary question).
    """
    text = text or ""
    null_hits = _hits(text, _NULL_PATTERNS)
    ambiguous_hits = _hits(text, _AMBIGUOUS_PATTERNS)
    sovereign_hits = _hits(text, _SOVEREIGN_PATTERNS)

    if null_hits and not sovereign_hits:
        classification = "NULL"
    elif sovereign_hits and not ambiguous_hits and not null_hits:
        classification = "SOVEREIGN"
    elif sovereign_hits:
        # Named, but co-present with process/automation language: not confirmed.
        classification = "AMBIGUOUS"
    elif ambiguous_hits:
        classification = "AMBIGUOUS"
    else:
        classification = "INSUFFICIENT"

    matched = {
        "sovereign": sovereign_hits,
        "null": null_hits,
        "ambiguous": ambiguous_hits,
    }
    return ScanResult(
        classification=classification,
        matched={k: v for k, v in matched.items() if v},
        suggested_next_step=_NEXT_STEP[classification],
    )


def _format(result: ScanResult) -> str:
    lines = [
        f"Provisional classification: {result.classification}",
        "",
        "Signals matched:",
    ]
    if result.matched:
        for bucket, labels in result.matched.items():
            for label in labels:
                lines.append(f"  [{bucket.upper()}] {label}")
    else:
        lines.append("  (none)")
    lines += [
        "",
        f"Suggested next step: {result.suggested_next_step}",
        "",
        f"NOTE: {result.disclaimer}",
    ]
    return "\n".join(lines)


def main() -> None:
    """Read an institutional reply from stdin and print a provisional scan."""
    import sys

    text = sys.stdin.read()
    print(_format(scan(text)))


if __name__ == "__main__":
    main()
