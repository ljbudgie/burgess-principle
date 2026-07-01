"""
Example: Email domain — inbound/outbound assessment (Phase 4A)

Scenario: an individual with an email-only reasonable adjustment writes to an
institution (outbound — a record is created), and the institution replies
(inbound — assessed on receipt). The reply is signed only "The Complaints Team",
directs the individual to log in to an online portal, and asks them to call a
telephone number to verify their identity.

Two records:
  1. OUTBOUND — the individual's own communication, recorded.
  2. INBOUND  — the institutional response, NULL on the binary test AND in
                breach of the non-negotiable accessibility requirements
                (portal redirect + telephone requirement) with no named
                individual for a significant response.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from verifiable_oversight import BinaryTest, Verifier
from verifiable_oversight.domains import EmailDomain


def _print_record(title, record, report):
    print("=" * 60)
    print(title)
    print("=" * 60)
    print(record)
    print()
    print("VERDICT:", record.verdict.value)
    print("SCORE:  ", f"{record.result.score}/5")
    print()
    print("DOMAIN METADATA:")
    for k, v in record.domain_metadata.items():
        print(f"  {k}: {v}")
    print()
    print("VALIDATION ISSUES (accessibility / procedural):")
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
    print()


def main() -> None:
    domain = EmailDomain()
    verifier = Verifier()

    # 1. OUTBOUND — the individual's own communication creates a record.
    outbound = domain.create_record(
        subject="Formal complaint — inaccessible refusal, email-only RA in place",
        institution="Example Council",
        binary_test=BinaryTest(
            context=(
                "Individual's outbound complaint. RA confirmed and recorded "
                "before this first substantive exchange."
            ),
        ),
        assessor="Lewis James Burgess",
        direction="outbound",
        ra_on_record=True,
        ra_description="email-only communication",
        ra_confirmed_before_first_substantive_exchange=True,
        first_substantive_exchange=True,
        thread_reference="THREAD-2026-0007",
        message_id="<out-0001@individual.example>",
    )
    _print_record("OUTBOUND RECORD (individual → institution)", outbound,
                  verifier.verify(outbound))

    # 2. INBOUND — the institutional response, assessed on receipt.
    inbound = domain.create_record(
        subject="Institutional reply — portal redirect + telephone verification",
        institution="Example Council",
        binary_test=BinaryTest(
            named_person=None,  # "The Complaints Team" — no named individual
            role_and_authority=None,
            specific_facts_considered=None,
            pre_decision_timing=None,
            authority_to_differ=None,
            context=(
                "Reply signed 'The Complaints Team'. Directs the individual to "
                "log in to a portal and telephone a number to verify identity. "
                "No named individual; email-only RA on record."
            ),
        ),
        assessor="Lewis James Burgess",
        direction="inbound",
        ra_on_record=True,
        ra_description="email-only communication",
        significant_response=True,
        named_individual_provided=False,
        portal_redirect=True,
        telephone_required=True,
        thread_reference="THREAD-2026-0007",
        message_id="<in-0001@council.example>",
        regulatory_framework="EA 2010 ss.20/21; LGSCO",
        notes="Permanently indexed. s.20/21 breach recorded on receipt.",
    )
    _print_record("INBOUND RECORD (institution → individual)", inbound,
                  verifier.verify(inbound))


if __name__ == "__main__":
    main()
