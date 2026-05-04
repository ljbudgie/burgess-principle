"""Tests for the optional FastAPI wrapper (api.py).

These tests require the ``api`` optional dependency group::

    pip install -e ".[api]"

They are automatically skipped when FastAPI is not installed.
"""

import hashlib
import os
import sys

import pytest

fastapi = pytest.importorskip("fastapi")
httpx = pytest.importorskip("httpx")

from starlette.testclient import TestClient  # noqa: E402

from api import app  # noqa: E402

# Ensure the on-chain SDK is importable for claims tests.
sys.path.insert(
    0, os.path.join(os.path.dirname(__file__), "..", "onchain-protocol", "sdk")
)

SAMPLE_TEXT = "Was a human member of the team able to personally review the specific facts of my situation?"
SAMPLE_HASH = hashlib.sha256(SAMPLE_TEXT.encode()).hexdigest()


@pytest.fixture()
def client():
    return TestClient(app)


class TestVerifyEndpoint:
    def test_matching_hash_returns_sovereign(self, client):
        resp = client.post(
            "/verify",
            json={"reasoning_text": SAMPLE_TEXT, "provided_hash": SAMPLE_HASH},
        )
        assert resp.status_code == 200
        body = resp.json()
        assert body["status"] == "SOVEREIGN"
        assert body["code"] == 1

    def test_mismatched_hash_returns_null(self, client):
        resp = client.post(
            "/verify",
            json={"reasoning_text": SAMPLE_TEXT, "provided_hash": "a" * 64},
        )
        assert resp.status_code == 200
        body = resp.json()
        assert body["status"] == "NULL"
        assert body["code"] == 0

    def test_empty_text_returns_422(self, client):
        resp = client.post(
            "/verify",
            json={"reasoning_text": "", "provided_hash": SAMPLE_HASH},
        )
        assert resp.status_code == 422

    def test_invalid_hash_format_returns_422(self, client):
        resp = client.post(
            "/verify",
            json={"reasoning_text": SAMPLE_TEXT, "provided_hash": "not-a-hash"},
        )
        assert resp.status_code == 422

    def test_missing_fields_returns_422(self, client):
        resp = client.post("/verify", json={})
        assert resp.status_code == 422

    def test_response_includes_description(self, client):
        resp = client.post(
            "/verify",
            json={"reasoning_text": SAMPLE_TEXT, "provided_hash": SAMPLE_HASH},
        )
        body = resp.json()
        assert body["description"] == "Individual Scrutiny Verified."

    def test_null_response_includes_description(self, client):
        resp = client.post(
            "/verify",
            json={"reasoning_text": SAMPLE_TEXT, "provided_hash": "b" * 64},
        )
        body = resp.json()
        assert body["description"] == "Information Mismatch / Bulk Noise."

    def test_uppercase_hash_returns_sovereign(self, client):
        resp = client.post(
            "/verify",
            json={"reasoning_text": SAMPLE_TEXT, "provided_hash": SAMPLE_HASH.upper()},
        )
        assert resp.status_code == 200
        assert resp.json()["status"] == "SOVEREIGN"

    def test_missing_reasoning_text_returns_422(self, client):
        resp = client.post(
            "/verify",
            json={"provided_hash": SAMPLE_HASH},
        )
        assert resp.status_code == 422

    def test_missing_provided_hash_returns_422(self, client):
        resp = client.post(
            "/verify",
            json={"reasoning_text": SAMPLE_TEXT},
        )
        assert resp.status_code == 422

    def test_extra_fields_are_ignored(self, client):
        resp = client.post(
            "/verify",
            json={
                "reasoning_text": SAMPLE_TEXT,
                "provided_hash": SAMPLE_HASH,
                "extra_field": "should be ignored",
            },
        )
        assert resp.status_code == 200
        assert resp.json()["status"] == "SOVEREIGN"

    def test_get_method_not_allowed(self, client):
        resp = client.get("/verify")
        assert resp.status_code == 405

    def test_hash_too_short_returns_422(self, client):
        resp = client.post(
            "/verify",
            json={"reasoning_text": SAMPLE_TEXT, "provided_hash": "abc123"},
        )
        assert resp.status_code == 422

    def test_hash_too_long_returns_422(self, client):
        resp = client.post(
            "/verify",
            json={"reasoning_text": SAMPLE_TEXT, "provided_hash": "a" * 65},
        )
        assert resp.status_code == 422

    def test_non_hex_hash_returns_422(self, client):
        resp = client.post(
            "/verify",
            json={"reasoning_text": SAMPLE_TEXT, "provided_hash": "g" * 64},
        )
        assert resp.status_code == 422

    def test_response_keys(self, client):
        resp = client.post(
            "/verify",
            json={"reasoning_text": SAMPLE_TEXT, "provided_hash": SAMPLE_HASH},
        )
        body = resp.json()
        assert set(body.keys()) == {"status", "code", "description"}

    def test_unicode_text_via_api(self, client):
        text = "日本語テスト 🇬🇧"
        text_hash = hashlib.sha256(text.encode()).hexdigest()
        resp = client.post(
            "/verify",
            json={"reasoning_text": text, "provided_hash": text_hash},
        )
        assert resp.status_code == 200
        assert resp.json()["status"] == "SOVEREIGN"


