"""Tests for the evidence anchoring helper."""

from __future__ import annotations

import hashlib
from datetime import datetime, timezone

from iris.anchor import (
    DISCLAIMER,
    build_anchor_manifest,
    canonical_json_sha256,
    sha256_file,
)


def test_sha256_file_matches_known_digest(tmp_path):
    f = tmp_path / "evidence.txt"
    f.write_bytes(b"burgess")
    assert sha256_file(f) == hashlib.sha256(b"burgess").hexdigest()


def test_canonical_json_is_order_independent():
    assert canonical_json_sha256({"a": 1, "b": 2}) == canonical_json_sha256({"b": 2, "a": 1})


def test_canonical_json_is_deterministic():
    digest = canonical_json_sha256({"classification": "NULL", "ts": 1})
    expected = hashlib.sha256(
        '{"classification":"NULL","ts":1}'.encode("utf-8")
    ).hexdigest()
    assert digest == expected


def test_manifest_structure_and_digests(tmp_path):
    a = tmp_path / "a.csv"
    a.write_bytes(b"row1\nrow2\n")
    b = tmp_path / "b.json"
    b.write_bytes(b"{}")
    fixed = datetime(2026, 6, 3, 12, 0, tzinfo=timezone.utc)

    manifest = build_anchor_manifest([a, b], now=fixed)

    assert manifest["algorithm"] == "sha256"
    assert manifest["anchored"] is False  # honesty: not submitted here
    assert manifest["computed_at"] == "2026-06-03T12:00:00+00:00"
    assert manifest["disclaimer"] == DISCLAIMER
    assert len(manifest["entries"]) == 2
    assert manifest["entries"][0]["sha256"] == sha256_file(a)
    assert manifest["entries"][0]["bytes"] == 10


def test_manifest_is_deterministic_with_fixed_time(tmp_path):
    f = tmp_path / "x.txt"
    f.write_bytes(b"x")
    fixed = datetime(2026, 1, 1, tzinfo=timezone.utc)
    assert build_anchor_manifest([f], now=fixed) == build_anchor_manifest([f], now=fixed)
