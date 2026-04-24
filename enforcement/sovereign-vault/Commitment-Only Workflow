# Commitment-Only Workflow

A lightweight path for proving what you said, without ever sharing what you said.

---

## What It Is

The commitment-only workflow lets you generate a cryptographic fingerprint (a SHA-256 commitment) of any facts or statement — locally, on your device — and share only that fingerprint. The underlying content never leaves your possession.

You can present the commitment in a letter, an email, or pass it to an AI agent. When challenged, you reveal the original content and anyone can verify it matches. A signed receipt confirms the commitment was registered, without revealing what it commits to.

Use this workflow when you need proof of knowledge or authorship, but have no reason — and no obligation — to disclose the content itself.

---

## Key Benefits

- **Facts never leave your device** — only the commitment hash is transmitted or stored externally.
- **SHA-256 integrity** — the commitment is a one-way cryptographic fingerprint; it cannot be reversed to reveal the original content.
- **Signed receipt** — you receive a verifiable receipt stamped `SOVEREIGN` or `NULL`, confirming registration without exposing the underlying facts.
- **Unlinkability via fresh salt** — each commitment uses a unique random salt, preventing correlation between separate commitments even if the content is identical.
- **Suitable for letters and AI agents** — the commitment string is short, portable, and can be embedded in any written or digital communication.

---

## Step-by-Step Workflow

### 1. Prepare Facts Locally

Write your statement, letter content, or facts in a plain text file on your device. Do not upload or transmit the content at this stage.

```
statement.txt
─────────────
On 14 April 2026, I requested written confirmation of the account closure
from the customer service representative named in my prior correspondence.
```

Keep this file safe. You will need it later to verify against the commitment.

---

### 2. Generate the Commitment

Run the commitment generator locally. This produces a SHA-256 hash of your content combined with a fresh random salt.

If you are working from the command line, use the CLI script. If you are integrating this into a larger TypeScript project, use the class directly.

**Command line:**

```bash
npx ts-node src/generate-commitment.ts --input statement.txt
```

**TypeScript:**

```ts
import { SovereignVault } from './src/SovereignVault';

const vault = new SovereignVault();
const result = vault.generateCommitment('Your statement text here');

console.log('Commitment:', result.commitment);
console.log('Salt:', result.salt);
console.log('Timestamp:', result.timestamp);
```

Store the returned `commitment`, `salt`, and `timestamp` securely on your device. You will need all three to verify later.

---

### 3. Send Only the Commitment

Include the commitment hash in your letter, email, or message. You are not disclosing the content — only the fingerprint.

**Sample phrase you can copy into correspondence:**

> I am registering a cryptographic commitment to a statement held privately on my device, generated using SHA-256 with a unique salt and timestamp.
>
> **Commitment:** `sha256:<your-commitment-hash-here>`
>
> I can disclose the underlying content and salt to any party with legitimate standing to request it, at which point the commitment can be independently verified.

Replace `<your-commitment-hash-here>` with the actual hash output from step 2.

---

### 4. Receive and Verify the Signed Receipt

After submitting a commitment, you will receive a signed receipt carrying one of two statuses:

| Status | Meaning |
|---|---|
| `SOVEREIGN` | Commitment accepted and registered. |
| `NULL` | Submission received but could not be registered. |

Verify the receipt signature locally before relying on it in any formal context:

```bash
npx ts-node src/verify-receipt.ts --receipt receipt.json
```

Store the receipt alongside your commitment and salt.

---

### 5. Export Evidence

When you need to demonstrate proof — to a regulator, ombudsman, or in correspondence — export a self-contained evidence package:

```bash
npx ts-node src/export-evidence.ts --commitment <hash> --salt <salt> --receipt receipt.json
```

This produces a portable bundle containing the commitment, salt, timestamp, and signed receipt. The recipient can verify the commitment independently using the disclosed content and salt. Share the bundle only when disclosure is appropriate and necessary.

---

## Quick Mobile-Friendly Option

Full CLI support requires a local development environment. If you are on a mobile device without one, the simplest approach is to note your statement carefully, then generate the commitment at your earliest opportunity from a desktop or laptop.

In the interim, record the exact wording of your statement — even a screenshot of a timestamped note is useful context when you later produce the formal commitment.

---

## Best Practices

- **Generate a fresh commitment for each distinct statement.** Do not reuse salts or commitments across different matters.
- **Back up the salt and timestamp immediately.** Without them, you cannot reproduce or verify the commitment later.
- **Do not alter the source content after committing.** Even a single character change will produce a different hash and invalidate the commitment.
- **Disclose only when there is standing.** The commitment-only workflow is designed to delay disclosure, not avoid it indefinitely. Reveal the underlying content only to parties with a legitimate and documented reason to receive it.

---

## When to Use the Full Encrypted Vault Instead

The commitment-only workflow is intentionally minimal. Consider using the full encrypted vault when:

- You need to store multiple related facts with structured metadata.
- You require time-locked disclosure or conditional release of content.
- You are managing an ongoing matter with many sequential commitments that need to be correlated securely.
- You want encrypted storage of the raw content alongside the commitment, rather than managing local files manually.

The commitment-only workflow is the right choice when simplicity and portability matter more than structured storage.

---

**Keep it sovereign. Keep it calm.**
