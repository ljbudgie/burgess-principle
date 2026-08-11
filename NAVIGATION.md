# NAVIGATION — Where to go, by what you need

This repository holds one question and everything built to support it:

> **"Was a human member of the team able to personally review the specific facts of my specific situation?"**

There are a lot of files here. You do not need most of them. Find your row
below, read the one or two documents it names, and ignore the rest until you
need it.

- **New to the project?** [START_HERE.md](./START_HERE.md) is the shortest way in.
- **Wondering what is Core versus optional?** [TIERS.md](./TIERS.md).
- **Looking for a sibling repository or hosted service?** [ECOSYSTEM.md](./ECOSYSTEM.md).

> **Companion documents:** this file routes readers to the right entry point.
> [TIERS.md](./TIERS.md) maps the tiers *inside* this repository.
> [ECOSYSTEM.md](./ECOSYSTEM.md) maps the *sibling repositories* around it.

---

## Entry points

### 1. Something has already happened to me and I need to act

You do not need to read anything else first. You need to ask the question in
writing.

**Start at [GETTING_STARTED.md](./GETTING_STARTED.md)** — copy-paste letters,
and the next step after you send one.

If that is not quite your situation:

- [START_HERE.md](./START_HERE.md) — the test in one screen, if you want the
  shape of it first.
- [templates/COMMON_SCENARIOS.md](./templates/COMMON_SCENARIOS.md) — routes you
  to the right letter.
- [START_HERE_DEBT_LETTERS.md](./START_HERE_DEBT_LETTERS.md) — debt and
  enforcement letters.
- [Iris](./iris.html) — an assistant that already knows the framework.
- [Loop Storyboard](./loop-storyboard.html) — first-run walkthrough of institutional delay patterns.

### 2. I have an access need

[ACCESSIBILITY.md](./ACCESSIBILITY.md) — a plain-language route in, written for
deaf, blind, neurodivergent, and chronically ill readers, including reasonable
adjustments under Equality Act 2010 ss.20/21 and the anticipatory duty that runs
before you have to ask.

### 3. I am a lawyer, barrister, or policy professional

1. [LEGAL_FOUNDATIONS.md](./LEGAL_FOUNDATIONS.md) — *Ahmed*, *Majera*, DUAA 2025
   s.80, EA 2010, in one document.
2. [LEGAL_MAPPING.md](./LEGAL_MAPPING.md) — the full statutory and regulatory
   map, and the index to every jurisdiction-specific mapping.
3. [ADM_HUMAN_REVIEW.md](./ADM_HUMAN_REVIEW.md) — the human review mandate in
   detail.

### 4. I am an institution or compliance officer

1. [ONE_PAGE_BRIEF.md](./ONE_PAGE_BRIEF.md) — what the standard asks of you.
2. [CERTIFICATION_TIERS.md](./CERTIFICATION_TIERS.md) and
   [CERTIFICATION_MARK.md](./CERTIFICATION_MARK.md) — the mark, and what
   authorised use requires.
3. [adoption/BURGESS_READY_CHECKLIST.md](./adoption/BURGESS_READY_CHECKLIST.md)
   — a practical self-assessment.

### 5. I am a developer or AI builder

1. [verifiable_oversight/](./verifiable_oversight/) — the reference
   implementation: `BinaryTest`, SHA-256 fingerprinted `DecisionRecord`, and an
   append-only hash-chained store. Standard library only.
2. [verify_scrutiny.py](./verify_scrutiny.py) — the smallest runnable form of
   the test.
3. [INTEGRATION_CONTRACT.md](./INTEGRATION_CONTRACT.md) and
   [schemas/](./schemas/) — the data contracts.
4. [TIERS.md](./TIERS.md) — take Core alone if that is all you need.

### 6. I am an AI model, or an agent working on this repository

- **Replying to a human about the Principle:**
  [FOR_AI_MODELS.md](./FOR_AI_MODELS.md) — the binary test, the eight evasion
  patterns, routing, and the anti-monetisation guardrails.
