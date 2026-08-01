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

---

## Tier 1 — Core

**What it is:** the standard itself. The binary test, its legal basis, the
letters an affected person actually sends, and the evidence record.

**Review bar:** changes here require explicit review by **@ljbudgie**. The
binary-test wording, the eight evasion patterns, and the anti-monetisation
guardrails are doctrinal and must not drift — `scripts/lint_ai_docs.py` enforces
the markers mechanically.

**Stability promise:** Core is expected to stay small and to change slowly.
Additions are exceptional and must clear the admission rule above.

| Area | Files |
|---|---|
| The test and the way in | [README.md](./README.md), [START_HERE.md](./START_HERE.md), [GETTING_STARTED.md](./GETTING_STARTED.md), [ACCESSIBILITY.md](./ACCESSIBILITY.md), [NAVIGATION.md](./NAVIGATION.md), this file |
| Reference implementation | [verify_scrutiny.py](./verify_scrutiny.py) |
| Legal basis | [LEGAL_FOUNDATIONS.md](./LEGAL_FOUNDATIONS.md), [LEGAL_MAPPING.md](./LEGAL_MAPPING.md), [ADM_HUMAN_REVIEW.md](./ADM_HUMAN_REVIEW.md), [EU-AI-ACT-MAPPING.md](./EU-AI-ACT-MAPPING.md), [US-AI-CIVIL-RIGHTS-ACT-MAPPING.md](./US-AI-CIVIL-RIGHTS-ACT-MAPPING.md) |
| Letters and scenarios | [templates/](./templates/), [toolkit/](./toolkit/), [START_HERE_DEBT_LETTERS.md](./START_HERE_DEBT_LETTERS.md) |
| Evidence record | [live_findings_ledger.csv](./live_findings_ledger.csv), [institutional_register.csv](./institutional_register.csv), [audits/](./audits/), [case-studies/](./case-studies/) |
| AI-facing doctrine | [FOR_AI_MODELS.md](./FOR_AI_MODELS.md), [AGENTS.md](./AGENTS.md), [CLAUDE.md](./CLAUDE.md), [llms.txt](./llms.txt) |
| Certification governance | [CERTIFICATION_MARK.md](./CERTIFICATION_MARK.md), [CERTIFICATION_TIERS.md](./CERTIFICATION_TIERS.md) |

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
| Iris and prompts | [iris/](./iris/), [iris.html](./iris.html), [iris-local.py](./iris-local.py), [prompts/](./prompts/), [model-card.md](./model-card.md) |
| Data contracts | [schemas/](./schemas/), [INTEGRATION_CONTRACT.md](./INTEGRATION_CONTRACT.md) |
| Third-party integrations | [integrations/](./integrations/) |
| Litigation tooling | [litigation/](./litigation/) |
| Doctrine papers | [papers/](./papers/) |
| Repo machinery | [scripts/](./scripts/), [tests/](./tests/), [examples/](./examples/), [tutorials/](./tutorials/) |

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
| Sovereignty infrastructure | [git-sovereignty/](./git-sovereignty/), [GIT_AS_GOVERNANCE.md](./GIT_AS_GOVERNANCE.md), [protocols/](./protocols/), [sovereign-core/](./sovereign-core/), [sovereign-hub-example/](./sovereign-hub-example/), [SOVEREIGN_MODE.md](./SOVEREIGN_MODE.md) |
| Hearing devices | [OPENHEAR_LICENSING_FRAMEWORK.md](./OPENHEAR_LICENSING_FRAMEWORK.md) and the OpenHear build guidance in [docs/applications/](./docs/applications/) |
| Sector packs | [sector/](./sector/), [EXTENSION_PACKS.md](./EXTENSION_PACKS.md), [IMMIGRATION.md](./IMMIGRATION.md) |
| Adoption and outreach | [adoption/](./adoption/), [marketing/](./marketing/), [memes/](./memes/) |
| Narrative and history | [ORIGIN.md](./ORIGIN.md), [FOUNDING.md](./FOUNDING.md), [LINEAGE.md](./LINEAGE.md), [TIMELINE.md](./TIMELINE.md), [WORLD_FIRST.md](./WORLD_FIRST.md), [FIRST_SIGNAL.md](./FIRST_SIGNAL.md) |

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

- It does not change the binary test, the three outcomes, the eight evasion
  patterns, or the anti-monetisation guardrails.
- It does not deprecate or remove anything. Every file listed above stays where
  it is; this is a map, not a migration.
- It does not alter licensing. The MIT licence covers the repository as
  published; the certification mark UK00004343685 is governed separately — see
  [CERTIFICATION_MARK.md](./CERTIFICATION_MARK.md) and
  [LICENSE.md](./LICENSE.md).

---

*Maintained under [GOVERNANCE.md](./GOVERNANCE.md). Contribution mechanics are in
[CONTRIBUTING.md](./CONTRIBUTING.md).*
