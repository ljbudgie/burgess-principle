# The Burgess Principle

> *"Was a human member of the team able to personally review the specific facts of my situation?"*

**UK Certification Mark:** UK00004343685 — Classes 41, 42, 45  
**Website:** [burgess-principle.vercel.app](https://burgess-principle.vercel.app/)

---

## What is the Burgess Principle?

The Burgess Principle is a simple, respectful framework that helps ordinary people hold institutions accountable by asking one question: **did a real human being actually look at my case?**

Modern institutions — utilities, councils, enforcement agencies, credit bureaus — make millions of automated decisions every day. Sometimes those decisions are wrong, and when they are, there is often no named person who reviewed the facts. The Burgess Principle gives you a calm, written way to surface that gap.

It is not legal advice, not confrontational, and not pseudolaw. It is a diagnostic question that creates a clear, documented record. For the deeper philosophy, see [SOUL.md](SOUL.md). For the full disclaimer, see [DISCLAIMER.md](DISCLAIMER.md).

---

## Who is this for?

- Anyone who has received an automated penalty, bill, or enforcement action that feels wrong.
- Anyone who wants to challenge an institutional decision but doesn't know where to start.
- Anyone who has a disability, sensory need, or communication preference that an institution has ignored.
- Researchers, legal professionals, and policy advocates interested in algorithmic accountability.
- AI developers who want to understand how to assist individuals navigating institutional systems — see [FOR_AI_MODELS.md](FOR_AI_MODELS.md).

No legal training is needed. No fee is charged. The framework is [MIT licensed](LICENSE.md) and free for personal use.

---

## Quick start

**If you need help right now**, head straight to the [templates](./templates) folder and pick the one that matches your situation. You don't need to read anything else first. Or drop the whole repo into [Grok](https://grok.com), [Claude](https://claude.ai), [ChatGPT](https://chat.openai.com), or any AI assistant — describe what happened and it will write a personalised letter for you.

For a guided walkthrough, see **[START_HERE.md](START_HERE.md)**.

### Commonly used templates

| Template | Use when… |
| --- | --- |
| [Request for human review](templates/REQUEST_FOR_HUMAN_REVIEW.md) | You want to ask any organisation whether a human reviewed your case |
| [General dispute](templates/GENERAL_DISPUTE_WITH_BURGESS_PRINCIPLE.md) | You need a universal dispute letter |
| [Council tax / penalty charge](templates/COUNCIL_TAX_PCN_TEMPLATE.md) | You're challenging a council tax or PCN decision |
| [Benefits claim](templates/BENEFITS_CLAIM_HELP.md) | A benefits decision feels wrong |
| [Bailiff threat](templates/BAILIFFS_THREAT_TEMPLATE.md) | Enforcement agents have contacted you |
| [Data subject access request](templates/DSAR_WITH_BURGESS_PRINCIPLE.md) | You want to see what data an organisation holds on you |

See the full list of templates and a [scenario comparison guide](templates/COMMON_SCENARIOS.md) in the [`/templates`](./templates) folder.

---

## The binary test

Every finding under the Burgess Principle resolves to one of two outcomes:

| Finding | Meaning |
| --- | --- |
| **SOVEREIGN** | A human mind was individually applied to the specific facts. |
| **NULL** | No individual human review took place. The instrument carries no lawful authority from inception. |

---

## Real-world results

The framework has been applied to real institutional interactions. See the [case studies](./case-studies) for documented outcomes:

- **[Wave Utilities](case-studies/CASE_STUDY_WAVE.md)** — both accounts resolved to £0.00 after a single human review.
- **[Passport Office](case-studies/CASE_STUDY_PASSPORT.md)** — Article 22 challenge to automated passport issuance.
- **[E.ON Next](case-studies/CASE_STUDY_EON.md)** — forced entry under unsigned warrant challenged.
- **[Equita](case-studies/CASE_STUDY_EQUITA.md)** — five enforcement cases with disability gatekeeping.
- **[Equifax](case-studies/CASE_STUDY_CREDIT_FILE.md)** — credit file entries registered without individual verification.

---

## Cryptographic Enforcement Layer (Optional)

The [Sovereign Personal Vault](enforcement/sovereign-vault/) gives you on-device encryption, SHA-256 commitments, and Ed25519-signed receipts — mathematical proof that an institution did (or did not) apply human review. You don't need it to use the Burgess Principle, but it's there for anyone who wants verifiable, tamper-evident records.

As of v0.4.0, the Sovereign Personal Vault now includes a minimal on-chain protocol layer. Users generate claims off-chain exactly as before, then post only a compact commitment fingerprint (SHA-256 hash + Ed25519 signature + minimal metadata) to an EVM L2. The chain provides neutral timestamping and public verifiability — no personal data ever touches the blockchain. See [onchain-protocol/spec.md](onchain-protocol/spec.md) and the [v0.4.0 release notes](https://github.com/ljbudgie/burgess-principle/releases/tag/v0.4.0) for details.

### On-Chain Burgess Claims (v0.4.0)

Every demand for human scrutiny becomes a globally verifiable, tamper-proof artifact — while full facts stay encrypted in your local Vault.

```python
from onchain_claims import generate_onchain_claim, verify_onchain_receipt

# Generate a claim ready for on-chain posting
claim = generate_onchain_claim(
    claim_details="My council tax was sent to enforcement without human review",
    target_entity="Example Council",
    category="enforcement",
    private_key_hex="<your-ed25519-private-key-hex>",
)
# claim.commitment_hash, claim.signature, claim.to_json()

# Verify an on-chain receipt
result = verify_onchain_receipt(
    commitment_hash="<from-chain>",
    signature="<from-chain>",
    public_key_hex="<claimant-pubkey>",
)
# result.valid, result.details
```

```
Local Vault              Commitment              EVM L2                 Verifiable
(encrypted facts)   →    Fingerprint         →   (hash + sig only)  →  Receipt
```

---

## Repository map

| Path | What's inside |
| --- | --- |
| [`START_HERE.md`](START_HERE.md) | Guided entry point — pick a template, read a case study, or explore the framework |
| [`/templates`](./templates) | Ready-to-send letter templates for common situations |
| [`/case-studies`](./case-studies) | Real-world examples and outcomes |
| [`/tutorials`](./tutorials) | Step-by-step walkthroughs |
| [`/papers`](./papers) | In-depth legal and policy analysis |
| [`LIVE_AUDIT_LOG.md`](LIVE_AUDIT_LOG.md) | Chronological record of every institutional interaction and finding |
| [`INSTITUTIONAL_REGISTER.md`](INSTITUTIONAL_REGISTER.md) | Every institution tested, with sector, response, and finding |
| [`/enforcement`](./enforcement) | Optional cryptographic enforcement tools (Sovereign Personal Vault) |
| [`/onchain-protocol`](./onchain-protocol) | On-chain Burgess Claims Protocol — smart contracts, SDK, and examples |
| [`/toolkit`](./toolkit) | AI integration and knowledge base |
| [`SOUL.md`](SOUL.md) | The philosophy behind the framework |
| [`CONTRIBUTING.md`](CONTRIBUTING.md) | How to contribute — including good first issues |
| [`SECURITY.md`](SECURITY.md) | Security policy and cryptographic baseline |

---

## Origin

This framework was not built in a university, a law firm, or a policy institute. It was built by an ordinary person whose home was broken into under a warrant that nobody signed. He read the warrant because the system assumed nobody would. He found the defect because the system assumed nobody could. He built the framework because the system assumed nobody would try.

For the full story, see [SOUL.md](SOUL.md).

---

## Contributing

Contributions are welcome — new templates, translations, case studies, tests, and documentation improvements. Please read [CONTRIBUTING.md](CONTRIBUTING.md) before opening a PR.

---

## Licence

[MIT](LICENSE.md) — doctrine is free to use and adapt.

The certification mark (UK00004343685) governs commercial use of the standard.
