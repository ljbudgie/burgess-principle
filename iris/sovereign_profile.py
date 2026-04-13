"""Personal sovereign profile helpers for local workflows."""
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import sys
from datetime import datetime, timezone
from functools import lru_cache
from pathlib import Path
from typing import Any, Mapping

_ROOT = Path(__file__).resolve().parent.parent
_ONCHAIN = _ROOT / "onchain-protocol" / "sdk" / "onchain_claims.py"
_VAULT_DIRNAME = ".sovereign-vault"
_PROFILE_FILENAME = "personal-profile.json"
_PROFILE_VERSION = "1.3.0"
_PROFILE_PBKDF2_ITERATIONS = 1_500_000
_MIRROR_GREETING_STYLE_DEFAULT = "neutral_professional"
_MIRROR_REFLECTION_SCOPE_DEFAULT = "vault_only"
_MIRROR_GREETING_STYLES = {
    "warm_personal": "Warm & Personal",
    "neutral_professional": "Neutral & Professional",
    "minimal": "Minimal",
}
_MIRROR_REFLECTION_SCOPES = {
    "off": "Do not include a Mirror Reflection block",
    "vault_only": "Keep the Mirror Reflection block in the internal vault only",
    "all_documents": "Include the Mirror Reflection block in generated documents",
}


@lru_cache(maxsize=1)
def _onchain_claims_module() -> Any:
    spec = importlib.util.spec_from_file_location("iris_sovereign_onchain_claims", _ONCHAIN)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load on-chain claims module from {_ONCHAIN}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


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


def normalize_mirror_greeting_style(value: str | None) -> str:
    """Return a supported Mirror Mode greeting style."""
    candidate = "_".join(str(value or "").strip().lower().replace("&", " ").split())
    return candidate if candidate in _MIRROR_GREETING_STYLES else _MIRROR_GREETING_STYLE_DEFAULT


def normalize_mirror_reflection_scope(value: str | None) -> str:
    """Return a supported Mirror Reflection scope."""
    candidate = str(value or "").strip().lower().replace(" ", "_")
    return candidate if candidate in _MIRROR_REFLECTION_SCOPES else _MIRROR_REFLECTION_SCOPE_DEFAULT


def mirror_mode_prompt(
    name: str,
    *,
    greeting_style: str | None = None,
    custom_greeting: str | None = None,
) -> str:
    """Return the default Mirror Mode greeting for the sovereign profile."""
    custom = str(custom_greeting or "").strip()
    if custom:
        return custom
    sovereign_name = str(name).strip() or "there"
    style = normalize_mirror_greeting_style(greeting_style)
    if style == "warm_personal":
        return (
            f"Hello {sovereign_name} — Mirror Mode active. "
            "The handshake continues: your energy + my structure = sovereign record."
        )
    if style == "minimal":
        return "Mirror Mode active."
    return (
        f"{sovereign_name} — Mirror Mode active. "
        "The handshake continues on this device."
    )


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
    if profile.get("signature_mode") == "hybrid":
        visible["signature_mode"] = "hybrid"
        visible["post_quantum_algorithm"] = str(profile.get("post_quantum_algorithm", "")).strip()
        visible["post_quantum_public_key_hex"] = str(
            profile.get("post_quantum_public_key_hex", "")
        ).strip()
    return json.dumps(visible, separators=(",", ":"), sort_keys=True)


