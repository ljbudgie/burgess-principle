"""
Example: Iris mid-conversation assessment (Phase 4C)

Scenario: a user tells Iris, a piece at a time, about a complaint response.
Iris assesses what it has so far (AMBIGUOUS while gathering), asks the next
question, and — once the user confirms no named individual was ever provided —
finalises a definitive NULL record onto the tamper-evident ledger.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from verifiable_oversight import BinaryTest, RecordStore
from verifiable_oversight.domains import CommunicationDomain
from verifiable_oversight.integrations import ConversationAssessor


def main() -> None:
    store = RecordStore()  # in-memory for the demo
    assessor = ConversationAssessor(CommunicationDomain(), store=store)

    print("=" * 60)
    print("TURN 1 — user describes the response (nothing named yet)")
    print("=" * 60)
    step = assessor.assess(
        subject="Complaint response from EASS",
        institution="EASS",
        binary_test=BinaryTest(
            context="Response signed 'Rachel.D' — no surname, no role.",
        ),
        channel="email",
        ra_on_record=True,
        ra_description="email-only communication",
    )
    print("Verdict:", step.verdict.value, "| complete:", step.complete)
    print("Iris asks next:")
    for q in step.follow_up_questions:
        print("  •", q)
    print()

    print("=" * 60)
    print("TURN 2 — user confirms no named individual was ever provided")
    print("=" * 60)
    final = assessor.finalise(
        subject="Complaint response from EASS",
        institution="EASS",
        binary_test=BinaryTest(
            context="User confirms: no full name, role, or authority was ever "
            "given across the whole thread.",
        ),
        assessor="Lewis James Burgess",
        channel="email",
        ra_on_record=True,
        ra_description="email-only communication",
    )
    print("Verdict:", final.verdict.value, "| finalised:", final.finalised)
    print("Ledger length:", len(store))
    print("Chain intact:", store.verify_chain())
    print()
    print("FINGERPRINT:", final.record.fingerprint[:32] + "…")


if __name__ == "__main__":
    main()
