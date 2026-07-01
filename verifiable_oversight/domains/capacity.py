"""
CapacityAssessment — Mental Capacity Act 2005 applied through the binary test.

The Mental Capacity Act 2005 (MCA) is, in effect, the binary test enacted in
statute for clinical and social-care decisions. It rests on two principles that
mirror the Burgess framework exactly:

1. **Presumption of capacity** (s.1(2)) — capacity is assumed unless evidence
   establishes otherwise. The burden is on the assessor to rebut the
   presumption, not on the individual to prove capacity.

2. **Decision and time specific** (s.2(1)) — capacity is not a general status.
   A person may have capacity to decide what to eat but not to manage finances.
   Assessment must be specific to the decision in question and to the time it is
   being made.

The binary test maps directly onto the MCA:

- SOVEREIGN: a named individual applied their mind to whether *this specific
  person* had capacity to make *this specific decision* at *this specific time*,
  following the two-stage test (s.2 diagnostic + s.3 functional).
- NULL: capacity assumed absent, or assumed present, without individual
  assessment. Or: a clinical decision-support system made the determination
  without named human review.

This module records these facts and applies the binary test. It never overrides
clinical judgment — it records whether a named clinician's judgment was applied
to the specific patient, for the specific decision, at the specific time.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from ..core.binary_test import Verdict


@dataclass
class CapacityAssessment:
    """
    Models a Mental Capacity Act 2005 capacity assessment.

    MCA s.1(2): presumption of capacity unless rebutted.
    MCA s.2(1): assessment is time-specific and decision-specific.
    MCA s.3:    functional test — can the person understand, retain,
                use/weigh, and communicate the information?
    MCA s.4:    best interests — if capacity absent, named decision-
                maker must act in the person's best interests.
    """

    # The decision in question — must be specific (s.2(1)).
    decision_in_question: str

    # Time of assessment — MCA s.2(1) requires this (ISO 8601).
    time_of_assessment: str

    # Named assessor — the binary test element.
    named_assessor: str = ""
    assessor_role: str = ""          # e.g. "Consultant Audiologist"
    assessor_qualification: str = ""  # relevant to s.3 functional test

    # MCA two-stage test.
    presumption_of_capacity: bool = True             # s.1(2) default
    diagnostic_condition_identified: bool = False    # s.2 stage 1
    functional_test_applied: bool = False            # s.3 stage 2

    # s.3 functional elements (all four must be considered).
    can_understand: Optional[bool] = None
    can_retain: Optional[bool] = None
    can_use_and_weigh: Optional[bool] = None
    can_communicate: Optional[bool] = None

    # Best interests (s.4) — only if capacity absent.
    capacity_present: Optional[bool] = None
    best_interests_decision_required: bool = False
    best_interests_named_decision_maker: str = ""
    best_interests_decision_maker_role: str = ""
    least_restrictive_option_considered: bool = False  # s.1(5)

    # Clinical AI / automated decision-support.
    automated_system_used: bool = False
    automated_system_name: str = ""     # e.g. "Phonak AutoSense OS"
    named_clinician_reviewed_output: bool = False
    # If automated_system_used=True and named_clinician_reviewed_output=False
    # → NULL finding under DUAA 2025 s.80 / UK GDPR Art.22.

    def _collect_issues(self) -> list[str]:
        """Collect all MCA / binary-test issues for this assessment."""
        issues: list[str] = []

        # Named assessor is non-negotiable.
        if not self.named_assessor:
            issues.append("No named assessor — MCA requires individual assessment")

        if not self.assessor_role:
            issues.append("Assessor role not specified")

        # Two-stage test.
        if not self.diagnostic_condition_identified and not self.functional_test_applied:
            issues.append("Neither stage of the MCA two-stage test is recorded")

        # If capacity in doubt, functional test must be applied.
        if self.diagnostic_condition_identified and not self.functional_test_applied:
            issues.append(
                "Diagnostic condition identified but functional test (s.3) not applied"
            )

        # All four functional elements must be considered.
        if self.functional_test_applied:
            for attr, label in [
                ("can_understand", "understand"),
                ("can_retain", "retain"),
                ("can_use_and_weigh", "use and weigh"),
                ("can_communicate", "communicate"),
            ]:
                if getattr(self, attr) is None:
                    issues.append(f"s.3 functional element not assessed: {label}")

        # Best interests — must have a named decision maker.
        if self.best_interests_decision_required:
            if not self.best_interests_named_decision_maker:
                issues.append(
                    "Best interests decision required (s.4) but no named "
                    "decision maker identified"
                )
            if not self.least_restrictive_option_considered:
                issues.append(
                    "s.1(5) least restrictive option not recorded as considered"
                )

        # Automated system without named clinician review.
        if self.automated_system_used and not self.named_clinician_reviewed_output:
            issues.append(
                f"Automated system '{self.automated_system_name}' used without "
                "named clinician review — potential DUAA 2025 s.80 / Art.22 issue"
            )

        return issues

    def assess(self) -> Verdict:
        """
        Apply the binary test to this capacity assessment.

        Returns SOVEREIGN, NULL, or AMBIGUOUS.

        SOVEREIGN:  a named assessor with a stated role recorded a complete,
                    issue-free two-stage assessment.
        AMBIGUOUS:  a named assessor or functional test is present, but the
                    record is incomplete — still gathering.
        NULL:       no named individual assessment (or an automated system
                    made the determination without named clinician review).
        """
        issues = self._collect_issues()

        if not issues and self.named_assessor and self.assessor_role:
            return Verdict.SOVEREIGN

        # Partially completed — still gathering.
        if self.named_assessor or self.functional_test_applied:
            return Verdict.AMBIGUOUS

        return Verdict.NULL

    def validation_issues(self) -> list[str]:
        """Return the list of issues found when applying the binary test."""
        return self._collect_issues()
