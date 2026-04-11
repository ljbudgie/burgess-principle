# Changelog — The Burgess Principle

All notable changes to this project will be documented in this file.  
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). This project uses [Semantic Versioning](https://semver.org/).

---

## Unreleased

### Added
- `POST /api/generate-claim` in `iris-local.py` for Sovereign Local Mode. The endpoint accepts a query plus profile data and returns the generated claim package with letter markdown.

### Changed
- Sovereign Local claim generation now writes encrypted records to the default local `.sovereign-vault/` directory instead of honoring per-request vault path overrides.

## v1.1.1 — Mirror Mode: Hardware Identity Reflection (11 April 2026)

### Added
- Mirror Mode for Sovereign Local Mode, built around a local encrypted sovereign profile and mirrored greeting flow.
- Local identity setup for name, handle, preferred signature block, and Ed25519-backed profile summaries.
- Mirror-aware PWA/site copy and manifest metadata so the hosted site, README, and local setup guides all point to the same current release.

### Changed
- Project/package metadata now consistently reports `v1.1.1` across Python, local vault, and package manifests.
- README, `START_HERE.md`, `SOVEREIGN_MODE.md`, `FOR_AI_MODELS.md`, `llms.txt`, and `iris/README.md` now describe Mirror Mode as part of the current Sovereign Local workflow.
- The Vercel site metadata, landing-page copy, and deployment rewrites now align with the v1.1.1 release.

## v0.6.0 — Sovereign Local Mode, Website Upgrade & Hardening (10 April 2026)

**Iris can now run entirely on your own hardware — and the Vercel site is now a full project landing page with Iris built in.**

This release adds Sovereign Local Mode for Iris, transforms the website from a chat-only window into a proper landing page, modernises the chat interface, and significantly expands test coverage across the codebase.

### Added

#### Sovereign Local Mode
- `iris-local.py` runs Iris entirely on local hardware using GGUF models via `llama-cpp-python`. No API keys, no cloud, no telemetry. Full instructions in [SOVEREIGN_MODE.md](SOVEREIGN_MODE.md).
- Platform install scripts: `scripts/install-linux.sh`, `scripts/install-macos.sh`, `scripts/install-windows.ps1` — each installs dependencies and downloads a default model.
- `iris-config.json` for local mode configuration (model path, context size, port, GPU acceleration).
- `index.html` auto-detects localhost and routes API calls to the local server when running in Sovereign Mode.
- New `local` optional dependency group in `pyproject.toml` (`llama-cpp-python`, `fastapi`, `uvicorn`).

#### Landing Page & Navigation
- **Landing page** — hero section, the binary test (SOVEREIGN / NULL) visualised as cards, key stats (18 institutions audited, 11 NULL findings, 35+ templates), template showcase, case study highlights, and feature overview (Templates, Vault, On-Chain).
- **Top navigation bar** — sticky nav with section anchors (The Test, Templates, Case Studies), GitHub link, and "Talk to Iris" CTA. Mobile hamburger menu.
- **Template showcase** — six template cards (Human Review, General Dispute, Council Tax, Benefits, Bailiff, DSAR) with icons and descriptions, linking to the GitHub templates.
- **Case study cards** — five real-world case studies (Wave, Passport Office, E.ON, Equita, Equifax) with SOVEREIGN/NULL finding badges and outcome summaries.
- Smooth view switching between the landing page and Iris chat via "Talk to Iris" CTA buttons, "← Home" back button, and sidebar home link.

#### Chat & UI Improvements
- **Markdown rendering** — Iris chat responses now render as rich HTML (headings, bold, italic, code blocks, tables, lists, blockquotes, links) via a lightweight built-in renderer with no external dependencies.
- Modernised Iris chat UI with improved typography, local-first privacy badge, suggestion buttons, and responsive mobile layout.
- Shared welcome HTML extracted for consistency between cloud and local modes.
- Richer Open Graph and Twitter Card metadata for better link sharing previews.

#### Testing
- Comprehensive new tests for `api/chat.py` and `onchain_claims.py` covering edge cases, error handling, and coverage gaps.
- New `tests/test_iris_local.py` test suite for the sovereign local server.
- 264 tests now passing (up from 218 in v0.5.0).

### Changed
- `index.html` refactored from chat-only to a two-view single-page app (landing + chat).
- CSS expanded with new design tokens (`--gold-bright`, `--blue`, `--red`, `--bg-card`, etc.) and responsive grid layouts.
- Mobile layout improved for both landing page sections and chat view.
- Chat sidebar now includes a "🏠 Home" link; chat header now includes a "← Home" button.
- `README.md` updated with Sovereign Mode section, dual-mode table (Cloud vs Local), and quick-start commands.
- `START_HERE.md` updated to mention sovereign local mode.
- `iris/README.md` updated with local-first architecture diagram and privacy details.

---

## v0.5.0 — Iris: AI Companion (10 April 2026)

**Iris — a calm, conversational AI companion that helps users apply the Burgess Principle directly from the website.**

The Vercel site at [burgess-principle.vercel.app](https://burgess-principle.vercel.app) is now a working chat interface. Iris applies the binary test, generates personalised templates, guides users through the Sovereign Personal Vault, and explains on-chain claims — all while keeping data sovereignty with the user.

### Added
- New `iris/` folder with system prompt (`system-prompt.md`), deployment notes (`README.md`), and example conversations.
- Vercel serverless function (`api/chat.py`) that streams AI responses via Server-Sent Events using the OpenAI-compatible API.
- Chat interface in `index.html` with sidebar navigation, privacy badge, suggestion buttons, and responsive mobile design.
- System prompt grounding Iris in the full project philosophy, binary test, templates, Vault guidance, on-chain protocol, and privacy guardrails.
- `vercel.json` updated with function configuration for the chat endpoint.
- `requirements.txt` now includes `openai` dependency for the serverless function.
- Updated `README.md` with "Meet Iris" section and repository map entry.
- Updated `FOR_AI_MODELS.md` with Iris-specific guidance.
- Updated `START_HERE.md` to recommend Iris as the conversational interface.
- Updated `INTEGRATIONS.md` with Iris section and corrected Vercel hosting description.

### Privacy
- No persistent user data storage — conversation history exists only in the browser session.
- System prompt enforces: "Your full facts remain in your local Vault. On-chain posts contain only cryptographic commitments."
- API key is server-side only; never exposed to the client.

---

## v0.4.0 — On-Chain Burgess Claims Protocol (10 April 2026)

**Lightweight on-chain protocol for issuing, storing, and verifying Burgess Claims as immutable, cryptographically signed commitment fingerprints.**

The same binary question — was a human there? — now produces a globally verifiable, tamper-proof artifact. Claims are generated off-chain in the Sovereign Personal Vault exactly as before. Only a compact commitment fingerprint (hash + signature + metadata) reaches the chain. No personal data is stored on-chain. The principle stays the same; the reach becomes universal.

### Added
- New `onchain-protocol/` folder with protocol specification (`spec.md`), Solidity smart contract (`BurgessClaimsRegistry.sol`), Python SDK, end-to-end example, and deployment guide.
- Python SDK (`onchain-protocol/sdk/onchain_claims.py`) with `generate_onchain_claim()`, `verify_onchain_receipt()`, and `verify_commitment()` functions.
- Ed25519 claim signing and verification via PyNaCl (optional dependency).
- Solidity contract for EVM L2 chains (Base, Arbitrum, Optimism) — stores only commitment hashes, signatures, and metadata on-chain.
- TypeScript vault extended with `generateOnchainClaim()` and `verifyOnchainReceipt()` methods.
- New `/claims/verify` API endpoint for verifying on-chain claim receipts.
- 46 new tests for the on-chain claims SDK and API endpoint (roundtrip, validation, selective disclosure).
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