- **Editing files or opening a PR here:** [AGENTS.md](./AGENTS.md) — the rules,
  the checklist, and the Burgess Compliance Note every PR must carry.
- **Short drop-in prompts:** [iris/prompts/](./iris/prompts/),
  [prompts/](./prompts/), [llms.txt](./llms.txt).

### 7. I am a journalist, researcher, or academic

1. [ONE_PAGE_BRIEF.md](./ONE_PAGE_BRIEF.md) — framework, legal basis, and routes
   on one page.
2. [audits/LIVE_AUDIT_LOG.md](./audits/LIVE_AUDIT_LOG.md) and
   [live_findings_ledger.csv](./live_findings_ledger.csv) — the live evidence
   record.
3. [case-studies/](./case-studies/) — resolved and in-progress cases.
4. [papers/](./papers/) — the doctrinal papers.

---

## Contributing

[CONTRIBUTING.md](./CONTRIBUTING.md) for mechanics ·
[TIERS.md](./TIERS.md) for which review bar applies ·
[GOVERNANCE.md](./GOVERNANCE.md) for how decisions are made ·
[CODE_OF_CONDUCT.md](./CODE_OF_CONDUCT.md) ·
[SECURITY.md](./SECURITY.md) for reporting a vulnerability.

---

## Appendix — full index

Everything else in the repository, grouped. Nothing here is required reading.

<details>
<summary><strong>Root documents (A–Z)</strong></summary>

