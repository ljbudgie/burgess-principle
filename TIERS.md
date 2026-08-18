# TIERS — What is Core, what is Toolkit, what is an Extension

The Burgess Principle is one question:

> **"Was a human member of the team able to personally review the specific facts of my specific situation?"**

Everything else in this repository exists to make that question askable,
answerable, and recordable. This document draws the boundary between the parts
that carry the standard and the parts that build on it.

It exists for three reasons:

1. **Adopters** should be able to take the test without taking the whole
   ecosystem.
2. **Contributors** should know which review bar applies before opening a PR.
3. **The project** should have a written defence against scope creep. The
   admission rule below is that defence.

> **Companion documents:** [NAVIGATION.md](./NAVIGATION.md) routes readers to the
> right entry point. [ECOSYSTEM.md](./ECOSYSTEM.md) maps the *sibling
> repositories* around this one. This file maps the tiers *inside* this one.

---

## The admission rule

> **Nothing enters Core unless it strengthens the binary test itself or the
> path an affected person walks from a decision to accountable human review.**

If a proposed change is useful but does not meet that bar, it belongs in
Toolkit or Extensions. A good idea in the wrong tier is still the wrong change.

Three questions to place a change:

| Ask | If yes |
|---|---|
| Does this change what the test *is*, what it *means in law*, or the letter a person sends? | **Core** |
| Does this *implement* the test in code, or help someone apply it? | **Toolkit** |
| Does this build something adjacent, sector-specific, or promotional on top? | **Extensions** |

### The default tier

Not every file in the repository is named in the tables below, and new work
arrives faster than this map is revised. The default resolves the ambiguity:

> **Anything not listed in a tier below is Toolkit.**

If you believe a change belongs in Core, say so in the pull request and explain
which half of the admission rule it meets. Claiming Core is a request for
founder review, not a shortcut past it. Nothing is Extensions by default —
Extensions is a deliberate placement, not a residue.

`scripts/check_doc_coverage.py` keeps this map honest: CI fails if a root
document is not placed in a tier below, or not indexed in
[NAVIGATION.md](./NAVIGATION.md).

---

## Tier 1 — Core

**What it is:** the standard itself. The binary test, its legal basis, the
letters an affected person actually sends, and the evidence record.

**Review bar:** Core carries two bars, not one.

| Change | Bar |
|---|---|
| **Doctrinal** — the binary-test wording, the three outcomes, the evasion patterns in [FOR_AI_MODELS.md](./FOR_AI_MODELS.md) Part 3, the anti-monetisation guardrails, any statement of legal effect, or any claim made on behalf of the certification mark | Explicit review by **@ljbudgie** |
| **Editorial** — typos, broken links, clearer phrasing, formatting, examples, and routing fixes that leave the meaning intact | Ordinary lazy consensus, same as Toolkit |

The distinction matters: doctrine must not drift, but a person should not need
founder approval to fix a dead link on the page an affected person lands on.
`scripts/lint_ai_docs.py` enforces the doctrinal markers mechanically, so an
editorial change that strays into doctrine fails CI rather than slipping
through. [CONTRIBUTING_AI_DOCS.md](./CONTRIBUTING_AI_DOCS.md) sets out the same
split in detail for the AI-facing documents.

**Stability promise:** Core is expected to stay small and to change slowly.
Additions are exceptional and must clear the admission rule above.

