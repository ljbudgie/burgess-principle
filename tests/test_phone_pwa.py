"""Targeted tests for the phone-first sovereign PWA assets."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = (ROOT / 'index.html').read_text(encoding='utf-8')
MANIFEST = json.loads((ROOT / 'manifest.json').read_text(encoding='utf-8'))
SERVICE_WORKER = (ROOT / 'service-worker.js').read_text(encoding='utf-8')
SIGNED_UPDATE_MANIFEST = json.loads((ROOT / 'signed-update-manifest.json').read_text(encoding='utf-8'))


def test_index_contains_phone_claim_builder_hooks():
    assert '+ New Claim' in INDEX
    assert 'voiceStatus' in INDEX
    assert 'claimProfilePanel' in INDEX
    assert 'indexedDB' in INDEX
    assert 'Setup My Identity' in INDEX
    assert 'Enable Mirror Mode' in INDEX
    assert 'mirrorModeToggle' in INDEX
    assert 'profileIdentityGreetingStyle' in INDEX
    assert 'profileIdentityCustomGreeting' in INDEX
    assert 'profileIdentityReflectionScope' in INDEX
    assert "return `${summary.name} — Mirror Mode active. The handshake continues on this device.`;" in INDEX
    assert 'profileIdentityName' in INDEX
    assert 'profileIdentityPassphrase' in INDEX
    assert '/api/my-profile' in INDEX
    assert 'Export Vault' in INDEX
    assert 'Import Vault' in INDEX
    assert 'queue-onchain-fingerprint' in INDEX
    assert 'verifyPwaIntegrityBtn' in INDEX
    assert 'applyVerifiedUpdateBtn' in INDEX
    assert 'signed-update-manifest.json' in INDEX
    assert 'PWA_UPDATE_PUBLIC_KEY_HEX' in INDEX


def test_manifest_declares_standalone_shortcuts():
    assert MANIFEST['display'] == 'standalone'
    assert 'standalone' in MANIFEST['display_override']
    assert MANIFEST['start_url'] == '/?source=pwa'
    shortcut_urls = {shortcut['url'] for shortcut in MANIFEST['shortcuts']}
    assert '/?shortcut=burgess-check&source=sovereign-mode' in shortcut_urls
    assert '/?shortcut=crypto-exchange' in shortcut_urls
    assert '/?shortcut=direct-debit' in shortcut_urls
    assert '/?shortcut=benefits' in shortcut_urls


def test_service_worker_caches_assets_and_syncs_reminders():
    assert 'PRECACHE_URLS' in SERVICE_WORKER
    assert 'staleWhileRevalidate' in SERVICE_WORKER
    assert 'navigationPreload' in SERVICE_WORKER
    assert 'burgess-fingerprint-sync' in SERVICE_WORKER
    assert 'burgess-reminder-sync' in SERVICE_WORKER
    assert 'burgess-critical-refresh' in SERVICE_WORKER
    assert "'/api/queue-onchain-fingerprint'" in SERVICE_WORKER
    assert '14-day escalation reminder' in SERVICE_WORKER
    assert "event.data.type === 'SKIP_WAITING'" in SERVICE_WORKER


def test_signed_update_manifest_requires_consent_and_assets():
    assert SIGNED_UPDATE_MANIFEST['key_id'] == 'iris-pwa-ed25519-2026-04'
    assert SIGNED_UPDATE_MANIFEST['public_key_hex']
    assert SIGNED_UPDATE_MANIFEST['signature']
    payload = SIGNED_UPDATE_MANIFEST['signed_payload']
    assert payload['consent_required'] is True
    assert payload['hash_algorithm'] == 'sha256'
    assert '/service-worker.js' in payload['critical_paths']
    assert any(asset['path'] == '/index.html' for asset in payload['assets'])