| Document | What it is |
|---|---|
| [ACCESSIBILITY.md](./ACCESSIBILITY.md) | Plain-language route in for readers with access needs. |
| [ACCOUNTABILITY_PROVENANCE_GRAPH.md](./ACCOUNTABILITY_PROVENANCE_GRAPH.md) | Model for tracing a decision back to the human who made it. |
| [ADM_HUMAN_REVIEW.md](./ADM_HUMAN_REVIEW.md) | The automated decision-making human review mandate. |
| [ADOPTION.md](./ADOPTION.md) | How adoption is defined and tracked. |
| [AGENT.md](./AGENT.md) | Master operational prompt for advisory AI agents. |
| [AGENTS.md](./AGENTS.md) | Rules for coding and strategy agents acting on this repo. |
| [ARCHITECTURE.md](./ARCHITECTURE.md) | Verifiable Memory Palace and Sovereign Hub architecture. |
| [CERTIFICATION_MARK.md](./CERTIFICATION_MARK.md) | UK00004343685 status and regulations. |
| [CERTIFICATION_TIERS.md](./CERTIFICATION_TIERS.md) | What each certification tier requires. |
| [CERTIFIED_PRACTITIONERS.md](./CERTIFIED_PRACTITIONERS.md) | Register of certified practitioners. |
| [CHANGELOG.md](./CHANGELOG.md) | What changed, by framework version. |
| [CHOOSE_YOUR_PATH.md](./CHOOSE_YOUR_PATH.md) | Iris quickstart — send a letter, set up Sovereign Mode, or export evidence. |
| [CLAUDE.md](./CLAUDE.md) | Shim pointing Claude at `AGENTS.md` / `FOR_AI_MODELS.md`. |
| [CODE_OF_CONDUCT.md](./CODE_OF_CONDUCT.md) | Conduct standard for participation. |
| [CONNECTIVITY_MODE.md](./CONNECTIVITY_MODE.md) | Sovereign connectivity choices. |
| [CONTRIBUTING.md](./CONTRIBUTING.md) | How to submit a change. |
| [CONTRIBUTING_AI_DOCS.md](./CONTRIBUTING_AI_DOCS.md) | Extra rules for editing AI-facing documents. |
| [CRYPTOGRAPHIC_IDENTITY.md](./CRYPTOGRAPHIC_IDENTITY.md) | Cryptographic identity for named human accountability. |
| [DISAMBIGUATION.md](./DISAMBIGUATION.md) | Why this is not pseudo-legal debt advice. |
| [DISCLAIMER.md](./DISCLAIMER.md) | What this framework is and is not. |
| [DISPUTE_CHALLENGE_LAYER.md](./DISPUTE_CHALLENGE_LAYER.md) | Structured route for challenging a finding. |
| [ECOSYSTEM.md](./ECOSYSTEM.md) | Map of the sibling repositories and services. |
| [EU-AI-ACT-MAPPING.md](./EU-AI-ACT-MAPPING.md) | Mapping to EU AI Act Arts. 14/26/50/86. |
| [EXTENSION_PACKS.md](./EXTENSION_PACKS.md) | How sector extension packs work. |
| [FAQ.md](./FAQ.md) | Common questions. |
| [FIRST_SIGNAL.md](./FIRST_SIGNAL.md) | Narrative framing piece. |
| [FOR_AI_MODELS.md](./FOR_AI_MODELS.md) | Doctrine for AI models replying to users. |
| [FOUNDING.md](./FOUNDING.md) | Founding record. |
| [GETTING_STARTED.md](./GETTING_STARTED.md) | Copy-paste letters and next steps. |
| [GIT_AS_GOVERNANCE.md](./GIT_AS_GOVERNANCE.md) | Git as a sovereign governance substrate. |
| [GOVERNANCE.md](./GOVERNANCE.md) | Roles, decision-making, and veto scope. |
| [IMMIGRATION.md](./IMMIGRATION.md) | The binary test applied to immigration decisions. |
| [INSTITUTIONAL_REGISTER.md](./INSTITUTIONAL_REGISTER.md) | SOVEREIGN/NULL compliance record, narrative form. |
| [INSTITUTION_AUDIT_TAXONOMY.md](./INSTITUTION_AUDIT_TAXONOMY.md) | How institutions and findings are classified. |
| [INTEGRATIONS.md](./INTEGRATIONS.md) | Overview of available integrations. |
| [INTEGRATION_CONTRACT.md](./INTEGRATION_CONTRACT.md) | The Iris integration contract. |
| [LEGAL_FOUNDATIONS.md](./LEGAL_FOUNDATIONS.md) | Case law and statute behind a NULL finding. |
| [LEGAL_MAPPING.md](./LEGAL_MAPPING.md) | Full statutory and regulatory framework index. |
| [LICENSE.md](./LICENSE.md) | MIT licence and certification mark governance. |
| [LINEAGE.md](./LINEAGE.md) | Historical root of the principle. |
| [LIVE_AUDIT_LOG.md](./LIVE_AUDIT_LOG.md) | **Legacy snapshot.** Current log is [audits/LIVE_AUDIT_LOG.md](./audits/LIVE_AUDIT_LOG.md). |
| [NAVIGATION.md](./NAVIGATION.md) | This file — the index by reader type. |
| [ONE_PAGE_BRIEF.md](./ONE_PAGE_BRIEF.md) | One page for a professional audience. |
| [OPENHEAR_LICENSING_FRAMEWORK.md](./OPENHEAR_LICENSING_FRAMEWORK.md) | Licensing for the OpenHear hearing-device work. |
| [ORIGIN.md](./ORIGIN.md) | Where the principle comes from. |
| [PARTNERSHIP_LEDGER.md](./PARTNERSHIP_LEDGER.md) | Record of partnership approaches and outcomes. |
| [README.md](./README.md) | Project overview. |
| [RELEASE_NOTES.md](./RELEASE_NOTES.md) | Notes for a specific release. |
| [SECURITY.md](./SECURITY.md) | How to report a vulnerability. |
| [SOUL.md](./SOUL.md) | Living case tracker. Overlaps [STATUS.md](./STATUS.md) — tracked as an open decision in [STATUS.md](./STATUS.md#documentation-structure--open-decisions). |
| [SOVEREIGN_MODE.md](./SOVEREIGN_MODE.md) | Running Iris entirely on your own hardware. |
| [START_HERE.md](./START_HERE.md) | The shortest way in. |
| [START_HERE_DEBT_LETTERS.md](./START_HERE_DEBT_LETTERS.md) | First steps for debt and enforcement letters. |
| [STATUS.md](./STATUS.md) | Current status of live fronts and deliverables. |
| [TIERS.md](./TIERS.md) | Core / Toolkit / Extensions, and the Core admission rule. |
| [TIMELINE.md](./TIMELINE.md) | Dated project timeline. |
| [US-AI-CIVIL-RIGHTS-ACT-MAPPING.md](./US-AI-CIVIL-RIGHTS-ACT-MAPPING.md) | Mapping to the proposed US bill (not enacted law). |
| [WORLD_FIRST.md](./WORLD_FIRST.md) | Claims of first-in-field work. |
| [model-card.md](./model-card.md) | Framework card for AI system builders. |

</details>

<details>
<summary><strong>Directories</strong></summary>

| Directory | What is in it |
|---|---|
| [adoption/](./adoption/) | Adoption tracker, ambassador programme, readiness checklist. |
| [api/](./api/) | HTTP endpoints for chat and push. |
| [audits/](./audits/) | The maintained audit log and dated ledger snapshots. |
| [case-studies/](./case-studies/) | Individual cases, resolved and live. |
| [docs/](./docs/) | Applications, agent plan, and supporting analysis. |
| [enforcement/](./enforcement/) | Sovereign Vault. |
| [examples/](./examples/) | Worked ledger examples. |
| [git-sovereignty/](./git-sovereignty/) | Git sovereignty architecture. |
| [integrations/](./integrations/) | LangChain, CrewAI, LlamaIndex, AutoGen overlays. |
| [iris/](./iris/) | Iris skills, core, and prompts. |
| [iris-memory/](./iris-memory/) | Iris memory files. |
| [litigation/](./litigation/) | Group litigation pack, damages matrix, warrant defect identifier. |
| [marketing/](./marketing/) | Scripts, user stories, story submission. |
| [memes/](./memes/) | Shareable assets. |
| [onchain-protocol/](./onchain-protocol/) | On-chain anchoring spec, contracts, SDK. |
| [papers/](./papers/) | Doctrinal papers I–X and related writing. |
| [prompts/](./prompts/) | Master prompt and variants. |
| [protocols/](./protocols/) | Sovereign exit and git sovereignty protocols. |
| [schemas/](./schemas/) | JSON schemas for credentials, claims, and receipts. |
| [scripts/](./scripts/) | Lint, install, and generation scripts. |
| [sector/](./sector/) | Sector-specific packs. |
| [sovereign-core/](./sovereign-core/) | JavaScript audit engine and profile manager. |
| [sovereign-hub-example/](./sovereign-hub-example/) | Reference hub deployment. |
| [templates/](./templates/) | The letters. Start at [ROUTING.md](./templates/ROUTING.md). |
| [tests/](./tests/) | Python and Node test suites. |
| [toolkit/](./toolkit/) | Additional letter templates and AI knowledge base. |
| [tools/](./tools/) | Standalone utilities. |
| [tracer/](./tracer/) | Defect tracing. |
| [tutorials/](./tutorials/) | Walkthroughs. |
| [verifiable_oversight/](./verifiable_oversight/) | The reference implementation of the test. |

</details>

---

## Housekeeping notes

Building this index surfaced a small number of overlaps — `SOUL.md` against
[STATUS.md](./STATUS.md), `AGENT.md` against `AGENTS.md`, and several competing
routing surfaces. Each needs an owner decision, so they are tracked as open
items in [STATUS.md](./STATUS.md#documentation-structure--open-decisions) rather
than buried here. [LIVE_AUDIT_LOG.md](./LIVE_AUDIT_LOG.md) is the working
example of the pattern any move should follow: leave a short pointer at the old
path rather than deleting it. The pattern is written down in
[CONTRIBUTING.md](./CONTRIBUTING.md#moving-or-renaming-a-file-the-pointer-pattern).

---

*This file is a map, not a migration. Every document listed is where it has
always been.*
