/**
 * generate-commitment.ts
 *
 * Standalone utility for the Sovereign Personal Vault.
 * Generates a fresh SHA-256 commitment from your facts and a random salt.
 *
 * Usage (Node.js ≥ 18):
 *   npx ts-node src/generate-commitment.ts "I received a bill for £400 that I believe was already paid"
 *
 * Usage (compiled):
 *   node dist/generate-commitment.js "My council tax account was sent to enforcement without review"
 *
 * What it does:
 *   1. Takes your facts as a single string argument.
 *   2. Generates a fresh random 32-byte salt (nonce).
 *   3. Computes SHA-256( salt + facts ).
 *   4. Prints only the commitment hash to stdout.
 *   5. Optionally saves the opening values (salt + facts) to a local file
 *      so you can prove your commitment later if needed.
 *
 * No new dependencies — uses Node.js built-in 'crypto' module.
 */

import { createHash, randomBytes } from 'crypto';
import { writeFileSync } from 'fs';
import { join } from 'path';

function generateCommitment(facts: string): {
  commitment: string;
  salt: string;
  facts: string;
} {
  const salt = randomBytes(32).toString('hex');
  const preimage = salt + facts;
  const commitment = createHash('sha256').update(preimage).digest('hex');

  return { commitment, salt, facts };
}

// --- CLI entry point ---
if (process.argv[1]?.endsWith('generate-commitment.ts') ||
    process.argv[1]?.endsWith('generate-commitment.js')) {

  const facts = process.argv[2];

  if (!facts) {
    console.error(
      '\nUsage:\n' +
      '  npx ts-node src/generate-commitment.ts "your facts here"\n' +
      '  node dist/generate-commitment.js "your facts here"\n'
    );
    process.exit(1);
  }

  const result = generateCommitment(facts);

  // Print only the hash — safe to paste into a template.
  console.log(result.commitment);

  // Save opening values locally so the user can prove the commitment later.
  const openingPath = join(process.cwd(), '.commitment-opening.json');
  writeFileSync(openingPath, JSON.stringify({
    commitment: result.commitment,
    salt: result.salt,
    facts: result.facts,
    createdAt: new Date().toISOString(),
    note: 'Keep this file private. You only need to share the commitment hash.'
  }, null, 2));

  console.error(`\nOpening values saved to ${openingPath}`);
  console.error('Share only the hash above. Keep the opening file private.\n');
}

export { generateCommitment };
