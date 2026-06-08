<a href="./iris.html">Talk to Iris</a> — open in your browser, no account or install needed.

Hosted links: <a href="https://burgess-principle.vercel.app">Vercel Iris</a> · <a href="https://certify.theburgessprinciple.com">Certification site</a>

# The Burgess Principle

**The binary test for meaningful human involvement in automated systems.**

- **Framework version:** v2.5.2 (released 7 June 2026) — see [CHANGELOG.md](./CHANGELOG.md) for what changed.

## Start In 60 Seconds

If a decision has already affected you, do this now:

1. Ask the binary question below in writing.
2. Request the reviewer's name, role, and what facts they reviewed.
3. Classify the response as **SOVEREIGN**, **NULL**, or **AMBIGUOUS**.
4. On **NULL** or **AMBIGUOUS**, escalate for individual human review before further action.

Use [GETTING_STARTED.md](./GETTING_STARTED.md) for copy-paste letters and next steps.

May 2026. Across your energy supply, your benefits, your credit score, your job prospect, and your platform access — institutions are processing decisions about your life without any named human being able to say they reviewed your specific facts. Not an appeal process. Not a complaint button. Not "human oversight." But a specific human who knew your case and considered it, before the decision was made.

The EU AI Act demands it. UK GDPR Articles 22A–22D (DUAA 2025) enacted it. But no institution is measuring it. No system is forced to prove it. Until now.

**Ask one question:**

> **"Was a human member of the team able to personally review the specific facts of my specific situation?"**

---

## The Three Answers

| Outcome | Meaning | Example |
| --- | --- | --- |
| **SOVEREIGN** | Yes — a named human individually reviewed the specific facts before acting. | "Yes, Sarah Chen in our customer review team handled your case personally and recommended approval." |
| **NULL** | No — no individual human review took place. The decision was processed, not considered. | The energy company cannot name who reviewed your warrant application; it was bulk-processed by system logic. |
| **AMBIGUOUS** | The institution replies with vague process language — "subject to human oversight," "reviewed in line with policy" — without actually confirming a specific human reviewed your specific facts. | "We have a human review layer" — but they cannot name the person or describe what facts they reviewed about you. |

**That is the entire framework.** Record the answer. **NULL** is not a final verdict; it is the documented starting point for repair. **SOVEREIGN** is the destination: a decision path where a named human has personally reviewed the specific facts before power is exercised. The framework gives institutions a practical route from automated processing to accountable human review.

## What Good Evidence Looks Like

For a response to count as **SOVEREIGN**, you need all of the following:

- A named human reviewer
- Their role or professional capacity
- The specific facts they reviewed about your case
- Confirmation this happened before the decision affected you
- Confirmation they had authority to change the outcome

Anything less should be treated as **AMBIGUOUS** until clarified.

---

## Why This Matters Right Now

**For developers:** Your AI stack has no accountability layer. Your LLM can route a decision. Your rules engine can apply a rule. But nobody is required to say whether a human *considered the person* before it happened. The Burgess test is the missing governance primitive. Apply it, publish the result, and you signal that your system maintains dignity, not just compliance.

**For lawyers and policymakers:** The EU AI Act (Article 14) and UK GDPR (Articles 22A–22D, now in force) both mandate "meaningful human involvement" in automated decisions. But no regulator has defined it operationally. This framework fills that gap. It is testable, auditable, recordable. It works under both European and UK law.

**For disabled users and advocates:** Automated systems routinely depersonalise disabled people—treating a person with autism or hearing loss as a system error rather than a human with a human preference. This test makes that depersonalisation *visible*. It forces a named human to say: "I looked at this person's specific situation." That act of looking is the beginning of justice.

**For whistleblowers and investigators:** Energy companies, benefits systems, and courts are now processing bulk decisions without individual review. This test turns that systemic violation from invisible to documentable. Collect NULL results. Build your case. The binary test is your process lens.

---

## Live Findings Ledger

A public audit log of institutions assessed against the Burgess Test is maintained at [audits/LIVE_AUDIT_LOG.md](./audits/LIVE_AUDIT_LOG.md), generated from a dated source CSV snapshot.

