#!/usr/bin/env python3
"""Generate a signed manifest for the sovereign PWA update envelope.

Keep the private signing seed offline. Only the signed manifest and public key belong in the repo.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from nacl.signing import SigningKey

DEFAULT_PATHS = [
    "/",
    "/index.html",
    "/manifest.json",
    "/service-worker.js",
    "/banner.png",
]
DEFAULT_OUTPUT = "signed-update-manifest.json"
DEFAULT_KEY_ID = "iris-pwa-ed25519-2026-04"


def canonicalize(value: object) -> str:
    if isinstance(value, dict):
        return "{" + ",".join(f"{json.dumps(key)}:{canonicalize(value[key])}" for key in sorted(value)) + "}"
    if isinstance(value, list):
        return "[" + ",".join(canonicalize(item) for item in value) + "]"
    return json.dumps(value, separators=(",", ":"), ensure_ascii=False)


def sha256_hex(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def materialize_path(repo_root: Path, web_path: str) -> Path:
    relative = "index.html" if web_path == "/" else web_path.lstrip("/")
    return repo_root / relative


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=Path(__file__).resolve().parents[1], type=Path)
    parser.add_argument("--version", required=True, help="PWA core version to embed in the signed manifest")
    parser.add_argument("--seed-hex", required=True, help="32-byte Ed25519 private seed as lowercase hex")
    parser.add_argument("--output", default=DEFAULT_OUTPUT, help="Output path relative to the repo root")
    parser.add_argument("--key-id", default=DEFAULT_KEY_ID, help="Stable identifier for the pinned public key")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    repo_root = args.repo_root.resolve()
    signing_key = SigningKey(bytes.fromhex(args.seed_hex))
    public_key_hex = signing_key.verify_key.encode().hex()

    assets: list[dict[str, str]] = []
    for web_path in DEFAULT_PATHS:
        file_path = materialize_path(repo_root, web_path)
        if not file_path.exists():
            raise FileNotFoundError(f"Missing asset for signed manifest: {file_path}")
        assets.append({"path": web_path, "sha256": sha256_hex(file_path)})

    signed_payload = {
        "app_id": "iris-sovereign-pwa",
        "version": args.version,
        "issued_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "hash_algorithm": "sha256",
        "consent_required": True,
        "critical_paths": DEFAULT_PATHS,
        "assets": assets,
    }
    signature = signing_key.sign(canonicalize(signed_payload).encode("utf-8")).signature
    manifest = {
        "key_id": args.key_id,
        "public_key_hex": public_key_hex,
        "signed_payload": signed_payload,
        "signature": base64.b64encode(signature).decode("ascii"),
    }

    output_path = repo_root / args.output
    output_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
