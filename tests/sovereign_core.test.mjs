import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import test from 'node:test';
import vm from 'node:vm';

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
  '/home/runner/work/burgess-principle/burgess-principle/sovereign-core/types.js',
  '/home/runner/work/burgess-principle/burgess-principle/sovereign-core/utils.js',
  '/home/runner/work/burgess-principle/burgess-principle/sovereign-core/commitment-orchestrator.js',
  '/home/runner/work/burgess-principle/burgess-principle/sovereign-core/audit-engine.js',
  '/home/runner/work/burgess-principle/burgess-principle/sovereign-core/profile-manager.js',
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
  const verified = await audit.verifySequentialChain([
    { id: 'one', previous_commitment_hash: '', commitment_hash: 'a' },
    { id: 'two', previous_commitment_hash: 'a', commitment_hash: 'b' },
  ]);
  assert.equal(verified, 2);
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