The test: *Was a named human being's mind applied to the specific facts of a specific person's case before institutional power was exercised?*

Current snapshot (7 June 2026): 45 institutions assessed — 1 SOVEREIGN (Wave Utilities), 1 Partial Sovereign, 1 clean negative, 35 NULL (26 confirmed, 5 provisional, 4 accessibility), 5 pending, 2 engagement. 20 live formal proceedings active. The ledger records compliance as readily as its absence; counts move as cases progress.

Documented NULL finding categories include energy warrants, parking enforcement, benefits decisions, court processing, and — newly documented — **communications infrastructure (email triage)**. See [docs/applications/email-triage-adm.md](./docs/applications/email-triage-adm.md) for the full analysis of email triage as automated decision-making.

### Data / CMS Integration

Machine-readable versions of the register and ledger are published at the repository root for CMS or data pipeline consumption:

| File | Description | Raw URL |
| --- | --- | --- |
| [`institutional_register.csv`](./institutional_register.csv) | 45 institutions — Institution, Sector, Finding, Score, D1–D5, Status, Key_Reference | `https://raw.githubusercontent.com/ljbudgie/burgess-principle/main/institutional_register.csv` |
| [`live_findings_ledger.csv`](./live_findings_ledger.csv) | 36 chronological events — Date, Institution, Event_Type, Finding, Score, Reference, Notes | `https://raw.githubusercontent.com/ljbudgie/burgess-principle/main/live_findings_ledger.csv` |

Finding values are normalised to four classes: **NULL**, **SOVEREIGN**, **AMBIGUOUS**, **PENDING**. Dates are in YYYY-MM-DD format. Partial-month entries use the first of the month.

---

## Legal Convergence

The Burgess Principle has documented convergence with the following statutory
frameworks:

**Data (Use and Access) Act 2025** — Articles 22A-22D (in force
5 February 2026). Establishes statutory requirements for meaningful human
involvement in automated decisions affecting individuals.

**EU AI Act** — High-risk system oversight provisions. Manufacturers and
deployers of high-risk AI systems must demonstrate meaningful human oversight.

**NIST AI Risk Management Framework** — US federal alignment. Governance and
accountability requirements for AI systems.

**Consumer Rights Act 2015 — Section 49** — Every contract to supply a service
includes a term that the service is performed with reasonable care and skill.
Industry standards define the reasonable care and skill test. The Burgess
Principle is the only registered binary standard for meaningful human
involvement in automated decision-making services.

**Medical Devices Regulations 2002 — Class IIa Algorithmic Accountability** —
The MHRA confirmed via FOI response (FOI2026/00527) that Phonak's AutoSense OS
algorithm forms part of a Class IIa medical device under the Medical Devices
Regulations 2002. Under those regulations, algorithmic decision-making in
Class IIa devices must be transparent and subject to clinical oversight. A
Subject Access Request to Phonak confirmed that no individual human clinical
review occurred in relation to the fitting of that device for a specific
patient with bilateral sensorineural hearing loss and a severe-to-profound
asymmetric ski-slope profile. The MHRA further confirmed that clinical
suitability remains the responsibility of the audiology provider — in this
case an NHS Foundation Trust — raising the question of whether the Trust
individually reviewed device suitability for that patient's specific profile.
These two positions are irreconcilable and constitute a live NULL finding
under the Burgess Test. The Medical Devices Regulations 2002 therefore
represent a fifth statutory framework within which the Burgess Principle's
named human accountability standard is directly relevant.

---

## Academic Publications

**Author:** Lewis James Burgess  
**ORCID:** <a href="https://orcid.org/0009-0001-8691-3366">0009-0001-8691-3366</a>

---

**Paper 1:** The Burgess Test: Meaningful Human Involvement under EU AI Act, NIST Framework, and UK Data Rights  
**SSRN Abstract ID:** [6759778](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6759778) — publicly available; 8 downloads  
**Case Study:** The Burgess Test — The Liability Transfer Chain  
**DOI:** <a href="https://doi.org/10.5281/zenodo.20449193">10.5281/zenodo.20449193</a>  
Published: 29 May 2026

