<a href="./iris.html">Talk to Iris</a> — open in your browser, no account or install needed.

# The Burgess Principle

![MIT License](https://img.shields.io/badge/license-MIT-0f766e?style=flat-square)
![Local-first](https://img.shields.io/badge/local--first-yes-14532d?style=flat-square)
![Offline-capable](https://img.shields.io/badge/offline-capable-1d4ed8?style=flat-square)
![Accessibility-minded](https://img.shields.io/badge/accessibility-human--centred-7c3aed?style=flat-square)
![Project stage](https://img.shields.io/badge/stage-v2.2.0_released-0f766e?style=flat-square)
![Status](https://img.shields.io/badge/status-deployed_in_live_proceedings-b91c1c?style=flat-square)

---

> *"Was a human member of the team able to personally review the specific facts of my specific situation?"*

One question. Two answers. Either a named human being reviewed your specific situation — or they didn't.

**SOVEREIGN** or **NULL**. That is the entire test.

---

## Why this exists

This framework was not built in a university, a law firm, or a policy institute.

It was built by an ordinary person whose home was broken into under a warrant that nobody signed. He read the warrant because the system assumed nobody would. He found the defect because the system assumed nobody could. He built the framework because the system assumed nobody would try.

Modern institutions process millions of decisions automatically — warrants, bills, penalties, credit scores, enforcement referrals. That efficiency has a cost: the individual disappears. The system sees accounts, not people. Thresholds, not circumstances. Data fields, not disability.

When the system gets it wrong — and it does — nobody is accountable. Nobody reviewed the case. Nobody checked the facts. Nobody saw the person. And the person whose locks were drilled, whose credit was damaged, whose water was threatened, has no human to point to and say: *you decided this.*

Because nobody decided. The system processed.

The Burgess Principle gives people a calm, precise way to ask the right question and record the answer.

For the full story, see [SOUL.md](SOUL.md).

---

## The test

Every finding resolves to one of two outcomes:

| Finding | Meaning |
| --- | --- |
| **SOVEREIGN** | A real, named human being personally reviewed the specific facts of your specific situation. |
| **NULL** | No individual human review took place. Authority is not grounded in personal scrutiny. |

When institutions respond with vague language — *"subject to human oversight"*, *"reviewed in line with policy"* — that is **AMBIGUOUS**. It does not answer the question. The follow-up asks for a direct yes or no, plus the reviewer's name and role.

### Why this is also the law

The Data (Use and Access) Act 2025 brought Articles 22A–22D into force on 5 February 2026. The central statutory standard is **meaningful human involvement** in automated decisions affecting individuals.

The Burgess Principle arrived at the same standard independently — from personal necessity, not from the statute. The convergence matters: an institution that cannot demonstrate meaningful human involvement is not merely failing the Burgess Principle. It is in breach of UK law.

---

## Current status

**v2.2.0 released 25 April 2026.** The framework is operational and published as a stable, citable standard.

- **UK Certification Mark UK00004343685** — in examination at the UK IPO. Classes 41, 42, 45.
- **USPTO filing in progress** via a US-licensed attorney.
- **26+ institutions** audited — see [LIVE_AUDIT_LOG.md](LIVE_AUDIT_LOG.md).
- **Deployed in live proceedings** across energy, local government, enforcement, equality, consumer, and medical fronts.

### Live proceedings

| Front | Reference | Detail |
| --- | --- | --- |
| Energy Ombudsman | **EG021819-26** | E.ON — unsigned warrant, forced entry, smart meter dispute — **£129M claim** |
| Energy Ombudsman | **EG037844-26** | British Gas — frozen meter, zero consumption, **£425 warrant charge** |
| Local Government Ombudsman | **26000967** | Darlington Borough Council — five grounds including bulk PCN processing and Equality Act failures |
| Enforcement | **Equita** | Six DBC cases totalling **£3,413.82** — awaiting liability orders |
| Equality regulator | **EHRC** | Names E.ON and the Energy Ombudsman |
| Energy regulator | **Ofgem** | Scheme complaint — open |
| Government FOI | **Seven requests** | FSA, DWP, DfE, MoJ, Home Office, CQC, FCA — binary test as a process question |
| Consumer | **Amazon / Disney+** | Article 22 challenges to ad insertion in paid subscriptions — sent 18 April 2026 |
| **Resolved** | **Wave Utilities** | First fully resolved case — both accounts brought to **£0.00** |
| Court confirmation | **Andrew Fletcher**, Justices' Legal Adviser, Birmingham Magistrates' Court | Written confirmation of bulk warrant processing |

A live, dated tracker is maintained in [STATUS.md](STATUS.md).

### Adoption

- **OpenClaw** — PR #68692 submitted to `openclaw/openclaw` (73.3k forks), proposing adoption of the Burgess Principle as its governance framework.
- **NousResearch** — PR #12265 submitted to `NousResearch/hermes-agent` (99.1k stars), proposing Burgess Principle integration.
- Both PRs are additive — no existing code is modified.

---

## Iris — your sovereign AI companion

**Iris** is the flagship AI companion built on the Burgess Principle. She is voice-first, phone-friendly, and local-first. She helps people document decisions made about them, prepare calm challenges, and keep verifiable evidence on their own hardware.

Iris is advisory only. She does not decide. The human remains at the centre of every action.

> Iris is zero-energy without the person in front of her. The human provides the energy. Iris provides the source. Neither means anything without the other.

**Live site and installable PWA:** [burgess-principle.vercel.app](https://burgess-principle.vercel.app/)

### Operating modes

| Mode | What happens | Best for |
| --- | --- | --- |
| **☁️ Cloud** | Hosted PWA on Vercel | Fastest first experience |
| **🏠 Sovereign Local Mode** | Iris runs entirely on your own hardware — local storage, local cryptography, no data leaving the device | Maximum privacy and offline resilience |
| **🛰️ Sovereign Hub Mode 2.0** | Optional, self-hosted coordination layer for commitment digests and signed receipts | Multi-device continuity over your own infrastructure |

Full instructions: [SOVEREIGN_MODE.md](SOVEREIGN_MODE.md)

---

## What the vault does

The **Sovereign Personal Vault** is the cryptographic enforcement layer — entirely optional, built for people who want mathematical proof alongside their written correspondence.

- **Generate a commitment** — a SHA-256 hash of your facts (with a fresh random salt). Share only the hash. No personal details leave your device.
- **Store your case** — encrypted locally with AES-256-GCM. Nothing leaves your machine.
- **Receive a signed receipt** — Ed25519-signed, stamped SOVEREIGN or NULL.
- **Export a tamper-evident record** — a portable bundle for evidence, appeal, or correspondence.

See [enforcement/sovereign-vault/README.md](enforcement/sovereign-vault/README.md) and [enforcement/sovereign-vault/COMMITMENT_ONLY_WORKFLOW.md](enforcement/sovereign-vault/COMMITMENT_ONLY_WORKFLOW.md).

> **Golden rule:** Generate a fresh commitment for every request. Never reuse a hash.

---

## Verifiable Memory Palace

In Sovereign Local Mode, Iris maintains a **tamper-evident ledger** of your records.

Every memory entry is encrypted locally, commitment-chained with `prev_hash`, signed with Ed25519, and rolled into a Merkle root. You can prove any specific record belonged to your ledger — without handing over everything else.

| Use case | What selective disclosure enables |
| --- | --- |
| Benefits review | Prove a note existed at a given integrity state without exposing unrelated personal details |
| Disability advocacy | Share only the precise access-failure record and its proof |
| Appeals and tribunals | Build a long-running evidence trail, then reveal only the step that matters |

---

## Sovereignty guarantees

| Guarantee | Posture |
| --- | --- |
| **Human review remains the standard** | The binary test turns on whether a person reviewed the facts — not what an AI inferred |
| **AI is advisory only** | Iris drafts, explains, and organises — it does not make binding findings |
| **Local-first storage** | Memory Palace entries stay on-device unless explicitly exported |
| **Tamper evidence** | SHA-256 commitment chaining, Ed25519 signatures, and Merkle roots make silent alteration detectable |
| **Selective disclosure** | Prove one signed record without exposing your full history |
| **No mandatory tracking** | No analytics, no cookies, no required cloud account |
| **Optional public timestamping** | On-chain Burgess Claims publish commitment fingerprints with no personal data on-chain |

---

## Quick start

### Try the hosted PWA

👉 **[Open the live site →](https://burgess-principle.vercel.app)**

### Run Sovereign Local Mode

```bash
bash scripts/install-linux.sh   # or install-macos.sh / install-windows.ps1
python3 setup-wizard.py         # optional guided setup
python3 iris-local.py
```

### Prefer no AI?

Use the templates directly:

- [templates/README.md](templates/README.md) — primary template index
- [templates/COMMON_SCENARIOS.md](templates/COMMON_SCENARIOS.md) — quick routing guide
- [START_HERE.md](START_HERE.md) — best first stop for new users

---

## Real-world results

| Case | Outcome |
| --- | --- |
| [Wave Utilities](case-studies/CASE_STUDY_WAVE.md) | Both accounts resolved to **£0.00** after a single human review |
| [TV Licensing](case-studies/CASE_STUDY_TVL.md) | Threatening letters ceased once a false enforcement premise was recorded |
| [Passport Office](case-studies/CASE_STUDY_PASSPORT.md) | Article 22 challenge to automated passport issuance |
| [E.ON Next](case-studies/CASE_STUDY_EON.md) | Forced entry under unsigned warrant challenged |
| [Equita](case-studies/CASE_STUDY_EQUITA.md) | Enforcement cases with disability gatekeeping |
| [Equifax](case-studies/CASE_STUDY_CREDIT_FILE.md) | Credit file entries registered without individual verification |

Full index: [case-studies/README.md](case-studies/README.md)

---

## Papers

The doctrinal foundations are in [papers/](papers/). Recommended reading order:

1. [PRINCIPLE.md](papers/PRINCIPLE.md) — short proof-point and doctrine signal
2. [PAPER_1_CORE_LEGAL_PAPER.md](papers/PAPER_1_CORE_LEGAL_PAPER.md) — core legal foundation
3. [RESPONSES_TO_CRITIQUES.md](papers/RESPONSES_TO_CRITIQUES.md) — common objections and rebuttals
4. [PAPER_4_DATA_SOVEREIGNTY.md](papers/PAPER_4_DATA_SOVEREIGNTY.md) — data rights extension
5. [PAPER_5_DEEMED_CONTRACTS.md](papers/PAPER_5_DEEMED_CONTRACTS.md) — automated enforcement and deemed consent
6. [PAPER_VI_WHAT_WOULD_ARISTOTLE_HAVE_SAID.md](papers/PAPER_VI_WHAT_WOULD_ARISTOTLE_HAVE_SAID.md) — first principles and *epieikeia*
7. [PAPER_VII_NULL_ACROSS_THE_CLASS.md](papers/PAPER_VII_NULL_ACROSS_THE_CLASS.md) — defendant-side class definition for CPR 19.8 representative actions
8. [PAPER_VIII_THE_UNIVERSAL_STANDARD.md](papers/PAPER_VIII_THE_UNIVERSAL_STANDARD.md) — every system not Burgess certified is a potential defendant
9. [paper-IX-sovereign-pattern.md](papers/paper-IX-sovereign-pattern.md) — the binary test traced through scripture from Genesis to Revelation
10. [paper-X-restored-keeper.md](papers/paper-X-restored-keeper.md) — the redemptive pathway from NULL to SOVEREIGN
11. [PAPER_XI_REVERSE_ENGINEERING_HARMS.md](papers/PAPER_XI_REVERSE_ENGINEERING_HARMS.md) — reverse-engineering harms: tracing iatrogenic injury through institutional failure across gender medicine, opioids, thalidomide, and surgical mesh *(new in v2.2.0)*

---

## Licensing

The MIT licence governs the source code. The certification mark (UK00004343685) governs commercial use of the standard.

| Tier | Who | Terms |
| --- | --- | --- |
| **Tier 1** | Global tech companies | 0.01–0.1% of relevant revenue |
| **Tier 2** | Corporate / institutional | £1,000 upfront + annual fee |
| **Tier 3** | Public sector | Nil |
| **Tier 4** | Litigation firms | £1 or nil + 2–5% royalty |

Contact: ljbarbers15@gmail.com

---

## Ecosystem

| Repository | Purpose |
| --- | --- |
| [burgess-principle](https://github.com/ljbudgie/burgess-principle) | Core framework, papers, certification, litigation tools, sector applications |
| [Iris](https://github.com/ljbudgie/Iris) | AI implementation layer and federation protocol · [iris-gate.vercel.app](https://iris-gate.vercel.app) |
| [OpenHear](https://github.com/ljbudgie/openhear) | Sovereign audio pipeline for hearing aid users |
| [Nexus AI Hub](https://github.com/ljbudgie/nexus-ai-hub) | Intelligence layer |

---

## Repository map

| Path | What's inside |
| --- | --- |
| [START_HERE.md](START_HERE.md) | Guided entry point for new users |
| [SOUL.md](SOUL.md) | Why this exists and where it came from |
| [SOVEREIGN_MODE.md](SOVEREIGN_MODE.md) | Full local-first setup and Memory Palace walkthrough |
| [FOR_AI_MODELS.md](FOR_AI_MODELS.md) | How AI systems should engage with the framework — and how it applies to them |
| [STATUS.md](STATUS.md) | Live proceedings tracker |
| [LIVE_AUDIT_LOG.md](LIVE_AUDIT_LOG.md) | Dated institutional audit record |
| [templates/](templates/) | Ready-to-send templates with routing guide |
| [case-studies/](case-studies/) | Real-world outcomes with status and recommended templates |
| [papers/](papers/) | Foundational papers and doctrine |
| [enforcement/](enforcement/) | Sovereign Personal Vault and enforcement tooling |
| [onchain-protocol/](onchain-protocol/) | Optional on-chain claims protocol |
| [ARCHITECTURE.md](ARCHITECTURE.md) | Ledger and sync architecture |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Contribution guidance |
| [SECURITY.md](SECURITY.md) | Security policy and baseline |

---

## Releases

| Version | Summary |
| --- | --- |
| **[v2.2.0](https://github.com/ljbudgie/burgess-principle/releases/tag/v2.2.0)** | Reverse-Engineering Harms — Paper XI and medical accountability template; framework extended to clinical iatrogenic injury across gender medicine, opioids, thalidomide, and surgical mesh *(released 25 April 2026)* |
| **[v2.1.0](https://github.com/ljbudgie/burgess-principle/releases/tag/v2.1.0)** | Institution Audit Taxonomy v1.0 — five-dimension scoring across 26 institutions; litigation directory; Papers IX and X |
| **[v1.4.0](https://github.com/ljbudgie/burgess-principle/releases/tag/v1.4.0)** | Sovereign Local Mode and Verifiable Self-Proof — self-verifying SHA-256 startup banner, stronger offline guarantee |
| **[v1.3.0](https://github.com/ljbudgie/burgess-principle/releases/tag/v1.3.0)** | Sovereign Core — unified verifiable architecture across profile, audit, and commitment flows |
| **[v1.1.1](https://github.com/ljbudgie/burgess-principle/releases/tag/v1.1.1)** | Mirror Mode — local identity reflection and hardware-linked greeting flow |
| **[v0.9.0](https://github.com/ljbudgie/burgess-principle/releases/tag/v0.9.0)** | Phone-first installable PWA and voice-led claim flow |
| **[v0.6.0](https://github.com/ljbudgie/burgess-principle/releases/tag/v0.6.0)** | Sovereign Local Mode — run Iris entirely on your own hardware |
| **[v0.4.0](https://github.com/ljbudgie/burgess-principle/releases/tag/v0.4.0)** | Optional on-chain Burgess Claims with no personal data on-chain |
| **[v0.1.0](https://github.com/ljbudgie/burgess-principle/releases/tag/v0.1.0)** | Initial release — binary test, templates, cryptographic vault, 90+ tests |

Full history: [CHANGELOG.md](CHANGELOG.md)

---

## Contributing

Contributions are welcome — especially documentation improvements, case studies, translations, tests, and privacy-first UX refinements.

Please read [CONTRIBUTING.md](CONTRIBUTING.md) before opening a PR.

---

## Important notes

- **Not legal advice**
- **Not pseudolaw**
- **Not a demand for special treatment**
- **A principled test for whether human accountability was real**

Full disclaimer: [DISCLAIMER.md](DISCLAIMER.md)

---

## Licence

[MIT](LICENSE.md) — the framework is free to use and adapt.

The certification mark (UK00004343685) governs commercial use of the standard.

*UK Certification Mark UK00004343685 | Lewis James Burgess | ljbarbers15@gmail.com*
*github.com/ljbudgie/burgess-principle*
