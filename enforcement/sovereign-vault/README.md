# Sovereign Personal Vault

**Optional cryptographic enforcement layer** for the Burgess Principle.

This is a lightweight, standalone TypeScript library (`iris-gate-person`) that gives you quiet mathematical backup when the gentle templates aren't quite enough.

It lets you keep every sensitive detail of your situation private on your own device, while creating a tamper-evident record that clearly shows whether a real human reviewed the specific facts of *your* case.

### How it works (simply)
- Store your private facts locally.
- Send only a cryptographic fingerprint (SHA-256 commitment) to the organisation.
- Receive a signed Ed25519 receipt: **SOVEREIGN** (a human personally reviewed your specific situation) or **NULL** (no specific human review — automated/generic).
- Everything stays encrypted in an AES-256-GCM vault on your device.
- You can challenge a NULL receipt or export a complete, independently verifiable bundle ready for tribunals or courts.

It is codependent with the main Iris agent but works perfectly on its own.

### Quick start (TypeScript)

```ts
import { SovereignVault } from './iris-gate-person';

const vault = new SovereignVault("your-strong-passphrase");

// Store your private facts (never leaves your device)
await vault.storeFacts({
  situation: "Full details of my case here...",
  requestedAction: "...",
  evidence: "..."
});

// Generate and send only the commitment (fingerprint)
const commitment = await vault.generateCommitment();

// Later, receive and store their signed receipt
await vault.receiveReceipt(signedReceiptFromOrganisation);

// Challenge a NULL decision if needed
const challenge = await vault.challenge();

// Export a tribunal-ready, verifiable record
const exportBundle = await vault.exportRecord();
