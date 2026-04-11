"""Iris claim builder for sovereign local mode."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import re
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

_IRIS_ROOT = Path(__file__).resolve().parent
_REPO_ROOT = _IRIS_ROOT.parent
_TEMPLATES_DIR = _REPO_ROOT / "templates"
_COMMON_SCENARIOS_PATH = _TEMPLATES_DIR / "COMMON_SCENARIOS.md"
_ONCHAIN_CLAIMS_PATH = _REPO_ROOT / "onchain-protocol" / "sdk" / "onchain_claims.py"

_PBKDF2_ITERATIONS = 210_000
_PBKDF2_SALT_BYTES = 16
_PLACEHOLDER_RE = re.compile(r"\[([^\[\]]+)\]")
_SCENARIO_LINK_RE = re.compile(r"\[`([^`]+)`\]\(\./[^)]+\)")

_EXACT_PLACEHOLDER_MAP = {
    "DATE": "date",
    "Date": "date",
    "Your Full Name": "full_name",
    "Your full name": "full_name",
    "Your Contact Details": "contact_details",
    "Your contact details": "contact_details",
    "Your address": "address",
    "Email address if known": "email",
    "Exchange / Platform / Compliance Team": "target_entity",
    "Institution / Team": "target_entity",
    "Institution / Company / Platform Name": "target_entity",
    "Institution / Company Name": "target_entity",
    "Institution Name & Full Address": "target_entity",
    "Team": "team_name",
    "Your Case / Warrant / Account / Decision Reference": "reference",
    "Your Case / Account / Decision Reference": "reference",
    "Your Case / Complaint / Review Reference": "reference",
    "Your Reference / Account / CCJ / Case Number if known": "reference",
    "Exchange Ticket / Account / Case Reference": "reference",
    "COMMITMENT_HASH": "commitment_hash",
    "SIGNATURE / RECEIPT / PUBLIC KEY": "signature_reference",
    "CLAIM ID / TX HASH / EXPLORER LINK": "onchain_reference",
    "CLAIM ID / TX HASH": "onchain_reference",
    "TX HASH / HASHES": "transaction_hashes",
    "ADDRESS / ADDRESSES": "wallet_addresses",
}

_FAST_MATCH_RULES = [
    {
        "template": "CRYPTO_EXCHANGE_ACCOUNT_RESTRICTION_WITH_BURGESS.md",
        "category": "exchange",
        "keywords": (
            "crypto exchange",
            "exchange froze",
            "froze my account",
            "withdrawal",
            "source-of-funds",
            "source of funds",
            "compliance review",
            "wallet",
        ),
    },
    {
        "template": "CRYPTOGRAPHIC_PROOF_AND_ONCHAIN_NOTICE_WITH_BURGESS.md",
        "category": "dao",
        "keywords": (
            "on-chain",
            "on chain",
            "commitment hash",
            "signature",
            "signed receipt",
            "public key",
            "proof reference",
        ),
    },
    {
        "template": "COMMITMENT_ONLY_PLACEHOLDER.md",
        "category": "dao",
        "keywords": (
            "minimal disclosure",
            "keep private",
            "privacy preserving",
            "privacy-preserving",
            "placeholder",
            "only share the hash",
        ),
    },
    {
        "template": "BAILIFFS_THREAT_TEMPLATE.md",
        "category": "enforcement",
        "keywords": ("bailiff", "forced entry", "enforcement visit"),
    },
    {
        "template": "COUNCIL_TAX_PCN_TEMPLATE.md",
        "category": "enforcement",
        "keywords": ("council tax", "pcn", "parking penalty", "arrears"),
    },
    {
        "template": "BENEFITS_CLAIM_HELP.md",
        "category": "enforcement",
        "keywords": ("benefits", "universal credit", "pip", "esa"),
    },
    {
        "template": "ARTICLE_22_WITH_BURGESS_PRINCIPLE.md",
        "category": "disclosure",
        "keywords": ("automated decision", "algorithm", "scoring model", "article 22"),
    },
    {
        "template": "EQUALITY_ACT_WITH_BURGESS_PRINCIPLE.md",
        "category": "dispute",
        "keywords": (
            "reasonable adjustment",
            "accessible communication",
            "disability",
            "plain language",
        ),
    },
    {
        "template": "DSAR_WITH_BURGESS_PRINCIPLE.md",
        "category": "disclosure",
        "keywords": ("subject access", "dsar", "data they hold", "data held about me"),
    },
    {
        "template": "FOI_WITH_BURGESS_PRINCIPLE.md",
        "category": "disclosure",
        "keywords": ("freedom of information", "foi", "public records", "public body"),
    },
]


def _load_onchain_claims_module():
    spec = importlib.util.spec_from_file_location(
        "iris_onchain_claims",
        _ONCHAIN_CLAIMS_PATH,
    )
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load on-chain claims module from {_ONCHAIN_CLAIMS_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


_ONCHAIN_CLAIMS = _load_onchain_claims_module()


def _validate_inputs(user_query: str, profile: dict[str, Any]) -> None:
    if not isinstance(user_query, str):
        raise TypeError(f"user_query must be a string, got {type(user_query).__name__}")
    if not user_query.strip():
        raise ValueError("user_query must not be empty")
    if not isinstance(profile, dict):
        raise TypeError(f"profile must be a dict, got {type(profile).__name__}")


def _normalize_text(value: str) -> str:
    return " ".join(value.lower().split())


def _normalize_key(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")


def _load_common_scenarios() -> dict[str, str]:
    scenarios: dict[str, str] = {}
    for line in _COMMON_SCENARIOS_PATH.read_text(encoding="utf-8").splitlines():
        if not line.startswith("|"):
            continue
        columns = [column.strip() for column in line.strip("|").split("|")]
        if len(columns) != 3 or columns[0] in {"Situation", "---"}:
            continue
        match = _SCENARIO_LINK_RE.search(columns[1])
        if match:
            scenarios[match.group(1)] = columns[0]
    return scenarios


def _match_scenario(user_query: str) -> dict[str, Any]:
    normalized_query = _normalize_text(user_query)
    scenarios = _load_common_scenarios()

    best_match: dict[str, Any] | None = None
    best_score = 0

    for rule in _FAST_MATCH_RULES:
        matched_keywords = [
            keyword for keyword in rule["keywords"] if keyword in normalized_query
        ]
        score = sum(2 if " " in keyword else 1 for keyword in matched_keywords)
        if score > best_score:
            best_score = score
            best_match = {
                "template": rule["template"],
                "category": rule["category"],
                "matched_keywords": matched_keywords,
                "situation": scenarios.get(rule["template"], ""),
            }

    if best_match is not None:
        return best_match

    template = "REQUEST_FOR_HUMAN_REVIEW.md"
    return {
        "template": template,
        "category": "dispute",
        "matched_keywords": [],
        "situation": scenarios.get(template, ""),
    }


def _load_template(template_name: str) -> str:
    return (_TEMPLATES_DIR / template_name).read_text(encoding="utf-8")


def _first_value(profile: dict[str, Any], *keys: str) -> str:
    for key in keys:
        value = profile.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return ""


def _summarize_query(user_query: str) -> str:
    summary = " ".join(user_query.strip().split())
    if len(summary) > 220:
        summary = summary[:217].rstrip() + "..."
    if summary and summary[-1] not in ".!?":
        summary += "."
    return summary


def _build_contact_details(profile: dict[str, Any]) -> str:
    explicit = _first_value(profile, "contact_details", "contact")
    if explicit:
        return explicit

    parts = [
        _first_value(profile, "email"),
        _first_value(profile, "phone", "telephone"),
        _first_value(profile, "address"),
    ]
    return " | ".join(part for part in parts if part)


def _build_context(user_query: str, profile: dict[str, Any]) -> dict[str, str]:
    now = datetime.now(timezone.utc)
    full_name = _first_value(profile, "full_name", "name")
    target_entity = _first_value(
        profile,
        "institution_name",
        "target_entity",
        "institution",
        "company_name",
        "team_name",
    )
    team_name = _first_value(profile, "team_name") or target_entity
    transaction_hashes = _first_value(profile, "transaction_hashes", "transaction_hash")
    wallet_addresses = _first_value(profile, "wallet_addresses", "wallet_address")

    return {
        "date": _first_value(profile, "date") or now.date().isoformat(),
        "reply_by": _first_value(profile, "reply_by")
        or (now + timedelta(days=14)).date().isoformat(),
        "full_name": full_name,
        "contact_details": _build_contact_details(profile),
        "email": _first_value(profile, "email"),
        "address": _first_value(profile, "address"),
        "target_entity": target_entity,
        "team_name": team_name,
        "reference": _first_value(
            profile,
            "reference",
            "case_reference",
            "account_reference",
            "ticket_reference",
        ),
        "query_summary": _summarize_query(user_query),
        "transaction_hashes": transaction_hashes,
        "wallet_addresses": wallet_addresses,
        "commitment_hash": _first_value(profile, "commitment_hash"),
        "signature_reference": _first_value(profile, "signature_reference"),
        "onchain_reference": _first_value(profile, "onchain_reference"),
    }


def _resolve_placeholder(
    label: str,
    profile: dict[str, Any],
    context: dict[str, str],
) -> str | None:
    exact_context_key = _EXACT_PLACEHOLDER_MAP.get(label)
    if exact_context_key:
        value = context.get(exact_context_key, "")
        return value or None

    normalized_label = _normalize_key(label)
    normalized_profile = {
        _normalize_key(key): str(value)
        for key, value in profile.items()
        if isinstance(value, (str, int, float)) and str(value).strip()
    }
    if normalized_label in normalized_profile:
        return normalized_profile[normalized_label]

    if "briefly_describe" in normalized_label or "neutral_sentence" in normalized_label:
        return context["query_summary"]
    if "reasonable_date" in normalized_label:
        return context["reply_by"]
    if "commitment" in normalized_label and "hash" in normalized_label:
        return context.get("commitment_hash") or None
    if any(token in normalized_label for token in ("signature", "receipt", "public_key")):
        return context.get("signature_reference") or None
    if any(token in normalized_label for token in ("claim_id", "tx_hash", "explorer_link")):
        return context.get("onchain_reference") or None
    if "wallet" in normalized_label and "address" in normalized_label:
        return context.get("wallet_addresses") or None
    if "transaction" in normalized_label and "hash" in normalized_label:
        return context.get("transaction_hashes") or None
    if any(token in normalized_label for token in ("reference", "ticket", "account", "case")):
        return context.get("reference") or None
    if "full_name" in normalized_label or normalized_label.startswith("your_name"):
        return context.get("full_name") or None
    if "contact_details" in normalized_label or normalized_label == "contact":
        return context.get("contact_details") or None
    if normalized_label.startswith("your_address"):
        return context.get("address") or None
    if "email" in normalized_label:
        return context.get("email") or None
    if any(
        token in normalized_label
        for token in ("exchange", "platform", "institution", "company", "team")
    ):
        return context.get("target_entity") or None
    if "date" == normalized_label:
        return context.get("date") or None

    return None


def _fill_template(
    template_text: str,
    profile: dict[str, Any],
    context: dict[str, str],
) -> str:
    def replace(match: re.Match[str]) -> str:
        label = match.group(1)
        value = _resolve_placeholder(label, profile, context)
        return value if value is not None else match.group(0)

    return _PLACEHOLDER_RE.sub(replace, template_text)


def _resolve_private_key(profile: dict[str, Any]) -> tuple[str, str | None]:
    private_key_hex = _first_value(
        profile,
        "private_key_hex",
        "signing_private_key_hex",
    )
    if private_key_hex:
        return private_key_hex, None

    try:
        from nacl.signing import SigningKey
    except ImportError:
        raise ImportError(
            "The 'PyNaCl' package is required for Ed25519 signing key generation. "
            "Install it with: pip install PyNaCl"
        ) from None

    generated_private_key_hex = SigningKey.generate().encode().hex()
    return generated_private_key_hex, generated_private_key_hex


def _resolve_vault_dir(profile: dict[str, Any]) -> Path:
    configured_path = _first_value(profile, "vault_path", "vault_dir")
    if configured_path:
        path = Path(configured_path).expanduser()
        return path if path.is_absolute() else (_REPO_ROOT / path)
    return _REPO_ROOT / ".sovereign-vault"


def _derive_vault_key(passphrase: str, salt: bytes, key_bytes: int) -> bytes:
    return hashlib.pbkdf2_hmac(
        "sha256",
        passphrase.encode("utf-8"),
        salt,
        _PBKDF2_ITERATIONS,
        dklen=key_bytes,
    )


def _encrypt_for_vault(plaintext: str, passphrase: str) -> str:
    try:
        from nacl.secret import SecretBox
    except ImportError:
        raise ImportError(
            "The 'PyNaCl' package is required for vault encryption. "
            "Install it with: pip install PyNaCl"
        ) from None

    salt = os.urandom(_PBKDF2_SALT_BYTES)
    nonce = os.urandom(SecretBox.NONCE_SIZE)
    key = _derive_vault_key(passphrase, salt, SecretBox.KEY_SIZE)
    encrypted = SecretBox(key).encrypt(plaintext.encode("utf-8"), nonce)
    return (salt + nonce + encrypted.ciphertext).hex()


def _decrypt_vault_payload(encrypted_payload: str, passphrase: str) -> str:
    try:
        from nacl.secret import SecretBox
    except ImportError:
        raise ImportError(
            "The 'PyNaCl' package is required for vault decryption. "
            "Install it with: pip install PyNaCl"
        ) from None

    packed = bytes.fromhex(encrypted_payload)
    salt = packed[:_PBKDF2_SALT_BYTES]
    nonce_end = _PBKDF2_SALT_BYTES + SecretBox.NONCE_SIZE
    nonce = packed[_PBKDF2_SALT_BYTES:nonce_end]
    ciphertext = packed[nonce_end:]
    key = _derive_vault_key(passphrase, salt, SecretBox.KEY_SIZE)
    return SecretBox(key).decrypt(ciphertext, nonce).decode("utf-8")


def _save_to_vault(
    *,
    user_query: str,
    filled_letter: str,
    template_name: str,
    profile: dict[str, Any],
    onchain_claim: dict[str, str],
) -> dict[str, str]:
    passphrase = _first_value(profile, "vault_passphrase", "passphrase")
    if not passphrase:
        raise ValueError("profile must include vault_passphrase to save an encrypted letter")

    created_at = onchain_claim["timestamp"]
    record_id = uuid.uuid4().hex
    vault_dir = _resolve_vault_dir(profile)
    vault_dir.mkdir(parents=True, exist_ok=True)
    vault_path = vault_dir / f"{record_id}.json"

    encrypted_payload = _encrypt_for_vault(
        json.dumps(
            {
                "created_at": created_at,
                "template": template_name,
                "user_query": user_query,
                "letter": filled_letter,
                "onchain_claim": onchain_claim,
            },
            separators=(",", ":"),
            sort_keys=True,
        ),
        passphrase,
    )

    vault_path.write_text(
        json.dumps(
            {
                "version": "0.8.0",
                "mode": "sovereign-local",
                "record_id": record_id,
                "created_at": created_at,
                "template": template_name,
                "commitment_hash": onchain_claim["commitment_hash"],
                "public_key": onchain_claim["public_key"],
                "encrypted_payload": encrypted_payload,
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    return {
        "record_id": record_id,
        "path": str(vault_path),
    }


def auto_generate_claim(user_query: str, profile: dict[str, Any]) -> dict[str, Any]:
    """Classify, draft, sign, and save a claim in sovereign local mode."""
    _validate_inputs(user_query, profile)

    scenario = _match_scenario(user_query)
    template_name = scenario["template"]
    template_text = _load_template(template_name)
    context = _build_context(user_query, profile)
    draft_letter = _fill_template(template_text, profile, context)

    private_key_hex, generated_private_key_hex = _resolve_private_key(profile)
    target_entity = context.get("target_entity") or "Institution / Team"
    claim = _ONCHAIN_CLAIMS.generate_onchain_claim(
        claim_details=draft_letter,
        target_entity=target_entity,
        category=scenario["category"],
        private_key_hex=private_key_hex,
    )
    onchain_claim = claim.to_dict()

    claim_context = {
        **context,
        "commitment_hash": onchain_claim["commitment_hash"],
        "signature_reference": (
            f"{onchain_claim['signature']} / {onchain_claim['public_key']}"
        ),
        "onchain_reference": context.get("onchain_reference")
        or "Pending local posting — commitment ready",
    }
    filled_letter = _fill_template(template_text, profile, claim_context)

    notice_template = _load_template(
        "CRYPTOGRAPHIC_PROOF_AND_ONCHAIN_NOTICE_WITH_BURGESS.md"
    )
    onchain_notice = _fill_template(notice_template, profile, claim_context)
    vault_record = _save_to_vault(
        user_query=user_query,
        filled_letter=filled_letter,
        template_name=template_name,
        profile=profile,
        onchain_claim=onchain_claim,
    )
    unresolved_placeholders = sorted(set(_PLACEHOLDER_RE.findall(filled_letter)))

    result = {
        "scenario": scenario,
        "template_path": str(_TEMPLATES_DIR / template_name),
        "letter": filled_letter,
        "commitment_hash": onchain_claim["commitment_hash"],
        "signature": onchain_claim["signature"],
        "public_key": onchain_claim["public_key"],
        "timestamp": onchain_claim["timestamp"],
        "nonce": onchain_claim["nonce"],
        "onchain_claim": onchain_claim,
        "onchain_notice": onchain_notice,
        "vault_record": vault_record,
        "ui_actions": [
            {"id": "save", "label": "Save"},
            {"id": "generate_commitment", "label": "Generate Commitment"},
            {"id": "copy_letter", "label": "Copy Letter"},
            {"id": "onchain_notice", "label": "On-Chain Notice"},
        ],
        "unresolved_placeholders": unresolved_placeholders,
    }
    if generated_private_key_hex is not None:
        result["generated_private_key_hex"] = generated_private_key_hex
    return result


__all__ = ["auto_generate_claim"]
