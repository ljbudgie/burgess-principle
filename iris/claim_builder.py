"""Compact Iris claim builder helpers for local sovereign workflows."""
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import re
import sys
import uuid
from datetime import datetime, timedelta, timezone
from functools import lru_cache
from pathlib import Path
from typing import Any, Mapping

_ROOT = Path(__file__).resolve().parent.parent
_TEMPLATES = _ROOT / "templates"
_SCENARIOS = _TEMPLATES / "COMMON_SCENARIOS.md"
_ONCHAIN = _ROOT / "onchain-protocol" / "sdk" / "onchain_claims.py"
_PLACEHOLDER_RE = re.compile(r"\[([^\[\]]+)\]")
_LINK_RE = re.compile(r"\[`([^`]+)`\]\(\./[^)]+\)")
_STOP = {"a", "about", "for", "i", "it", "just", "me", "my", "need", "or", "the", "to", "want", "with"}
_EXACT = {"DATE": "date", "Team": "team_name", "Your Full Name": "full_name", "Your Contact Details": "contact_details", "Your address": "address", "Email address if known": "email", "Exchange / Platform / Compliance Team": "target_entity", "Institution / Team": "target_entity", "Institution / Company / Platform Name": "target_entity", "Institution / Company Name": "target_entity", "Institution Name & Full Address": "target_entity", "Your Case / Warrant / Account / Decision Reference": "reference", "Your Case / Account / Decision Reference": "reference", "Your Case / Complaint / Review Reference": "reference", "Your Reference / Account / CCJ / Case Number if known": "reference", "Exchange Ticket / Account / Case Reference": "reference", "COMMITMENT_HASH": "commitment_hash", "SIGNATURE / RECEIPT / PUBLIC KEY": "signature_reference", "CLAIM ID / TX HASH / EXPLORER LINK": "onchain_reference", "CLAIM ID / TX HASH": "onchain_reference", "TX HASH / HASHES": "transaction_hashes", "ADDRESS / ADDRESSES": "wallet_addresses"}
_CATEGORY = {"CRYPTO_EXCHANGE_ACCOUNT_RESTRICTION_WITH_BURGESS.md": "exchange", "CRYPTOGRAPHIC_PROOF_AND_ONCHAIN_NOTICE_WITH_BURGESS.md": "dao", "COMMITMENT_ONLY_PLACEHOLDER.md": "dao", "ARTICLE_22_WITH_BURGESS_PRINCIPLE.md": "disclosure", "DSAR_WITH_BURGESS_PRINCIPLE.md": "disclosure", "FOI_WITH_BURGESS_PRINCIPLE.md": "disclosure", "BENEFITS_CLAIM_HELP.md": "enforcement", "COUNCIL_TAX_PCN_TEMPLATE.md": "enforcement", "BAILIFFS_THREAT_TEMPLATE.md": "enforcement"}
_HINTS = {"REQUEST_FOR_HUMAN_REVIEW.md": ("human review", "first letter"), "GENERAL_DISPUTE_WITH_BURGESS_PRINCIPLE.md": ("dispute letter", "challenging outcome"), "EQUALITY_ACT_WITH_BURGESS_PRINCIPLE.md": ("reasonable adjustments", "accessible communication"), "CRYPTOGRAPHIC_PROOF_AND_ONCHAIN_NOTICE_WITH_BURGESS.md": ("hash", "signature", "receipt", "on-chain", "on chain"), "COMMITMENT_ONLY_PLACEHOLDER.md": ("minimal disclosure", "placeholder", "keep private")}
_FALLBACKS = (("briefly_describe", "query_summary"), ("neutral_sentence", "query_summary"), ("reasonable_date", "reply_by"), ("commitment", "commitment_hash"), ("signature", "signature_reference"), ("receipt", "signature_reference"), ("public_key", "signature_reference"), ("claim_id", "onchain_reference"), ("tx_hash", "onchain_reference"), ("explorer_link", "onchain_reference"), ("wallet", "wallet_addresses"), ("transaction", "transaction_hashes"))
_QUERY_SUMMARY_MAX_LENGTH = 217

def _module() -> Any:
    spec = importlib.util.spec_from_file_location("iris_onchain_claims", _ONCHAIN)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load on-chain claims module from {_ONCHAIN}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module

def _norm(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", text.lower()).strip("_")

def _tokens(text: str) -> set[str]:
    return {word for word in re.findall(r"[a-z0-9']+", text.lower()) if len(word) > 2 and word not in _STOP}

def _pick(values: Mapping[str, Any], *keys: str) -> str:
    """Return the first non-empty string-like value for the given keys."""
    for key in keys:
        value = values.get(key)
        if value not in (None, ""):
            return str(value).strip()
    return ""

def _score_row(query: str, words: set[str], row: Mapping[str, str]) -> tuple[int, list[str]]:
    phrases = (row["situation"].lower(), *_HINTS.get(row["template"], ()))
    matched = [phrase for phrase in phrases if phrase in query]
    return len(words & set().union(*(_tokens(phrase) for phrase in phrases))) + 3 * len(matched), matched

_ONCHAIN_CLAIMS = _module()

@lru_cache(maxsize=1)
def _scenario_rows() -> tuple[dict[str, str], ...]:
    """Parse the fast-match table from `templates/COMMON_SCENARIOS.md`."""
    rows, in_table = [], False
    for line in _SCENARIOS.read_text(encoding="utf-8").splitlines():
        in_table = in_table or line.strip() == "## Fast match table"
        if not in_table or not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) != 3 or cells[0] in {"Situation", "---"}:
            continue
        match = _LINK_RE.search(cells[1])
        if match:
            rows.append({"situation": cells[0], "template": match.group(1)})
    return tuple(rows)