def _apply_profile_signatures(
    profile: dict[str, Any],
    *,
    post_quantum: bool,
    post_quantum_private_key_hex: str | None = None,
    post_quantum_public_key_hex: str | None = None,
) -> dict[str, Any]:
    module = _onchain_claims_module()
    if not post_quantum:
        signed_profile = _signed_profile_payload(profile)
        bundle = module.build_signature_bundle(
            signed_profile.encode("utf-8"),
            str(profile["private_key_hex"]).strip(),
            post_quantum=False,
        )
        profile["signature_mode"] = "classical"
        profile.pop("profile_signatures", None)
        profile.pop("profile_public_keys", None)
        profile.pop("post_quantum_algorithm", None)
        profile.pop("post_quantum_public_key_hex", None)
        profile["signed_profile"] = signed_profile
        profile["profile_signature"] = bundle["signature"]
        return profile

    # Generate or recover the PQ key material first, then sign the final visible
    # profile payload once the PQ public key metadata has been embedded.
    provisional = module.build_signature_bundle(
        b"sovereign-profile",
        str(profile["private_key_hex"]).strip(),
        post_quantum=True,
        post_quantum_private_key_hex=post_quantum_private_key_hex,
        post_quantum_public_key_hex=post_quantum_public_key_hex,
    )
    profile["signature_mode"] = "hybrid"
    profile["post_quantum_algorithm"] = provisional["post_quantum_algorithm"]
    profile["post_quantum_public_key_hex"] = provisional["public_keys"][
        provisional["post_quantum_algorithm"].lower()
    ]
    if provisional["generated_post_quantum_private_key_hex"]:
        profile["post_quantum_private_key_hex"] = provisional[
            "generated_post_quantum_private_key_hex"
        ]
    elif post_quantum_private_key_hex:
        profile["post_quantum_private_key_hex"] = post_quantum_private_key_hex
    signed_profile = _signed_profile_payload(profile)
    bundle = module.build_signature_bundle(
        signed_profile.encode("utf-8"),
        str(profile["private_key_hex"]).strip(),
        post_quantum=True,
        post_quantum_private_key_hex=_select_first_valid(
            profile, "post_quantum_private_key_hex"
        ),
        post_quantum_public_key_hex=profile["post_quantum_public_key_hex"],
    )
    profile["signed_profile"] = signed_profile
    profile["profile_signature"] = bundle["signature"]
    profile["profile_signatures"] = dict(bundle["signatures"])
    profile["profile_public_keys"] = dict(bundle["public_keys"])
    return profile


def build_personal_profile(
    *,
    name: str,
    handle: str = "sovereign-user",
    preferred_signature_block: str | None = None,
    private_key_hex: str | None = None,
    post_quantum: bool = False,
    post_quantum_private_key_hex: str | None = None,
    post_quantum_public_key_hex: str | None = None,
    mirror_mode_enabled: bool = False,
    mirror_greeting_style: str | None = None,
    mirror_custom_greeting: str | None = None,
    mirror_reflection_scope: str | None = None,
) -> dict[str, str]:
    """Generate or load an Ed25519-backed personal sovereign profile."""
    from nacl.signing import SigningKey

    signed_at = datetime.now(timezone.utc).isoformat()
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
        "handle": (handle or "sovereign-user").strip() or "sovereign-user",
        "preferred_signature_block": profile_signature_block(sovereign_name, preferred_signature_block),
        "public_key_hex": public_key_hex,
        "private_key_hex": signing_key.encode().hex(),
        "key_fingerprint": fingerprint_public_key(public_key_hex),
        "signed_at": signed_at,
        "mirror_mode_enabled": bool(mirror_mode_enabled),
        "mirror_mode_activated_at": signed_at if mirror_mode_enabled else "",
        "mirror_greeting_style": normalize_mirror_greeting_style(mirror_greeting_style),
        "mirror_custom_greeting": str(mirror_custom_greeting or "").strip(),
        "mirror_reflection_scope": normalize_mirror_reflection_scope(mirror_reflection_scope),
    }
    return _apply_profile_signatures(
        profile,
        post_quantum=post_quantum,
        post_quantum_private_key_hex=post_quantum_private_key_hex,
        post_quantum_public_key_hex=post_quantum_public_key_hex,
    )


def verify_personal_profile(profile: Mapping[str, Any]) -> bool:
    """Verify the stored signed sovereign profile."""
    try:
        module = _onchain_claims_module()
        signed_profile = _select_first_valid(profile, "signed_profile")
        result = module.verify_signature_bundle(
            signed_profile.encode("utf-8"),
            _select_first_valid(profile, "profile_signature"),
            _select_first_valid(profile, "public_key_hex"),
            signatures=profile.get("profile_signatures"),
            public_keys=profile.get("profile_public_keys"),
        )
        if not result.valid:
            return False
    except (ImportError, TypeError, ValueError):
        return False
    return True


