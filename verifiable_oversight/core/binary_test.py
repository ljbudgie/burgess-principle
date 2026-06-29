"""
Binary Test Engine — the five-element SOVEREIGN/NULL assessment.

The Burgess Binary Test answers one question:
    "Was a named human being's mind applied to the specific facts
     of a specific person's case before institutional power was exercised?"

All five elements must be present for a SOVEREIGN verdict.
Any missing element yields NULL (or AMBIGUOUS if the information
is unavailable to the assessor rather than absent in practice).
"""

from __future__ import annotations

import textwrap
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class Verdict(str, Enum):
    SOVEREIGN = "SOVEREIGN"
    NULL = "NULL"
    AMBIGUOUS = "AMBIGUOUS"


@dataclass
class BinaryTest:
    """
    The five elements that constitute meaningful human review.

    Set each field to a non-empty string if the element is satisfied,
    or leave as None / empty string if it is absent or unconfirmed.

    Fields
    ------
    named_person:
        The full name of the individual who made the decision.
        "The team" or "our department" does not satisfy this element.

    role_and_authority:
        Their role AND the authority they held to reach a different
        outcome. A reviewer without power to differ is not review —
        it is ratification.

    specific_facts_considered:
        Concrete evidence that the specific facts of THIS person's
        case were considered, not just the general category of case.
        Bulk grants, templated responses, and algorithmic outputs
        do not satisfy this element without supplementary evidence.

    pre_decision_timing:
        Confirmation that the review took place BEFORE the decision
        was exercised. Post-hoc review of an automated decision is
        involvement; it is not review that could have changed the outcome.

    authority_to_differ:
        Confirmation that the named person had the practical and
        institutional authority to reach a different conclusion.
        This is distinct from role — an agent may have the role but
        not the authority if internal policy constrained the outcome.
    """

    named_person: Optional[str] = None
    role_and_authority: Optional[str] = None
    specific_facts_considered: Optional[str] = None
    pre_decision_timing: Optional[str] = None
    authority_to_differ: Optional[str] = None

    # Optional: free-text context that informs the assessment
    # but does not itself constitute an element.
    context: Optional[str] = None

    def _element_present(self, value: Optional[str]) -> bool:
        return bool(value and value.strip())

    @property
    def elements_present(self) -> dict[str, bool]:
        return {
            "named_person": self._element_present(self.named_person),
            "role_and_authority": self._element_present(self.role_and_authority),
            "specific_facts_considered": self._element_present(self.specific_facts_considered),
            "pre_decision_timing": self._element_present(self.pre_decision_timing),
            "authority_to_differ": self._element_present(self.authority_to_differ),
        }

    @property
    def score(self) -> int:
        """Number of elements satisfied (0–5)."""
        return sum(1 for v in self.elements_present.values() if v)

    def assess(self, ambiguous_if_missing: bool = False) -> "BinaryTestResult":
        """
        Run the binary test and return a BinaryTestResult.

        Parameters
        ----------
        ambiguous_if_missing:
            If True, a NULL result caused by missing information
            (rather than confirmed absence) returns AMBIGUOUS instead.
            Use this when the assessor cannot determine whether an
            element was present — e.g. the institution has not yet
            responded to a direct question about named review.
        """
        present = self.elements_present
        missing = [k for k, v in present.items() if not v]

        if not missing:
            verdict = Verdict.SOVEREIGN
            reasoning = self._sovereign_reasoning()
        elif ambiguous_if_missing:
            verdict = Verdict.AMBIGUOUS
            reasoning = self._ambiguous_reasoning(missing)
        else:
            verdict = Verdict.NULL
            reasoning = self._null_reasoning(missing)

        return BinaryTestResult(
            verdict=verdict,
            score=self.score,
            elements_present=present,
            missing_elements=missing,
            reasoning=reasoning,
        )

    def _sovereign_reasoning(self) -> str:
        lines = [
            "All five elements satisfied. SOVEREIGN.",
            f"  Named person:              {self.named_person}",
            f"  Role and authority:        {self.role_and_authority}",
            f"  Specific facts considered: {self.specific_facts_considered}",
            f"  Pre-decision timing:       {self.pre_decision_timing}",
            f"  Authority to differ:       {self.authority_to_differ}",
        ]
        if self.context:
            lines.append(f"  Context: {self.context}")
        return "\n".join(lines)

    def _null_reasoning(self, missing: list[str]) -> str:
        readable = {
            "named_person": "Named person",
            "role_and_authority": "Role and authority",
            "specific_facts_considered": "Specific facts considered",
            "pre_decision_timing": "Pre-decision timing",
            "authority_to_differ": "Authority to differ",
        }
        lines = ["NULL — the following required elements are absent:"]
        for m in missing:
            lines.append(f"  ✗ {readable[m]}")
        present = [k for k, v in self.elements_present.items() if v]
        if present:
            lines.append("Elements present:")
            for p in present:
                lines.append(f"  ✓ {readable[p]}")
        if self.context:
            lines.append(f"Context: {self.context}")
        return "\n".join(lines)

    def _ambiguous_reasoning(self, missing: list[str]) -> str:
        readable = {
            "named_person": "Named person",
            "role_and_authority": "Role and authority",
            "specific_facts_considered": "Specific facts considered",
            "pre_decision_timing": "Pre-decision timing",
            "authority_to_differ": "Authority to differ",
        }
        lines = [
            "AMBIGUOUS — information is unavailable to confirm these elements:",
        ]
        for m in missing:
            lines.append(f"  ? {readable[m]}")
        lines.append(
            textwrap.dedent("""\

            A follow-up question is always required before reclassifying
            as SOVEREIGN. Process language ('reviewed by our team',
            'subject to human oversight') does not satisfy any element.
            """)
        )
        return "\n".join(lines)


@dataclass
class BinaryTestResult:
    """Immutable result of running a BinaryTest."""

    verdict: Verdict
    score: int
    elements_present: dict[str, bool]
    missing_elements: list[str]
    reasoning: str

    def __str__(self) -> str:
        return f"[{self.verdict.value}] {self.score}/5 elements — {self.reasoning.splitlines()[0]}"