def classify_scenario(user_query: str) -> dict[str, Any]:
    """Classify a user query against the parsed common-scenarios fast-match table."""
    query, words, best = " ".join(user_query.lower().split()), _tokens(user_query), None
    for row in _scenario_rows():
        score, matched = _score_row(query, words, row)
        if best is None or score > best["score"]:
            best = {**row, "category": _CATEGORY.get(row["template"], "dispute"), "matched_keywords": matched, "score": score}
    return best or {"situation": "", "template": "REQUEST_FOR_HUMAN_REVIEW.md", "category": "dispute", "matched_keywords": [], "score": 0}

def load_template(template_name: str) -> str:
    """Load a template file from the repository templates directory."""
    return (_TEMPLATES / template_name).read_text(encoding="utf-8")

def _context(user_query: str, profile: Mapping[str, Any]) -> dict[str, str]:
    now, summary = datetime.now(timezone.utc), " ".join(user_query.split())
    target = _pick(profile, "target_entity", "institution_name", "institution", "company_name", "team_name")
    contact = _pick(profile, "contact_details", "contact") or " | ".join(filter(None, (_pick(profile, "email"), _pick(profile, "phone", "telephone"), _pick(profile, "address"))))
    return {
        "date": _pick(profile, "date") or now.date().isoformat(), "reply_by": _pick(profile, "reply_by") or (now + timedelta(days=14)).date().isoformat(),
        "full_name": _pick(profile, "full_name", "name"), "contact_details": contact, "email": _pick(profile, "email"), "address": _pick(profile, "address"),
        "target_entity": target, "team_name": _pick(profile, "team_name") or target, "reference": _pick(profile, "reference", "case_reference", "account_reference", "ticket_reference"),
        "query_summary": summary[:_QUERY_SUMMARY_MAX_LENGTH].rstrip() + ("..." if len(summary) > _QUERY_SUMMARY_MAX_LENGTH else "") + ("" if not summary or summary.endswith((".", "!", "?")) else "."),
        "transaction_hashes": _pick(profile, "transaction_hashes", "transaction_hash"), "wallet_addresses": _pick(profile, "wallet_addresses", "wallet_address"),
        "commitment_hash": _pick(profile, "commitment_hash"), "signature_reference": _pick(profile, "signature_reference"), "onchain_reference": _pick(profile, "onchain_reference"),
    }

def fill_placeholders(template_text: str, profile: Mapping[str, Any], context: Mapping[str, Any] | None = None) -> str:
    """Fill template placeholders from exact labels, normalized keys, and common heuristics."""
    values: dict[str, str] = {}
    for source in (profile, context or {}):
        for key, value in source.items():
            if value not in (None, ""):
                values[_norm(key)] = str(value).strip()
    def repl(match: re.Match[str]) -> str:
        key = _EXACT.get(match.group(1)) or _norm(match.group(1))
        if values.get(key):
            return values[key]
        for needle, fallback in _FALLBACKS:
            if needle in key and values.get(fallback):
                return values[fallback]
        return match.group(0)
    return _PLACEHOLDER_RE.sub(repl, template_text)

def generate_commitment(claim_text: str, profile: Mapping[str, Any], *, category: str, target_entity: str) -> dict[str, str]:
    """Generate and verify an on-chain commitment using the existing SDK helpers."""
    private_key, generated = _pick(profile, "private_key_hex", "signing_private_key_hex"), ""
    if not private_key:
        from nacl.signing import SigningKey
        generated = private_key = SigningKey.generate().encode().hex()
    claim = _ONCHAIN_CLAIMS.generate_onchain_claim(claim_text, target_entity or "Institution / Team", category, private_key).to_dict()
    if not _ONCHAIN_CLAIMS.verify_onchain_receipt(claim["commitment_hash"], claim["signature"], claim["public_key"]).valid:
        raise ValueError("Generated commitment failed verification")
    return {**claim, **({"generated_private_key_hex": generated} if generated else {})}

def _derive_key(passphrase: str, salt: bytes, key_bytes: int) -> bytes:
    return hashlib.pbkdf2_hmac("sha256", passphrase.encode("utf-8"), salt, 210_000, dklen=key_bytes)

