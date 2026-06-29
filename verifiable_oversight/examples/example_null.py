"""
Example: NULL decision record — communication domain

Scenario: EASS sends a fourth response directing a deaf complainant to the EHRC
(the body that commissioned EASS, which had already confirmed disability
discrimination). The response includes a telephone number as the contact method
for a person with an email-only reasonable adjustment on record.

Four responses across the thread — zero named individuals in any of them.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from verifiable_oversight import BinaryTest, Verifier
from verifiable_oversight.domains import CommunicationDomain


def main() -> None:
    domain = CommunicationDomain()

    record = domain.create_record(
        subject="Fourth response — circular referral to EHRC post-whistleblowing",
        institution="EASS (Equality Advisory Support Service)",
        binary_test=BinaryTest(
            named_person=None,  # "Rachel.D" — no surname, no role confirmed
            role_and_authority=None,
            specific_facts_considered=None,
            pre_decision_timing=None,
            authority_to_differ=None,
            context=(
                "Four responses across the thread. Respondent cited as 'Rachel.D' "
                "but no surname, job title, or authority level confirmed. "
                "Circular referral: EASS directed complainant to EHRC, "
                "which commissions EASS and had already confirmed disability "
                "discrimination in this case. No evidence any named individual "
                "reviewed the specific facts before the response was sent."
            ),
        ),
        decision_date="2026-06-27",
        assessor="Lewis James Burgess",
        channel="email (with telephone number provided)",
        ra_on_record=True,
        ra_description="email-only communication",
        channel_accessible=False,
        regulatory_framework="EA 2010 ss.20/21; EHRC enforcement framework",
        notes=(
            "s.136 and s.27 letters sent. EHRC whistleblowing cc'd. "
            "Telephone number (0808 800 0082) given four times across "
            "four responses to a person with a formal email-only RA. "
            "Permanently indexed."
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
    print("DOMAIN METADATA:")
    for k, v in record.domain_metadata.items():
        print(f"  {k}: {v}")
    print()
    print("VALIDATION ISSUES (domain-specific):")
    issues = record.domain_metadata.get("_validation_issues", [])
    if issues:
        for issue in issues:
            print(f"  ⚠ {issue}")
    else:
        print("  None")
    print()
    print("VERIFICATION REPORT:")
    print(report)
    print()
    print("FINGERPRINT: ", record.fingerprint[:32] + "…")


if __name__ == "__main__":
    main()
