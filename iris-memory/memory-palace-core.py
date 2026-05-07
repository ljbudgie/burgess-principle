#!/usr/bin/env python3
"""Core Verifiable Memory Palace for the Iris sovereign AI agent."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import runpy
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey


VERSION = "0.1.0"
BASE_DIR = Path(__file__).resolve().parent
PALACE_PATH = BASE_DIR / "memory-palace.json"
RECEIPT_PATH = BASE_DIR / "memory-palace-receipt.json"


def canonical_json(data: Any) -> bytes:
    """Return stable JSON bytes so hashes and signatures are reproducible."""
    return json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode(
        "utf-8"
    )


def sha256_hex(data: bytes) -> str:
    """Return a SHA-256 digest as hex."""
    return hashlib.sha256(data).hexdigest()


def load_signing_key() -> Ed25519PrivateKey:
    """Load an Ed25519 private key from IRIS_MEMORY_PRIVATE_KEY, or create one.

    Production deployments should provide a PEM-encoded Ed25519 private key in
    IRIS_MEMORY_PRIVATE_KEY. If none is provided, a fresh local key is generated
    for the current receipt only; the private key is never written to disk.
    """
    pem = os.environ.get("IRIS_MEMORY_PRIVATE_KEY")
    if not pem:
        return Ed25519PrivateKey.generate()

    key = serialization.load_pem_private_key(pem.encode("utf-8"), password=None)
    if not isinstance(key, Ed25519PrivateKey):
        raise TypeError("IRIS_MEMORY_PRIVATE_KEY must contain an Ed25519 private key")
    return key


def public_key_hex(signing_key: Ed25519PrivateKey) -> str:
    """Expose the Ed25519 public key in raw hex for receipt verification."""
    return signing_key.public_key().public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw,
    ).hex()


@dataclass(frozen=True)
class MemoryEntry:
    """A signed, hash-committed memory entry."""

    content: str
    metadata: dict[str, Any]
    signing_key: Ed25519PrivateKey

    def payload(self) -> dict[str, Any]:
        return {"content": self.content, "metadata": self.metadata}

    def commitment(self) -> str:
        # SHA-256 creates the local commitment described in Phase 3 of
        # 05-infrastructure.md: content is reduced to a tamper-evident digest.
        return sha256_hex(canonical_json(self.payload()))

    def signature(self) -> str:
        # Ed25519 signs the commitment so a later verifier can detect whether the
        # committed entry was altered after the receipt was created.
        return self.signing_key.sign(bytes.fromhex(self.commitment())).hex()

    def to_receipt_entry(self) -> dict[str, Any]:
        return {
            "commitment": self.commitment(),
            "signature": self.signature(),
            "metadata": self.metadata,
        }


class MemoryPalace:
    """Load Memory Palace JSON, sign entries, and produce a Merkle receipt."""

    def __init__(self, path: Path = PALACE_PATH, signing_key: Ed25519PrivateKey | None = None):
        self.path = path
        self.signing_key = signing_key or load_signing_key()
        self.data = json.loads(path.read_text(encoding="utf-8"))
        self.entries = self._create_entries()

    def _create_entries(self) -> list[MemoryEntry]:
        entries: list[MemoryEntry] = []
        for document_index, document in enumerate(self.data.get("documents", [])):
            for section_index, section in enumerate(document.get("sections", [])):
                metadata = {
                    "source_file": document["source_file"],
                    "document_title": document["title"],
                    "section_title": section["title"],
                    "document_sha256": document["sha256"],
                    "document_index": document_index,
                    "section_index": section_index,
                }
                entries.append(
                    MemoryEntry(
                        content=section["content"],
                        metadata=metadata,
                        signing_key=self.signing_key,
                    )
                )
        return entries

    def merkle_root(self) -> str:
        """Calculate the Phase 3 Merkle root over all signed entry commitments."""
        leaves = [bytes.fromhex(entry.commitment()) for entry in self.entries]
        if not leaves:
            return sha256_hex(b"")

        level = leaves
        while len(level) > 1:
            if len(level) % 2:
                level.append(level[-1])
            level = [
                hashlib.sha256(level[index] + level[index + 1]).digest()
                for index in range(0, len(level), 2)
            ]
        return level[0].hex()

    def signed_receipt(self) -> dict[str, Any]:
        """Export a signed root receipt without exposing any private key material."""
        root = self.merkle_root()
        # The root signature anchors the full set of entry commitments. This is
        # the signed-root receipt referenced by the Phase 3 architecture.
        root_signature = self.signing_key.sign(bytes.fromhex(root)).hex()
        return {
            "version": VERSION,
            "source_version": self.data.get("version"),
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "source_file": self.path.name,
            "entry_count": len(self.entries),
            "merkle_root": root,
            "root_signature": root_signature,
            "public_key_ed25519": public_key_hex(self.signing_key),
            "entries": [entry.to_receipt_entry() for entry in self.entries],
            "integrity_note": (
                "Cryptography proves the Memory Palace record has not changed; "
                "it does not replace individual human review under the Burgess Principle."
            ),
        }

    def write_receipt(self, path: Path = RECEIPT_PATH) -> Path:
        receipt = self.signed_receipt()
        path.write_text(json.dumps(receipt, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        return path


def ensure_memory_json() -> None:
    """Run the builder if the structured Memory Palace JSON does not exist."""
    if not PALACE_PATH.exists():
        runpy.run_path(str(BASE_DIR / "build-memory-palace.py"), run_name="__main__")


def build_command() -> int:
    runpy.run_path(str(BASE_DIR / "build-memory-palace.py"), run_name="__main__")
    palace = MemoryPalace()
    receipt_path = palace.write_receipt()
    print("Verifiable Memory Palace receipt created.")
    print(f"- Entries signed: {len(palace.entries)}")
    print(f"- Merkle root: {palace.merkle_root()}")
    print(f"- Receipt: {receipt_path.name}")
    return 0


def receipt_command() -> int:
    ensure_memory_json()
    palace = MemoryPalace()
    receipt_path = palace.write_receipt()
    print("Memory Palace receipt refreshed.")
    print(f"- Entries signed: {len(palace.entries)}")
    print(f"- Merkle root: {palace.merkle_root()}")
    print(f"- Receipt: {receipt_path.name}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Build or receipt the Iris Memory Palace.")
    parser.add_argument("command", choices=("build", "receipt"))
    args = parser.parse_args()

    if args.command == "build":
        return build_command()
    return receipt_command()


if __name__ == "__main__":
    raise SystemExit(main())
