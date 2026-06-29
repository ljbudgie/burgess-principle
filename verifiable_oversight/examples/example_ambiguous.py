"""
Example: AMBIGUOUS decision record

Scenario: Trading 212 account withdrawal cap applied. Eight agents have
responded across three days. Ivan B (Onboarding & Authentication Team Lead)
has been named, but the one question that matters — 'Was the EA 2010
Schedule 2 assessment for my specific account completed before the cap was
applied?' — remains unanswered across all eight agents.

This is AMBIGUOUS, not NULL:
- A named person exists (Ivan B)
- Their role exists (Team Lead, Onboarding & Authentication)
- Whether they considered the specific facts is UNKNOWN (not confirmed absent)
- Pre-decision timing is UNKNOWN
- Authority to differ is UNKNOWN

The distinction matters legally. AMBIGUOUS = a follow-up question is required.
NULL = the institution has confirmed (by silence or denial) that no review occurred.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from verifiable_oversight import BinaryTest, Verifier
from verifiable_oversight.domains import GeneralDomain


def main() -> None:
    domain = GeneralDomain()

    record = domain.create_record(
        subject="Withdrawal cap application — EA 2010 Schedule 2 assessment question",
        institution="Trading 212 UK Ltd",
        binary_test=BinaryTest(
            named_person="Ivan B.",
            role_and_authority="Onboarding & Authentication Team Lead",
            specific_facts_considered=None,  # Unknown — question unanswered
            pre_decision_timing=None,         # Unknown — question unanswered
            authority_to_differ=None,          # Unknown — question unanswered
            context=(
                "Eight agents across three days. Ivan B. named and role confirmed. "
                "Three cards confirmed (ending 6414, 0594, 2641). "
                "Core question unanswered: 'Was an EA 2010 Schedule 2 proportionality "
                "assessment completed for my specific account before the withdrawal "
                "cap was applied?' "
                "Day 3 interest running: Sempra Metals [2007] UKHL 34 / "
                "Late Payment Act 1998 / SCA 1981 s.35A — £0.08/day on £222."
            ),
        ),
        decision_date="2026-06-25",
        assessor="Lewis James Burgess",
        ambiguous_if_missing=True,  # AMBIGUOUS because info is unavailable, not confirmed absent
        notes=(
            "Accruing interest notice served. s.94(11) DPA 2018 reserved. "
            "Zendesk ticket: WN32KP-G2EXP. Platform: trading2129704.zendesk.com. "
            "Zendesk account-matching by registered email = EA 2010 s.19 "
            "indirect discrimination — separate finding."
        ),
    )

    verifier = Verifier()
    report = verifier.verify(record)

    print("=" * 60)
    print("DECISION RECORD")
    print("=" * 60)
    print(record)
    print()
    print("VERDICT:", record.verdict.value)
    print("SCORE:  ", f"{record.result.score}/5")
    print()
    print("REASONING:")
    print(record.result.reasoning)
    print()
    print("VERIFICATION REPORT:")
    print(report)
    print()
    print("INTEGRITY OK:", report.integrity_ok)
    print("FINGERPRINT: ", record.fingerprint[:32] + "…")


if __name__ == "__main__":
    main()
