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

import difflib
import re
from dataclasses import dataclass, field
from typing import Sequence

__all__ = [
    "scan",
    "scan_thread",
    "ScanResult",
    "ThreadAssessment",
    "DISCLAIMER",
    "BOILERPLATE_LOOP_THRESHOLD",
]

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
# The name portion is case-sensitive (capitalised words) so that phrases like
# "reviewed by the relevant team" do not false-positive as a named reviewer;
# surrounding verbs/adverbs stay case-insensitive via inline (?i:...) groups.
_NAME = r"[A-Z][a-z]+(?:\s+[A-Z][a-z]+)+"
_PERSONAL = r"(?i:personally|individually|in\s+person)"
_REVIEWVERB = r"(?i:review|reviewed|consider|considered|assess|assessed|handle|handled|looked\s+at)"
_SOVEREIGN_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("'I, <Name>, personally reviewed'", re.compile(rf"\b(?i:I),?\s+{_NAME},?\s+{_PERSONAL}\s+{_REVIEWVERB}")),
    ("'reviewed by <Name>'", re.compile(rf"\b{_REVIEWVERB}\s+(?i:by)\s+{_NAME}\b")),
    ("named person + personal review (name first)", re.compile(rf"\b{_NAME}\b[^.\n]{{0,60}}?{_PERSONAL}\s+\w*\s*{_REVIEWVERB}")),
    ("named person + personal review (verb first)", re.compile(rf"\b{_NAME}\b[^.\n]{{0,60}}?{_REVIEWVERB}[^.\n]{{0,30}}?{_PERSONAL}")),
    ("'<Name> personally handled your case'", re.compile(rf"\b{_NAME}\b[^.\n]{{0,60}}?(?i:handled|dealt\s+with)\b[^.\n]{{0,30}}?{_PERSONAL}")),
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


# --- Correspondence-history tracking (boilerplate-loop detection) ----------
#
# A single reply is scanned in isolation by :func:`scan`. But a common evasion
# pattern only becomes visible across a *thread*: the institution sends reply
# after reply of varying boilerplate — process language, auto-acknowledgements,
# near-duplicate paragraphs — while never once naming a human who personally
# reviewed the specific facts. Each individual reply may scan AMBIGUOUS; the
# *pattern* is the signal.
#
# The thread tracker surfaces that pattern. It does NOT override the
# per-message classifications (they are preserved, unchanged, in
# ``per_message``), and it does not create a new classification state. It
# issues a separate, explicit, thread-level PROVISIONAL NULL — using the
# confidence-tier vocabulary from FOR_AI_MODELS.md — with the evasion pattern
# documented as its basis, and escalates to a human for confirmation. Like
# every other output of this module, it is advisory only.

# "More than 3" boilerplate replies with no named human triggers the
# thread-level signal, i.e. the 4th such reply.
BOILERPLATE_LOOP_THRESHOLD = 3

# Two replies this similar (difflib ratio) are treated as recycled boilerplate
# even if neither matches a pattern list.
_NEAR_DUPLICATE_RATIO = 0.75

_THREAD_NEXT_STEP = (
    "Boilerplate-loop pattern: escalate for individual human review. Preserve "
    "the full thread as evidence, then send a written request naming the "
    "pattern and asking the binary question. Templates: "
    "templates/REQUEST_FOR_HUMAN_REVIEW.md and "
    "templates/FOLLOW_UP_WEASEL_RESPONSE.md."
)


@dataclass
class ThreadAssessment:
    """A provisional, thread-level assessment of a correspondence history.

    Mirrors the standard confidence-tier form from FOR_AI_MODELS.md:
    ``Classification · Confidence · Uncertainty · Basis · Would change it``.
    Always advisory; per-message results are preserved unchanged.
    """

    classification: str  # SOVEREIGN | NULL | AMBIGUOUS | INSUFFICIENT (provisional)
    confidence: str  # CONFIRMED | PROVISIONAL | SPECULATIVE
    uncertainty: str  # e.g. "[provisional-final]" or "none"
    basis: str
    would_change_it: str
    boilerplate_count: int
    named_human_seen: bool
    per_message: list[ScanResult] = field(default_factory=list)
    suggested_next_step: str = ""
    requires_human_confirmation: bool = True
    disclaimer: str = DISCLAIMER

    def standard_form(self) -> str:
        """One-line standard form (FOR_AI_MODELS.md confidence-tier format)."""
        return (
            f"Classification: {self.classification} · "
            f"Confidence: {self.confidence} · "
            f"Uncertainty: {self.uncertainty} · "
            f"Basis: {self.basis} · "
            f"Would change it: {self.would_change_it}"
        )

    def as_dict(self) -> dict:
        return {
            "classification": self.classification,
            "confidence": self.confidence,
            "uncertainty": self.uncertainty,
            "basis": self.basis,
            "would_change_it": self.would_change_it,
            "provisional": True,
            "boilerplate_count": self.boilerplate_count,
            "named_human_seen": self.named_human_seen,
            "per_message": [r.as_dict() for r in self.per_message],
            "suggested_next_step": self.suggested_next_step,
            "requires_human_confirmation": self.requires_human_confirmation,
            "disclaimer": self.disclaimer,
        }


