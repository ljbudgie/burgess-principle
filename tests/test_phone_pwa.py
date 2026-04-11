"""Targeted tests for the phone-first sovereign PWA assets."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = (ROOT / 'index.html').read_text(encoding='utf-8')
MANIFEST = json.loads((ROOT / 'manifest.json').read_text(encoding='utf-8'))
SERVICE_WORKER = (ROOT / 'service-worker.js').read_text(encoding='utf-8')


def test_index_contains_phone_claim_builder_hooks():
    assert '+ New Claim' in INDEX
    assert 'voiceStatus' in INDEX
    assert 'claimProfilePanel' in INDEX
    assert 'indexedDB' in INDEX
    assert 'Export Vault' in INDEX
    assert 'Import Vault' in INDEX
    assert 'queue-onchain-fingerprint' in INDEX


def test_manifest_declares_standalone_shortcuts():
    assert MANIFEST['display'] == 'standalone'
    assert MANIFEST['start_url'] == '/?source=pwa'
    shortcut_urls = {shortcut['url'] for shortcut in MANIFEST['shortcuts']}
    assert '/?shortcut=crypto-exchange' in shortcut_urls
    assert '/?shortcut=direct-debit' in shortcut_urls
    assert '/?shortcut=benefits' in shortcut_urls


def test_service_worker_caches_assets_and_syncs_reminders():
    assert 'PRECACHE_URLS' in SERVICE_WORKER
    assert 'burgess-fingerprint-sync' in SERVICE_WORKER
    assert 'burgess-reminder-sync' in SERVICE_WORKER
    assert "'/api/queue-onchain-fingerprint'" in SERVICE_WORKER
    assert '14-day escalation reminder' in SERVICE_WORKER