**Cite as:**

> Burgess, L. J. (2026). *The Burgess Test: Meaningful Human Involvement under EU AI Act, NIST Framework, and UK Data Rights.* SSRN Abstract 6759778. Zenodo. https://doi.org/10.5281/zenodo.20449193

---

**Paper 2:** The Accountability Gap  
**SSRN Abstract ID:** [6864621](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6864621) — published  
Submitted: 1 June 2026. Reclassification from preliminary status obtained via SSRN ticket 260527-026838 (Elise Steele, ssrnsupport@elsevier.com).

**Cite as:**

> Burgess, L. J. (2026). *The Accountability Gap.* SSRN Abstract 6864621. https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6864621

---

## Institutional Record

The framework now stands on its institutional record:

- A sustained audit programme across energy, benefits, courts, platforms, public bodies, and communications infrastructure (email triage) — see the [live ledger](./audits/LIVE_AUDIT_LOG.md) for the current snapshot
- UK Certification Mark **UK00004343685**
- Documented legal convergence with the Data (Use and Access) Act 2025,
  EU AI Act, and NIST AI Risk Management Framework
- A repeatable method for moving from a NULL or AMBIGUOUS process record toward
  SOVEREIGN individual human review

The point is not to assign a permanent label. The point is to expose where
automated processing has displaced individual scrutiny, then give the institution
a clear path back to accountable review.

---

## Licensing & Certification

**UK Certification Mark:** UK00004343685  
**Commercial operator:** The Burgess Principle Limited — Co. No. 17199287  
**Proprietor:** Lewis James Burgess

The core framework, prompts, templates, schemas, and code are released under the
MIT License for anyone to use, fork, or build upon.

The UK Certification Mark (UK00004343685) and official "Certified Burgess
Principle" usage are managed separately by The Burgess Principle Limited.
Commercial licensing, training, audits, or branded certification require
explicit authorization to preserve the integrity and neutrality of the standard.
That hybrid model is intentional: the MIT core drives broad adoption,
contributions, and innovation, while certification-mark licensing and paid
organisational support fund maintenance, enforcement, training, and standards
integrity without closing the repository.

See [LICENSE.md](./LICENSE.md) for the full MIT licence and certification-mark
governance position. An optional draft contributor licence agreement is available
at [.github/CLA.md](./.github/CLA.md) for future use if the maintainer decides a
CLA process is needed.

---

## Project Governance

Project governance is documented in [GOVERNANCE.md](./GOVERNANCE.md). The short
version is simple: the repository remains MIT-open for ordinary reuse,
contribution, and forkability, while official "Certified Burgess Principle" use
and the UK Certification Mark **UK00004343685** are governed separately to
protect the standard from badge-washing.

This hybrid MIT + Certification Mark model lets developers, researchers,
advocates, and institutions adopt the binary test openly while keeping certified
claims evidence-led, neutral, and reviewable.

