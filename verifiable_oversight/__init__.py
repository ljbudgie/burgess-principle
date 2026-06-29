"""
Verifiable Human Oversight — top-level package.

Quick start:

    from verifiable_oversight import BinaryTest, DecisionRecord, Verifier
    from verifiable_oversight.domains import CommunicationDomain

    domain = CommunicationDomain()
    record = domain.create_record(
        subject="Complaint response from EASS",
        institution="EASS",
        binary_test=BinaryTest(
            named_person=None,
            role_and_authority=None,
            specific_facts_considered=None,
            pre_decision_timing=None,
            authority_to_differ=None,
            context="Fourth response. Circular referral to commissioning body.",
        ),
        channel="telephone",
        ra_on_record=True,
        ra_description="email-only communication",
    )

    verifier = Verifier()
    report = verifier.verify(record)
    print(record)   # [NULL] EASS — Complaint response from EASS
    print(report)   # [VALID] … integrity confirmed, all checks passed.
"""

from .core import BinaryTest, Verdict, BinaryTestResult, DecisionRecord, Verifier

__all__ = [
    "BinaryTest",
    "Verdict",
    "BinaryTestResult",
    "DecisionRecord",
    "Verifier",
]

__version__ = "0.1.0"