| Area | Files |
|---|---|
| The test and the way in | [README.md](./README.md), [START_HERE.md](./START_HERE.md), [GETTING_STARTED.md](./GETTING_STARTED.md), [ACCESSIBILITY.md](./ACCESSIBILITY.md), [NAVIGATION.md](./NAVIGATION.md), [FAQ.md](./FAQ.md), [ONE_PAGE_BRIEF.md](./ONE_PAGE_BRIEF.md), [TIERS.md](./TIERS.md) (this file) |
| Reference implementation | [verify_scrutiny.py](./verify_scrutiny.py) |
| Legal basis | [LEGAL_FOUNDATIONS.md](./LEGAL_FOUNDATIONS.md), [LEGAL_MAPPING.md](./LEGAL_MAPPING.md), [ADM_HUMAN_REVIEW.md](./ADM_HUMAN_REVIEW.md), [EU-AI-ACT-MAPPING.md](./EU-AI-ACT-MAPPING.md), [US-AI-CIVIL-RIGHTS-ACT-MAPPING.md](./US-AI-CIVIL-RIGHTS-ACT-MAPPING.md) |
| Scope limits | [DISCLAIMER.md](./DISCLAIMER.md), [DISAMBIGUATION.md](./DISAMBIGUATION.md) — what the framework is not; both bound the legal claims above |
| Letters and scenarios | [templates/](./templates/), [toolkit/](./toolkit/), [START_HERE_DEBT_LETTERS.md](./START_HERE_DEBT_LETTERS.md) |
| Evidence record | [live_findings_ledger.csv](./live_findings_ledger.csv), [institutional_register.csv](./institutional_register.csv), [audits/](./audits/), [case-studies/](./case-studies/), [INSTITUTIONAL_REGISTER.md](./INSTITUTIONAL_REGISTER.md), [LIVE_AUDIT_LOG.md](./LIVE_AUDIT_LOG.md) (legacy pointer) |
| AI-facing doctrine | [FOR_AI_MODELS.md](./FOR_AI_MODELS.md), [AGENTS.md](./AGENTS.md), [AGENT.md](./AGENT.md), [CLAUDE.md](./CLAUDE.md), [llms.txt](./llms.txt) |
| Certification governance | [CERTIFICATION_MARK.md](./CERTIFICATION_MARK.md), [CERTIFICATION_TIERS.md](./CERTIFICATION_TIERS.md), [CERTIFIED_PRACTITIONERS.md](./CERTIFIED_PRACTITIONERS.md) |

**Portability goal:** a person or institution should be able to adopt Core alone
— the question, the three outcomes, a letter, and a record — without installing
anything from the tiers below.

---

## Tier 2 — Toolkit

**What it is:** implementations of the test, and tools that help someone apply
it. Toolkit depends on Core. Core never depends on Toolkit.

