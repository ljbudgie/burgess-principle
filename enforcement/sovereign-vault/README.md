# Sovereign Personal Vault

**Optional** cryptographic enforcement layer for the Burgess Principle.

> **You do not need this to use the Burgess Principle.** The human-first templates and the one-question approach work perfectly on their own. This vault is for people who want an extra layer of mathematical proof.

## What it does

The Sovereign Personal Vault is a lightweight TypeScript library that lets you:

1. **Store the facts of your case** — encrypted on your own device (AES-256-GCM). Nothing leaves your machine.
2. **Generate a commitment** — a SHA-256 hash of your facts that you can share with an institution without revealing any personal details.
3. **Receive a signed receipt** — the institution returns an Ed25519-signed response saying whether a real human reviewed your specific case (`SOVEREIGN`) or not (`NULL`).
4. **Export a tamper-evident record** — a bundle you can keep, share, or present as evidence.

## Who is this for?

- Privacy-conscious individuals who want cryptographic proof alongside their written correspondence.
- Developers building tools on top of the Burgess Principle.
- Anyone who wants verifiable, tamper-evident records of institutional responses.

## Quick start

```ts
import { SovereignVault } from './src/index.js';

const vault = new SovereignVault("your-strong-passphrase");
await vault.storeFacts({ situation: "...", requestedAction: "..." });
const commitment = await vault.generateCommitment();
await vault.receiveReceipt(signedReceipt);
const bundle = await vault.exportRecord();
```

## Files in this folder

| File / Folder | Purpose |
|---|---|
| `src/index.ts` | Main library source code |
| `package.json` | Node.js package configuration |
| `tsconfig.json` | TypeScript compiler settings |

## Remember

This layer is **completely optional**. The Burgess Principle works without it. The vault simply adds on-device encryption and tamper-evident receipts for users who want cryptographic proof of their verification results.