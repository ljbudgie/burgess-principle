"""Targeted tests for the phone-first sovereign PWA assets."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = (ROOT / 'index.html').read_text(encoding='utf-8')
MANIFEST = json.loads((ROOT / 'manifest.json').read_text(encoding='utf-8'))
SERVICE_WORKER = (ROOT / 'service-worker.js').read_text(encoding='utf-8')
SIGNED_UPDATE_MANIFEST = json.loads((ROOT / 'signed-update-manifest.json').read_text(encoding='utf-8'))
PHASE3_CLIENT = (ROOT / 'phase3-memory-hub.js').read_text(encoding='utf-8')
MEMORY_WORKER = (ROOT / 'memory-palace-worker.js').read_text(encoding='utf-8')
HUB_APP = (ROOT / 'sovereign-hub-example' / 'app.py').read_text(encoding='utf-8')


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
    assert 'triggerPassphrase' in INDEX
    assert 'triggerNaturalLanguage' in INDEX
    assert 'triggerTemplatePreset' in INDEX
    assert 'fiber_hardwired_review' in INDEX
    assert 'Connectivity profile check-in (Starlink vs Fiber)' in INDEX
    assert 'Environmental note on wired setup' in INDEX
    assert 'applyTriggerTemplateBtn' in INDEX
    assert 'parseTriggerRuleBtn' in INDEX
    assert 'scanClipboardBtn' in INDEX
    assert 'triggerBackgroundUnlockToggle' in INDEX
    assert 'triggerLedgerList' in INDEX
    assert 'voice_command' in INDEX
    assert 'HELP_ME_NOW_PATTERN' in INDEX
    assert 'hubConnectivityProfile' in INDEX
    assert 'Fiber Hardwired' in INDEX
    assert 'Minimized local wireless preference (user-controlled)' in INDEX
    assert 'hubLowWirelessToggle' in INDEX
    assert 'hubQueuedSyncPreferenceToggle' in INDEX
    assert 'phase3-memory-hub.js' in INDEX


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
    assert 'burgess-trigger-queue-sync' in SERVICE_WORKER
    assert "'/api/queue-onchain-fingerprint'" in SERVICE_WORKER
    assert '14-day escalation reminder' in SERVICE_WORKER
    assert "event.data.type === 'SKIP_WAITING'" in SERVICE_WORKER
    assert 'triggerQueue' in SERVICE_WORKER
    assert 'triggerLedger' in SERVICE_WORKER
    assert 'triggerReceipts' in SERVICE_WORKER
    assert 'memoryEntries' in SERVICE_WORKER
    assert 'memoryRoots' in SERVICE_WORKER
    assert 'memoryReceipts' in SERVICE_WORKER
    assert 'hubSyncQueue' in SERVICE_WORKER
    assert 'flushHubSyncQueue' in SERVICE_WORKER
    assert 'appendTriggerLedgerEvent' in SERVICE_WORKER
    assert 'Human review required' in SERVICE_WORKER


def test_signed_update_manifest_requires_consent_and_assets():
    assert SIGNED_UPDATE_MANIFEST['key_id'] == 'iris-pwa-ed25519-2026-04-v130'
    assert SIGNED_UPDATE_MANIFEST['public_key_hex']
    assert SIGNED_UPDATE_MANIFEST['signature']
    payload = SIGNED_UPDATE_MANIFEST['signed_payload']
    assert payload['consent_required'] is True
    assert payload['hash_algorithm'] == 'sha256'
    assert '/service-worker.js' in payload['critical_paths']
    assert any(asset['path'] == '/index.html' for asset in payload['assets'])


def test_docs_cover_phase_2_living_triggers():
    docs = (ROOT / 'SOVEREIGN_MODE.md').read_text(encoding='utf-8')
    assert '## Phase 2 — Proactive Living Triggers Engine' in docs
    assert '### Environmental trigger templates' in docs
    assert '### Sovereignty Audit' in docs
    assert 'device-only background unlock' in docs
    assert 'triggerQueue' in docs


def test_phase_3_memory_palace_and_hub_assets_exist():
    assert 'memoryPalacePanel' in PHASE3_CLIENT
    assert 'verifyMemoryIntegrity' in PHASE3_CLIENT
    assert 'runFullSystemIntegrityCheck' in PHASE3_CLIENT
    assert 'performHubSync' in PHASE3_CLIENT
    assert 'memoryEnvironmentalNoteBtn' in PHASE3_CLIENT
    assert 'hubEnvironmentFingerprint' in PHASE3_CLIENT
    assert 'normalizeConnectivityProfile' in PHASE3_CLIENT
    assert 'connectivity_suggestions' in PHASE3_CLIENT
    assert 'memoryEntries' in PHASE3_CLIENT
    assert 'hubSyncQueue' in PHASE3_CLIENT
    assert 'buildMerkleState' in MEMORY_WORKER
    assert 'searchEntries' in MEMORY_WORKER
    assert '/api/sovereign-sync-v2' in HUB_APP
    assert 'public_key_hex' in HUB_APP


def test_docs_cover_phase_3_memory_palace_and_hub():
    docs = (ROOT / 'SOVEREIGN_MODE.md').read_text(encoding='utf-8')
    assert '## Phase 3 — Cryptographic Memory Palace Evolution + Sovereign Hub Mode 2.0' in docs
    assert '### Hardwired connectivity options for personal environmental preferences' in docs
    assert '### Memory Palace environmental notes' in docs
    assert '#### Diagram — Hardwired Connectivity Options Flow' in docs
    assert 'Fiber hardwired review' in docs
    assert 'memoryEntries' in docs
    assert 'sovereign-hub-example/' in docs
    assert 'Push commitments' in docs
