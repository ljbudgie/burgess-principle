# Immigration Decisions and the Burgess Binary Test

**Part of:** The Burgess Principle · UK Certification Mark UK00004343685  
**Status:** Live analysis — updated 17 June 2026  
**Permalink:** `IMMIGRATION.md`

---

## Scope and Purpose

This document applies the Burgess Principle binary test — *was a named human being's mind applied to the specific facts of this person's case before institutional power was exercised?* — to immigration decision-making in the UK, with particular focus on the use of AI and automated processing in asylum determination, age assessment, and enforcement prioritisation.

It integrates the statutory framework established by the **Data (Use and Access) Act 2025 (s.80)** and the **Border Security, Asylum and Immigration Act 2025 (c.31)**, maps each decision type to the correct governing limb, and records documented accountability gaps where no named human review is publicly confirmed.

For the full statutory analysis of DUAA 2025 s.80, see [`ADM_HUMAN_REVIEW.md`](./ADM_HUMAN_REVIEW.md). For the master legal index, see [`LEGAL_MAPPING.md`](./LEGAL_MAPPING.md).

---

## Governing Statutory Framework

### Data (Use and Access) Act 2025, s.80

Royal Assent: **19 June 2025**. In force: **5 February 2026** (SI 2026/82).

Operative definition:

