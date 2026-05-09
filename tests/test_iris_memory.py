"""Tests for the Iris Memory Palace builder and receipt core."""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey
from cryptography.hazmat.primitives.asymmetric.rsa import generate_private_key


_ROOT = Path(__file__).resolve().parents[1]
_BUILDER_PATH = _ROOT / "iris-memory" / "build-memory-palace.py"
_CORE_PATH = _ROOT / "iris-memory" / "memory-palace-core.py"


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


_BUILDER = _load_module("iris_memory_builder_test", _BUILDER_PATH)
_CORE = _load_module("iris_memory_core_test", _CORE_PATH)


def _write_source_files(base_dir: Path) -> None:
    contents = {
        "01-identity.md": "# Identity\n\nThe named human review standard.\n\n## Purpose\n\nSovereign review before action.",
        "02-lewis-profile.md": "# Lewis Profile\n\nLocal-first profile.",
        "03-partners.md": "# Partners\n\nTrusted support.",
        "04-live-cases.md": "# Live Cases\n\nCase evidence.",
        "05-infrastructure.md": "# Infrastructure\n\nMerkle receipt design.",
    }
    for filename, content in contents.items():
        (base_dir / filename).write_text(content, encoding="utf-8")


def _write_palace(path: Path) -> None:
    path.write_text(
        json.dumps(
            {
                "version": "source-test",
                "documents": [
                    {
                        "source_file": "one.md",
                        "title": "One",
                        "sha256": "a" * 64,
                        "sections": [
                            {"title": "First", "content": "alpha"},
                            {"title": "Second", "content": "beta"},
                            {"title": "Third", "content": "gamma"},
                        ],
                    }
                ],
            }
        ),
        encoding="utf-8",
    )


def test_builder_extracts_title_or_uses_fallback():
    assert _BUILDER.extract_title("Intro\n# Canonical Title\nBody", "fallback.md") == "Canonical Title"
    assert _BUILDER.extract_title("Intro only", "fallback.md") == "fallback.md"


def test_builder_split_sections_preserves_preamble_and_heading_content():
    sections = _BUILDER.split_sections("Opening\n\n# First\nBody\n## Second\nMore")

    assert sections == [
        {"title": "Preamble", "content": "Opening"},
        {"title": "First", "content": "# First\nBody"},
        {"title": "Second", "content": "## Second\nMore"},
    ]


def test_builder_keywords_are_ranked_limited_and_filter_stopwords():
    keywords = _BUILDER.keywords_for(
        "Review Review Alpha",
        "the and review beta beta gamma delta epsilon zeta eta theta iota kappa lambda mu nu xi omicron pi rho sigma tau upsilon phi chi psi omega aardvark buffalo cougar",
    )

    assert keywords[:2] == ["review", "beta"]
    assert "alpha" in keywords
    assert "the" not in keywords
    assert "and" not in keywords
    assert len(keywords) == _BUILDER.MAX_KEYWORDS


def test_build_memory_palace_reads_all_sources_and_builds_index(tmp_path):
    _write_source_files(tmp_path)

    palace, index = _BUILDER.build_memory_palace(tmp_path)

    assert palace["version"] == _BUILDER.VERSION
    assert set(palace["file_hashes"]) == set(_BUILDER.SOURCE_FILES)
    assert [document["source_file"] for document in palace["documents"]] == _BUILDER.SOURCE_FILES
    assert palace["documents"][0]["title"] == "Identity"
    assert palace["documents"][0]["sections"][1]["title"] == "Purpose"
    assert index[0]["source_file"] == "01-identity.md"
    assert "review" in index[0]["keywords"]


def test_core_canonical_json_and_memory_entry_signature_are_stable():
    signing_key = Ed25519PrivateKey.generate()
    entry = _CORE.MemoryEntry(
        content="specific facts",
        metadata={"b": 2, "a": 1},
        signing_key=signing_key,
    )

    assert _CORE.canonical_json({"b": 2, "a": [3, 1]}) == b'{"a":[3,1],"b":2}'
    assert entry.commitment() == _CORE.sha256_hex(_CORE.canonical_json(entry.payload()))
    signing_key.public_key().verify(bytes.fromhex(entry.signature()), bytes.fromhex(entry.commitment()))
    assert entry.to_receipt_entry() == {
        "commitment": entry.commitment(),
        "signature": entry.signature(),
        "metadata": {"b": 2, "a": 1},
    }


