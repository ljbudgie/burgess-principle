"""Tests for the NULL Hunter advisory signal scanner."""

from __future__ import annotations

from iris.null_hunter import DISCLAIMER, scan


def test_ambiguous_process_language():
    result = scan("Thank you. Our systems are subject to human oversight.")
    assert result.classification == "AMBIGUOUS"
    assert result.matched.get("ambiguous")


def test_null_automated_processing():
    result = scan("Your application was processed automatically by our system.")
    assert result.classification == "NULL"
    assert result.matched.get("null")


def test_null_bulk_processing():
    result = scan("The warrants were uploaded in bulk via a CSV file.")
    assert result.classification == "NULL"


def test_sovereign_named_personal_review():
    result = scan(
        "Sarah Chen in our customer review team handled your case "
        "personally and recommended approval."
    )
    assert result.classification == "SOVEREIGN"
    assert result.matched.get("sovereign")


def test_named_but_weaselled_is_ambiguous():
    # A named person co-present with process language is NOT confirmation.
    result = scan("Sarah Chen personally reviewed your case in line with our policy.")
    assert result.classification == "AMBIGUOUS"


def test_insufficient_when_no_signal():
    result = scan("Thank you for your email. We will respond within 10 working days.")
    assert result.classification == "INSUFFICIENT"
    assert result.matched == {}


def test_empty_input_is_insufficient():
    assert scan("").classification == "INSUFFICIENT"


def test_always_requires_human_confirmation():
    for text in [
        "processed automatically",
        "subject to human oversight",
        "Sarah Chen personally reviewed your case",
        "hello",
    ]:
        result = scan(text)
        assert result.requires_human_confirmation is True
        assert result.disclaimer == DISCLAIMER
        assert result.as_dict()["provisional"] is True


def test_suggested_next_step_present():
    for text in ["processed automatically", "subject to human oversight", "hello"]:
        assert scan(text).suggested_next_step
