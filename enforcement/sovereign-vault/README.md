### Quick start

```ts
import { SovereignVault } from './src/index.js';

const vault = new SovereignVault("your-strong-passphrase");

await vault.storeFacts({
  situation: "Full details of my case here...",
  requestedAction: "..."
});

const commitment = await vault.generateCommitment();
// Send only this commitment to the organisation

// Later when you receive a signed receipt:
await vault.receiveReceipt(signedReceipt);

const bundle = await vault.exportRecord();   // tribunal-ready