> *"a decision is based solely on automated processing if there is no meaningful human involvement in the taking of the decision."*
>
> Primary source: [legislation.gov.uk/ukpga/2025/18/section/80](https://www.legislation.gov.uk/ukpga/2025/18/section/80)

**Two limbs — both active in immigration contexts:**

**Limb A — Art 22A (general processing, Part 2 UK GDPR):** Applies to decisions producing a legal or similarly significant effect on the data subject. Governs administrative immigration decisions — asylum determination, age assessment for entitlement purposes, AI-assisted casework.

**Limb B — s.50A LE limb (law enforcement processing, Part 3 DPA 2018):** Applies to decisions producing an adverse legal or similarly significant adverse effect where the processing is for a law enforcement purpose. Governs Home Office immigration enforcement — detention prioritisation, removal sequencing, deportation decision-making.

### Border Security, Asylum and Immigration Act 2025 (c.31)

Royal Assent: **2 December 2025**.  
Primary source: [legislation.gov.uk/ukpga/2025/31](https://www.legislation.gov.uk/ukpga/2025/31)

Provides the statutory framework within which AI age assessment tools and enforcement prioritisation systems operate. Subject to Lords scrutiny at Report Stage (3 November 2025) where AI-based age assessment was specifically examined.

---

## The Binary Test Applied — Immigration Decision Types

### 1. Asylum Determination

**What happens:** A Home Office decision-maker determines whether an applicant qualifies for refugee status or humanitarian protection. Since at least May 2024, decision-makers have been presented with AI-generated outputs from the Asylum Case Summarisation (ACS) and Asylum Policy Search (APS) tools before or during the determination process.

**Tech involvement:**

- **ACS** — GPT-4 converts asylum interview transcripts into summaries presented to decision-makers. GOV.UK evaluation (29 April 2025): [gov.uk/government/publications/evaluation-of-ai-trials-in-the-asylum-decision-making-process](https://www.gov.uk/government/publications/evaluation-of-ai-trials-in-the-asylum-decision-making-process/evaluation-of-ai-trials-in-the-asylum-decision-making-process)
  - 9% of summaries removed pre-use by technical specialists for inaccuracy or missing information. *Precision: this is a pre-use QA removal rate, not a post-decision error rate.*
  - 23% of decision-maker users reported not being fully confident in summaries.
  
- **APS** — AI search assistant for Country Policy and Information Notes and Country of Origin Information Reports.
  - 5% of users reported lacking confidence in tool accuracy. *Note: the 9% figure belongs to ACS; the 5% figure is specific to APS.*

**Evidence of (lack of) meaningful human involvement:**

- Applicants are not informed that AI tools are used in their case — breach of the Art 22A transparency safeguard.
- Applicants cannot access or correct AI-generated outputs — breach of the right to make representations and contest.
- No named decision-maker is confirmed as individually reviewing AI outputs against the specific facts of the specific applicant before the determination.
- Legal opinion (Robin Allen KC, Dee Masters — Cloisters; Joshua Jackson — Doughty Street; commissioned by Open Rights Group; **17 March 2026**): Home Office use of ACS and APS is *"likely to be unlawful"* because both tools "create new text for the Decision-Maker to consider rather than simply indexing or organising the existing source information."
  - [Open Rights Group (17 March 2026)](https://www.openrightsgroup.org/press-releases/home-office-use-of-ai-in-asylum-cases-likely-to-be-unlawful-legal-opinion-finds/)
  - [Doughty Street Chambers (17 March 2026)](https://www.doughtystreet.co.uk/news/home-office-use-ai-asylum-decision-making-significant-risk-being-unlawful-legal-opinion-finds)

**Governing limb:** **Art 22A** (Part 2 — general processing; legal / significantly significant effect on asylum entitlement)

**Burgess classification: NULL** — no named human review of AI-specific outputs against individual applicant's facts publicly confirmed; transparency and contest safeguards not met.

**Statutory / safeguard hooks:** DUAA 2025 Art 22A–22D (transparency, representations, human intervention, contest); Equality Act 2010 s.149 (PSED — individual consideration before exercising functions affecting protected groups)

---

### 2. Age Assessment

**What happens:** The Home Office determines the age of an asylum applicant where age is disputed. Age classification affects entitlement (adult vs child asylum support and accommodation pathways), detention decisions, and vulnerability designation. The Home Office announced in July 2025 plans to use AI facial estimation tools in this process.

**Tech involvement:** AI facial age estimation (Home Office July 2025 announcement). Scrutinised at Lords Report Stage, 3 November 2025 — Border Security, Asylum and Immigration Bill.

**Hansard reference:** HC Lords, 3 November 2025  
**Debate ID:** `A8A75F9A-F73A-448E-9F33-52646DA4A9F1`  
**URL:** [hansard.parliament.uk/lords/2025-11-03/debates/A8A75F9A-F73A-448E-9F33-52646DA4A9F1/BorderSecurityAsylumAndImmigrationBill](https://hansard.parliament.uk/lords/2025-11-03/debates/A8A75F9A-F73A-448E-9F33-52646DA4A9F1/BorderSecurityAsylumAndImmigrationBill)  
**Column references:** To be confirmed from full Hansard pull.

> **Provenance note:** Debates on the BSAIA Bill also occurred at Committee Stage on 3 and 8 September 2025. The 3 November 2025 Report Stage is the sitting at which AI-based age assessment was specifically scrutinised. No quotes have been extracted from the November sitting pending column reference confirmation.

**Evidence of (lack of) meaningful human involvement:**

- No public confirmation of a named human individually verifying AI facial estimation output against the specific applicant's individual circumstances before the age classification is recorded and acted upon.
- Lords scrutiny raised accuracy and bias concerns (3 November 2025 — specifics to be confirmed from Hansard).
- Age determination via algorithmic facial estimation without named human verification of the specific output is structurally equivalent to ACS summarisation: AI generates the substantive material; no confirmed named reviewer validates it against the individual before it affects entitlement.

**Governing limb:** **Art 22A** (Part 2 — administrative age determination affecting asylum entitlement; legal / similarly significant effect)

**Burgess classification: NULL** — no named human reviewer confirmed as individually verifying AI output against specific applicant facts before age classification affects entitlement. Accountability gap recorded.

**Statutory / safeguard hooks:** DUAA 2025 Art 22A; BSAIA 2025 (c.31); Equality Act 2010 s.20 (anticipatory reasonable adjustment for vulnerability and disability); Equality Act 2010 s.149 (PSED)

---

### 3. Enforcement Prioritisation

**What happens:** The Home Office prioritises individuals for immigration detention, removal from the UK, or deportation. This involves case-scoring, risk-flagging, or algorithmic sequencing of enforcement action.

**Tech involvement:** Algorithmic case-scoring / risk-flagging tools. No specific named tool has been publicly confirmed by the Home Office as at 17 June 2026.

**Evidence of (lack of) meaningful human involvement:**

> **Accountability gap — recorded 17 June 2026:** No public disclosure has been made of a named reviewer or named human sign-off individually verifying the specific facts of each case before that case is prioritised for enforcement action (detention, removal, or deportation). The systemic batch-processing pattern is documented. The absence of any public confirmation of named individual review before enforcement is triggered is itself the accountability gap this entry records.
>
> This is a NULL finding on the basis of documented process architecture: the institution has not confirmed that a named human, with authority to change the outcome, individually reviewed the specific facts of the specific person's case before enforcement action was initiated. The burden of demonstrating SOVEREIGN rests on the institution. It has not been discharged.

**Governing limb:** **s.50A LE limb** (Part 3 DPA 2018 / DUAA 2025 — law enforcement processing; adverse legal / similarly significant adverse effect)

**Burgess classification: NULL** — no named human individual review publicly confirmed before batch enforcement prioritisation. Clear accountability gap.

**Statutory / safeguard hooks:** DUAA 2025 ss.50A–50D; DPA 2018 Part 3; BSAIA 2025 (c.31); Equality Act 2010 s.149 (PSED — public authority must consider individual circumstances before exercising enforcement functions)

---

## Summary Mapping Table

| Decision type | Tech involvement | Evidence of (lack of) meaningful human involvement | Governing limb | Burgess classification | Statutory / safeguard hooks |
|---|---|---|---|---|---|
| **Asylum determination** | ACS (GPT-4 summaries) + APS (policy search) | Not disclosed to applicant; applicant cannot access/correct; 9% ACS pre-use inaccuracy; legal opinion 17 Mar 2026 — likely unlawful | **Art 22A** (Part 2 DUAA 2025) | **NULL** | DUAA 2025 Art 22A–22D; Equality Act 2010 s.149 |
| **Age assessment** | AI facial estimation (Jul 2025 announcement); Lords scrutiny 3 Nov 2025 (col. refs TBC) | No named reviewer confirmed verifying AI output against individual facts before classification affects entitlement | **Art 22A** (Part 2 DUAA 2025) | **NULL** | DUAA 2025 Art 22A; BSAIA 2025 (c.31); Equality Act 2010 ss.20, 149 |
| **Enforcement prioritisation** (detention / removal / deportation) | Algorithmic case-scoring (no specific tool publicly named as at 17 Jun 2026) | **Accountability gap:** no named reviewer or human sign-off publicly confirmed before batch enforcement action is initiated | **s.50A LE limb** (Part 3 DPA 2018) | **NULL** | DUAA 2025 ss.50A–50D; DPA 2018 Part 3; BSAIA 2025 (c.31); Equality Act 2010 s.149 |

---

## Home Office Precedent — Duty to Power (March 2026)

The Home Office simultaneously provides the most important **positive** external validation of the binary test. In March 2026, the Home Secretary converted asylum support under the Immigration and Asylum Act 1999 (ss.4, 95, 98) from a blanket statutory duty (NULL architecture — automatic, no named reviewer required) into a conditional power (SOVEREIGN architecture — named caseworker, specific facts, individual review before power is exercised).

The Government has therefore enacted, in statute, the exact standard the Burgess binary test applies — and applied it to the same department that is simultaneously operating NULL-classified AI tools in asylum determination.

**The binary test does not require new law. The law already requires it.**

Full analysis: [`docs/applications/home-office-asylum-support-parallel.md`](./docs/applications/home-office-asylum-support-parallel.md)

---

## Reusable Argument Block

For use in DSARs, subject access requests, pre-action protocol letters, and formal institutional correspondence in immigration matters. Full block: [`ADM_HUMAN_REVIEW.md — Reusable "Human Review Mandate" Argument Block`](./ADM_HUMAN_REVIEW.md#reusable-human-review-mandate-argument-block).

---

## Cross-links

- [ADM Human Review — DUAA 2025 s.80 full analysis and reusable argument block](./ADM_HUMAN_REVIEW.md)
- [Legal mapping — master statutory index](./LEGAL_MAPPING.md)
- [Home Office parallel — duty to power (IAA 1999 ss.4/95/98)](./docs/applications/home-office-asylum-support-parallel.md)
- [Cross-sector template paragraphs including EASS/EHRC and Parliamentary Standards](./templates/GOVERNMENT_PARALLEL_ACCOUNTABILITY_WITH_BURGESS.md)
- [EU AI Act mapping](./EU-AI-ACT-MAPPING.md)
- [Structural defect analysis](./docs/STRUCTURAL_DEFECT_ANALYSIS.md)
- [Model card](./model-card.md)
- [Live audit log](./audits/LIVE_AUDIT_LOG.md)

---

*The Burgess Principle — UK Certification Mark UK00004343685*  
*lewisjames@theburgessprinciple.com · theburgessprinciple.com*  
*github.com/ljbudgie/burgess-principle*
