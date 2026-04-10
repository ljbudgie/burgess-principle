"""Tests for the optional FastAPI wrapper (api.py).

These tests require the ``api`` optional dependency group::

    pip install -e ".[api]"

They are automatically skipped when FastAPI is not installed.
"""

import hashlib

import pytest

fastapi = pytest.importorskip("fastapi")
httpx = pytest.importorskip("httpx")

from starlette.testclient import TestClient  # noqa: E402

from api import app  # noqa: E402

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
