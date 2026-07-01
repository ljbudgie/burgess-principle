"""
Example: Mental Capacity Act 2005 capacity domain (Phase 5)

Three decisions:
  1. Phonak AutoSense OS adjusts a hearing profile automatically, with no named
     audiologist reviewing the specific patient's response — NULL, engaging
     DUAA 2025 s.80 / UK GDPR Art.22 and MCA s.2(1).
  2. An NHS best-interests decision for a patient who lacks capacity, made by a
     named decision-maker who considered the least restrictive option —
     SOVEREIGN.
  3. A consent-to-treatment capacity assessment recorded by a named clinician,
     two-stage test complete — SOVEREIGN.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from verifiable_oversight.core.binary_test import Verdict
from verifiable_oversight.domains.capacity import CapacityAssessment


def _print(title, assessment):
    verdict = assessment.assess()
    print("=" * 64)
    print(title)
    print("=" * 64)
    print("DECISION:", assessment.decision_in_question)
    print("TIME:    ", assessment.time_of_assessment)
    print("VERDICT: ", verdict.value)
    print("FINDINGS:")
    for issue in assessment.validation_issues() or ["  None"]:
        print(f"  ⚠ {issue}")
    print()


def main() -> None:
    # 1. Phonak AutoSense OS — automated adjustment, no named clinician review.
    phonak = CapacityAssessment(
        decision_in_question=(
            "Adjustment of hearing aid programme for patient with bilateral "
            "sensorineural high-frequency sloping loss, PTAs ~68-70 dB HL"
        ),
        time_of_assessment="2026-07-01T00:00:00Z",
        automated_system_used=True,
        automated_system_name="Phonak AutoSense OS 5.0",
        named_clinician_reviewed_output=False,
    )
    assert phonak.assess() == Verdict.NULL
    _print("1. Phonak AutoSense OS — no named clinician review (NULL)", phonak)

    # 2. NHS best-interests decision, named decision-maker, least restrictive.
    best_interests = CapacityAssessment(
        decision_in_question="Consent to elective hip replacement surgery",
        time_of_assessment="2026-07-01T09:30:00Z",
        named_assessor="Dr Amara Okoye",
        assessor_role="Consultant Geriatrician",
        assessor_qualification="MB ChB, MRCP",
        diagnostic_condition_identified=True,
        functional_test_applied=True,
        can_understand=False,
        can_retain=False,
        can_use_and_weigh=False,
        can_communicate=True,
        capacity_present=False,
        best_interests_decision_required=True,
        best_interests_named_decision_maker="Dr Amara Okoye",
        best_interests_decision_maker_role="Consultant Geriatrician",
        least_restrictive_option_considered=True,
    )
    assert best_interests.assess() == Verdict.SOVEREIGN
    _print("2. NHS best-interests decision — named decision-maker (SOVEREIGN)", best_interests)

    # 3. Consent-to-treatment capacity assessment, two-stage test complete.
    consent = CapacityAssessment(
        decision_in_question="Consent to fitting of behind-the-ear hearing aids",
        time_of_assessment="2026-07-01T14:00:00Z",
        named_assessor="Priya Sharma",
        assessor_role="Consultant Audiologist",
        assessor_qualification="BSc Audiology, RCCP registered",
        diagnostic_condition_identified=True,
        functional_test_applied=True,
        can_understand=True,
        can_retain=True,
        can_use_and_weigh=True,
        can_communicate=True,
        capacity_present=True,
    )
    assert consent.assess() == Verdict.SOVEREIGN
    _print("3. Consent-to-treatment capacity assessment (SOVEREIGN)", consent)


if __name__ == "__main__":
    main()
