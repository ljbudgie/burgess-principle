import assert from 'node:assert/strict';
import { execFileSync, spawnSync } from 'node:child_process';
import { createHash } from 'node:crypto';
import { existsSync, mkdtempSync, readFileSync, rmSync } from 'node:fs';
import { join } from 'node:path';
import { tmpdir } from 'node:os';
import test from 'node:test';
import { fileURLToPath } from 'node:url';

import { ed25519 } from '@noble/curves/ed25519.js';
import { bytesToHex } from '@noble/hashes/utils.js';

import { generateCommitment } from '../src/generate-commitment.ts';
import { SovereignVault, type SignedReceipt } from '../src/index.ts';

const VALID_PASSPHRASE = 'correct horse battery staple';
const RECEIPT_PRIVATE_KEY = Uint8Array.from({ length: 32 }, (_, index) => index + 1);
const PACKAGE_ROOT = fileURLToPath(new URL('..', import.meta.url));
const GENERATE_COMMITMENT_SCRIPT = `${PACKAGE_ROOT}/src/generate-commitment.ts`;

function buildSignedReceipt(type: SignedReceipt['type'], commitment: string): SignedReceipt {
  const reviewerPubKey = bytesToHex(ed25519.getPublicKey(RECEIPT_PRIVATE_KEY));
  const receipt = {
    type,
    commitment,
    reviewerPubKey,
    signature: '',
    date: '2026-04-11T21:37:37.939Z',
    organisation: 'Example Council',
  };
  const message = JSON.stringify(
    {
      commitment: receipt.commitment,
      date: receipt.date,
      organisation: receipt.organisation,
      type: receipt.type,
    },
    ['commitment', 'date', 'organisation', 'type'],
  );
  return {
    ...receipt,
    signature: bytesToHex(ed25519.sign(new TextEncoder().encode(message), RECEIPT_PRIVATE_KEY)),
  };
}

test('generateCommitment returns a verifiable hash with the original facts', () => {
  const facts = 'My council tax account was sent to enforcement without review';
  const result = generateCommitment(facts);

  assert.equal(result.facts, facts);
  assert.match(result.salt, /^[0-9a-f]{64}$/);
  assert.match(result.commitment, /^[0-9a-f]{64}$/);
  assert.equal(
    result.commitment,
    createHash('sha256').update(result.salt + facts).digest('hex'),
  );
});

test('generate-commitment CLI writes the opening file and prints only the hash', () => {
  const tempDir = mkdtempSync(join(tmpdir(), 'sovereign-vault-cli-'));
  try {
    const facts = 'I need a human review of an automated refusal';
    const result = execFileSync(
      'node',
      ['--experimental-strip-types', GENERATE_COMMITMENT_SCRIPT, facts],
      {
        cwd: tempDir,
        encoding: 'utf8',
        env: process.env,
        stdio: ['ignore', 'pipe', 'pipe'],
      },
    ).trim();
    const openingPath = join(tempDir, '.commitment-opening.json');

    assert.equal(existsSync(openingPath), true);
    const opening = JSON.parse(readFileSync(openingPath, 'utf8'));
    assert.equal(opening.facts, facts);
    assert.equal(opening.commitment, result);
    assert.match(opening.salt, /^[0-9a-f]{64}$/);
  } finally {
    rmSync(tempDir, { recursive: true, force: true });
  }
});

test('generate-commitment CLI exits with usage when facts are omitted', () => {
  const result = spawnSync(
    'node',
    ['--experimental-strip-types', GENERATE_COMMITMENT_SCRIPT],
    {
      cwd: PACKAGE_ROOT,
      encoding: 'utf8',
    },
  );

  assert.equal(result.status, 1);
  assert.match(result.stderr, /Usage:/);
});

test('SovereignVault enforces passphrase and commitment prerequisites', async () => {
  assert.throws(() => new SovereignVault('short'), /at least 8 characters/);

  const vault = new SovereignVault(VALID_PASSPHRASE);
  await assert.rejects(vault.generateCommitment(), /No facts stored yet/);
  assert.throws(() => vault.getCommitmentSalt(), /No commitment generated yet/);
});

test('SovereignVault stores signed receipts, exports them, and challenges NULL results', async () => {
  const vault = new SovereignVault(VALID_PASSPHRASE);
  await vault.storeFacts({
    situation: 'My data was processed in bulk',
    requestedAction: 'Provide a human review',
    evidence: 'Reference 123',
  });

  const commitment = await vault.generateCommitment();
  const nullReceipt = buildSignedReceipt('NULL', commitment);
  const sovereignReceipt = buildSignedReceipt('SOVEREIGN', commitment);

  await vault.receiveReceipt(nullReceipt);
  await vault.receiveReceipt(sovereignReceipt);

  const exported = await vault.exportRecord();
  assert.equal(exported.receipts.length, 2);
  assert.deepEqual(exported.receipts.map((receipt) => receipt.type), ['NULL', 'SOVEREIGN']);
  assert.match(exported.commitment, /^[0-9a-f]{64}$/);

  const challenge = await vault.challenge();
  assert.equal(challenge.nullReceipts.length, 1);
  assert.deepEqual(challenge.nullReceipts[0], nullReceipt);
  assert.match(challenge.commitment, /^[0-9a-f]{64}$/);
});

test('SovereignVault rejects receipts with invalid signatures or missing reviewer keys', async () => {
  const vault = new SovereignVault(VALID_PASSPHRASE);
  await vault.storeFacts({
    situation: 'My complaint was closed automatically',
    requestedAction: 'Escalate to a human reviewer',
  });

  const commitment = await vault.generateCommitment();
  const receipt = buildSignedReceipt('NULL', commitment);

  await assert.rejects(
    vault.receiveReceipt({ ...receipt, signature: `${'0'.repeat(127)}1` }),
    /Invalid receipt signature/,
  );
  await assert.rejects(
    vault.receiveReceipt({ ...receipt, reviewerPubKey: '' }),
    /reviewerPubKey/,
  );
});

test('SovereignVault generates and verifies on-chain claims', async () => {
  const vault = new SovereignVault(VALID_PASSPHRASE);
  await vault.storeFacts({
    situation: 'My access request was rejected',
    requestedAction: 'Reopen the case',
  });

  const claim = await vault.generateOnchainClaim(RECEIPT_PRIVATE_KEY, 'Example Council', 'dispute', 3600);

  assert.equal(claim.target, 'Example Council');
  assert.equal(claim.category, 'dispute');
  assert.equal(claim.expiry, 3600);
  assert.match(claim.commitmentHash, /^[0-9a-f]{64}$/);
  assert.match(claim.signature, /^[0-9a-f]+$/);
  assert.match(claim.publicKey, /^[0-9a-f]{64}$/);
  assert.equal(SovereignVault.verifyOnchainReceipt(claim.commitmentHash, claim.signature, claim.publicKey), true);
  const lastByte = parseInt(claim.signature.slice(-2), 16);
  const flippedByte = (lastByte ^ 0xff).toString(16).padStart(2, '0');
  assert.equal(
    SovereignVault.verifyOnchainReceipt(claim.commitmentHash, claim.signature.slice(0, -2) + flippedByte, claim.publicKey),
    false,
  );

  await assert.rejects(vault.generateOnchainClaim(RECEIPT_PRIVATE_KEY, '', 'dispute'), /target must not be empty/);
  await assert.rejects(vault.generateOnchainClaim(RECEIPT_PRIVATE_KEY, 'Example Council', ''), /category must not be empty/);
});
