"""Tests for scripts/generate_pwa_update_manifest.py."""

from __future__ import annotations

import argparse
import base64
import hashlib
import importlib.util
import json
from pathlib import Path

import pytest
from nacl.signing import SigningKey


_MODULE_PATH = (
    Path(__file__).resolve().parents[1]
    / "scripts"
    / "generate_pwa_update_manifest.py"
)
_SPEC = importlib.util.spec_from_file_location(
    "generate_pwa_update_manifest",
    _MODULE_PATH,
)
_MODULE = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(_MODULE)


def _write_repo_asset(repo_root: Path, web_path: str, content: bytes) -> None:
    relative = "index.html" if web_path == "/" else web_path.lstrip("/")
    path = repo_root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(content)


def test_canonicalize_sorts_dict_keys_and_preserves_lists():
    value = {"b": [2, {"z": 1, "a": "x"}], "a": True}

    assert _MODULE.canonicalize(value) == (
        '{"a":true,"b":[2,{"a":"x","z":1}]}'
    )


def test_materialize_path_maps_root_to_index():
    repo_root = Path("/tmp/example")

    assert _MODULE.materialize_path(repo_root, "/") == repo_root / "index.html"
    assert _MODULE.materialize_path(repo_root, "/service-worker.js") == (
        repo_root / "service-worker.js"
    )


def test_main_writes_signed_manifest(monkeypatch, tmp_path):
    signing_key = SigningKey.generate()
    seed_hex = signing_key.encode().hex()

    for web_path in _MODULE.DEFAULT_PATHS:
        content = f"asset:{web_path}".encode("utf-8")
        if web_path == "/banner.png":
            content = b"\x89PNG\r\nasset"
        _write_repo_asset(tmp_path, web_path, content)

    monkeypatch.setattr(
        _MODULE,
        "parse_args",
        lambda: argparse.Namespace(
            repo_root=tmp_path,
            version="9.9.9",
            seed_hex=seed_hex,
            output="custom-manifest.json",
            key_id="test-key-id",
        ),
    )

    _MODULE.main()

    manifest = json.loads((tmp_path / "custom-manifest.json").read_text(encoding="utf-8"))
    assert manifest["key_id"] == "test-key-id"
    assert manifest["public_key_hex"] == signing_key.verify_key.encode().hex()

    payload = manifest["signed_payload"]
    assert payload["app_id"] == "iris-sovereign-pwa"
    assert payload["version"] == "9.9.9"
    assert payload["hash_algorithm"] == "sha256"
    assert payload["consent_required"] is True
    assert payload["critical_paths"] == _MODULE.DEFAULT_PATHS
    assert payload["issued_at"].endswith("Z")

    assets_by_path = {asset["path"]: asset["sha256"] for asset in payload["assets"]}
    assert set(assets_by_path) == set(_MODULE.DEFAULT_PATHS)
    for web_path in _MODULE.DEFAULT_PATHS:
        path = _MODULE.materialize_path(tmp_path, web_path)
        assert assets_by_path[web_path] == hashlib.sha256(path.read_bytes()).hexdigest()

    signature = base64.b64decode(manifest["signature"])
    verified_payload = signing_key.verify_key.verify(
        _MODULE.canonicalize(payload).encode("utf-8"),
        signature,
    )
    assert verified_payload == _MODULE.canonicalize(payload).encode("utf-8")


def test_main_raises_when_required_asset_is_missing(monkeypatch, tmp_path):
    signing_key = SigningKey.generate()
    for web_path in _MODULE.DEFAULT_PATHS[:-1]:
        _write_repo_asset(tmp_path, web_path, f"asset:{web_path}".encode("utf-8"))

    monkeypatch.setattr(
        _MODULE,
        "parse_args",
        lambda: argparse.Namespace(
            repo_root=tmp_path,
            version="1.0.0",
            seed_hex=signing_key.encode().hex(),
            output="custom-manifest.json",
            key_id="test-key-id",
        ),
    )

    with pytest.raises(FileNotFoundError, match="Missing asset for signed manifest"):
        _MODULE.main()
