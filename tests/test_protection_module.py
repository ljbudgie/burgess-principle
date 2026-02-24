"""
tests/test_protection_module.py — Tests for the Digital Armor protection module.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from protection_module import WarrantDefectIdentifier, SovereigntyShield, VOID_AB_INITIO, VALID


class TestWarrantDefectIdentifier:
    def setup_method(self):
        self.identifier = WarrantDefectIdentifier()

    def test_defective_warrant_is_void_ab_initio(self):
        """A warrant under the 1954 Act with a facial defect must be VOID AB INITIO."""
        warrant = {
            "act": "Rights of Entry (Gas and Electricity Boards) Act 1954",
            "facial_validity": "wrong_address",
            "date": "2026-01-15",
            "issuer": "Example Utility Company",
        }
        result = self.identifier.evaluate_warrant(warrant)
        assert result["status"] == VOID_AB_INITIO
        assert "wrong_address" in result["defects"]

    def test_valid_warrant_is_not_void(self):
        """A warrant under the 1954 Act with no defects should be VALID."""
        warrant = {
            "act": "Rights of Entry (Gas and Electricity Boards) Act 1954",
            "facial_validity": "valid",
            "date": "2026-01-15",
            "issuer": "Example Utility Company",
        }
        result = self.identifier.evaluate_warrant(warrant)
        assert result["status"] == VALID
        assert result["defects"] == []

    def test_different_act_with_defect_is_not_void_under_burgess_principle(self):
        """A warrant under a different Act is not evaluated under the Burgess Principle."""
        warrant = {
            "act": "Some Other Act 2000",
            "facial_validity": "wrong_address",
        }
        result = self.identifier.evaluate_warrant(warrant)
        assert result["status"] == VALID

    def test_multiple_defects_detected(self):
        """Multiple facial defects should all be reported."""
        warrant = {
            "act": "Rights of Entry (Gas and Electricity Boards) Act 1954",
            "facial_validity": ["wrong_address", "no_signature"],
        }
        result = self.identifier.evaluate_warrant(warrant)
        assert result["status"] == VOID_AB_INITIO
        assert "wrong_address" in result["defects"]
        assert "no_signature" in result["defects"]

    def test_no_signature_defect_is_void(self):
        """A warrant with no signature is void ab initio."""
        warrant = {
            "act": "Rights of Entry (Gas and Electricity Boards) Act 1954",
            "facial_validity": "no_signature",
        }
        result = self.identifier.evaluate_warrant(warrant)
        assert result["status"] == VOID_AB_INITIO


class TestSovereigntyShield:
    def setup_method(self):
        self.shield = SovereigntyShield()

    def test_assertion_contains_burgess_principle(self):
        text = self.shield.generate_assertion()
        assert "BURGESS PRINCIPLE" in text

    def test_assertion_contains_void_ab_initio(self):
        text = self.shield.generate_assertion()
        assert "void ab initio" in text

    def test_assertion_contains_1954_act(self):
        text = self.shield.generate_assertion()
        assert "1954" in text
