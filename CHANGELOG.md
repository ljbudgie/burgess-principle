# Changelog — The Burgess Principle

All notable changes to this project will be documented in this file.  
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). This project uses [Semantic Versioning](https://semver.org/).

---

## v2.5.3 — June 2026

### Added
- SSRN Paper 3 approved 9 June 2026 — *NULL at Scale* (abstract 6894860)
  - Status: APPROVED (pending distribution) | Views: 1 | Downloads: 1
  - Three-paper series now complete: theory, philosophy, empirical proof
  - Written evidence submitted to Justice Committee and ICO ADM consultation 29 May 2026
- SSRN ledger entry #47 added to `audits/LIVE_AUDIT_LOG.md` — Finding: SOVEREIGN (named human reviewer approved submission)
- SSRN Paper 5 submitted 10 June 2026 — *SOVEREIGN Counsel: Attributable Judgment, Fractional Models, and NULL Drift in Legal Services* (abstract 6913498)
  - Status: SUBMITTED — under review | Views: 0 | Downloads: 0
  - JEL codes: D02, H83, D73
  - Applies the binary test to legal services: NULL drift in solicitor engagements, fractional models as higher SOVEREIGN density, self-represented litigant as owning mind, machine-assisted workflow analysis
  - Closing case study: Parliamentary Standards Commissioner "we do not provide the names of individuals"
  - SSRN ledger entry #48 added to `audits/LIVE_AUDIT_LOG.md` — Finding: PENDING
- Five-paper series now submitted in full: theory (6759778) · philosophy (6864621) · empirical proof (6894860) · behavioural consequences (6909118) · legal services (6913498)
- Public Framer site live at [theburgessprinciple.framer.website](https://theburgessprinciple.framer.website) (custom domain theburgessprinciple.com — DNS transfer in progress)
  - Tables on site pull live from `institutional_register.csv` and `live_findings_ledger.csv` via raw GitHub URLs — no manual re-upload needed
  - SEO, dropdowns, and live CSV sync confirmed working (Fin Kendall, Ink Marketing, 4 June 2026)
- `iris.html`: Framer embed mode (PR #427)
  - `?embed=1` — strips chrome (header, footer) to bare chat surface for iframe use
  - `?theme=light|dark` — overrides OS preference to match host site theme
  - `?context=<string>` — 64-char host-side telemetry tag (no impact on system prompt)
  - Height reporting via `ResizeObserver` + `postMessage` so Framer can auto-size the iframe
  - `✦ Run Sovereign Local Mode` pill shown in embed mode to preserve signpost to on-device option
  - `frame-ancestors` CSP added to `vercel.json` for `theburgessprinciple.com`, `*.framer.app`, `*.framer.website`

### Changed
- RMOK Legal (rmoklegal.com) removed from certified register — certification terminated 9 June 2026
  - Aggregate score 5/20 (NULL band) across five assessed dimensions
  - Failed primary instruction (litigation referral and bond structure assessment)
  - Disability reasonable adjustment acknowledged 12 May 2026; not actioned 5 June 2026
  - Substantive questions returned with process acknowledgements throughout
  - Register entry inconsistent with SOVEREIGN standard; £3,000 paid
- `INSTITUTIONAL_REGISTER.md` summary statistics updated: total 45 → 46; removed count added
- `audits/LIVE_AUDIT_LOG.md` summary updated: total 46 → 47; SSRN SOVEREIGN entry added; Academic Publishing sector added; Legal Services sector 1 → 2
- `institutional_register.csv` and `live_findings_ledger.csv` updated with RMOK Legal row (Finding: REMOVED)
- `README.md` Academic Publications section updated — three-paper series with current SSRN stats:
  - Paper 1 (6759778): DISTRIBUTED | 52 views | 9 downloads
  - Paper 2 (6864621): DISTRIBUTED | 27 views | 9 downloads
  - Paper 3 (6894860): APPROVED (pending distribution) | 1 view | 1 download

---

## v2.5.2 — June 2026

### Added
- Live findings ledger expanded from 37 to 45 institutions (7 June 2026 snapshot): NPCC, College of Policing, APP Team (College of Policing), IOPC, Home Affairs Committee, Hodge Jones & Allen LLP, E.ON Next DPO, Fujitsu
- New dated source CSVs: `audits/2026-06-07_institutional_register.csv` and `audits/2026-06-07_live_audit_log.csv`
- Four new audit log events (4–6 June 2026):
  - DBC TPT DK00003-2605 supplementary submission — liability transfer document absent; Carolyn Pistellato conflict noted; decision option deadline 11 June
  - E.ON Next Article 15(1)(h) served on named DPO — automated triage pattern confirmed (Jessica / Riya; no surnames; system returned question to data subject)
  - DBC / VWFS ICO complaint IC-521371-M3C2 confirmed active — Lee Downey: no DPA, Article 6(1)(e) misapplied, Prolific Offender label undisclosed
  - Henry Nowak / policing impartiality — submissions to 5 bodies (NPCC, IOPC, College of Policing, APP Team, Home Affairs Committee); structural NULL in APP guidance confirmed
- DBC Accountability Audit File produced (12-section formal document)
- HJA intake submission (7-section document; Route A/B bifurcation)
- Live site launched: [theburgessprinciple.framer.website](https://theburgessprinciple.framer.website)
- Second SSRN paper published: *The Accountability Gap* (Abstract 6864621, submitted 1 June 2026)
- Live proceedings count added to README snapshot: 20 formal active proceedings

### Changed
- README snapshot updated: 37 → 45 institutions; NULL total 29 → 35; proceedings count added
- `INSTITUTIONAL_REGISTER.md` summary statistics updated to 7 June 2026
- `audits/LIVE_AUDIT_LOG.md` summary, sector breakdown, and notable live proceedings updated
- `README.md` Academic Publication section updated: now lists both SSRN papers with individual citation blocks

---

## v2.5.1 — May 2026

### Added
- ORCID iD (0009-0001-8691-3366) added to Academic Publication section of `README.md`
- Legal convergence: Medical Devices Regulations 2002 added as fifth statutory framework (MHRA FOI2026/00527)
- Case study: "The Burgess Test — The Liability Transfer Chain" added to `papers/` directory (Zenodo DOI to be added on publication)
- Case study published on Zenodo — DOI: 10.5281/zenodo.20449193
- NULL findings ledger published at `audits/LIVE_AUDIT_LOG.md` (15-institution audit: 11 NULL, 0 SOVEREIGN, 4 AMBIGUOUS)
- Equality Act 2010 (ss.20/29) reasonable-adjustment line added to 29 letter templates — accessibility footer coverage rises from 12 to 41 templates
- New template `templates/THIRD_PARTY_REFERRAL_REVIEW_WITH_BURGESS_PRINCIPLE.md` for decisions based on a third-party assessor (medical / occupational health / work capability / expert report); applies the binary test to both the assessment and the institution's reliance on it
- "Cite as" academic citation block (SSRN abstract 6759778, ORCID 0009-0001-8691-3366, Zenodo DOI 10.5281/zenodo.20449193) added to the whitepaper header

### Changed
- Reframed institution statistics away from a NULL "scoreboard" toward a path-to-sovereignty framing (help, not shame); removed brittle hardcounts in favour of the live register in `llms.txt`, `toolkit/XAI_INTEGRATION.md`, `memes/README.md`, and `templates/MEDIA_AND_LIBEL.md`
- Bumped package, API, PWA, Vercel-facing, and local install metadata to v2.5.1

---

## v2.5.0 — May 2026

### Added
- Institutional Certification workflow with encrypted local vault
- Statutory Challenge Generator (7 challenge types)
- Evidence Bundle Builder
- Institutional Register Export (Framer CMS format)
- Tier 1 Integration Package (burgess-gate.js, system prompt generator, /integration/docs)
- Hermes 5-domain autonomous agent
- Memory Palace institutional intelligence
- Federation Protocol distributed ledger
- OpenHear Bridge haptic notification system
- Sovereign Command Centre dashboard
- Burgess brand applied throughout (navy/gold/cream)
- localStorage form persistence
- Ollama graceful fallback

### Framework
- Academic paper submitted to SSRN and peer-reviewed journals
- ORCID registered
- Burgess Bond financial instrument concept documented
- Consumer Rights Act 2015 Section 49 convergence identified

---

## v2.5.0 — Governance & Ecosystem: Certified Pathways and Community Foundations (9 May 2026)

### Added
- `GOVERNANCE.md` establishes lightweight project governance: maintainer roles, lazy consensus for ordinary work, founder review for doctrinal and mark-sensitive changes, contribution ladder, succession guidance, and neutral advisory review for sensitive certification questions.
- `CODE_OF_CONDUCT.md` adds a calm, accessibility-aware community standard adapted from Contributor Covenant 2.1, including explicit protection against misleading certification claims.
- Contributor onboarding now includes issue-friendly community paths, with an Iris enhancement template suitable for good first issues around Iris, Sovereign Core, and supporting workflows.
- LangChain governance overlay documentation in `integrations/LANGCHAIN_BURGESS_OVERLAY.md`, plus integration PR templates for AutoGen, CrewAI, LlamaIndex, and related ecosystem routes.
- `ECOSYSTEM.md` updates the surrounding project map, including Iris, Mirror, OpenHear, Nexus AI Hub, OpenClaw, Hermes Agent, and their relationship to the Burgess Principle core.
- Certification-site materials now include public routes for certified pathways, GoCardless confirmation, partnership ledger automation, and `CERTIFICATION_TIERS.md` as a repository mirror of the live tier structure.
- Founding rate information for certification pathways is now recorded: Tier 03 practitioner, Tier 02 technology and advocacy, and Tier 01 institutional routes, with the founding-rate window documented to 31 July 2026.
- Optional contributor licence agreement draft at `.github/CLA.md` for future maintainer use if relicensing flexibility ever requires a formal process.
- Adoption and community foundation materials, including adoption trackers, ambassador programme notes, public leaderboard scaffolding, and certification-ready checklists.

### Changed
- Root `README.md` now links hosted Iris and the certification site separately, clarifies public-facing project structure, and explains the hybrid MIT + Certification Mark model.
- `LICENSE.md`, `CONTRIBUTING.md`, docs routing, and certification pages now clarify that MIT reuse remains open while official "Certified Burgess Principle" mark use requires separate authorisation.
- `ECOSYSTEM.md`, `ADOPTION.md`, `STATUS.md`, `SOUL.md`, and Iris memory files now align with the v2.5.0 governance and ecosystem release framing.
- Vercel-facing PWA metadata, service-worker cache versioning, package metadata, Python package metadata, API version metadata, Iris local version reporting, and local install scripts now report v2.5.0.
- Public docs and certification pages now use stronger accessibility patterns, clearer skip links, and more direct certification copy without changing the binary test.
- The Sovereign Vault dependency baseline was refreshed through Dependabot updates for `@noble/curves`, `@noble/hashes`, TypeScript, and related build/test expectations.
- Python/API dependencies were refreshed through Dependabot updates, including `uvicorn`, `cryptography`, and `openai` requirement updates.

### Fixed
- Documentation links and Iris prompt references were synced so AI-facing docs, README paths, and public routing remain lint-clean.
- Sovereign Vault TypeScript build warnings and stale test expectations were corrected after dependency updates.
- Personal contact/address details were redacted from public-facing repository records, leaving only appropriate commercial certification contact routes.

### Release Notes
- Short adopter and contributor release notes are available in [`RELEASE_NOTES.md`](./RELEASE_NOTES.md), including a draft GitHub Release description in Keep a Changelog style.

---

## v2.1.0 — The Pattern Completed (24 April 2026)

### Added
- `POST /api/generate-claim` in `iris-local.py` for Sovereign Local Mode. The endpoint accepts a query plus profile data and returns the generated claim package with letter markdown.
- New `templates/FOLLOW_UP_WEASEL_RESPONSE.md` for calm second letters when institutions reply with vague claims about "human oversight" or policy review.
- New `setup-wizard.py` guided local setup for model choice, Easy Mode defaults, and first-run configuration.
- New `enforcement/sovereign-vault/COMMITMENT_ONLY_WORKFLOW.md` — full step-by-step commitment-only workflow covering CLI, TypeScript, correspondence phrasing, receipt verification, evidence export, mobile options, and best practices.
- `SOUL.md` now includes a new section — The Pattern Behind the Test — grounding the SOVEREIGN/NULL binary in its scriptural origin, from Cain's denial in Genesis 4 to Peter's threefold restoration on the shore of Galilee. The closing passage has been rewritten to reflect the redemptive dimension introduced in Paper X: the framework is not only diagnostic, the pathway back from NULL to SOVEREIGN exists and is personal.

### Changed
- Sovereign Local claim generation now writes encrypted records to the default local `.sovereign-vault/` directory instead of honoring per-request vault path overrides.
- Core review templates now include a reusable weasel-word rebuttal asking for a direct YES/NO answer plus the name and role of any reviewer.
- `iris/system-prompt.md` now classifies institutional replies as SOVEREIGN, NULL, or AMBIGUOUS for follow-up purposes and guides Iris toward the next polite letter automatically.
- Local install scripts, `iris-config.json`, `README.md`, `START_HERE.md`, and `SOVEREIGN_MODE.md` now provide a clearer non-technical path into Sovereign Local Mode, including Easy Mode defaults and setup wizard guidance.
- Mirror Mode now supports configurable greeting style, custom greeting text, and a user-controlled Mirror Reflection scope for internal vault use or outward-facing documents.
- `case-studies/` now uses a shared operational format with explicit response classification, next-step guidance, a folder index, and a shorter passport case backed by appendices.
- Hosted Iris API docs now distinguish the narrow Vercel helper routes from the richer local-first `/api/*` surface, and `api/chat.py` now returns a generic upstream failure message instead of exposing raw exception details.
- Root `README.md` restructured to lead with the origin story and the binary test. Technical depth follows rather than competing for attention at the top. Sections covering Neuralink framing, time as invertible template, and Starlink connectivity have been moved to their dedicated documents.
- `enforcement/sovereign-vault/README.md` updated to reference `COMMITMENT_ONLY_WORKFLOW.md` in the introduction and files table.

---

## v1.3.0 — Sovereign Core: Unified Verifiable Architecture (12 April 2026)

### Added
- New `sovereign-core/` shared runtime for profile types, connectivity utilities, commitment orchestration, audit helpers, and unified profile management.

### Changed
- Sovereignty-critical profile, audit, and commitment flows now share one implementation across the PWA, Memory Palace, Sovereign Hub Mode, and service worker.
- Project metadata, release references, and user-facing copy now point to the `v1.3.0` release.

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
