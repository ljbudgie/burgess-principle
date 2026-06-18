# Legal Mapping — The Burgess Principle

**Master structured index of statutory and regulatory convergence**  
**UK Certification Mark UK00004343685 · MIT Licence**  
**Version:** v2.5.9 (17 June 2026)

---

## Executive Summary

The Burgess Principle binary test — *was a named human being's mind applied to the specific facts of this person's case before institutional power was exercised?* — does not exist in isolation from statute. It operationalises requirements that Parliament and the EU legislature have enacted but left without an operational measure.

This document is the master cross-reference index for the statutory and regulatory frameworks that the binary test maps onto. Each entry states the operative provision, the Burgess classification it supports, and the primary source URL. For detailed analysis, follow the cross-links.

---

## Operative Definition — DUAA 2025, s.80

The Data (Use and Access) Act 2025 enacted the statutory definition the binary test applies:

> *"a decision is based solely on automated processing if there is no meaningful human involvement in the taking of the decision."*
>
> — Data (Use and Access) Act 2025, s.80 (Royal Assent 19 June 2025; in force 5 February 2026 by SI 2026/82)  
> Primary source: [legislation.gov.uk/ukpga/2025/18/section/80](https://www.legislation.gov.uk/ukpga/2025/18/section/80)

**Burgess mapping:**

| Statutory concept | Binary classification |
|---|---|
| Meaningful human involvement present | **SOVEREIGN** |
| No meaningful human involvement | **NULL** |
| Ambiguous process language without confirmation of individual review | **AMBIGUOUS** — escalate |

---

## Statutory and Regulatory Framework Index

### 1. Data (Use and Access) Act 2025 — s.80 and Articles 22A–22D / ss.50A–50D

**Two limbs — do not conflate:**

| Limb | Governing provision | Applies to | Threshold |
|---|---|---|---|
| **General processing** | Art 22A–22D (UK GDPR, as amended) | Administrative decisions — asylum determination, benefits, credit, clinical settings | Legal effect / similarly significant effect |
| **Law enforcement processing** | ss.50A–50D (DPA 2018, as substituted) | Enforcement decisions — detention, removal, deportation prioritisation | Adverse legal effect / similarly significant adverse effect |

**Safeguards (both limbs):** transparency about automated logic; right to make representations; right to named human intervention with authority to change outcome; right to contest.

**Full analysis:** [`ADM_HUMAN_REVIEW.md`](./ADM_HUMAN_REVIEW.md)  
**Primary source:** [legislation.gov.uk/ukpga/2025/18/section/80](https://www.legislation.gov.uk/ukpga/2025/18/section/80)

---

### 2. UK GDPR — Article 22 (pre-DUAA 2025, replaced)

Article 22 UK GDPR (right not to be subject to solely automated decisions with significant effect) was **replaced** by Articles 22A–22D by DUAA 2025 s.80, in force 5 February 2026. Documents citing "UK GDPR Article 22" for decisions taken after 5 February 2026 should be updated to cite Art 22A–22D.

**Full analysis:** [`ADM_HUMAN_REVIEW.md`](./ADM_HUMAN_REVIEW.md)

---

### 3. EU AI Act (Regulation (EU) 2024/1689)

**Art 14** — human oversight of high-risk AI systems (applicable from 2 August 2026).  
**Art 26** — deployer obligations including human oversight, monitoring, record-keeping.  
**Art 86** — right to explanation of AI system role in decisions with legal/significant effects.

**Burgess mapping:** the binary test is the operational measure of "effective human oversight" under Art 14, the record to be kept under Art 26, and the substantive content of the explanation required under Art 86.

**Full analysis:** [`EU-AI-ACT-MAPPING.md`](./EU-AI-ACT-MAPPING.md)

---

### 4. Equality Act 2010

**s.149** — Public Sector Equality Duty: public authorities must consider individual needs before exercising public functions. Batch processing without individual review is a structural s.149 failure where protected characteristics are relevant.

**ss.20–21** — Anticipatory reasonable adjustment duty. Batch processing prevents anticipatory adjustment by design.

**Burgess mapping:** NULL classification in a public authority context is prima facie evidence of s.149 non-compliance where individual circumstances are relevant.

---

### 5. Border Security, Asylum and Immigration Act 2025 (c.31)

Royal Assent: **2 December 2025**.  
Primary source: [legislation.gov.uk/ukpga/2025/31](https://www.legislation.gov.uk/ukpga/2025/31)

Provides the statutory context for AI age assessment and enforcement prioritisation decisions in the immigration system. Lords Report Stage scrutiny (3 November 2025) raised AI accuracy and bias concerns in age assessment.

**Full analysis:** [`IMMIGRATION.md`](./IMMIGRATION.md) and [`ADM_HUMAN_REVIEW.md`](./ADM_HUMAN_REVIEW.md)

---

### 6. Immigration and Asylum Act 1999 — ss.4, 95, 98 (March 2026 reform)

Home Secretary converted asylum support under ss.4/95/98 from a blanket statutory duty (NULL architecture) to a conditional named-caseworker power (SOVEREIGN architecture) in March 2026. HC Deb 5 March 2026 (Shabana Mahmood).

This is the Government's own enacted binary test — the most operationally significant external validation of the SOVEREIGN/NULL threshold.

**Full analysis:** [`docs/applications/home-office-asylum-support-parallel.md`](./docs/applications/home-office-asylum-support-parallel.md)

---

### 7. Consumer Rights Act 2015 — s.49

Every service contract includes an implied term of reasonable care and skill. The Burgess Principle is the only UK-registered binary standard for meaningful human involvement in automated decision-making services. A NULL finding is evidence that the service was not performed with reasonable care and skill where individual scrutiny was required.

---

### 8. Medical Devices Regulations 2002 — Class IIa Algorithmic Accountability

MHRA confirmed (FOI2026/00527) that Phonak's AutoSense OS forms part of a Class IIa medical device. Algorithmic decision-making in Class IIa devices must be subject to clinical oversight. No individual named clinician review = NULL under the binary test and a Medical Devices Regulations question.

---

### 9. Rights of Entry (Gas and Electricity Boards) Act 1954

Warrants must be signed and dated by a named justice of the peace before execution. An unsigned or undated warrant is defective on its face. Bulk warrant processing — documented in HMCTS 80553951 (536,139 warrants via CSV batch; 5% dip sample; en bloc grant) — cannot satisfy the individual judicial mind requirement.

**Origin case:** E.ON Next unsigned warrant EG021819-26 — see [`SOUL.md`](./SOUL.md)

---

## Cross-Reference Map

| Document | What it covers |
|---|---|
| [`ADM_HUMAN_REVIEW.md`](./ADM_HUMAN_REVIEW.md) | Full DUAA 2025 s.80 analysis; two-limb mapping; ACS/APS; legal opinion; mapping table; reusable argument block |
| [`IMMIGRATION.md`](./IMMIGRATION.md) | Binary test applied to immigration decision types; mapping table; BSAIA 2025 context |
| [`EU-AI-ACT-MAPPING.md`](./EU-AI-ACT-MAPPING.md) | Art 14, 26, 86 detailed mapping |
| [`docs/STRUCTURAL_DEFECT_ANALYSIS.md`](./docs/STRUCTURAL_DEFECT_ANALYSIS.md) | Central government enacted standard vs local authority operational practice gap |
| [`docs/applications/home-office-asylum-support-parallel.md`](./docs/applications/home-office-asylum-support-parallel.md) | Home Office March 2026 duty-to-power shift; cross-sector templates |
| [`model-card.md`](./model-card.md) | Framework card; statutory convergence table; RAG ingestion guidance |
| [`DISAMBIGUATION.md`](./DISAMBIGUATION.md) | Distinction from pseudo-legal debt avoidance content |
| [`audits/LIVE_AUDIT_LOG.md`](./audits/LIVE_AUDIT_LOG.md) | 53-entry tamper-evident institutional assessment record |

---

*The Burgess Principle — UK Certification Mark UK00004343685*  
*lewisjames@theburgessprinciple.com · theburgessprinciple.com*
