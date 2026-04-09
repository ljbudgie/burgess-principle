"""Tests for the Burgess Principle Binary Test (verify_scrutiny)."""

import hashlib

import pytest

from verify_scrutiny import (
    NULL,
    SOVEREIGN,
    VerificationResult,
    main,
    verify_instrument,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _hash(text: str) -> str:
    """Return the SHA-256 hex-digest of *text*."""
    return hashlib.sha256(text.encode()).hexdigest()


SAMPLE_TEXT = "Was a human member of the team able to personally review the specific facts of my situation?"
SAMPLE_HASH = _hash(SAMPLE_TEXT)


# ---------------------------------------------------------------------------
# VerificationResult
# ---------------------------------------------------------------------------

class TestVerificationResult:
    def test_sovereign_is_truthy(self):
        assert bool(SOVEREIGN) is True

    def test_null_is_falsy(self):
        assert bool(NULL) is False

    def test_sovereign_value(self):
        assert SOVEREIGN.value == 1
        assert SOVEREIGN.label == "SOVEREIGN"

    def test_null_value(self):
        assert NULL.value == 0
        assert NULL.label == "NULL"

    def test_immutable(self):
        with pytest.raises(AttributeError):
            SOVEREIGN.value = 42  # type: ignore[misc]


# ---------------------------------------------------------------------------
# verify_instrument — happy path
# ---------------------------------------------------------------------------

class TestVerifyInstrumentHappyPath:
    def test_matching_hash_returns_sovereign(self):
        result = verify_instrument(SAMPLE_TEXT, SAMPLE_HASH)
        assert result is SOVEREIGN
        assert result.value == 1

    def test_mismatched_hash_returns_null(self):
        wrong_hash = "a" * 64
        result = verify_instrument(SAMPLE_TEXT, wrong_hash)
        assert result is NULL
        assert result.value == 0

    def test_uppercase_hash_accepted(self):
        result = verify_instrument(SAMPLE_TEXT, SAMPLE_HASH.upper())
        assert result is SOVEREIGN


# ---------------------------------------------------------------------------
# verify_instrument — input validation
# ---------------------------------------------------------------------------

class TestVerifyInstrumentValidation:
    def test_none_reasoning_text_raises_type_error(self):
        with pytest.raises(TypeError, match="reasoning_text must be a string"):
            verify_instrument(None, SAMPLE_HASH)  # type: ignore[arg-type]

    def test_int_reasoning_text_raises_type_error(self):
        with pytest.raises(TypeError, match="reasoning_text must be a string"):
            verify_instrument(123, SAMPLE_HASH)  # type: ignore[arg-type]

    def test_none_provided_hash_raises_type_error(self):
        with pytest.raises(TypeError, match="provided_hash must be a string"):
            verify_instrument(SAMPLE_TEXT, None)  # type: ignore[arg-type]

    def test_empty_reasoning_text_raises_value_error(self):
        with pytest.raises(ValueError, match="must not be empty"):
            verify_instrument("", SAMPLE_HASH)

    def test_short_hash_raises_value_error(self):
        with pytest.raises(ValueError, match="64-character hexadecimal"):
            verify_instrument(SAMPLE_TEXT, "abc123")

    def test_non_hex_hash_raises_value_error(self):
        with pytest.raises(ValueError, match="64-character hexadecimal"):
            verify_instrument(SAMPLE_TEXT, "g" * 64)


# ---------------------------------------------------------------------------
# CLI (main)
# ---------------------------------------------------------------------------

class TestCLI:
    def test_matching_hash_exits_zero(self):
        assert main([SAMPLE_TEXT, SAMPLE_HASH]) == 0

    def test_mismatched_hash_exits_one(self):
        assert main([SAMPLE_TEXT, "a" * 64]) == 1

    def test_invalid_input_exits_two(self):
        assert main(["", SAMPLE_HASH]) == 2

    def test_output_contains_sovereign(self, capsys):
        main([SAMPLE_TEXT, SAMPLE_HASH])
        captured = capsys.readouterr()
        assert "SOVEREIGN" in captured.out

    def test_output_contains_null(self, capsys):
        main([SAMPLE_TEXT, "a" * 64])
        captured = capsys.readouterr()
        assert "NULL" in captured.out
