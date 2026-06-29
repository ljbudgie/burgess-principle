"""
Example: SOVEREIGN decision record

Scenario: LGO investigator Rebecca Hunt signs and returns a review letter
personally, engaging with the specific facts of case 26 000 967.

The process is SOVEREIGN even though her legal analysis was wrong —
the binary test records process, not outcome. A named individual applied
their mind to specific facts before the decision. That is what SOVEREIGN means.

Challenging the legal analysis is a separate question (e.g. FirstGroup v Paulley
misapplication) — addressed by substantive appeal, not by reclassifying the process.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from verifiable_oversight import BinaryTest, Verifier
from verifiable_oversight.domains import LegalDomain


def main() -> None:
    domain = LegalDomain()

    record = domain.create_record(
        subject="Review letter — LGO case 26 000 967 (DBC reasonable adjustments)",
        institution="Local Government Ombudsman (LGO)",
        binary_test=BinaryTest(
            named_person="Rebecca Hunt",
            role_and_authority=(
                "LGO Investigator — authority to uphold, not uphold, or refer "
                "the complaint to the Ombudsman for further consideration."
            ),
            specific_facts_considered=(
                "Signed review letter personally addresses the specific DBC complaint: "
                "two complaint responses by email found to constitute reasonable "
                "adjustments. Five items of new information present in the case file."
            ),
            pre_decision_timing=(
                "Review letter dated and signed before the finding was communicated "
                "to the complainant. Decision issued 25 June 2026."
            ),
            authority_to_differ=(
                "LGO investigators have authority to uphold, partially uphold, or "
                "not uphold complaints. Rebecca Hunt had authority to reach a "
                "different finding on the anticipatory duty question."
            ),
            context=(
                "Legal analysis disputed — FirstGroup v Paulley [2017] UKSC 4 "
                "misapplied (policy compliance vs individual circumstances). "
                "Five pillars of new information not engaged. "
                "SOVEREIGN classification records process, not correctness of outcome."
            ),
        ),
        decision_date="2026-06-25",
        assessor="Lewis James Burgess",
        case_reference="LGO 26 000 967",
        decision_type="ombudsman",
        statutory_basis="Local Government Act 1974 Part III",
        case_law_anchors=[
            "FirstGroup plc v Paulley [2017] UKSC 4",
            "ZH (Tanzania) v SSHD [2011] UKSC 4",
        ],
        notes=(
            "SOVEREIGN on process. Legal challenge proceeds separately: "
            "five-pillar new information letter sent; FirstGroup v Paulley "
            "anticipatory duty misapplication documented."
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
    print()
    print("FULL JSON:")
    print(record.to_json())


if __name__ == "__main__":
    main()
