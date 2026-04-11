"""Personal sovereign profile helpers for Lewis-first local workflows."""
from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping

_ROOT = Path(__file__).resolve().parent.parent
_VAULT_DIRNAME = ".sovereign-vault"
_PROFILE_FILENAME = "personal-profile.json"
_PROFILE_VERSION = "1.0.0"
_PROFILE_PBKDF2_ITERATIONS = 1_500_000


def _select_first_valid(values: Mapping[str, Any], *keys: str) -> str:
    for key in keys:
        value = values.get(key)
        if value not in (None, ""):
            return str(value).strip()
    return ""


def _derive_key(passphrase: str, salt: bytes, key_bytes: int) -> bytes:
    return hashlib.pbkdf2_hmac(
        "sha256",
        passphrase.encode("utf-8"),
        salt,
        _PROFILE_PBKDF2_ITERATIONS,
        dklen=key_bytes,
    )


def _encrypt_payload(payload: Mapping[str, Any], passphrase: str) -> str:
    from nacl.secret import SecretBox

    salt, nonce = os.urandom(16), os.urandom(SecretBox.NONCE_SIZE)
    key = _derive_key(passphrase, salt, SecretBox.KEY_SIZE)
    encrypted = SecretBox(key).encrypt(
        json.dumps(dict(payload), separators=(",", ":"), sort_keys=True).encode("utf-8"),
        nonce,
    )
    return (salt + nonce + encrypted.ciphertext).hex()


def decrypt_profile_payload(encrypted_payload: str, passphrase: str) -> dict[str, Any]:
    """Decrypt a stored personal-profile payload."""
    from nacl.secret import SecretBox

    packed, nonce_end = bytes.fromhex(encrypted_payload), 16 + SecretBox.NONCE_SIZE
    key = _derive_key(passphrase, packed[:16], SecretBox.KEY_SIZE)
    payload = SecretBox(key).decrypt(packed[nonce_end:], packed[16:nonce_end]).decode("utf-8")
    return json.loads(payload)


def profile_signature_block(name: str, preferred_signature_block: str | None = None) -> str:
    """Return the visible signature block label for the sovereign profile."""
    return (preferred_signature_block or f"{name} [Burgess Principle]").strip()


def fingerprint_public_key(public_key_hex: str, length: int = 16) -> str:
    """Create a compact SHA-256 fingerprint for the Ed25519 public key."""
    return hashlib.sha256(bytes.fromhex(public_key_hex)).hexdigest()[:length]


def _signed_profile_payload(profile: Mapping[str, str]) -> str:
    visible = {
        "handle": profile["handle"],
        "key_fingerprint": profile["key_fingerprint"],
        "name": profile["name"],
        "preferred_signature_block": profile["preferred_signature_block"],
        "public_key_hex": profile["public_key_hex"],
    }
    return json.dumps(visible, separators=(",", ":"), sort_keys=True)


def build_personal_profile(
    *,
    name: str,
    handle: str = "ljbudgie",
    preferred_signature_block: str | None = None,
    private_key_hex: str | None = None,
) -> dict[str, str]:
    """Generate or load an Ed25519-backed personal sovereign profile."""
    from nacl.signing import SigningKey

    sovereign_name = name.strip()
    if not sovereign_name:
        raise ValueError("name must be a non-empty string")

    signing_key = (
        SigningKey(bytes.fromhex(private_key_hex))
        if private_key_hex
        else SigningKey.generate()
    )
    public_key_hex = signing_key.verify_key.encode().hex()
    profile = {
        "version": _PROFILE_VERSION,
        "name": sovereign_name,
        "handle": (handle or "ljbudgie").strip() or "ljbudgie",
        "preferred_signature_block": profile_signature_block(sovereign_name, preferred_signature_block),
        "public_key_hex": public_key_hex,
        "private_key_hex": signing_key.encode().hex(),
        "key_fingerprint": fingerprint_public_key(public_key_hex),
        "signed_at": datetime.now(timezone.utc).isoformat(),
    }
    signed_profile = _signed_profile_payload(profile)
    profile["signed_profile"] = signed_profile
    profile["profile_signature"] = signing_key.sign(signed_profile.encode("utf-8")).signature.hex()
    return profile


