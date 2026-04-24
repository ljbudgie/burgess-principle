# Commitment-Only Workflow

A simple, privacy-first way to use the Sovereign Vault without ever exposing your facts.

## Why use Commitment-Only Mode

- Your actual facts never leave your device.
- You send **only** a SHA-256 commitment (a cryptographic fingerprint).
- You receive a signed receipt proving whether a human reviewed your specific case.
- The fresh random salt per commitment ensures **unlinkability** — different submissions cannot be correlated.
- Perfect for letters, emails, AI agents, or direct submissions to institutions.

## Step-by-step Workflow

1. **Prepare your facts locally**  
   Write down the specific details of your situation in a private note or document. Keep this file on your own device only.

2. **Generate the commitment**  
   Use the built-in generator:

   ```bash
   npx ts-node src/generate-commitment.ts "Paste your facts here as a single string"
