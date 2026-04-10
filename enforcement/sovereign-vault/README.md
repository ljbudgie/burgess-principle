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

## How to use — the short version

### Why a fresh commitment every time?

Each commitment is a one-time hash. If you reuse the same hash across different emails or AI prompts, someone could link those messages together and build a profile. A fresh commitment for every interaction means every request stands alone — no correlation, no trail, no pattern.

Think of it like a sealed envelope: one set of facts, one seal. Open a new envelope for the next conversation.

### On your phone (no setup needed)

You don't need Node.js, a terminal, or any build tools. All you need is a way to generate a SHA-256 hash of some text. Here's the simplest path:

1. **Write your facts** in a plain text note on your phone.  
   > Example: *"I received a council tax bill on 3 March 2026 for a property I moved into on 1 January 2026. The bill covers the previous occupant's period."*

2. **Add a fresh random salt** — type a long random string at the start of your note (mash the keyboard, use a password manager, anything unpredictable). This is your nonce.  
   > Example: `k7Qz9xPmW4...your facts here...`

3. **Hash it.** Open any free SHA-256 tool in your mobile browser (search "SHA-256 online") and paste in the full text (salt + facts). Copy the resulting hash.

4. **Use the placeholder template.** Open [`COMMITMENT_ONLY_PLACEHOLDER.md`](../../templates/COMMITMENT_ONLY_PLACEHOLDER.md), fill in the details, and replace `[COMMITMENT_HASH]` with the hash you just copied.

5. **Keep your facts and salt private.** Only share the hash. If you ever need to prove what the hash covers, you can reveal the original text.

That's it. The whole process takes about two minutes.

### On a computer (one command)

If you have Node.js (v18+) installed:

```bash
npx ts-node src/generate-commitment.ts "your facts here"
```

This generates a fresh random salt, computes the SHA-256 commitment, and prints only the hash. It also saves the opening values (salt + facts) to a local file so you can prove the commitment later.

### Using the full vault library

```ts
import { SovereignVault } from './src/index.js';

const vault = new SovereignVault("your-strong-passphrase");
await vault.storeFacts({ situation: "...", requestedAction: "..." });
const commitment = await vault.generateCommitment();
await vault.receiveReceipt(signedReceipt);
const bundle = await vault.exportRecord();
```

### Using placeholders with AI prompts

Never paste your real commitment hash into an AI prompt. Instead:

1. Use the template with `[COMMITMENT_HASH]` as a placeholder.
2. Let the AI help you draft the letter.
3. Replace `[COMMITMENT_HASH]` with your real hash **locally, on your own device**, just before sending.

This way, the AI never sees your actual commitment — and can never link it to your identity.

## Files in this folder

| File / Folder | Purpose |
|---|---|
| `src/index.ts` | Main library source code |
| `src/generate-commitment.ts` | Standalone commitment generator (no build step needed) |
| `package.json` | Node.js package configuration |
| `tsconfig.json` | TypeScript compiler settings |

## Remember

This layer is **completely optional**. The Burgess Principle works without it. The vault simply adds on-device encryption and tamper-evident receipts for users who want cryptographic proof of their verification results.