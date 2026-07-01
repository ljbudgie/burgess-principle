"""Tests for verifiable_oversight Phase 4A — the Email domain.

Covers inbound/outbound assessment, the non-negotiable accessibility
requirements (no portal redirect, no telephone, no CAPTCHA, no app-only
verification), the named-individual-for-significant-responses rule, and the
RA-confirmed-before-first-substantive-exchange rule.
"""

import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from verifiable_oversight import BinaryTest, Verdict, Verifier
from verifiable_oversight.domains import EmailDomain


def _domain() -> EmailDomain:
    return EmailDomain()


def _issues(record) -> list:
    return record.domain_metadata.get("_validation_issues", [])


def _sovereign_bt() -> BinaryTest:
    return BinaryTest(
        named_person="Rebecca Hunt",
        role_and_authority="Complaints Manager, authority to overturn",
        specific_facts_considered="Reviewed the specific facts of this case",
        pre_decision_timing="Reviewed before the response was sent",
        authority_to_differ="Held authority to reach a different outcome",
    )


def test_name_and_registration():
    assert _domain().name == "email"


def test_email_domain_exported():
    from verifiable_oversight.domains import __all__ as domain_all

    assert "EmailDomain" in domain_all


def test_outbound_record_created_and_sealed():
    record = _domain().create_record(
        subject="Outbound complaint",
        institution="Example Council",
        binary_test=BinaryTest(context="Individual's own communication."),
        direction="outbound",
        ra_on_record=True,
    )
    assert record.domain == "email"
    assert record.domain_metadata["direction"] == "outbound"
    assert record.verify_integrity()


def test_unknown_direction_flagged():
    record = _domain().create_record(
        subject="Bad direction",
        institution="X",
        binary_test=BinaryTest(context="?"),
        direction="sideways",
    )
    assert any("Unknown message direction" in i for i in _issues(record))


def test_default_direction_is_outbound():
    record = _domain().create_record(
        subject="No direction given",
        institution="X",
        binary_test=BinaryTest(context="?"),
    )
    assert record.domain_metadata["direction"] == "outbound"


@pytest.mark.parametrize(
    "flag,fragment",
    [
        ("portal_redirect", "portal"),
        ("telephone_required", "telephone"),
        ("captcha_required", "CAPTCHA"),
        ("app_only_verification", "app-only"),
    ],
)
def test_inbound_accessibility_barrier_flagged(flag, fragment):
    record = _domain().create_record(
        subject="Inbound reply with barrier",
        institution="Example Council",
        binary_test=_sovereign_bt(),
        direction="inbound",
        ra_on_record=True,
        **{flag: True},
    )
    assert any(fragment in issue for issue in _issues(record))


def test_inbound_all_barriers_recorded_even_when_false():
    record = _domain().create_record(
        subject="Clean inbound reply",
        institution="Example Council",
        binary_test=_sovereign_bt(),
        direction="inbound",
        ra_on_record=True,
    )
    md = record.domain_metadata
    for flag in (
        "portal_redirect",
        "telephone_required",
        "captcha_required",
        "app_only_verification",
    ):
        assert md[flag] is False
    assert _issues(record) == []


def test_accessibility_barrier_not_flagged_for_outbound():
    # Barrier flags only apply to inbound institutional responses.
    record = _domain().create_record(
        subject="Outbound message",
        institution="Example Council",
        binary_test=BinaryTest(context="Individual's own communication."),
        direction="outbound",
        portal_redirect=True,
        telephone_required=True,
    )
    assert _issues(record) == []


def test_significant_response_without_named_individual_flagged():
    record = _domain().create_record(
        subject="Significant inbound reply, no name",
        institution="Example Council",
        binary_test=BinaryTest(context="Signed 'The Complaints Team'."),
        direction="inbound",
        ra_on_record=True,
        significant_response=True,
        named_individual_provided=False,
    )
    assert any("named individual" in issue for issue in _issues(record))
    assert record.verdict == Verdict.NULL


def test_significant_response_with_named_individual_ok():
    record = _domain().create_record(
        subject="Significant inbound reply, named",
        institution="Example Council",
        binary_test=_sovereign_bt(),
        direction="inbound",
        ra_on_record=True,
        significant_response=True,
        named_individual_provided=True,
    )
    assert _issues(record) == []
    assert record.verdict == Verdict.SOVEREIGN


def test_non_significant_response_without_name_not_flagged():
    record = _domain().create_record(
        subject="Acknowledgement",
        institution="Example Council",
        binary_test=BinaryTest(context="Automated acknowledgement."),
        direction="inbound",
        ra_on_record=True,
        significant_response=False,
        named_individual_provided=False,
    )
    assert not any("named individual" in issue for issue in _issues(record))


def test_first_exchange_without_ra_confirmed_flagged():
    record = _domain().create_record(
        subject="First substantive exchange, RA not confirmed",
        institution="Example Council",
        binary_test=BinaryTest(context="?"),
        direction="outbound",
        ra_on_record=True,
        first_substantive_exchange=True,
        ra_confirmed_before_first_substantive_exchange=False,
    )
    assert any(
        "before the first substantive exchange" in issue for issue in _issues(record)
    )


def test_first_exchange_with_ra_confirmed_ok():
    record = _domain().create_record(
        subject="First substantive exchange, RA confirmed",
        institution="Example Council",
        binary_test=BinaryTest(context="?"),
        direction="outbound",
        ra_on_record=True,
        first_substantive_exchange=True,
        ra_confirmed_before_first_substantive_exchange=True,
    )
    assert not any(
        "before the first substantive exchange" in issue for issue in _issues(record)
    )


def test_later_exchange_does_not_require_ra_confirmation_flag():
    record = _domain().create_record(
        subject="Later exchange",
        institution="Example Council",
        binary_test=BinaryTest(context="?"),
        direction="outbound",
        ra_on_record=True,
        first_substantive_exchange=False,
    )
    assert not any(
        "before the first substantive exchange" in issue for issue in _issues(record)
    )


def test_metadata_optional_fields_preserved():
    record = _domain().create_record(
        subject="Threaded message",
        institution="Example Council",
        binary_test=_sovereign_bt(),
        direction="inbound",
        ra_on_record=True,
        ra_description="email-only communication",
        thread_reference="THREAD-1",
        message_id="<abc@example>",
        regulatory_framework="EA 2010 ss.20/21",
    )
    md = record.domain_metadata
    assert md["thread_reference"] == "THREAD-1"
    assert md["message_id"] == "<abc@example>"
    assert md["regulatory_framework"] == "EA 2010 ss.20/21"
    assert md["ra_description"] == "email-only communication"


def test_full_record_verifies():
    record = _domain().create_record(
        subject="Inbound reply",
        institution="Example Council",
        binary_test=_sovereign_bt(),
        direction="inbound",
        ra_on_record=True,
        significant_response=True,
        named_individual_provided=True,
    )
    report = Verifier().verify(record)
    assert report.is_valid
