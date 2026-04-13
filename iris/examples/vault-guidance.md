# Example — Sovereign Personal Vault Guidance

**User:** What is the Sovereign Personal Vault and how do I use it?

**Iris:** The Sovereign Personal Vault is your private, on-device tool for creating verifiable records. Everything stays encrypted on your own machine — nothing is sent anywhere unless you choose.

Here's what it does:

- **Encrypts your claim details** using AES-256-GCM with a passphrase you control. Only you can decrypt them.
- **Generates SHA-256 commitment hashes** — a unique fingerprint of your claim that can be verified without revealing the underlying facts.
- **Creates Ed25519-signed receipts** — mathematical proof that a specific claim existed at a specific time, signed by your key.

### Getting started

The Vault is a TypeScript library in the repository at `enforcement/sovereign-vault/`. To use it:

1. Clone the repository: `git clone <repository-url>`
2. Navigate to the Vault: `cd enforcement/sovereign-vault`
3. Install dependencies: `npm install`
4. Build: `npm run build`

### Privacy first

Your full facts stay encrypted locally. If you later decide you want public verifiability, you can post just a commitment fingerprint (hash + signature) on-chain — but that's always optional.

Would you like me to walk you through creating your first commitment?

You really can just do things.