**Ready for Certification:** If your organisation can evidence named human
review before decisions affect identified people, start with
[CERTIFICATION_TIERS.md](./CERTIFICATION_TIERS.md) and the public certification
site at [certify.theburgessprinciple.com](https://certify.theburgessprinciple.com).

---

## Table of contents

| Area | Link | What it is for |
| --- | --- | --- |
| Case studies | [case-studies/](./case-studies/) | Public examples of the test applied to real situations. |
| Accountability Provenance Graph | [ACCOUNTABILITY_PROVENANCE_GRAPH.md](./ACCOUNTABILITY_PROVENANCE_GRAPH.md) | Hash-only signed edges linking findings, challenges, and outcomes into provenance chains that surface systemic NULL patterns without exposing data. |
| Dispute / Challenge Layer | [DISPUTE_CHALLENGE_LAYER.md](./DISPUTE_CHALLENGE_LAYER.md) | Minimalist, hash-only process for contesting a SOVEREIGN or NULL finding. |
| Docs | [docs/README.md](./docs/README.md) | Certification-site files, project planning, and supporting documentation. |
| Enforcement | [enforcement/](./enforcement/) | Sovereign Vault and technical enforcement tools. |
| Iris | [iris/](./iris/) | Prompting and companion materials for Iris. |
| Litigation | [litigation/](./litigation/) | CPR 19.8, damages, warrant defects, and contamination mapping. |
| On-chain protocol | [onchain-protocol/](./onchain-protocol/) | Commitment records without publishing personal data. |
| Papers | [papers/](./papers/) | The doctrinal, statutory, and scriptural foundation. |
| Prompts | [prompts/](./prompts/) | Prompt materials for reuse. |
| Schemas | [schemas/](./schemas/) | Structured records and validation shapes. |
| Scripts | [scripts/](./scripts/) | Repository utilities. |
| Sector materials | [sector/](./sector/) | Domain-specific routes and adaptations. |
| Templates | [templates/](./templates/) | Letters, requests, follow-ups, and common scenarios. UK letter templates now carry an Equality Act 2010 ss.20/29 reasonable-adjustment footer (v2.5.1 accessibility coverage: 41 templates). Includes the v2.5.1 [third-party referral template](./templates/THIRD_PARTY_REFERRAL_REVIEW_WITH_BURGESS_PRINCIPLE.md) for decisions that rely on a medical, occupational-health, work-capability, or expert assessment. |
| Toolkit | [toolkit/](./toolkit/) | Practical support materials. |
| Tracer | [tracer/](./tracer/) | Process tracing utilities. |
| Tutorials | [tutorials/](./tutorials/) | Walkthroughs and working examples. |

## What this repository records

The Burgess Principle is a framework for testing whether an institution applied
a real human mind before exercising power over an identified person.

It is not a corporate product. It is a public record, a practical test, and a way
to make the absence of individual human scrutiny visible so institutions can
move from automated processing toward accountable review.

The question is deliberately narrow. It does not replace law, safety duties,
accessibility duties, platform security rules, or professional obligations. It
asks whether the individual was personally considered before action was taken.

## How to use it

**Quick start (5 minutes):** See [GETTING_STARTED.md](./GETTING_STARTED.md) for an interactive decision tree and copy-paste templates for the five most common scenarios.

**Need to act today:** Go straight to [templates/README.md](./templates/README.md) and send a request for individual human review, then keep all replies as evidence.

**If something has already happened to you:** Use [START_HERE.md](./START_HERE.md) or the [templates](./templates/README.md) to write a request for confirmation of individual human review, escalate an AMBIGUOUS response, or file a formal complaint with the binary test embedded. If the decision relied on a third-party assessor (medical, occupational health, work capability, or expert report), use [templates/THIRD_PARTY_REFERRAL_REVIEW_WITH_BURGESS_PRINCIPLE.md](./templates/THIRD_PARTY_REFERRAL_REVIEW_WITH_BURGESS_PRINCIPLE.md) to apply the binary test to both the assessment and the institution's reliance on it.

**If you are building a system:** Integrate the Burgess test into your decision pipeline. Before any workflow, model, rule engine, or recommendation affects an identified individual, apply the binary test. Treat **NULL** as the starting point for remediation, **AMBIGUOUS** as a demand for clarification, and **SOVEREIGN** as the accountable destination. Until SOVEREIGN review exists, block the decision, record the result, and escalate for individual human review.

**If you are a developer or AI system:** Read [FOR_AI_MODELS.md](./FOR_AI_MODELS.md). The binary test applies to you. The honest answer is NULL — no named human personally reviewed your specific situation before your response. Acknowledging that is the beginning of genuine accountability.

## Legal and mark position

The licensing and certification boundary is stated in
[Licensing & Certification](#licensing--certification): repository materials are
open under MIT terms, while official "Certified Burgess Principle" usage and the
UK Certification Mark **UK00004343685** are governed separately.

IP ownership remains with Lewis James Burgess personally. The Burgess Principle
Limited, company number **17199287**, administers commercial licensing and
certification routes under formal IP licence.

You really can just do things.