def _decrypt_vault_payload(encrypted_payload: str, passphrase: str) -> str:
    """Decrypt a vault payload created by `encrypt_to_vault`."""
    from nacl.secret import SecretBox
    packed, nonce_end = bytes.fromhex(encrypted_payload), 16 + SecretBox.NONCE_SIZE
    key = _derive_key(passphrase, packed[:16], SecretBox.KEY_SIZE)
    return SecretBox(key).decrypt(packed[nonce_end:], packed[16:nonce_end]).decode("utf-8")

def encrypt_to_vault(payload: Mapping[str, Any], profile: Mapping[str, Any], template_name: str) -> dict[str, str]:
    """Encrypt a claim payload and persist it in the local sovereign vault."""
    from nacl.secret import SecretBox
    passphrase = _pick(profile, "vault_passphrase", "passphrase")
    if not passphrase:
        raise ValueError("profile must include vault_passphrase to save an encrypted letter")
    salt, nonce = os.urandom(16), os.urandom(SecretBox.NONCE_SIZE)
    key = _derive_key(passphrase, salt, SecretBox.KEY_SIZE)
    vault_dir = (_ROOT / ".sovereign-vault").resolve()
    vault_dir.mkdir(parents=True, exist_ok=True)
    record_id = uuid.uuid4().hex
    claim = payload.get("onchain_claim", {}) if isinstance(payload.get("onchain_claim"), Mapping) else {}
    encrypted = SecretBox(key).encrypt(json.dumps(dict(payload), separators=(",", ":"), sort_keys=True).encode("utf-8"), nonce)
    metadata = {"version": "0.8.0", "mode": "sovereign-local", "record_id": record_id, "created_at": str(payload.get("created_at", "")), "template": template_name, "commitment_hash": str(claim.get("commitment_hash", "")), "public_key": str(claim.get("public_key", "")), "encrypted_payload": (salt + nonce + encrypted.ciphertext).hex()}
    path = vault_dir / f"{record_id}.json"
    path.write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    return {"record_id": record_id, "path": str(path)}

def queue_onchain_fingerprint(fingerprint: Mapping[str, Any]) -> dict[str, str]:
    """Persist a privacy-first fingerprint package for later on-chain posting."""
    required = ("commitment_hash", "signature", "public_key")
    missing = [key for key in required if not str(fingerprint.get(key, "")).strip()]
    if missing:
        raise ValueError("fingerprint must include commitment_hash, signature, and public_key")
    queue_dir = (_ROOT / ".sovereign-vault" / "pending-onchain-fingerprints").resolve()
    queue_dir.mkdir(parents=True, exist_ok=True)
    queue_id = uuid.uuid4().hex
    payload = {
        "version": "0.9.0",
        "queue_id": queue_id,
        "queued_at": datetime.now(timezone.utc).isoformat(),
        "fingerprint": {
            key: str(value).strip()
            for key, value in fingerprint.items()
            if value not in (None, "")
        },
    }
    path = queue_dir / f"{queue_id}.json"
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return {"queue_id": queue_id, "path": str(path)}

def auto_generate_claim(user_query: str, profile: dict[str, Any]) -> dict[str, Any]:
    """Classify a query, fill a template, generate a commitment, and save a vault copy."""
    if not isinstance(user_query, str) or not user_query.strip() or not isinstance(profile, dict):
        raise ValueError("user_query must be a non-empty string and profile must be a dict")
    scenario, base = classify_scenario(user_query), _context(user_query, profile)
    template_text = load_template(scenario["template"])
    claim = generate_commitment(fill_placeholders(template_text, profile, base), profile, category=scenario["category"], target_entity=base["target_entity"])
    claim_context = {**base, **{key: value for key, value in claim.items() if isinstance(value, str)}, "signature_reference": f"{claim['signature']} / {claim['public_key']}", "onchain_reference": base["onchain_reference"] or "Pending local posting — commitment ready"}
    letter = fill_placeholders(template_text, profile, claim_context)
    payload = {"created_at": claim["timestamp"], "template": scenario["template"], "user_query": user_query, "letter": letter, "onchain_claim": {key: value for key, value in claim.items() if key != "generated_private_key_hex"}}
    result = {
        "scenario": scenario, "template_path": str(_TEMPLATES / scenario["template"]), "letter": letter, "onchain_notice": fill_placeholders(load_template("CRYPTOGRAPHIC_PROOF_AND_ONCHAIN_NOTICE_WITH_BURGESS.md"), profile, claim_context),
        "vault_record": encrypt_to_vault(payload, profile, scenario["template"]), "ui_actions": [{"id": "save", "label": "Save"}, {"id": "generate_commitment", "label": "Generate Commitment"}, {"id": "copy_letter", "label": "Copy Letter"}, {"id": "onchain_notice", "label": "On-Chain Notice"}],
        "unresolved_placeholders": sorted(set(_PLACEHOLDER_RE.findall(letter))), **claim,
    }
    result["onchain_claim"] = payload["onchain_claim"]
    if claim.get("generated_private_key_hex"):
        result["generated_private_key_hex"] = claim["generated_private_key_hex"]
    return result

__all__ = ["auto_generate_claim", "classify_scenario", "encrypt_to_vault", "fill_placeholders", "generate_commitment", "load_template", "queue_onchain_fingerprint"]
