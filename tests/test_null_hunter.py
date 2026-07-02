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


# --- Thread tracker (boilerplate-loop detection) ---------------------------

from iris.null_hunter import BOILERPLATE_LOOP_THRESHOLD, scan_thread  # noqa: E402

_BOILERPLATE = [
    "Thank you for contacting us. Your query is being handled in line with our policy.",
    "We have robust processes in place and your case is subject to human oversight.",
    "Your correspondence has been reviewed by the relevant team in accordance with our procedures.",
    "This is an automated acknowledgement. Your query will be processed by our system.",
]


def test_thread_loop_flags_provisional_null():
    result = scan_thread(_BOILERPLATE)
    assert result.classification == "NULL"
    assert result.confidence == "PROVISIONAL"
    assert result.boilerplate_count > BOILERPLATE_LOOP_THRESHOLD
    assert result.named_human_seen is False
    assert "boilerplate-loop" in result.basis
    assert result.requires_human_confirmation is True


def test_thread_loop_standard_form_line():
    line = scan_thread(_BOILERPLATE).standard_form()
    assert line.startswith("Classification: NULL · Confidence: PROVISIONAL")
    assert "Basis:" in line and "Would change it:" in line


def test_thread_below_threshold_stays_ambiguous():
    result = scan_thread(_BOILERPLATE[:3])
    assert result.classification == "AMBIGUOUS"
    assert result.confidence == "PROVISIONAL"


def test_named_human_prevents_thread_null():
    replies = _BOILERPLATE + [
        "Your case was reviewed by Sarah Chen, who personally considered the facts."
    ]
    result = scan_thread(replies)
    assert result.classification == "AMBIGUOUS"
    assert result.named_human_seen is True


def test_per_message_results_not_overridden():
    result = scan_thread(_BOILERPLATE)
    assert len(result.per_message) == len(_BOILERPLATE)
    # The thread-level PROVISIONAL NULL never silently rewrites the
    # per-message classifications.
    for msg in result.per_message:
        assert msg.classification in {"NULL", "AMBIGUOUS", "SOVEREIGN", "INSUFFICIENT"}
        assert msg.requires_human_confirmation is True
    assert any(m.classification == "AMBIGUOUS" for m in result.per_message)


def test_near_duplicate_replies_count_as_boilerplate():
    reply = "Dear customer, thank you for your patience while we look into this matter for you."
    result = scan_thread([reply, reply, reply, reply])
    assert result.boilerplate_count > BOILERPLATE_LOOP_THRESHOLD
    assert result.classification == "NULL"
    assert result.confidence == "PROVISIONAL"


def test_empty_thread_is_insufficient():
    result = scan_thread([])
    assert result.classification == "INSUFFICIENT"
    assert result.boilerplate_count == 0


def test_thread_as_dict_is_provisional():
    d = scan_thread(_BOILERPLATE).as_dict()
    assert d["provisional"] is True
    assert d["requires_human_confirmation"] is True
    assert len(d["per_message"]) == len(_BOILERPLATE)


def test_lowercase_team_phrase_is_not_a_named_reviewer():
    # Regression: "reviewed by the relevant team" must not match the
    # named-reviewer (SOVEREIGN) pattern via case-insensitive name matching.
    result = scan("Your case has been reviewed by the relevant team.")
    assert not result.matched.get("sovereign")
    assert result.classification == "AMBIGUOUS"