class TestScrutinyAssessmentEndpoint:
    def test_confirmed_pre_action_review_returns_sovereign(self, client):
        resp = client.post(
            "/scrutiny/assess",
            json={
                "reviewer_name": "Alice Example",
                "reviewer_role": "Appeals officer",
                "specific_facts_reviewed": True,
                "review_timing": "before_action",
                "review_notes": "Reviewed the specific facts before action.",
            },
        )
        assert resp.status_code == 200
        body = resp.json()
        assert body["status"] == "SOVEREIGN"
        assert body["code"] == 1
        assert "Was a human member of the team" in body["question"]
        assert "Proceed only" in body["required_action"]

    def test_confirmed_no_review_returns_null(self, client):
        resp = client.post(
            "/scrutiny/assess",
            json={
                "specific_facts_reviewed": False,
                "review_timing": "before_action",
            },
        )
        assert resp.status_code == 200
        body = resp.json()
        assert body["status"] == "NULL"
        assert body["code"] == 0
        assert "Block the decision" in body["required_action"]

    def test_vague_process_language_returns_ambiguous(self, client):
        resp = client.post(
            "/scrutiny/assess",
            json={
                "reviewer_name": "Case team",
                "reviewer_role": "Human oversight",
                "specific_facts_reviewed": True,
                "review_timing": "before_action",
                "review_notes": "Reviewed in line with policy.",
            },
        )
        assert resp.status_code == 200
        body = resp.json()
        assert body["status"] == "AMBIGUOUS"
        assert body["code"] == -1
        assert "Ask for a direct yes or no" in body["required_action"]

    def test_unknown_payload_returns_ambiguous(self, client):
        resp = client.post("/scrutiny/assess", json={})
        assert resp.status_code == 200
        assert resp.json()["status"] == "AMBIGUOUS"

    def test_invalid_review_timing_returns_422(self, client):
        resp = client.post(
            "/scrutiny/assess",
            json={"review_timing": "eventually"},
        )
        assert resp.status_code == 422


# ---------------------------------------------------------------------------
# /claims/verify endpoint
# ---------------------------------------------------------------------------


class TestClaimVerifyEndpoint:
    @pytest.fixture(autouse=True)
    def _setup(self):
        from nacl.signing import SigningKey
        from onchain_claims import generate_onchain_claim

        sk = SigningKey.generate()
        self.private_key = sk.encode().hex()
        self.public_key = sk.verify_key.encode().hex()
        self.claim = generate_onchain_claim(
            claim_details="API test claim",
            target_entity="Test Org",
            category="enforcement",
            private_key_hex=self.private_key,
        )

    def test_valid_claim_returns_true(self, client):
        resp = client.post(
            "/claims/verify",
            json={
                "commitment_hash": self.claim.commitment_hash,
                "signature": self.claim.signature,
                "public_key_hex": self.claim.public_key,
            },
        )
        assert resp.status_code == 200
        body = resp.json()
        assert body["valid"] is True
        assert body["commitment_hash"] == self.claim.commitment_hash

    def test_invalid_signature_returns_false(self, client):
        resp = client.post(
            "/claims/verify",
            json={
                "commitment_hash": self.claim.commitment_hash,
                "signature": "aa" * 64,
                "public_key_hex": self.claim.public_key,
            },
        )
        assert resp.status_code == 200
        assert resp.json()["valid"] is False

    def test_missing_fields_returns_422(self, client):
        resp = client.post("/claims/verify", json={})
        assert resp.status_code == 422

    def test_invalid_hash_format_returns_422(self, client):
        resp = client.post(
            "/claims/verify",
            json={
                "commitment_hash": "not-a-hash",
                "signature": "aa" * 64,
                "public_key_hex": self.claim.public_key,
            },
        )
        assert resp.status_code == 422

    def test_response_keys(self, client):
        resp = client.post(
            "/claims/verify",
            json={
                "commitment_hash": self.claim.commitment_hash,
                "signature": self.claim.signature,
                "public_key_hex": self.claim.public_key,
            },
        )
        body = resp.json()
        assert set(body.keys()) == {"valid", "commitment_hash", "public_key", "details"}
