# Sovereign Personal Vault

Optional cryptographic enforcement layer for the Burgess Principle.

This is a lightweight standalone TypeScript library (iris-gate-person) that keeps sensitive facts private on your own device and creates verifiable proof of human review.

### How it works
- Store your private facts locally (never leaves your device).
- Generate and send only a SHA-256 commitment (cryptographic fingerprint).
- Receive a signed Ed25519 receipt: **SOVEREIGN** (a human personally reviewed the specific facts of your case) or **NULL** (no specific human review — automated/generic).
- Everything is stored in an AES-256-GCM encrypted vault.
- You can challenge a NULL receipt or export a tribunal-ready, independently verifiable bundle.

### Quick start

```ts
import { SovereignVault } from './src/index.js';

const vault = new SovereignVault("your-strong-passphrase");

await vault.storeFacts({
  situation: "Full details of my case here...",
  requestedAction: "..."
});

const commitment = await vault.generateCommitment();

// Later when you receive their signed receipt:
await vault.receiveReceipt(signedReceipt);

// Export a tribunal-ready bundle
const bundle = await vault.exportRecord();
Full source is in src/index.ts.
This layer is entirely optional. The Burgess Principle stands strong with just the calm templates. The sovereign vault adds cryptographic proof when you need it.
Back to the Burgess Principle
---
