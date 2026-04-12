"""Tests for the sovereign hub example application."""

from __future__ import annotations

import base64
import importlib.util
import json
import sys
from pathlib import Path

import pytest
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parent.parent
MODULE_PATH = ROOT / "sovereign-hub-example" / "app.py"


def _load_module(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, *, name: str) -> object:
    monkeypatch.setenv("HUB_DATA_DIR", str(tmp_path / "hub-data"))
    monkeypatch.setenv("HUB_SHARED_SECRET", "0123456789abcdef0123456789abcdef")
    monkeypatch.setenv("HUB_SIGNING_SEED_HEX", "11" * 32)
    monkeypatch.setenv("HUB_SERVER_ID", "test-hub")

    spec = importlib.util.spec_from_file_location(name, MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    module.PBKDF2_ITERATIONS = 1
    return module


@pytest.fixture
def hub_module(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    return _load_module(tmp_path, monkeypatch, name=f"sovereign_hub_{tmp_path.name}")


def _salt_b64() -> str:
    return base64.b64encode(b"0123456789abcdef").decode("utf-8")


def _public_key_hex(private_key: Ed25519PrivateKey) -> str:
    return private_key.public_key().public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw,
    ).hex()


def test_import_requires_long_shared_secret(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("HUB_DATA_DIR", str(tmp_path / "hub-data"))
    monkeypatch.setenv("HUB_SHARED_SECRET", "short-secret")
    monkeypatch.setenv("HUB_SIGNING_SEED_HEX", "11" * 32)

    spec = importlib.util.spec_from_file_location(
        f"sovereign_hub_invalid_{tmp_path.name}",
        MODULE_PATH,
    )
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module

    with pytest.raises(RuntimeError, match="HUB_SHARED_SECRET"):
        spec.loader.exec_module(module)


def test_canonicalize_sorts_nested_dict_keys(hub_module):
    value = {"z": [3, {"b": 2, "a": 1}], "a": {"d": 4, "c": 3}}

    assert hub_module.canonicalize(value) == '{"a":{"c":3,"d":4},"z":[3,{"a":1,"b":2}]}'


def test_encrypt_and_decrypt_envelope_round_trip(hub_module):
    payload = {"claims": [{"commitment_hash": "claim-1"}], "direction": "push"}

    encrypted = hub_module.encrypt_envelope(payload, {"salt": _salt_b64()})

    assert hub_module.decrypt_envelope(encrypted) == payload


def test_merge_unique_replaces_duplicates_and_sorts(hub_module):
    merged = hub_module.merge_unique(
        [
            {"id": "b", "created_at": "2026-04-02T00:00:00Z", "value": "old"},
            {"id": "a", "created_at": "2026-04-01T00:00:00Z", "value": "first"},
        ],
        [
            {"id": "b", "created_at": "2026-04-03T00:00:00Z", "value": "new"},
            {"id": "c", "created_at": "2026-04-04T00:00:00Z", "value": "last"},
            {"created_at": "2026-04-05T00:00:00Z", "value": "ignored"},
        ],
        "id",
    )

    assert merged == [
        {"id": "a", "created_at": "2026-04-01T00:00:00Z", "value": "first"},
        {"id": "b", "created_at": "2026-04-03T00:00:00Z", "value": "new"},
        {"id": "c", "created_at": "2026-04-04T00:00:00Z", "value": "last"},
    ]


def test_hello_and_sync_endpoints_round_trip_state(hub_module):
    client = TestClient(hub_module.app)

    hello = client.get("/api/hub/hello")
    assert hello.status_code == 200
    assert hello.json()["server_id"] == "test-hub"
    assert hello.json()["public_key_hex"] == hub_module.public_key_hex

    signed_request = {"cursor": "", "request_id": "req-1"}
    client_key = Ed25519PrivateKey.generate()
    envelope = hub_module.encrypt_envelope(
        {
            "direction": "push",
            "exported_at": "2026-04-12T20:00:00.000000Z",
            "memory_root": {"root_commitment_hash": "root-1"},
            "claims": [{"commitment_hash": "claim-1", "created_at": "2026-04-12T20:00:01.000000Z"}],
            "triggers": [{"id": "trigger-1", "created_at": "2026-04-12T20:00:02.000000Z"}],
        },
        {"salt": _salt_b64()},
    )
    response = client.post(
        "/api/sovereign-sync-v2",
        json={
            "envelope": envelope,
            "signed_request": signed_request,
            "client_signature": {
                "device_id": "device-1",
                "public_key_hex": _public_key_hex(client_key),
                "signature_hex": client_key.sign(
                    hub_module.canonicalize(signed_request).encode("utf-8")
                ).hex(),
            },
        },
    )

    assert response.status_code == 200
    body = response.json()
    decrypted = hub_module.decrypt_envelope(body["payload"])
    saved_state = json.loads(hub_module.STATE_PATH.read_text(encoding="utf-8"))

    assert body["public_key_hex"] == hub_module.public_key_hex
    assert decrypted["received"] == 3
    assert decrypted["audit_event"]["device_id"] == "device-1"
    assert saved_state["cursor"] == decrypted["next_cursor"]
    assert saved_state["memory_roots"] == [
        {
            "root_commitment_hash": "root-1",
            "created_at": "2026-04-12T20:00:00.000000Z",
        }
    ]
    assert saved_state["claim_commitments"] == [
        {"commitment_hash": "claim-1", "created_at": "2026-04-12T20:00:01.000000Z"}
    ]
    assert saved_state["trigger_heads"] == [
        {"id": "trigger-1", "created_at": "2026-04-12T20:00:02.000000Z"}
    ]
    assert saved_state["audit_log"][0]["summary"] == (
        "Processed 1 claim commitments and 1 trigger digests."
    )


def test_sync_rejects_invalid_client_signature(hub_module):
    client = TestClient(hub_module.app)
    response = client.post(
        "/api/sovereign-sync-v2",
        json={
            "envelope": hub_module.encrypt_envelope({"claims": []}, {"salt": _salt_b64()}),
            "signed_request": {"cursor": ""},
            "client_signature": {
                "device_id": "device-1",
                "public_key_hex": "22" * 32,
                "signature_hex": "00",
            },
        },
    )

    assert response.status_code == 401
    assert "Invalid client signature" in response.json()["detail"]