def test_memory_palace_creates_entries_merkle_root_and_signed_receipt(tmp_path):
    palace_path = tmp_path / "memory-palace.json"
    _write_palace(palace_path)
    signing_key = Ed25519PrivateKey.generate()

    palace = _CORE.MemoryPalace(path=palace_path, signing_key=signing_key)
    receipt = palace.signed_receipt()

    assert [entry.metadata["section_title"] for entry in palace.entries] == ["First", "Second", "Third"]
    assert receipt["version"] == _CORE.VERSION
    assert receipt["source_version"] == "source-test"
    assert receipt["source_file"] == "memory-palace.json"
    assert receipt["entry_count"] == 3
    assert receipt["merkle_root"] == palace.merkle_root()
    assert receipt["public_key_ed25519"] == _CORE.public_key_hex(signing_key)
    assert "does not replace individual human review" in receipt["integrity_note"]

    public_key = Ed25519PublicKey.from_public_bytes(bytes.fromhex(receipt["public_key_ed25519"]))
    public_key.verify(bytes.fromhex(receipt["root_signature"]), bytes.fromhex(receipt["merkle_root"]))
    first = receipt["entries"][0]
    public_key.verify(bytes.fromhex(first["signature"]), bytes.fromhex(first["commitment"]))


def test_memory_palace_returns_empty_hash_for_no_entries(tmp_path):
    palace_path = tmp_path / "memory-palace.json"
    palace_path.write_text(json.dumps({"version": "empty", "documents": []}), encoding="utf-8")

    palace = _CORE.MemoryPalace(path=palace_path, signing_key=Ed25519PrivateKey.generate())

    assert palace.entries == []
    assert palace.merkle_root() == _CORE.sha256_hex(b"")


def test_write_receipt_writes_pretty_json(tmp_path):
    palace_path = tmp_path / "memory-palace.json"
    receipt_path = tmp_path / "receipt.json"
    _write_palace(palace_path)
    palace = _CORE.MemoryPalace(path=palace_path, signing_key=Ed25519PrivateKey.generate())

    assert palace.write_receipt(receipt_path) == receipt_path

    text = receipt_path.read_text(encoding="utf-8")
    assert text.endswith("\n")
    assert json.loads(text)["entry_count"] == 3


def test_load_signing_key_uses_environment_pem(monkeypatch):
    signing_key = Ed25519PrivateKey.generate()
    pem = signing_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    ).decode("utf-8")
    monkeypatch.setenv("IRIS_MEMORY_PRIVATE_KEY", pem)

    loaded = _CORE.load_signing_key()

    assert _CORE.public_key_hex(loaded) == _CORE.public_key_hex(signing_key)


def test_load_signing_key_rejects_non_ed25519_private_key(monkeypatch):
    rsa_key = generate_private_key(public_exponent=65537, key_size=2048)
    pem = rsa_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    ).decode("utf-8")
    monkeypatch.setenv("IRIS_MEMORY_PRIVATE_KEY", pem)

    with pytest.raises(TypeError, match="Ed25519 private key"):
        _CORE.load_signing_key()


def test_ensure_memory_json_builds_only_when_missing(monkeypatch, tmp_path):
    palace_path = tmp_path / "memory-palace.json"
    calls = []
    monkeypatch.setattr(_CORE, "PALACE_PATH", palace_path)
    monkeypatch.setattr(_CORE, "write_memory_json", lambda: calls.append("built"))

    _CORE.ensure_memory_json()
    palace_path.write_text("{}", encoding="utf-8")
    _CORE.ensure_memory_json()

    assert calls == ["built"]


def test_receipt_command_refreshes_receipt(monkeypatch, tmp_path, capsys):
    palace_path = tmp_path / "memory-palace.json"
    receipt_path = tmp_path / "receipt.json"
    _write_palace(palace_path)
    real_memory_palace = _CORE.MemoryPalace

    class TestMemoryPalace(real_memory_palace):
        def __init__(self):
            super().__init__(path=palace_path, signing_key=Ed25519PrivateKey.generate())

        def write_receipt(self, path=receipt_path):
            return super().write_receipt(path)

    monkeypatch.setattr(_CORE, "MemoryPalace", TestMemoryPalace)
    monkeypatch.setattr(_CORE, "PALACE_PATH", palace_path)

    assert _CORE.receipt_command() == 0

    assert receipt_path.exists()
    output = capsys.readouterr().out
    assert "Memory Palace receipt refreshed." in output
    assert "- Entries signed: 3" in output