**Review bar:** ordinary lazy consensus under
[GOVERNANCE.md](./GOVERNANCE.md#decision-making-process). Open to future
co-maintainers. Changes must not restate or reinterpret doctrine — where a
Toolkit component needs the test wording, it should cite Core rather than copy
it.

| Area | Files |
|---|---|
| Verifiable oversight | [verifiable_oversight/](./verifiable_oversight/) — `BinaryTest`, `DecisionRecord`, hash-chained store |
| Defect tracing | [tracer/](./tracer/) |
| Services and CLIs | [api.py](./api.py), [api/](./api/), [bgsp.py](./bgsp.py) |
| Iris and prompts | [iris/](./iris/), [iris.html](./iris.html), [iris-local.py](./iris-local.py), [iris-memory/](./iris-memory/), [prompts/](./prompts/), [model-card.md](./model-card.md), [CHOOSE_YOUR_PATH.md](./CHOOSE_YOUR_PATH.md), [ARCHITECTURE.md](./ARCHITECTURE.md) |
| Data contracts | [schemas/](./schemas/), [INTEGRATION_CONTRACT.md](./INTEGRATION_CONTRACT.md) |
| Third-party integrations | [integrations/](./integrations/), [INTEGRATIONS.md](./INTEGRATIONS.md) |
| Litigation tooling | [litigation/](./litigation/) |
| Audit method | [INSTITUTION_AUDIT_TAXONOMY.md](./INSTITUTION_AUDIT_TAXONOMY.md), [DISPUTE_CHALLENGE_LAYER.md](./DISPUTE_CHALLENGE_LAYER.md), [ACCOUNTABILITY_PROVENANCE_GRAPH.md](./ACCOUNTABILITY_PROVENANCE_GRAPH.md) — how findings are classified, challenged, and traced |
| Doctrine papers | [papers/](./papers/) — papers *apply* the test; they do not restate or amend it |
| Build, test, and tooling | [scripts/](./scripts/), [tests/](./tests/), [examples/](./examples/), [tutorials/](./tutorials/), [tools/](./tools/) |

---

## Tier 3 — Extensions

**What it is:** work built on top of the Principle that is valuable but is not
the standard and is not required to use it. Extensions may move at their own
pace, and may be split out into separate repositories without weakening Core.

**Review bar:** ordinary lazy consensus. Extensions must not be presented as
prerequisites for applying the binary test.

| Area | Files |
|---|---|
| Cryptographic and on-chain | [onchain-protocol/](./onchain-protocol/), [enforcement/sovereign-vault/](./enforcement/), [CRYPTOGRAPHIC_IDENTITY.md](./CRYPTOGRAPHIC_IDENTITY.md) |
| Sovereignty infrastructure | [git-sovereignty/](./git-sovereignty/), [GIT_AS_GOVERNANCE.md](./GIT_AS_GOVERNANCE.md), [protocols/](./protocols/), [sovereign-core/](./sovereign-core/), [sovereign-hub-example/](./sovereign-hub-example/), [SOVEREIGN_MODE.md](./SOVEREIGN_MODE.md), [CONNECTIVITY_MODE.md](./CONNECTIVITY_MODE.md) |
| Hearing devices | [OPENHEAR_LICENSING_FRAMEWORK.md](./OPENHEAR_LICENSING_FRAMEWORK.md) and the OpenHear build guidance in [docs/applications/](./docs/applications/) |
| Sector packs | [sector/](./sector/), [EXTENSION_PACKS.md](./EXTENSION_PACKS.md), [IMMIGRATION.md](./IMMIGRATION.md) |
| Adoption and outreach | [adoption/](./adoption/), [marketing/](./marketing/), [memes/](./memes/), [ADOPTION.md](./ADOPTION.md), [PARTNERSHIP_LEDGER.md](./PARTNERSHIP_LEDGER.md) |
| Narrative and history | [ORIGIN.md](./ORIGIN.md), [FOUNDING.md](./FOUNDING.md), [LINEAGE.md](./LINEAGE.md), [TIMELINE.md](./TIMELINE.md), [WORLD_FIRST.md](./WORLD_FIRST.md), [FIRST_SIGNAL.md](./FIRST_SIGNAL.md), [SOUL.md](./SOUL.md) |

---

## Outside the tiers

Some files govern the repository rather than sitting inside it. They are not
Core, Toolkit, or Extensions, and the admission rule does not apply to them.

| Area | Files |
|---|---|
| Contribution and conduct | [CONTRIBUTING.md](./CONTRIBUTING.md), [CONTRIBUTING_AI_DOCS.md](./CONTRIBUTING_AI_DOCS.md), [CODE_OF_CONDUCT.md](./CODE_OF_CONDUCT.md), [GOVERNANCE.md](./GOVERNANCE.md), [SECURITY.md](./SECURITY.md) |
| Licensing and design rationale | [LICENSE.md](./LICENSE.md), [EPONYMOUS_DESIGN.md](./EPONYMOUS_DESIGN.md), [CITATION.cff](./CITATION.cff) |
| Project record | [CHANGELOG.md](./CHANGELOG.md), [RELEASE_NOTES.md](./RELEASE_NOTES.md), [STATUS.md](./STATUS.md) |
| Published site and supporting docs | [docs/](./docs/) — the published site surface, the 90-day plan, and long-form analysis |
| Sibling repositories | [ECOSYSTEM.md](./ECOSYSTEM.md) — the map outside this repository |

---

## Dependency direction

```
Core  ←  Toolkit  ←  Extensions
```

Dependencies point inward only. An Extension may rely on Toolkit and Core; Core
relies on nothing above it. A PR that makes Core depend on a lower tier should
be restructured rather than merged.

---

## What this document does not do

- It does not change the binary test, the three outcomes, the evasion patterns
  in [FOR_AI_MODELS.md](./FOR_AI_MODELS.md) Part 3, or the anti-monetisation
  guardrails.
- It does not deprecate or remove anything. Every file listed above stays where
  it is; this is a map, not a migration.
- It does not alter licensing. The MIT licence covers the repository as
  published; the certification mark UK00004343685 is governed separately — see
  [CERTIFICATION_MARK.md](./CERTIFICATION_MARK.md) and
  [LICENSE.md](./LICENSE.md).

---

*Maintained under [GOVERNANCE.md](./GOVERNANCE.md). Contribution mechanics are in
[CONTRIBUTING.md](./CONTRIBUTING.md).*