def _boilerplate_flags(per_message: list[ScanResult], replies: list[str]) -> list[bool]:
    """Mark each reply that counts as boilerplate.

    A reply is boilerplate if it shows automation/process language with no
    named-reviewer signal. Near-duplicate replies are also boilerplate: when
    two replies are recycled copies of each other, *both* count.
    """
    n = len(replies)
    eligible = [not per_message[i].matched.get("sovereign") for i in range(n)]
    flags = [
        eligible[i]
        and bool(per_message[i].matched.get("null") or per_message[i].matched.get("ambiguous"))
        for i in range(n)
    ]
    for i in range(n):
        for j in range(i + 1, n):
            if not (eligible[i] and eligible[j]) or (flags[i] and flags[j]):
                continue
            if difflib.SequenceMatcher(None, replies[i], replies[j]).ratio() >= _NEAR_DUPLICATE_RATIO:
                flags[i] = flags[j] = True
    return flags


def scan_thread(replies: Sequence[str]) -> ThreadAssessment:
    """Assess a correspondence history (oldest first) for the boilerplate loop.

    Scans each reply with :func:`scan` (results preserved unchanged in
    ``per_message`` — the thread signal never silently overrides them). If the
    institution has sent more than :data:`BOILERPLATE_LOOP_THRESHOLD`
    boilerplate replies without ever identifying a named human reviewer, the
    thread is flagged **PROVISIONAL NULL** with the evasion pattern documented
    as the basis, and escalated for individual human review. Otherwise the
    thread-level view stays AMBIGUOUS or INSUFFICIENT.

    This is a heuristic aid, not a verdict: every assessment carries
    ``requires_human_confirmation = True``.
    """
    replies = [r or "" for r in replies]
    per_message = [scan(text) for text in replies]
    named_human_seen = any(r.matched.get("sovereign") for r in per_message)

    boilerplate_count = sum(_boilerplate_flags(per_message, replies))

    if boilerplate_count > BOILERPLATE_LOOP_THRESHOLD and not named_human_seen:
        return ThreadAssessment(
            classification="NULL",
            confidence="PROVISIONAL",
            uncertainty="[provisional-final]",
            basis=(
                f"boilerplate-loop evasion pattern: {boilerplate_count} "
                "boilerplate replies across the thread with no named human "
                "reviewer identified in any of them"
            ),
            would_change_it=(
                "written confirmation that a named human personally reviewed "
                "the specific facts of this case"
            ),
            boilerplate_count=boilerplate_count,
            named_human_seen=named_human_seen,
            per_message=per_message,
            suggested_next_step=_THREAD_NEXT_STEP,
        )

    if named_human_seen:
        classification = "AMBIGUOUS"
        basis = (
            "a named human appears in the thread but the pattern is not yet "
            "confirmed either way"
        )
        next_step = _NEXT_STEP["AMBIGUOUS"]
    elif boilerplate_count:
        classification = "AMBIGUOUS"
        basis = (
            f"{boilerplate_count} boilerplate repl"
            f"{'y' if boilerplate_count == 1 else 'ies'} so far, below the "
            "loop threshold; no named human yet"
        )
        next_step = _NEXT_STEP["AMBIGUOUS"]
    else:
        classification = "INSUFFICIENT"
        basis = "no clear signal in the thread either way"
        next_step = _NEXT_STEP["INSUFFICIENT"]

    return ThreadAssessment(
        classification=classification,
        confidence="PROVISIONAL",
        uncertainty="[facts-missing]",
        basis=basis,
        would_change_it=(
            "a direct written answer to the binary question, with the "
            "reviewer's name and role"
        ),
        boilerplate_count=boilerplate_count,
        named_human_seen=named_human_seen,
        per_message=per_message,
        suggested_next_step=next_step,
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
