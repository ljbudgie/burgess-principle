from __future__ import annotations

import base64
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

DATA_DIR = Path(os.environ.get('HUB_DATA_DIR', '/data'))
STATE_PATH = DATA_DIR / 'hub-state.json'
DATA_DIR.mkdir(parents=True, exist_ok=True)
SHARED_SECRET = os.environ.get('HUB_SHARED_SECRET', '').encode('utf-8')
SIGNING_SEED_HEX = os.environ.get('HUB_SIGNING_SEED_HEX', '')
SERVER_ID = os.environ.get('HUB_SERVER_ID', 'iris-sovereign-hub')
PBKDF2_ITERATIONS = 310000

if len(SHARED_SECRET) < 16:
    raise RuntimeError('HUB_SHARED_SECRET must be set to a long random value.')
if len(SIGNING_SEED_HEX) != 64:
    raise RuntimeError('HUB_SIGNING_SEED_HEX must be a 32-byte hex seed.')

signing_key = Ed25519PrivateKey.from_private_bytes(bytes.fromhex(SIGNING_SEED_HEX))
public_key_hex = signing_key.public_key().public_bytes(
    encoding=serialization.Encoding.Raw,
    format=serialization.PublicFormat.Raw,
).hex()

app = FastAPI(title='Iris Sovereign Hub Example', version='2.0')


class ClientSignature(BaseModel):
    device_id: str
    public_key_hex: str
    signature_hex: str


class SyncRequest(BaseModel):
    envelope: dict[str, str]
    signed_request: dict[str, Any]
    client_signature: ClientSignature



def canonicalize(value: Any) -> str:
    if isinstance(value, list):
        return '[' + ','.join(canonicalize(item) for item in value) + ']'
    if isinstance(value, dict):
        return '{' + ','.join(f'{json.dumps(key)}:{canonicalize(value[key])}' for key in sorted(value)) + '}'
    return json.dumps(value)



def now_iso() -> str:
    return datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%fZ')



def derive_key(secret: bytes, salt_b64: str) -> bytes:
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=base64.b64decode(salt_b64), iterations=PBKDF2_ITERATIONS)
    return kdf.derive(secret)



def decrypt_envelope(envelope: dict[str, str]) -> dict[str, Any]:
    key = derive_key(SHARED_SECRET, envelope['salt'])
    aesgcm = AESGCM(key)
    plaintext = aesgcm.decrypt(
        base64.b64decode(envelope['iv']),
        base64.b64decode(envelope['ciphertext']),
        None,
    )
    return json.loads(plaintext.decode('utf-8'))



def encrypt_envelope(payload: dict[str, Any], envelope: dict[str, str]) -> dict[str, str]:
    key = derive_key(SHARED_SECRET, envelope['salt'])
    aesgcm = AESGCM(key)
    iv = os.urandom(12)
    ciphertext = aesgcm.encrypt(iv, json.dumps(payload).encode('utf-8'), None)
    return {
        'salt': envelope['salt'],
        'iv': base64.b64encode(iv).decode('utf-8'),
        'ciphertext': base64.b64encode(ciphertext).decode('utf-8'),
    }



def verify_client_signature(request: SyncRequest) -> None:
    try:
        key = Ed25519PublicKey.from_public_bytes(bytes.fromhex(request.client_signature.public_key_hex))
        key.verify(
            bytes.fromhex(request.client_signature.signature_hex),
            canonicalize(request.signed_request).encode('utf-8'),
        )
    except Exception as exc:  # pragma: no cover - defensive edge for malformed inputs
        raise HTTPException(status_code=401, detail=f'Invalid client signature: {exc}') from exc



def sign_response(payload: dict[str, Any]) -> tuple[dict[str, Any], str]:
    signature = signing_key.sign(canonicalize(payload).encode('utf-8')).hex()
    return payload, signature



def load_state() -> dict[str, Any]:
    if STATE_PATH.exists():
        return json.loads(STATE_PATH.read_text(encoding='utf-8'))
    return {
        'cursor': '',
        'memory_roots': [],
        'claim_commitments': [],
        'trigger_heads': [],
        'audit_log': [],
    }



def save_state(state: dict[str, Any]) -> None:
    STATE_PATH.write_text(json.dumps(state, indent=2), encoding='utf-8')



def merge_unique(items: list[dict[str, Any]], additions: list[dict[str, Any]], key: str) -> list[dict[str, Any]]:
    existing = {item.get(key): item for item in items if item.get(key)}
    for item in additions:
        identifier = item.get(key)
        if identifier:
            existing[identifier] = item
    return sorted(existing.values(), key=lambda item: item.get('created_at', ''))


@app.get('/api/hub/hello')
def hello() -> dict[str, Any]:
    return {
        'server_id': SERVER_ID,
        'public_key_hex': public_key_hex,
        'pairing_hint': {
            'url': 'https://your-hub.tailnet.ts.net',
            'public_key_hex': public_key_hex,
        },
        'audit': 'Pin this public key in Iris after verifying it over Tailscale/WireGuard or another trusted channel.',
    }


@app.post('/api/sovereign-sync-v2')
def sync(request: SyncRequest) -> dict[str, Any]:
    verify_client_signature(request)
    decrypted = decrypt_envelope(request.envelope)
    state = load_state()

    if decrypted.get('memory_root'):
        state['memory_roots'] = merge_unique(
            state['memory_roots'],
            [{
                **decrypted['memory_root'],
                'created_at': decrypted.get('exported_at', now_iso()),
            }],
            'root_commitment_hash',
        )
    state['claim_commitments'] = merge_unique(state['claim_commitments'], decrypted.get('claims', []), 'commitment_hash')
    state['trigger_heads'] = merge_unique(state['trigger_heads'], decrypted.get('triggers', []), 'id')

    cursor = now_iso()
    deltas = {
        'memory_roots': state['memory_roots'][-10:],
        'claim_commitments': state['claim_commitments'][-25:],
        'trigger_heads': state['trigger_heads'][-25:],
    }
    audit_event = {
        'id': f"audit-{cursor}",
        'created_at': cursor,
        'device_id': request.client_signature.device_id,
        'direction': decrypted.get('direction', 'push'),
        'summary': f"Processed {len(decrypted.get('claims', []))} claim commitments and {len(decrypted.get('triggers', []))} trigger digests.",
    }
    state['audit_log'].append(audit_event)
    state['cursor'] = cursor
    save_state(state)

    response_payload = {
        'server_id': SERVER_ID,
        'received': len(decrypted.get('claims', [])) + len(decrypted.get('triggers', [])) + (1 if decrypted.get('memory_root') else 0),
        'next_cursor': cursor,
        'remote_deltas': deltas,
        'audit_event': audit_event,
        'advisory': 'The hub only coordinates commitment digests by default. Raw memories require an explicit receipt export from Iris.',
    }
    encrypted = encrypt_envelope(response_payload, request.envelope)
    signed_response, signature_hex = sign_response({
        'server_id': SERVER_ID,
        'payload_hash': canonicalize(encrypted),
        'issued_at': now_iso(),
        'next_cursor': cursor,
    })
    return {
        'payload': encrypted,
        'signed_response': signed_response,
        'signature_hex': signature_hex,
        'public_key_hex': public_key_hex,
    }
