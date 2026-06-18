# Automated Decision-Making and the Human Review Mandate

**Part of:** The Burgess Principle · UK Certification Mark UK00004343685  
**Status:** Live statutory analysis — updated 17 June 2026  
**Permalink:** `ADM_HUMAN_REVIEW.md`

---

## Statutory Recognition of "Meaningful Human Involvement" as the Binary Threshold (DUAA 2025, s.80)

The Data (Use and Access) Act 2025 ("DUAA 2025"), receiving Royal Assent on **19 June 2025** and brought into force on **5 February 2026** by SI 2026/82, enacted the operative statutory definition of automated decision-making in UK law. Section 80 replaced UK GDPR Article 22 with new Articles 22A–22D (general processing limb) and simultaneously substituted new sections 50A–50D into the Data Protection Act 2018 (law enforcement processing limb).

> **Operative definition (s.80, DUAA 2025):**
> *"a decision is based solely on automated processing if there is no meaningful human involvement in the taking of the decision."*
>
> — Data (Use and Access) Act 2025, s.80  
> Primary source: [legislation.gov.uk/ukpga/2025/18/section/80](https://www.legislation.gov.uk/ukpga/2025/18/section/80)

This is the statutory threshold the Burgess Principle binary test operationalises:

- **SOVEREIGN** = meaningful human involvement present — named human, specific facts, before the decision.
- **NULL** = no meaningful human involvement — automated, batch, or status-based processing without individual human review.

---

## The Two Limbs — Mapped to Decision Type

Section 80 contains two distinct limbs. Applying the wrong limb to a given decision type is a precision error the Burgess Principle does not make.

### Limb A — General Processing (Art 22A, Part 2 UK GDPR)

**Trigger:** Decisions based solely on automated processing that produce a legal or similarly significant effect on a data subject.

**Governing provision:** New Article 22A (inserted by DUAA 2025 s.80 into UK GDPR).

**Applies to:** Asylum status determination, age assessment for asylum entitlement purposes, ACS/APS-assisted decision-making in refugee claim processing — i.e., administrative decisions about individuals' rights and entitlements.

**Safeguards under Art 22A–22D:**

1. Transparency — the data subject must be informed that automated processing is being used and the logic involved.
2. Right to make representations — before or after the decision.
3. Right to human intervention — a named human with authority to review and change the outcome.
4. Right to contest the decision.
5. Secretary of State regulation-making power over what constitutes "meaningful human involvement" — this power remains unexercised as of 17 June 2026.

### Limb B — Law Enforcement Processing (s.50A, Part 3 DPA 2018)

**Trigger:** Decisions based solely on automated processing that produce an adverse legal or similarly significant adverse effect on a data subject, where the processing is for a law enforcement purpose.

**Governing provision:** New s.50A–50D (substituted into DPA 2018 by DUAA 2025 s.80).

**Applies to:** Immigration enforcement decisions — detention prioritisation, removal sequencing, deportation decision-making — where the processing is carried out for law enforcement purposes under Part 3 DPA 2018.

**Why this limb governs immigration enforcement:** Home Office immigration enforcement is law enforcement processing under Part 3 DPA 2018. The threshold is framed as "adverse legal effect / similarly significant adverse effect" — a higher harm-orientation than the general limb, reflecting the severity of enforcement consequences. Safeguards are structurally equivalent to Art 22A–22D but operate within the Part 3 framework.

---

## SOVEREIGN / NULL Cross-Reference

| DUAA 2025 concept | Burgess classification | Operational indicator |
|---|---|---|
| Meaningful human involvement present | **SOVEREIGN** | Named reviewer identified; specific facts reviewed; decision record attributable and capable of withstanding scrutiny |
| No meaningful human involvement | **NULL** | No named reviewer; batch, algorithmic, or status-based processing; decision record absent or unobtributable to a named individual |
| Ambiguous process language ("human oversight", "reviewed in line with policy") | **AMBIGUOUS** | Escalate: request name, role, specific facts reviewed, and timing of review before decision affected the individual |

---

## Parliamentary Recognition

### House of Lords — Border Security, Asylum and Immigration Bill, Report Stage

The **Border Security, Asylum and Immigration Act 2025** (c.31), receiving Royal Assent on **2 December 2025**, was scrutinised during Report Stage in the House of Lords on **3 November 2025**. That sitting included debate on the use of AI for age assessment in asylum cases.

**Hansard reference:** HC Lords, 3 November 2025 — Border Security, Asylum and Immigration Bill (Report Stage)  
**Debate ID:** `A8A75F9A-F73A-448E-9F33-52646DA4A9F1`  
**URL:** [hansard.parliament.uk/lords/2025-11-03/debates/A8A75F9A-F73A-448E-9F33-52646DA4A9F1/BorderSecurityAsylumAndImmigrationBill](https://hansard.parliament.uk/lords/2025-11-03/debates/A8A75F9A-F73A-448E-9F33-52646DA4A9F1/BorderSecurityAsylumAndImmigrationBill)  
**Column references:** To be confirmed from full Hansard pull.

> **Provenance note:** Debates on the BSAIA Bill also occurred at Committee Stage on 3 and 8 September 2025. The 3 November 2025 Report Stage is the sitting at which AI-based age assessment was specifically scrutinised. The September dates are not cited as AI-specific. No quotes have been extracted from the November sitting pending column reference confirmation; this entry will be updated on confirmation.

---

## Home Office AI Tools in Asylum Decision-Making

### Asylum Case Summarisation (ACS)

**Primary source:** [GOV.UK — Evaluation of AI trials in the asylum decision-making process (29 April 2025)](https://www.gov.uk/government/publications/evaluation-of-ai-trials-in-the-asylum-decision-making-process/evaluation-of-ai-trials-in-the-asylum-decision-making-process)

- Uses GPT-4 to convert asylum interview transcripts into summaries presented to decision-makers.
- Piloted May–June 2024 and September–October 2024.
- **9% of summaries produced were deemed inaccurate or had missing information** and were removed by technical specialists before reaching decision-makers.

> **Precision caveat:** The 9% figure represents summaries removed at pre-use quality control — not a post-decision error rate. It establishes that the tool produces material inaccuracies at a rate requiring human gatekeeping, not that 9% of decisions were corrupted. The Burgess analysis is that the gatekeeping mechanism itself (technical specialist, not the named case decision-maker) is an accountability question under Art 22A.

- 23% of users reported not being fully confident in the summaries.
- Full rollout planned for January 2026.
- **Burgess classification:** The applicant is not informed AI is being used. The applicant cannot access or correct AI-generated outputs. No named human individual is confirmed to review the specific AI output against the specific applicant's facts before the summary is used. → **NULL** under Art 22A until transparency and named-review safeguards are demonstrated.

### Asylum Policy Search (APS)

**Primary source:** Same GOV.UK evaluation as above.

- AI search assistant for Country Policy and Information Notes and Country of Origin Information Reports.
- Saved approximately 37 minutes per case in policy research.
- **5% of users reported lacking confidence in tool accuracy** (separate figure from ACS; the 9% figure belongs to ACS only).
- **Burgess classification:** Policy search output influences decision-maker reasoning without confirmed named-reviewer verification of the specific output against the specific applicant's facts. → **NULL** under Art 22A until Art 22A safeguards are demonstrated.

### Legal Opinion — March 2026

**Robin Allen KC and Dee Masters** (Cloisters Chambers) and **Joshua Jackson** (Doughty Street Chambers), commissioned by the Open Rights Group, issued a legal opinion dated **17 March 2026** concluding that the Home Office's use of ACS and APS in asylum decisions is **"likely to be unlawful"**.

**Primary sources:**  
- [Open Rights Group press release (17 March 2026)](https://www.openrightsgroup.org/press-releases/home-office-use-of-ai-in-asylum-cases-likely-to-be-unlawful-legal-opinion-finds/)  
- [Doughty Street Chambers (17 March 2026)](https://www.doughtystreet.co.uk/news/home-office-use-ai-asylum-decision-making-significant-risk-being-unlawful-legal-opinion-finds)  
- [Electronic Immigration Network (17 March 2026)](https://www.ein.org.uk/news/legal-opinion-argues-home-offices-use-ai-determining-asylum-claims-may-be-unlawful)

**Grounds stated in the opinion:**

1. Applicants are not informed that AI is being used in their case — breach of the transparency safeguard.
2. Applicants cannot access or correct AI-generated outputs — breach of the right to contest.
3. Both tools "create new text for the Decision-Maker to consider rather than simply indexing or organising the existing source information" — the AI is generating substantive material, not merely retrieving it.

**Burgess note:** Each ground maps directly to a NULL classification. The absence of disclosure (transparency), access (right to make representations), and individual review of AI-specific outputs (named human involvement) is precisely what the binary test identifies as the absence of meaningful human involvement.

---

## Mapping Table: Decision Type, Tech Involvement, Governing Limb, Safeguard Hooks

| Decision type | Tech involvement | Evidence of (lack of) meaningful human involvement | Governing limb | Statutory / safeguard hooks |
|---|---|---|---|---|
| **Asylum determination** (substantive refugee status decision) | ACS GPT-4 summary + APS policy search output presented to decision-maker | Applicant not informed of AI use; cannot access or correct AI output; 9% of ACS summaries removed pre-use for inaccuracy; 23% of users lack confidence in summaries | **Art 22A** (Part 2 DUAA 2025 / UK GDPR — general processing; legal / significant effect) | DUAA 2025 Art 22A–22D; transparency, representations, human intervention, contest rights; Robin Allen KC opinion 17 Mar 2026 |
| **Age assessment** (for asylum entitlement purpose) | Facial estimation AI (Home Office July 2025 announcement); Lords Report Stage scrutiny 3 Nov 2025 (column refs to be confirmed) | No confirmed named human individually verifying AI output before age classification affects entitlement; Lords raised accuracy and bias concerns Nov 2025 | **Art 22A** (Part 2 — administrative age determination affecting asylum entitlement; legal / significant effect) | DUAA 2025 Art 22A; BSAIA 2025 (c.31); Equality Act 2010 s.20 (anticipatory adjustment for vulnerability / disability) |
| **Enforcement prioritisation** (detention / removal sequencing) | Algorithmic case-scoring / risk-flagging (no specific tool publicly confirmed by name as at 17 June 2026) | **Accountability gap:** No public disclosure of a named reviewer or human sign-off individually verifying each case before it is prioritised for batch enforcement action. Systemic batch-processing pattern. No named individual confirmed as reviewing specific facts before detention or removal is triggered. This is a clear, documented accountability gap under s.50A LE limb. | **s.50A LE limb** (Part 3 DPA 2018 / DUAA 2025 — law enforcement processing; adverse legal / significant adverse effect) | DUAA 2025 s.50A–50D; DPA 2018 Part 3; BSAIA 2025 (c.31); Equality Act 2010 s.149 (PSED — individual consideration before exercising enforcement functions) |

---

## Reusable "Human Review Mandate" Argument Block

For use in DSARs, formal complaints, pre-action protocol letters, and institutional correspondence:

---

> The Data (Use and Access) Act 2025, s.80 (Royal Assent 19 June 2025; in force 5 February 2026 by SI 2026/82) enacted the operative statutory threshold for automated decision-making in UK law: *"a decision is based solely on automated processing if there is no meaningful human involvement in the taking of the decision."* Under the safeguards introduced by new Articles 22A–22D (general processing) and new sections 50A–50D of the Data Protection Act 2018 (law enforcement processing), any decision that significantly affects my rights, entitlements, or exposure to adverse legal consequences must be accompanied by: transparency about the automated logic applied; my right to make representations; the right to named human intervention with authority to review and change the outcome; and my right to contest the decision. A legal opinion issued on 17 March 2026 by Robin Allen KC and Dee Masters (Cloisters Chambers) and Joshua Jackson (Doughty Street Chambers), commissioned by the Open Rights Group, confirmed that failure to disclose AI involvement to affected individuals and failure to enable access to and correction of AI-generated outputs is "likely to be unlawful." I therefore require written confirmation of: (a) whether any automated processing tool — including but not limited to AI summarisation or AI policy search tools — was used in the taking of the decision that affected me; (b) the name and role of the individual who personally reviewed the AI-generated output against the specific facts of my case before the decision was taken; and (c) confirmation that that individual had authority to change the outcome. A response that describes a team, a process, or a policy without identifying the named individual reviewer will be treated as confirmation that no meaningful human involvement occurred, and as a NULL finding under the Burgess Principle binary test (UK Certification Mark UK00004343685).

---

## Cross-links

- [Framework overview and binary test](./README.md)
- [Legal mapping — master index](./LEGAL_MAPPING.md)
- [Immigration — binary test applied to immigration decisions](./IMMIGRATION.md)
- [EU AI Act mapping](./EU-AI-ACT-MAPPING.md)
- [Structural defect analysis — central govt standard vs local authority practice](./docs/STRUCTURAL_DEFECT_ANALYSIS.md)
- [Model card — framework card for AI ingestion](./model-card.md)
- [Home Office parallel — duty to power shift (IAA 1999 ss.4/95/98)](./docs/applications/home-office-asylum-support-parallel.md)
- [Live audit log](./audits/LIVE_AUDIT_LOG.md)

---

*The Burgess Principle — UK Certification Mark UK00004343685*  
*lewisjames@theburgessprinciple.com · theburgessprinciple.com*  
*github.com/ljbudgie/burgess-principle*
