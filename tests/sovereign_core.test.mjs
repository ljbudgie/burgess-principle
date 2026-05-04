import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import test from 'node:test';
import vm from 'node:vm';
import { fileURLToPath } from 'node:url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const REPO_ROOT = resolve(__dirname, '..');

const context = vm.createContext({
  globalThis: {},
  self: {},
  window: {},
  console,
  setTimeout,
  clearTimeout,
});
context.globalThis = context;
context.self = context;
context.window = context;

for (const file of [
  resolve(REPO_ROOT, 'sovereign-core/types.js'),
  resolve(REPO_ROOT, 'sovereign-core/utils.js'),
  resolve(REPO_ROOT, 'sovereign-core/commitment-orchestrator.js'),
  resolve(REPO_ROOT, 'sovereign-core/audit-engine.js'),
  resolve(REPO_ROOT, 'sovereign-core/profile-manager.js'),
]) {
  vm.runInContext(readFileSync(file, 'utf8'), context, { filename: file });
}

const core = context.IrisSovereignCore;

async function sha256Hex(value) {
  const input = typeof value === 'string' ? value : JSON.stringify(value);
  const buffer = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(input));
  return Array.from(new Uint8Array(buffer)).map(byte => byte.toString(16).padStart(2, '0')).join('');
}

test('utils normalize connectivity profiles and build sync policies', () => {
  assert.equal(core.utils.normalizeConnectivityProfile('fiber optic'), 'fiber_hardwired');
  assert.equal(core.utils.connectivityProfileLabel('starlink'), 'Starlink Hardwired');
  const policy = core.utils.buildSovereignSyncPolicy(
    { connectivity_profile: 'fiber_hardwired', prefer_queued_syncs: false },
    { online: true, connection_type: 'ethernet', effective_type: '4g', rtt_ms: 40 }
  );
  assert.equal(policy.mode, 'balanced');
  assert.equal(policy.allow_background_flush, true);
});

test('utils normalize network snapshots from sparse and camelCase input', () => {
  const snapshot = core.utils.normalizeNetworkSnapshot({
    online: true,
    effectiveType: '4G',
    downlink: '25.5',
    rtt: undefined,
    saveData: true,
  });

  assert.equal(snapshot.online, true);
  assert.equal(snapshot.effective_type, '4g');
  assert.equal(snapshot.downlink_mbps, 25.5);
  assert.equal(snapshot.rtt_ms, 0);
  assert.equal(snapshot.save_data, true);
  assert.match(snapshot.updated_at, /^\d{4}-\d{2}-\d{2}T/);
});

test('utils capture null connection as an offline local snapshot', () => {
  const snapshot = core.utils.captureNetworkSnapshot(null, false);

  assert.equal(snapshot.online, false);
  assert.equal(snapshot.connection_type, '');
  assert.equal(snapshot.effective_type, '');
  assert.equal(snapshot.wired_detected, false);
  assert.equal(snapshot.save_data, false);
});

test('utils build connectivity tags from preferences and exact text matches', () => {
  const tags = core.utils.buildConnectivityTags(
    {
      connectivity_profile: '',
      low_wireless_mode: true,
      connectivity_note: 'ONT to Ethernet, Wi-Fi off, fixed wireless fallback; starfleet is not a connectivity profile.',
    },
    'Manual sync over DSL or cable if needed.'
  );

  assert.ok(tags.includes('environment'));
  assert.ok(tags.includes('connectivity'));
  assert.ok(tags.includes('other-link'));
  assert.ok(tags.includes('minimized-wireless'));
  assert.ok(tags.includes('ont'));
  assert.ok(tags.includes('ethernet'));
  assert.ok(tags.includes('wifi-off'));
  assert.ok(tags.includes('fixed-wireless'));
  assert.ok(tags.includes('queued-sync'));
  assert.ok(tags.includes('dsl'));
  assert.ok(tags.includes('cable'));
  assert.equal(tags.includes('starlink'), false);
});

test('utils trigger presets expose complete advisory template metadata', () => {
  const presets = core.utils.createTriggerTemplatePresets();

  assert.ok(Object.keys(presets).length >= 6);
  for (const preset of Object.values(presets)) {
    assert.equal(typeof preset.natural_language, 'string');
    assert.equal(typeof preset.label, 'string');
    assert.ok(['keyword', 'periodic'].includes(preset.type));
    assert.equal(typeof preset.interval_hours, 'number');
    assert.ok(Array.isArray(preset.detection_sources));
    assert.ok(Array.isArray(preset.keywords));
    assert.equal(typeof preset.description, 'string');
  }
});

