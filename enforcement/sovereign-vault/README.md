# Sovereign Personal Vault

**Optional cryptographic enforcement layer** for the Burgess Principle.

This is a lightweight, standalone TypeScript library (`iris-gate-person`) that acts as quiet mathematical backup when the gentle templates aren't enough.

It keeps every sensitive detail of your situation private on your own device, while letting you create a tamper-evident record that clearly shows whether a real human reviewed the specific facts of *your* case.

### How it works

- Store your private facts locally (never leaves your device).
- Generate and send only a SHA-256 commitment (cryptographic fingerprint).
- Receive a signed Ed25519 receipt: **SOVEREIGN** (a human personally reviewed your specific situation) or **NULL** (no specific human review — automated/generic).
- All data is stored in an AES-256-GCM encrypted vault on your device.
- You can `challenge()` a NULL receipt or `exportRecord()` a complete, independently verifiable bundle ready for tribunals or courts.

It works standalone or alongside the main Iris agent.

### Quick start

```ts
import { SovereignVault } from './src/index.js';

const vault = new SovereignVault("your-strong-passphrase");

await vault.storeFacts({
  situation: "Full details of my case here...",
  requestedAction: "...",
  evidence: "..."          // optional
});

// Generate and send only the commitment (fingerprint only)
const commitment = await vault.generateCommitment();

// Later, receive and store their signed receipt
await vault.receiveReceipt(signedReceiptFromOrganisation);

// Challenge a NULL decision if needed
const challenge = await vault.challenge();

// Export a tribunal-ready, independently verifiable bundle
const exportBundle = await vault.exportRecord();
Installation
cd enforcement/sovereign-vault
npm install
npm run build
Full source is in src/index.ts.
This layer is entirely optional.
The Burgess Principle works powerfully with just the calm templates and a respectful request for human review.
The sovereign vault simply adds extra strength — cryptographic proof — when you need it.
Back to the Burgess Principle
Commit it with a message like: `Update sovereign-vault README with clean quick start and installation`

---

After you commit this, the sovereign-vault folder will look complete and professional.

### Final small step (optional but nice)

If you want, add this one line to `CONTRIBUTING.md` (under the contributions section):

```markdown
- Optional enforcement components like the sovereign-vault cryptographic layer that add mathematical accountability while preserving the calm, human-first tone.
