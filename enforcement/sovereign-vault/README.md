# Sovereign Personal Vault

Optional cryptographic enforcement layer for the Burgess Principle.

Lightweight TypeScript library. Keeps facts private on-device. Sends only SHA-256 commitment. Receives signed Ed25519 receipts: **SOVEREIGN** (human reviewed specific case) or **NULL** (no specific human review). AES-256-GCM encrypted vault. Supports challenge() and exportRecord().

### Quick start

```ts
import { SovereignVault } from './src/index.js';

const vault = new SovereignVault("your-strong-passphrase");

await vault.storeFacts({ situation: "...", requestedAction: "..." });
const commitment = await vault.generateCommitment();
await vault.receiveReceipt(signedReceipt);
const bundle = await vault.exportRecord();
Full source: src/index.ts
This layer is optional.