def summarize_personal_profile(profile: Mapping[str, Any]) -> dict[str, Any]:
    """Return the public summary that can safely auto-load on app startup."""
    name = _select_first_valid(profile, "name")
    mirror_mode_enabled = bool(profile.get("mirror_mode_enabled"))
    mirror_greeting_style = normalize_mirror_greeting_style(
        _select_first_valid(profile, "mirror_greeting_style")
    )
    mirror_custom_greeting = _select_first_valid(profile, "mirror_custom_greeting")
    mirror_reflection_scope = normalize_mirror_reflection_scope(
        _select_first_valid(profile, "mirror_reflection_scope")
    )
    return {
        "name": name,
        "handle": _select_first_valid(profile, "handle") or "sovereign-user",
        "preferred_signature_block": _select_first_valid(profile, "preferred_signature_block"),
        "key_fingerprint": _select_first_valid(profile, "key_fingerprint"),
        "public_key_hex": _select_first_valid(profile, "public_key_hex"),
        "profile_signature": _select_first_valid(profile, "profile_signature"),
        "signature_mode": _select_first_valid(profile, "signature_mode") or "classical",
        "post_quantum_algorithm": _select_first_valid(profile, "post_quantum_algorithm"),
        "post_quantum_public_key_hex": _select_first_valid(
            profile, "post_quantum_public_key_hex"
        ),
        "signed_at": _select_first_valid(profile, "signed_at"),
        "mirror_mode_enabled": mirror_mode_enabled,
        "mirror_mode_activated_at": _select_first_valid(profile, "mirror_mode_activated_at"),
        "mirror_greeting_style": mirror_greeting_style,
        "mirror_custom_greeting": mirror_custom_greeting,
        "mirror_reflection_scope": mirror_reflection_scope,
        "mirror_greeting": (
            mirror_mode_prompt(
                name,
                greeting_style=mirror_greeting_style,
                custom_greeting=mirror_custom_greeting,
            )
            if name and mirror_mode_enabled
            else ""
        ),
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


def load_personal_profile_summary(*, root: Path | None = None) -> dict[str, Any] | None:
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
    handle: str = "sovereign-user",
    preferred_signature_block: str | None = None,
    private_key_hex: str | None = None,
    post_quantum: bool | None = None,
    post_quantum_private_key_hex: str | None = None,
    post_quantum_public_key_hex: str | None = None,
    mirror_mode_enabled: bool | None = None,
    mirror_greeting_style: str | None = None,
    mirror_custom_greeting: str | None = None,
    mirror_reflection_scope: str | None = None,
) -> dict[str, Any]:
    """Load an existing profile or create-and-save one if none exists yet."""
    path = profile_path(root)
    if path.exists():
        profile = load_personal_profile(vault_passphrase, root=root)
        should_save = False
        if mirror_mode_enabled is not None:
            profile["mirror_mode_enabled"] = bool(mirror_mode_enabled)
            profile["mirror_mode_activated_at"] = (
                datetime.now(timezone.utc).isoformat() if mirror_mode_enabled else ""
            )
            should_save = True
        if mirror_greeting_style is not None:
            profile["mirror_greeting_style"] = normalize_mirror_greeting_style(mirror_greeting_style)
            should_save = True
        if mirror_custom_greeting is not None:
            profile["mirror_custom_greeting"] = str(mirror_custom_greeting).strip()
            should_save = True
        if mirror_reflection_scope is not None:
            profile["mirror_reflection_scope"] = normalize_mirror_reflection_scope(
                mirror_reflection_scope
            )
            should_save = True
        if post_quantum is not None:
            profile = _apply_profile_signatures(
                dict(profile),
                post_quantum=bool(post_quantum),
                post_quantum_private_key_hex=post_quantum_private_key_hex
                or _select_first_valid(profile, "post_quantum_private_key_hex"),
                post_quantum_public_key_hex=post_quantum_public_key_hex
                or _select_first_valid(profile, "post_quantum_public_key_hex"),
            )
            should_save = True
        if should_save:
            save_personal_profile(profile, vault_passphrase, root=root)
        return {"created": False, "stored_path": str(path), "profile": summarize_personal_profile(profile)}
    if not name:
        raise ValueError("name must be a non-empty string")

    created_profile = build_personal_profile(
        name=name,
        handle=handle,
        preferred_signature_block=preferred_signature_block,
        private_key_hex=private_key_hex,
        post_quantum=bool(post_quantum),
        post_quantum_private_key_hex=post_quantum_private_key_hex,
        post_quantum_public_key_hex=post_quantum_public_key_hex,
        mirror_mode_enabled=bool(mirror_mode_enabled),
        mirror_greeting_style=mirror_greeting_style,
        mirror_custom_greeting=mirror_custom_greeting,
        mirror_reflection_scope=mirror_reflection_scope,
    )
    stored = save_personal_profile(created_profile, vault_passphrase, root=root)
    return {"created": True, "stored_path": stored["path"], "profile": stored["profile"]}


__all__ = [
    "build_personal_profile",
    "decrypt_profile_payload",
    "fingerprint_public_key",
    "load_personal_profile",
    "load_personal_profile_summary",
    "mirror_mode_prompt",
    "normalize_mirror_greeting_style",
    "normalize_mirror_reflection_scope",
    "profile_path",
    "profile_signature_block",
    "save_personal_profile",
    "setup_personal_profile",
    "summarize_personal_profile",
    "verify_personal_profile",
]
