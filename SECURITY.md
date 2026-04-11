# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability in this repository, please report it responsibly.

**Do not open a public issue.**

Instead, please email the maintainer directly or use [GitHub's private vulnerability reporting](https://docs.github.com/en/code-security/security-advisories/guidance-on-reporting-and-writing-information-about-vulnerabilities/privately-reporting-a-security-vulnerability) feature on this repository.

We will acknowledge your report within 72 hours and aim to provide a fix or mitigation plan within 14 days.

## Scope

This policy covers:

- The core verification logic (`verify_scrutiny.py`, `api.py`)
- The cryptographic enforcement layer (`enforcement/sovereign-vault/`)
- The on-chain claims protocol (`onchain-protocol/`)
- The tracer module (`tracer/`)
- The Iris chat API (`api/chat.py`)
- The Iris system prompt and configuration (`iris/`)
- The sovereign local server (`iris-local.py`, `iris-config.json`)
- The project website (`index.html`)
- Platform install scripts (`scripts/`)
- CI/CD configuration (`.github/workflows/`)

## Cryptographic Baseline (v0.3.0)

The Sovereign Personal Vault (`enforcement/sovereign-vault/`) reached v0.3.0 after an internal security review that identified and resolved eight vulnerabilities in the original implementation. That review is the cryptographic baseline for the repository. All vault code on `main` must conform to it.

### Primitives

| Primitive | Implementation | Requirement |
|---|---|---|
| Authenticated encryption | AES-256-GCM (random 12-byte IV, 128-bit auth tag) | Mandatory for all local vault storage |
| Key derivation | PBKDF2-SHA-256, 210,000 iterations, per-encryption random salt | OWASP 2023 minimum. Lower iteration counts are not accepted |
| Commitment hashing | SHA-256 with fresh 32-byte random salt per request | Every commitment must be unlinkable |
| Receipt signatures | Ed25519 via `@noble/curves` | Unsigned receipts must be rejected. Signature verification is not optional |
| Serialisation | Canonical sorted-key JSON (no whitespace) | Prevents concatenation-ambiguity attacks on signed payloads |
| Dependencies | `@noble/hashes`, `@noble/curves`, Node.js built-in `crypto` | No other cryptographic dependencies are permitted |

### What the v0.3.0 Review Found

The review identified eight deficiencies in the pre-v0.3.0 vault:

1. **CryptoJS** — deprecated library using AES-CBC and an MD5-based key derivation function. Replaced with Node.js built-in AES-256-GCM.
2. **Unsalted KDF** — a single unsalted SHA-256 hash of the passphrase was used as the encryption key. Replaced with PBKDF2-SHA-256 at 210,000 iterations with per-encryption random salt.
3. **Commitment over ciphertext** — commitments hashed the ciphertext rather than the plaintext facts. Commitments now hash plaintext facts with a fresh random salt.
4. **Missing signature verification** — receipts without a `reviewerPubKey` were silently accepted. They are now rejected.
5. **Non-canonical serialisation** — signed messages had no guaranteed field order, allowing concatenation-ambiguity attacks. Canonical sorted-key JSON is now enforced.
6. **Base64 fragility** — `atob`/`btoa` decoding was used instead of hex encoding. Hex is now used throughout.
7. **No authenticated encryption** — AES-CBC does not verify ciphertext integrity. AES-256-GCM provides authentication.
8. **Missing per-operation randomness** — IVs and salts were not guaranteed fresh. Every encryption now uses a random 12-byte IV and every commitment uses a fresh 32-byte salt.

Every fix was merged, tested, and released as [v0.3.0](https://github.com/ljbudgie/burgess-principle/releases/tag/v0.3.0). The pre-v0.3.0 code is superseded and must not be reintroduced.

## Iris & API Security (v0.5.0+)

Iris is the project's conversational AI interface. It runs in two modes: **cloud** (Vercel serverless via `api/chat.py`) and **local** (sovereign inference via `iris-local.py`). Both modes handle user input and are security-sensitive.

### Cloud Mode (`api/chat.py`)

- **API key handling** — `IRIS_API_KEY` must be a server-side environment variable. It must never appear in client-side code, logs, or error messages returned to users.
- **Input validation** — User messages are validated for correct JSON structure and required fields before being forwarded to the AI backend.
- **No persistent storage** — Conversation history exists only in the browser session. The server is stateless and must not log or persist user messages.
- **SSE streaming** — Responses are streamed via Server-Sent Events. Only the `content` field from the model response is forwarded to the client.

### Sovereign Local Mode (`iris-local.py`)

- **Localhost binding** — The local server binds to `127.0.0.1` only. It must never bind to `0.0.0.0` or any externally reachable address.
- **No telemetry** — The local server must not make any outbound network requests. All inference is performed on the user's hardware.
- **Model file integrity** — Install scripts (`scripts/`) download GGUF model files from Hugging Face. Users should verify model checksums when available. Contributors must not change download URLs without review.
- **No API keys required** — Local mode operates without any API keys or credentials.

### On-Chain Claims SDK (`onchain-protocol/sdk/`, v0.4.0+)

- **Ed25519 via PyNaCl** — The Python on-chain SDK uses [PyNaCl](https://pynacl.readthedocs.io/) for Ed25519 signing and verification. PyNaCl (libsodium binding) is the accepted cryptographic dependency for the Python SDK.
- **No personal data on-chain** — Only SHA-256 commitment hashes, Ed25519 signatures, and minimal metadata are posted to the chain.
- **Fresh nonce per claim** — Every on-chain claim must use an independently generated random nonce for unlinkability.

## Security Expectations for Contributors

All contributions must follow these security principles:

1. **No hardcoded secrets** — Never commit API keys, tokens, or credentials.
2. **Input validation** — All user-facing inputs must be validated and sanitised.
3. **No dangerous patterns** — Avoid `eval()`, `innerHTML` with untrusted data, or other injection-prone patterns.
4. **Minimal dependencies** — Only add dependencies that are strictly necessary. Each new dependency increases the attack surface.
5. **Scoped changes** — Do not bundle unrelated application code (e.g., demo apps, e-commerce integrations) into PRs. Unrelated code introduces unrelated vulnerabilities.
6. **Install scripts** — Changes to `scripts/` that alter download URLs, add new external downloads, or modify installed packages require explicit review. Model download URLs must point to well-known, trusted sources (e.g., Hugging Face).

### Vault-Specific Requirements

Contributions that touch `enforcement/sovereign-vault/` must also meet the following:

- **No additional cryptographic dependencies** beyond `@noble/hashes`, `@noble/curves`, and Node.js built-in `crypto` for TypeScript vault code. For the Python on-chain SDK, `PyNaCl` is the accepted Ed25519 dependency. CryptoJS, crypto-js, tweetnacl, and similar libraries are not accepted.
- **AES-256-GCM only** for symmetric encryption. AES-CBC, AES-CTR, and other modes are not accepted.
- **PBKDF2-SHA-256 at ≥ 210,000 iterations** for key derivation. Argon2 or scrypt may be considered as future upgrades but must not reduce the iteration floor below OWASP 2023 guidance.
- **Ed25519 only** for receipt signatures. RSA and ECDSA are not accepted.
- **Canonical JSON** (sorted keys, no whitespace) for all signed payloads.
- **Hex encoding** for all binary-to-text conversions. Base64 (`atob`/`btoa`) is not accepted.
- **Fresh randomness per operation** — every IV, salt, and commitment nonce must be generated independently.

## Supported Versions

| Version | Supported |
| ------- | --------- |
| Latest on `main` | ✅ |
| Older commits | ❌ |

Thank you for helping keep the Burgess Principle safe and trustworthy.
