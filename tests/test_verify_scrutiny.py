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

    def test_sovereign_description(self):
        assert SOVEREIGN.description == "Individual Scrutiny Verified."

    def test_null_description(self):
        assert NULL.description == "Information Mismatch / Bulk Noise."

    def test_null_immutable(self):
        with pytest.raises(AttributeError):
            NULL.label = "CHANGED"  # type: ignore[misc]

    def test_sovereign_and_null_are_distinct(self):
        assert SOVEREIGN is not NULL
        assert SOVEREIGN != NULL

    def test_custom_result_truthy_when_value_one(self):
        custom = VerificationResult(value=1, label="X", description="Y")
        assert bool(custom) is True

    def test_custom_result_falsy_when_value_zero(self):
        custom = VerificationResult(value=0, label="X", description="Y")
        assert bool(custom) is False

    def test_custom_result_falsy_when_value_non_one(self):
        custom = VerificationResult(value=2, label="X", description="Y")
        assert bool(custom) is False

    def test_sovereign_to_dict(self):
        d = SOVEREIGN.to_dict()
        assert d == {"status": "SOVEREIGN", "code": 1, "description": "Individual Scrutiny Verified."}

    def test_null_to_dict(self):
        d = NULL.to_dict()
        assert d == {"status": "NULL", "code": 0, "description": "Information Mismatch / Bulk Noise."}

    def test_custom_to_dict(self):
        custom = VerificationResult(value=1, label="X", description="Y")
        assert custom.to_dict() == {"status": "X", "code": 1, "description": "Y"}


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

    def test_mixed_case_hash_accepted(self):
        mixed = "".join(
            c.upper() if i % 2 else c for i, c in enumerate(SAMPLE_HASH)
        )
        result = verify_instrument(SAMPLE_TEXT, mixed)
        assert result is SOVEREIGN

    def test_different_texts_produce_different_results(self):
        text_a = "Hello"
        text_b = "World"
        assert verify_instrument(text_a, _hash(text_a)) is SOVEREIGN
        assert verify_instrument(text_b, _hash(text_a)) is NULL

    def test_unicode_text_verified(self):
        text = "日本語テスト 🇬🇧"
        assert verify_instrument(text, _hash(text)) is SOVEREIGN

    def test_whitespace_only_text_is_accepted(self):
        text = "   "
        assert verify_instrument(text, _hash(text)) is SOVEREIGN

    def test_multiline_text_verified(self):
        text = "Line 1\nLine 2\nLine 3"
        assert verify_instrument(text, _hash(text)) is SOVEREIGN

    def test_very_long_text_verified(self):
        text = "x" * 100_000
        assert verify_instrument(text, _hash(text)) is SOVEREIGN


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

    def test_int_provided_hash_raises_type_error(self):
        with pytest.raises(TypeError, match="provided_hash must be a string"):
            verify_instrument(SAMPLE_TEXT, 12345)  # type: ignore[arg-type]

    def test_list_reasoning_text_raises_type_error(self):
        with pytest.raises(TypeError, match="reasoning_text must be a string"):
            verify_instrument(["text"], SAMPLE_HASH)  # type: ignore[arg-type]

    def test_hash_too_long_raises_value_error(self):
        with pytest.raises(ValueError, match="64-character hexadecimal"):
            verify_instrument(SAMPLE_TEXT, "a" * 65)

    def test_hash_63_chars_raises_value_error(self):
        with pytest.raises(ValueError, match="64-character hexadecimal"):
            verify_instrument(SAMPLE_TEXT, "a" * 63)

    def test_hash_with_spaces_raises_value_error(self):
        with pytest.raises(ValueError, match="64-character hexadecimal"):
            verify_instrument(SAMPLE_TEXT, "a" * 32 + " " * 32)

    def test_hash_with_0x_prefix_raises_value_error(self):
        with pytest.raises(ValueError, match="64-character hexadecimal"):
            verify_instrument(SAMPLE_TEXT, "0x" + "a" * 62)

    def test_bool_provided_hash_raises_type_error(self):
        with pytest.raises(TypeError, match="provided_hash must be a string"):
            verify_instrument(SAMPLE_TEXT, True)  # type: ignore[arg-type]


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

    def test_sovereign_output_has_checkmark(self, capsys):
        main([SAMPLE_TEXT, SAMPLE_HASH])
        captured = capsys.readouterr()
        assert "✅" in captured.out

    def test_null_output_has_cross(self, capsys):
        main([SAMPLE_TEXT, "a" * 64])
        captured = capsys.readouterr()
        assert "❌" in captured.out

    def test_error_output_goes_to_stderr(self, capsys):
        main(["", SAMPLE_HASH])
        captured = capsys.readouterr()
        assert "Error:" in captured.err
        assert captured.out == ""

    def test_sovereign_output_includes_description(self, capsys):
        main([SAMPLE_TEXT, SAMPLE_HASH])
        captured = capsys.readouterr()
        assert "Individual Scrutiny Verified." in captured.out

    def test_null_output_includes_description(self, capsys):
        main([SAMPLE_TEXT, "a" * 64])
        captured = capsys.readouterr()
        assert "Information Mismatch / Bulk Noise." in captured.out

    def test_sovereign_output_includes_value(self, capsys):
        main([SAMPLE_TEXT, SAMPLE_HASH])
        captured = capsys.readouterr()
        assert "(1)" in captured.out

    def test_null_output_includes_value(self, capsys):
        main([SAMPLE_TEXT, "a" * 64])
        captured = capsys.readouterr()
        assert "(0)" in captured.out

    def test_invalid_hash_exits_two(self):
        assert main([SAMPLE_TEXT, "not-a-hash"]) == 2

    def test_error_triggers_logging(self, caplog):
        import logging
        with caplog.at_level(logging.ERROR, logger="verify_scrutiny"):
            main(["", SAMPLE_HASH])
        assert "Validation error" in caplog.text


