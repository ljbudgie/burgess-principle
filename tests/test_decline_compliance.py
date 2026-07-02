"""Tests for the decline-compliance checker (four pillars of a SOVEREIGN decline)."""

from __future__ import annotations

import pytest

from iris.decline_compliance import (
    BSEP_SIGNPOST,
    DISCLAIMER,
    PILLARS,
    NonCompliantDeclineError,
    check_decline,
)

COMPLIANT_DECLINE = """
Dear Mr Burgess,

Thank you for your letter of 12 June 2026, reference DC-4471/26. You asked
us to reopen the assessment of your application.

I have personally considered your request. It falls outside our remit
because the criteria in section 4 are not met: the application window closed
before your submission was received, and the criterion of continuous
residence was not satisfied.

If you disagree, you may request a review of this decision within 28 days,
or escalate to the Ombudsman via our complaints procedure.

Yours sincerely,
Jane Smith
Head of Assessments
"""

BOILERPLATE_DECLINE = (
    "Thank you for contacting us. Unfortunately we are unable to assist "
    "with this matter. This mailbox is not monitored."
)


def test_compliant_decline_passes_all_pillars():
    result = check_decline(COMPLIANT_DECLINE)
    assert result.compliant is True
    assert result.absent_pillars == []
    assert set(result.present) == set(PILLARS)
    assert result.bsep_signpost == ""


def test_boilerplate_decline_fails_all_pillars():
    result = check_decline(BOILERPLATE_DECLINE)
    assert result.compliant is False
    assert set(result.absent_pillars) == set(PILLARS)
    assert len(result.follow_ups) == len(PILLARS)
    assert result.bsep_signpost == BSEP_SIGNPOST


def test_missing_identity_only():
    text = COMPLIANT_DECLINE.replace("Jane Smith", "the team").replace(
        "I have personally considered", "We have considered"
    )
    result = check_decline(text)
    assert "attributable_identity" in result.absent_pillars
    assert "specific_request" not in result.absent_pillars


def test_missing_signposting_only():
    text = """
    Dear Mr Burgess,
    Thank you for your letter of 12 June 2026, reference DC-4471/26.
    You asked us to reopen the assessment. I have reviewed this and it falls
    outside our remit because the section 4 criteria are not met.
    Yours sincerely, Jane Smith, Head of Assessments
    """
    result = check_decline(text)
    assert result.absent_pillars == ["assessment_signposting"]


def test_strict_mode_raises_with_assessment():
    with pytest.raises(NonCompliantDeclineError) as excinfo:
        check_decline(BOILERPLATE_DECLINE, strict=True)
    err = excinfo.value
    assert err.assessment.compliant is False
    assert DISCLAIMER in str(err)
    # The error signposts the human-owned BSEP route; it never auto-executes.
    assert "tools/bgsp-exit.py" in str(err)
    assert "human" in str(err).lower()


def test_strict_mode_does_not_raise_when_compliant():
    result = check_decline(COMPLIANT_DECLINE, strict=True)
    assert result.compliant is True


def test_always_requires_human_confirmation():
    for text in [COMPLIANT_DECLINE, BOILERPLATE_DECLINE, ""]:
        result = check_decline(text)
        assert result.requires_human_confirmation is True
        assert result.disclaimer == DISCLAIMER
        assert result.as_dict()["provisional"] is True


def test_empty_input_fails_all_pillars():
    result = check_decline("")
    assert result.compliant is False
    assert set(result.absent_pillars) == set(PILLARS)


def test_signpost_points_to_existing_bsep_tooling_not_a_payload():
    # The checker points to the existing spec and helper for a human to use;
    # it must not describe compiling or generating an exit itself.
    assert "protocols/burgess-sovereign-exit.md" in BSEP_SIGNPOST
    assert "tools/bgsp-exit.py" in BSEP_SIGNPOST
    assert "will not compile or execute" in BSEP_SIGNPOST


def test_follow_ups_match_absent_pillars():
    result = check_decline(BOILERPLATE_DECLINE)
    assert len(result.follow_ups) == len(result.absent_pillars)
    joined = " ".join(result.follow_ups)
    assert "name and role" in joined
