# Changelog — The Burgess Principle

All notable changes to this project are documented in this file.

---

## v0.4.0 — On-Chain Burgess Claims Protocol (10 April 2026)

**Lightweight on-chain protocol for issuing, storing, and verifying Burgess Claims as immutable, cryptographically signed commitment fingerprints.**

### Added
- New `onchain-protocol/` folder with protocol specification (`spec.md`), Solidity smart contract (`BurgessClaimsRegistry.sol`), Python SDK, end-to-end example, and deployment guide.
- Python SDK (`onchain-protocol/sdk/onchain_claims.py`) with `generate_onchain_claim()`, `verify_onchain_receipt()`, and `verify_commitment()` functions.
- Ed25519 claim signing and verification via PyNaCl (optional dependency).
- Solidity contract for EVM L2 chains (Base, Arbitrum, Optimism) — stores only commitment hashes, signatures, and metadata on-chain.
- TypeScript vault extended with `generateOnchainClaim()` and `verifyOnchainReceipt()` methods.
- New `/claims/verify` API endpoint for verifying on-chain claim receipts.
- 41 new tests for the on-chain claims SDK (roundtrip, validation, selective disclosure).
- End-to-end example (`onchain-protocol/examples/vault_to_chain.py`).
- Deployment guide for Base Sepolia, Arbitrum Sepolia, and Optimism Sepolia testnets.
- Updated `README.md`, `INTEGRATIONS.md`, `FOR_AI_MODELS.md` with on-chain protocol documentation.

### Security
- No personal data stored on-chain — only SHA-256 hashes and Ed25519 signatures.
- Fresh random nonce per claim for unlinkability.
- Constant-time comparison for commitment verification.
- Follows existing cryptographic baseline from SECURITY.md.

---

## v0.3.0 — Cryptographic Security Patch (10 April 2026)

**Sovereign Personal Vault — Security Patch.** All users of v0.2.0 should upgrade.

### Fixed
- Replaced AES-CBC with MD5-based KDF with proper AES-256-GCM authenticated encryption (128-bit auth tag, 96-bit IV).
- Replaced single unsalted SHA-256 of passphrase with PBKDF2-SHA-256 (210,000 iterations, fresh 16-byte random salt per encryption — OWASP 2023 guidance).
- Commitment now hashes `SHA-256(fresh-32-byte-salt ‖ plaintext-facts-JSON)` instead of ciphertext — stable and verifiable.
- Missing public key on `SignedReceipt` now throws instead of silently returning true (receipt forgery prevention).
- Replaced string concatenation for signed messages with canonical sorted-key JSON serialisation.
- Replaced `atob`/`btoa` (browser-only) with hex encoding via `@noble/hashes`.
- Removed deprecated `crypto-js` dependency entirely.
- README now accurately documents all cryptographic primitives with a crypto details table.

### Dependencies
- Zero third-party crypto dependencies beyond audited `@noble/*` libraries.

---

## v0.2.0 — Commitment-Only Mode (10 April 2026)

### Added
- **Commitment-only mode** — send only a single cryptographic commitment (SHA-256 hash) instead of personal facts or documents.
- **Fresh commitments by default** — generate a new commitment (with fresh random salt/nonce) per request for unlinkability.
- Placeholder-based templates so real hashes are never pasted into AI prompts.
- Improved guidance on unlinkability and data minimisation.

---

## v0.1.0 — Initial Release (10 April 2026)

### Added
- One binary predicate: SOVEREIGN (1) / NULL (0).
- 30+ ready-to-use, calm letter templates covering enforcement, DSAR, FOI, Equality Act, council tax, benefits, content moderation, media, music copyright, and more.
- Optional cryptographic enforcement layer (`sovereign-vault`) with signed, verifiable receipts.
- Hardened Python verification toolkit (`verify_scrutiny.py`) with constant-time checks, structured output, logging, and FastAPI wrapper.
- 90+ passing pytest tests, tracer utilities, and CI pipeline.
- Core papers on legal foundations, data sovereignty, representative actions, and responses to critiques.
- Real-world evidence via `LIVE_AUDIT_LOG.md`, case studies, and `INSTITUTIONAL_REGISTER.md`.
- AI toolkit and `FOR_AI_MODELS.md` for seamless integration with Grok, Claude, ChatGPT, and other AI assistants.
- `llms.txt`, `robots.txt`, `sitemap.xml` for discoverability.
- Website at burgess-principle.vercel.app.

---

**Maintained under the Burgess Principle**  
UK Certification Mark: UK00004343685  
[github.com/ljbudgie/burgess-principle](https://github.com/ljbudgie/burgess-principle)