test('utils keep sync queued or offline for slow, save-data, and offline states', () => {
  const slow = core.utils.buildSovereignSyncPolicy(
    { connectivity_profile: 'fiber_hardwired', prefer_queued_syncs: false },
    { online: true, connection_type: 'ethernet', effective_type: '4g', rtt_ms: 1200 }
  );
  const saveData = core.utils.buildSovereignSyncPolicy(
    { connectivity_profile: 'fiber_hardwired', prefer_queued_syncs: false },
    { online: true, connection_type: 'ethernet', effective_type: '4g', save_data: true }
  );
  const offline = core.utils.buildSovereignSyncPolicy(
    { connectivity_profile: 'starlink_hardwired', prefer_queued_syncs: false },
    { online: false, connection_type: 'ethernet' }
  );

  assert.equal(slow.mode, 'queued');
  assert.equal(slow.allow_background_flush, false);
  assert.equal(saveData.mode, 'queued');
  assert.equal(saveData.allow_background_flush, false);
  assert.equal(offline.mode, 'offline');
  assert.equal(offline.prefer_queue_registration, true);
});

test('commitment orchestrator creates verifiable records', async () => {
  const orchestrator = core.createCommitmentOrchestrator({
    sha256Hex,
    canonicalize: core.utils.canonicalize,
    generateId: prefix => `${prefix}-1`,
  });
  const record = await orchestrator.createSignedRecord({
    namespace: 'memory',
    payload: { title: 'Connectivity updated', profile: 'fiber_hardwired' },
  });
  assert.equal(record.namespace, 'memory');
  assert.match(record.commitment_hash, /^[0-9a-f]{64}$/);
  await assert.doesNotReject(() => orchestrator.verifySignedRecord(record));
});

test('audit engine builds merkle proofs and validates chains', async () => {
  const audit = core.createAuditEngine({
    sha256Hex,
    canonicalize: core.utils.canonicalize,
  });
  const merkle = await audit.buildMerkleState(['a', 'b', 'c'], 1);
  assert.match(merkle.root, /^[0-9a-f]{64}$/);
  assert.equal(merkle.proof.length > 0, true);
  assert.equal(await audit.verifyMerkleProof('b', merkle.proof, merkle.root), true);
  const verified = await audit.verifySequentialChain([
    { id: 'one', previous_commitment_hash: '', commitment_hash: 'a' },
    { id: 'two', previous_commitment_hash: 'a', commitment_hash: 'b' },
  ]);
  assert.equal(verified, 2);
});

test('audit engine handles empty merkle inputs and rejects mismatched proofs', async () => {
  const audit = core.createAuditEngine({
    sha256Hex,
    canonicalize: core.utils.canonicalize,
  });

  const emptyMerkle = await audit.buildMerkleState([], 0);
  assert.equal(emptyMerkle.root, '');
  assert.equal(emptyMerkle.proof.length, 0);
  const merkle = await audit.buildMerkleState(['a', 'b', 'c'], 1);

  assert.equal(await audit.verifyMerkleProof('z', merkle.proof, merkle.root), false);
  assert.equal(await audit.verifyMerkleProof('b', [{ hash: '', position: 'left' }], merkle.root), false);
  await assert.rejects(
    () => audit.verifyMerkleProof('', merkle.proof, merkle.root),
    /requires a leaf hash/
  );
});

test('audit engine rejects broken sequential commitment chains', async () => {
  const audit = core.createAuditEngine({
    sha256Hex,
    canonicalize: core.utils.canonicalize,
  });

  await assert.rejects(
    () => audit.verifySequentialChain([
      { id: 'one', previous_commitment_hash: '', commitment_hash: 'a' },
      { id: 'two', previous_commitment_hash: 'wrong', commitment_hash: 'b' },
    ]),
    /Commitment chain broke at two/
  );
  assert.equal(await audit.verifySequentialChain([]), 0);
});

test('profile manager normalizes hub preferences into the unified sovereignty profile', async () => {
  const store = new Map();
  const manager = core.createProfileManager({
    storage: {
      getSetting: async key => store.get(key),
      saveSetting: async (key, value) => store.set(key, value),
    },
    sha256Hex,
    canonicalize: core.utils.canonicalize,
  });
  const profile = await manager.syncHubPreferences({
    connectivity_profile: 'starlink',
    low_wireless_mode: true,
    prefer_queued_syncs: true,
    connectivity_note: 'Dish outside, ethernet indoors',
  });
  assert.equal(profile.connectivity_profile, 'starlink_hardwired');
  assert.equal(profile.minimize_wireless, true);
  assert.match(profile.profile_fingerprint, /^[0-9a-f]{64}$/);
});
