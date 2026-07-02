"""Decline-compliance checker — the four pillars of a SOVEREIGN decline.

An institution is allowed to say no. The Burgess Principle does not demand a
yes — it demands that the *no* shows a human mind was individually applied to
the specific facts. This module checks a written rejection ("decline") for the
four pillars that distinguish a SOVEREIGN decline from a boilerplate brush-off:

1. **Attributable identity** — a named human (name and, ideally, role) owns
   the decision.
2. **Record of the specific request** — the reply demonstrably engages with
   *what was actually asked*, not a generic category of query.
3. **Reasoned exclusion boundary** — a stated reason *why this request falls
   outside* what the institution will do, not a bare "we are unable to assist".
4. **Assessment signposting** — a route onward: how to challenge, escalate,
   or seek review of the decline.

.. note::
   The "four pillars" framing is doctrinal/analytical vocabulary for this
   project, not a claim of statutory wording. It requires explicit human
   review by @ljbudgie before being cited externally.

Design principles (shared with :mod:`iris.null_hunter`, and load-bearing):

* **Advisory only.** This is a heuristic aid, not a verdict. Every result
  carries ``requires_human_confirmation = True``. A human confirms the
  assessment; the checker only surfaces which pillars appear absent.
* **No automated exit.** When a decline fails the pillars, the checker points
  the user to the existing Burgess Sovereign Exit Protocol tooling
  (``tools/bgsp-exit.py``, ``protocols/burgess-sovereign-exit.md``) so a human
  can decide whether to leave. It never compiles or executes an exit itself —
  an exit is an act of power over the individual's own affairs, and a human
  must own it.
* **Local-first.** Pure standard library. No network, nothing leaves the
  device.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field

__all__ = [
    "check_decline",
    "DeclineAssessment",
    "NonCompliantDeclineError",
    "PILLARS",
    "DISCLAIMER",
]

DISCLAIMER = (
    "Provisional signal only. The decline-compliance checker is a heuristic "
    "aid, not a determination. A human must confirm the assessment before it "
    "is recorded or relied upon."
)

BSEP_SIGNPOST = (
    "If, after human confirmation, the decline stands non-compliant and you "
    "choose to leave the system, the Burgess Sovereign Exit Protocol is the "
    "human-owned route: read protocols/burgess-sovereign-exit.md and use "
    "tools/bgsp-exit.py yourself. This checker will not compile or execute an "
    "exit for you — that decision belongs to a human."
)


def _c(pattern: str, flags: int = re.IGNORECASE) -> re.Pattern[str]:
    return re.compile(pattern, flags)


# Case-sensitive: two-plus capitalised words, as in null_hunter.
_NAME = r"[A-Z][a-z]+(?:\s+[A-Z][a-z]+)+"

# --- Pillar signal patterns -------------------------------------------------
# Each pillar maps to (label, pattern) pairs. A pillar is "present" if any of
# its patterns match. Patterns are intentionally simple and readable;
# precision is traded for transparency, and the human gate covers the
# residual error.

_PILLAR_PATTERNS: dict[str, list[tuple[str, re.Pattern[str]]]] = {
    "attributable_identity": [
        ("signed with a full name", _c(rf"(?:regards|sincerely|faithfully|yours|signed)[,\s]+{_NAME}", 0)),
        ("named decision-maker", _c(rf"(?i:decision\s+(?:was\s+)?(?:made|taken|reviewed)\s+by)\s+{_NAME}", 0)),
        ("'I, <Name>' ownership", _c(rf"\b(?i:I),?\s+{_NAME}\b", 0)),
        ("name with stated role", _c(rf"{_NAME},?\s+(?i:head\s+of|director|manager|officer|caseworker|partner|solicitor)", 0)),
    ],
    "specific_request": [
        ("quotes the request date", _c(r"\byour\s+(?:letter|email|request|application|complaint)\s+(?:of|dated|received\s+on)\s+\d")),
        ("references a case/reference number", _c(r"\b(?:reference|ref\.?|case|complaint)\s*(?:number|no\.?|#|:)?\s*[A-Z0-9][A-Z0-9\-/]{3,}")),
        ("restates the specific ask", _c(r"\byou\s+(?:asked|requested|applied\s+for|raised|queried|sought)\b")),
        ("engages the specific subject", _c(r"\b(?:specifically|in\s+particular|regarding\s+your\s+(?:request|question|point))\b")),
    ],
    "reasoned_boundary": [
        ("states why it is outside scope", _c(r"\b(?:because|as|since)\b[^.\n]{5,}\b(?:outside|beyond|not\s+within|does\s+not\s+fall|falls\s+outside|out\s+of\s+scope|not\s+covered|ineligible|criteria)\b")),
        ("names the criterion not met", _c(r"\b(?:criterion|criteria|threshold|requirement|condition)s?\b[^.\n]{0,80}\b(?:not\s+met|unmet|not\s+satisfied|does\s+not\s+meet)\b")),
        ("cites a specific rule/policy section", _c(r"\b(?:under|pursuant\s+to|in\s+accordance\s+with)\s+(?:section|s\.|paragraph|para\.?|regulation|reg\.?|clause|article)\s*\d")),
        ("explains what would have qualified", _c(r"\b(?:would\s+(?:have\s+)?(?:qualify|qualified|be\s+eligible)|to\s+be\s+eligible)\b")),
    ],
    "assessment_signposting": [
        ("names a review/appeal route", _c(r"\b(?:appeal|request\s+a\s+review|review\s+of\s+this\s+decision|reconsideration|challenge\s+this\s+decision)\b")),
        ("names an ombudsman/regulator", _c(r"\b(?:ombudsman|regulator|ICO|adjudicator|tribunal)\b")),
        ("gives a complaint escalation route", _c(r"\b(?:complaints?\s+(?:procedure|process|team|policy)|escalate\s+(?:this|your))\b")),
        ("gives a deadline for challenge", _c(r"\b(?:within\s+\d+\s+(?:days|weeks|months))\b[^.\n]{0,60}\b(?:appeal|review|challenge|respond|complain)")),
    ],
}

#: The four pillars of a SOVEREIGN decline, with human-readable descriptions.
PILLARS: dict[str, str] = {
    "attributable_identity": "a named human owns the decision",
    "specific_request": "the reply engages with the specific request actually made",
    "reasoned_boundary": "a stated reason why this request falls outside what will be done",
    "assessment_signposting": "a route to challenge, escalate, or seek review",
}

_FOLLOW_UP = {
    "attributable_identity": (
        "Ask in writing for the name and role of the person who made this "
        "decision. Template: templates/REQUEST_FOR_HUMAN_REVIEW.md."
    ),
    "specific_request": (
        "Ask the institution to confirm, in writing, precisely which request "
        "of yours this decline answers."
    ),
    "reasoned_boundary": (
        "Ask for the specific reason your request falls outside what the "
        "institution will do — not a restatement that it does."
    ),
    "assessment_signposting": (
        "Ask for the route to challenge or seek review of this decision, and "
        "any deadline that applies."
    ),
}


class NonCompliantDeclineError(Exception):
    """Raised by :func:`check_decline` in strict mode when pillars are absent.

    Carries the full :class:`DeclineAssessment` so the caller retains the
    per-pillar detail, the disclaimer, and the BSEP signpost. Raising this
    error is a *signal to a human* — it never triggers any automated action.
    """

    def __init__(self, assessment: "DeclineAssessment") -> None:
        self.assessment = assessment
        missing = ", ".join(assessment.absent_pillars)
        super().__init__(
            f"Decline appears non-compliant (provisional): missing pillar(s): "
            f"{missing}. {DISCLAIMER} {BSEP_SIGNPOST}"
        )


@dataclass
class DeclineAssessment:
    """The provisional output of a decline-compliance check."""

    compliant: bool  # provisional: all four pillars present
    present: dict[str, list[str]] = field(default_factory=dict)
    absent_pillars: list[str] = field(default_factory=list)
    follow_ups: list[str] = field(default_factory=list)
    bsep_signpost: str = ""
    requires_human_confirmation: bool = True
    disclaimer: str = DISCLAIMER

    def as_dict(self) -> dict:
        return {
            "compliant": self.compliant,
            "provisional": True,
            "present": self.present,
            "absent_pillars": self.absent_pillars,
            "follow_ups": self.follow_ups,
            "bsep_signpost": self.bsep_signpost,
            "requires_human_confirmation": self.requires_human_confirmation,
            "disclaimer": self.disclaimer,
        }


def check_decline(text: str, *, strict: bool = False) -> DeclineAssessment:
    """Check the text of a written rejection for the four pillars.

    Returns a :class:`DeclineAssessment` listing, per pillar, the exact
    signals matched — and, for each absent pillar, the follow-up question to
    put to the institution. The result is always provisional and requires
    human confirmation.

    If ``strict=True`` and any pillar is absent, raises
    :class:`NonCompliantDeclineError` (carrying the same assessment). The
    exception is a signal for a human: on a confirmed non-compliant decline,
    the human — not this module — may choose to invoke the Burgess Sovereign
    Exit Protocol via ``tools/bgsp-exit.py``.
    """
    text = text or ""
    present: dict[str, list[str]] = {}
    absent: list[str] = []
    for pillar, patterns in _PILLAR_PATTERNS.items():
        hits = [label for label, pat in patterns if pat.search(text)]
        if hits:
            present[pillar] = hits
        else:
            absent.append(pillar)

    assessment = DeclineAssessment(
        compliant=not absent,
        present=present,
        absent_pillars=absent,
        follow_ups=[_FOLLOW_UP[p] for p in absent],
        bsep_signpost=BSEP_SIGNPOST if absent else "",
    )
    if strict and absent:
        raise NonCompliantDeclineError(assessment)
    return assessment


def _format(assessment: DeclineAssessment) -> str:
    lines = [
        "Provisional decline-compliance check "
        f"({'all four pillars present' if assessment.compliant else 'pillar(s) absent'})",
        "",
    ]
    for pillar, description in PILLARS.items():
        if pillar in assessment.present:
            lines.append(f"  [PRESENT] {pillar} — {description}")
            for label in assessment.present[pillar]:
                lines.append(f"            matched: {label}")
        else:
            lines.append(f"  [ABSENT]  {pillar} — {description}")
    if assessment.follow_ups:
        lines += ["", "Suggested follow-ups:"]
        lines += [f"  - {f}" for f in assessment.follow_ups]
    if assessment.bsep_signpost:
        lines += ["", assessment.bsep_signpost]
    lines += ["", f"NOTE: {assessment.disclaimer}"]
    return "\n".join(lines)


def main() -> None:
    """Read a written rejection from stdin and print a provisional check."""
    import sys

    print(_format(check_decline(sys.stdin.read())))


if __name__ == "__main__":
    main()