def verify_personal_profile(profile: Mapping[str, Any]) -> bool:
    """Verify the stored signed sovereign profile."""
    from nacl.exceptions import BadSignatureError
    from nacl.signing import VerifyKey

    try:
        signed_profile = _select_first_valid(profile, "signed_profile")
        signature = bytes.fromhex(_select_first_valid(profile, "profile_signature"))
        public_key = bytes.fromhex(_select_first_valid(profile, "public_key_hex"))
        VerifyKey(public_key).verify(signed_profile.encode("utf-8"), signature)
    except (BadSignatureError, TypeError, ValueError):
        return False
    return True


def summarize_personal_profile(profile: Mapping[str, Any]) -> dict[str, str]:
    """Return the public summary that can safely auto-load on app startup."""
    return {
        "name": _select_first_valid(profile, "name"),
        "handle": _select_first_valid(profile, "handle") or "ljbudgie",
        "preferred_signature_block": _select_first_valid(profile, "preferred_signature_block"),
        "key_fingerprint": _select_first_valid(profile, "key_fingerprint"),
        "public_key_hex": _select_first_valid(profile, "public_key_hex"),
        "profile_signature": _select_first_valid(profile, "profile_signature"),
        "signed_at": _select_first_valid(profile, "signed_at"),
    }


def profile_path(root: Path | None = None) -> Path:
    """Return the canonical encrypted personal-profile path."""
    base_root = (root or _ROOT).resolve()
    return base_root / _VAULT_DIRNAME / _PROFILE_FILENAME


def save_personal_profile(
    profile: Mapping[str, Any],
    vault_passphrase: str,
    *,
    root: Path | None = None,
) -> dict[str, Any]:
    """Encrypt and save a sovereign personal profile inside the local vault."""
    if not vault_passphrase:
        raise ValueError("vault_passphrase must be a non-empty string")
    if not verify_personal_profile(profile):
        raise ValueError("profile signature verification failed")

    path = profile_path(root)
    path.parent.mkdir(parents=True, exist_ok=True)
    summary = summarize_personal_profile(profile)
    record = {
        "version": _PROFILE_VERSION,
        "record_type": "personal-sovereign-profile",
        "stored_at": datetime.now(timezone.utc).isoformat(),
        **summary,
        "encrypted_payload": _encrypt_payload(profile, vault_passphrase),
    }
    path.write_text(json.dumps(record, indent=2), encoding="utf-8")
    return {"path": str(path), "profile": summary}


def load_personal_profile(
    vault_passphrase: str,
    *,
    root: Path | None = None,
) -> dict[str, Any]:
    """Load and verify the encrypted sovereign personal profile."""
    if not vault_passphrase:
        raise ValueError("vault_passphrase must be a non-empty string")

    record = json.loads(profile_path(root).read_text(encoding="utf-8"))
    profile = decrypt_profile_payload(record["encrypted_payload"], vault_passphrase)
    if not verify_personal_profile(profile):
        raise ValueError("profile signature verification failed")
    return profile


def load_personal_profile_summary(*, root: Path | None = None) -> dict[str, str] | None:
    """Load the public summary without decrypting the private payload."""
    path = profile_path(root)
    if not path.exists():
        return None

    record = json.loads(path.read_text(encoding="utf-8"))
    summary = summarize_personal_profile(record)
    return summary if summary["name"] else None


def setup_personal_profile(
    *,
    vault_passphrase: str,
    root: Path | None = None,
    name: str | None = None,
    handle: str = "ljbudgie",
    preferred_signature_block: str | None = None,
    private_key_hex: str | None = None,
) -> dict[str, Any]:
    """Load an existing profile or create-and-save one if none exists yet."""
    path = profile_path(root)
    if path.exists():
        profile = load_personal_profile(vault_passphrase, root=root)
        return {"created": False, "stored_path": str(path), "profile": summarize_personal_profile(profile)}
    if not name:
        raise ValueError("name must be a non-empty string")

    created_profile = build_personal_profile(
        name=name,
        handle=handle,
        preferred_signature_block=preferred_signature_block,
        private_key_hex=private_key_hex,
    )
    stored = save_personal_profile(created_profile, vault_passphrase, root=root)
    return {"created": True, "stored_path": stored["path"], "profile": stored["profile"]}


__all__ = [
    "build_personal_profile",
    "decrypt_profile_payload",
    "fingerprint_public_key",
    "load_personal_profile",
    "load_personal_profile_summary",
    "profile_path",
    "profile_signature_block",
    "save_personal_profile",
    "setup_personal_profile",
    "summarize_personal_profile",
    "verify_personal_profile",
]