# ---------------------------------------------------------------------------
# CLI — edge cases
# ---------------------------------------------------------------------------

class TestCLIEdgeCases:
    def test_main_with_none_argv_triggers_argparse(self):
        """main(None) delegates to sys.argv; argparse errors out."""
        import sys
        original = sys.argv
        try:
            sys.argv = ["verify_scrutiny"]
            with pytest.raises(SystemExit) as exc_info:
                main(None)
            assert exc_info.value.code == 2  # argparse exits with code 2
        finally:
            sys.argv = original

    def test_invalid_hash_error_message_goes_to_stderr(self, capsys):
        main([SAMPLE_TEXT, "not-a-hash"])
        captured = capsys.readouterr()
        assert "Error:" in captured.err
        assert "64-character hexadecimal" in captured.err

    def test_type_error_from_cli_impossible_via_argparse(self):
        """argparse always passes strings, so TypeError path is not hit via CLI."""
        # Verifying that both args as strings never raise TypeError
        result = main(["any-text", "a" * 64])
        assert result in (0, 1)


# ---------------------------------------------------------------------------
# VerificationResult — edge cases
# ---------------------------------------------------------------------------

class TestVerificationResultEdgeCases:
    def test_equality_same_values(self):
        a = VerificationResult(value=1, label="SOVEREIGN", description="test")
        b = VerificationResult(value=1, label="SOVEREIGN", description="test")
        assert a == b

    def test_inequality_different_values(self):
        a = VerificationResult(value=1, label="A", description="test")
        b = VerificationResult(value=0, label="A", description="test")
        assert a != b

    def test_hashable(self):
        """Frozen dataclasses should be hashable."""
        s = {SOVEREIGN, NULL}
        assert len(s) == 2

    def test_repr_contains_fields(self):
        r = repr(SOVEREIGN)
        assert "SOVEREIGN" in r
        assert "1" in r

    def test_to_dict_returns_new_dict_each_call(self):
        d1 = SOVEREIGN.to_dict()
        d2 = SOVEREIGN.to_dict()
        assert d1 == d2
        assert d1 is not d2

    def test_negative_value_is_falsy(self):
        custom = VerificationResult(value=-1, label="X", description="Y")
        assert bool(custom) is False


# ---------------------------------------------------------------------------
# verify_instrument — additional edge cases
# ---------------------------------------------------------------------------

class TestVerifyInstrumentEdgeCases:
    def test_special_characters_verified(self):
        text = "tab\there\nnewline\r\nwindows"
        assert verify_instrument(text, _hash(text)) is SOVEREIGN

    def test_null_byte_in_text(self):
        text = "before\x00after"
        assert verify_instrument(text, _hash(text)) is SOVEREIGN

    def test_empty_hash_raises_value_error(self):
        with pytest.raises(ValueError, match="64-character hexadecimal"):
            verify_instrument(SAMPLE_TEXT, "")

    def test_bytes_reasoning_text_raises_type_error(self):
        with pytest.raises(TypeError, match="reasoning_text must be a string"):
            verify_instrument(b"bytes", SAMPLE_HASH)  # type: ignore[arg-type]

    def test_dict_reasoning_text_raises_type_error(self):
        with pytest.raises(TypeError, match="reasoning_text must be a string"):
            verify_instrument({"key": "val"}, SAMPLE_HASH)  # type: ignore[arg-type]

    def test_float_provided_hash_raises_type_error(self):
        with pytest.raises(TypeError, match="provided_hash must be a string"):
            verify_instrument(SAMPLE_TEXT, 3.14)  # type: ignore[arg-type]

    def test_bytes_provided_hash_raises_type_error(self):
        with pytest.raises(TypeError, match="provided_hash must be a string"):
            verify_instrument(SAMPLE_TEXT, b"abc")  # type: ignore[arg-type]

    def test_single_character_text_verified(self):
        text = "x"
        assert verify_instrument(text, _hash(text)) is SOVEREIGN

    def test_hash_with_newline_raises_value_error(self):
        with pytest.raises(ValueError, match="64-character hexadecimal"):
            verify_instrument(SAMPLE_TEXT, "a" * 63 + "\n")

    def test_all_zero_hash_returns_null(self):
        result = verify_instrument(SAMPLE_TEXT, "0" * 64)
        assert result is NULL

    def test_all_f_hash_returns_null(self):
        result = verify_instrument(SAMPLE_TEXT, "f" * 64)
        assert result is NULL

    def test_idempotent_calls(self):
        """Calling verify_instrument twice with same args gives same result."""
        r1 = verify_instrument(SAMPLE_TEXT, SAMPLE_HASH)
        r2 = verify_instrument(SAMPLE_TEXT, SAMPLE_HASH)
        assert r1 is r2
