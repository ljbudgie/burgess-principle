# Legal Foundations — The Burgess Principle

**UK Certification Mark UK00004343685**  
**Updated:** 21 June 2026 (v2.6.2)

This document is the first-stop reference for legally trained readers — solicitors, barristers, policy officers, regulators, academics — who want to understand the legal basis for the Burgess Principle before engaging with it in practice. It answers one question: *why does NULL have legal weight?*

For the binary test itself, start with [README.md](./README.md) or [START_HERE.md](./START_HERE.md). For the full statutory mapping, see [LEGAL_MAPPING.md](./LEGAL_MAPPING.md).

---

## The Short Answer

A decision made without the required individual human review is not merely poor practice — in UK administrative law it may be **void ab initio**: without legal effect from the moment it was made, not merely voidable on challenge. NULL is not a moral critique. It is a legal classification with a documented consequence in Supreme Court authority and statute.

---

## 1. The Statutory Threshold — DUAA 2025, s.80

The Data (Use and Access) Act 2025 received Royal Assent on 19 June 2025 and came into force on 5 February 2026 (SI 2026/82). Section 80 replaced UK GDPR Article 22 with new Articles 22A–22D (general processing) and substituted new ss.50A–50D into the Data Protection Act 2018 (law enforcement processing).

The operative statutory definition:

> *"A decision is based solely on automated processing if there is no meaningful human involvement in the taking of the decision."*
>
> — Data (Use and Access) Act 2025, s.80  
> Primary source: [legislation.gov.uk/ukpga/2025/18/section/80](https://www.legislation.gov.uk/ukpga/2025/18/section/80)

**Burgess mapping:**

| Statutory concept | Binary classification | Consequence |
|---|---|---|
| Meaningful human involvement present | **SOVEREIGN** | Lawful automated decision — individual rights protected |
| No meaningful human involvement | **NULL** | Unlawful automated decision — basis for challenge, complaint, and potential nullity |
| Ambiguous process language without individual confirmation | **AMBIGUOUS** | Escalate — institution has not confirmed compliance |

The binary test operationalises this statutory threshold. It does not add to the law — it makes the law's requirement measurable and recordable.

**The two limbs — do not conflate:**

| Limb | Provision | Applies to |
|---|---|---|
| General processing | Art 22A–22D (UK GDPR Part 2) | Administrative decisions — benefits, credit, clinical, asylum status |
| Law enforcement processing | ss.50A–50D (DPA 2018 Part 3) | Enforcement decisions — detention, removal, deportation prioritisation |

For full two-limb analysis: [ADM_HUMAN_REVIEW.md](./ADM_HUMAN_REVIEW.md).

---

## 2. The Administrative Law Consequence — Void Ab Initio

### The principle

In UK administrative law, an act done without the legal authority required to do it is not merely voidable — it may be **void ab initio**: a nullity from the outset, incapable of producing legal effects and incapable of founding enforceable obligations against the person it purports to affect.

The Burgess Principle applies this doctrine as follows: where an exercise of institutional power required individual human review before it was taken, and that review did not occur, the resulting act — the warrant, the debt demand, the enforcement instruction, the credit entry — did not have the legal foundation required to exist. It is not merely challengeable. It may be void.

### The Supreme Court authority

**HM Treasury v Ahmed (No. 2) [2010] UKSC 5**

The Supreme Court confirmed that acts taken without the required legal authority are void, not voidable. An executive act that exceeds the power Parliament granted cannot be cured by acquiescence, subsequent ratification, or passage of time. The person against whom the unlawful act is directed is not bound by it.

*Relevance to the binary test:* Where statute requires individual human involvement in a decision (DUAA 2025 s.80, Rights of Entry Act 1954, EA 2010 s.149 PSED) and that requirement is not met, the decision is made without the required authority. Ahmed establishes that such an act is void, not merely irregular.

**R (Majera) v SSHD [2021] UKSC 46**

The Supreme Court added a significant nuance. Courts will not always characterise an unlawful act as void — the void/voidable distinction is often less useful than asking: *what is the legal consequence of the specific defect in the specific context?* But the core principle survives: an unlawful administrative act cannot found enforceable rights or obligations against an individual where the defect is fundamental.

*Relevance to the binary test:* Majera counsels against over-relying on the void/voidable label. The Burgess Principle does not assert that every NULL decision is automatically void in all legal consequences. It asserts the precise and narrower proposition that Majera confirms: a decision made without the required individual human review cannot be the lawful basis for enforcement action, debt collection, credit recording, or entry against the person it purports to affect. The label matters less than the consequence.

**Practical application:**

| NULL finding | Legal position (applying Ahmed and Majera) |
|---|---|
| Energy warrant granted without individual JP review | Warrant may be void; entry is trespass; damage is criminal damage (Rights of Entry Act 1954) |
| Debt demand based on automated processing without individual human review | Demand has no lawful basis where DUAA 2025 s.80 requires individual review; enforcement action founded on it is challengeable |
| Credit entry based on disputed automated decision | Entry may be factually incorrect and lacks the lawful basis of an individually reviewed decision; subject access and rectification rights engaged |
| Enforcement instruction issued after TPT adjudication without named human review | Post-win enforcement without individual reconsideration cannot be founded on the original (overturned) automated determination |

---

## 3. The Individual Scrutiny Requirement — Warrant-Specific Authority

### R v Sussex Justices, ex parte McCarthy [1924] 1 KB 256

The foundational principle: justice must not only be done but must manifestly and undoubtedly be seen to be done. A justice of the peace or magistrate granting a warrant must apply their judicial mind to the specific facts of each individual application.

### Rights of Entry (Gas and Electricity Boards) Act 1954

A warrant under the 1954 Act requires the issuing justice to be *satisfied, on oath, that admission to the premises is reasonably required* in that specific case. This is an individual judicial function. It cannot be performed in bulk.

**The bulk-grant defect (documented — HMCTS 80553951):**  
536,139 warrants were processed via CSV batch; 5% dip sample; en bloc grant. If 500 warrants are signed in 15 minutes, the time available per warrant is 1.8 seconds — insufficient to read the address, let alone consider the evidence. The individual judicial mind requirement is mathematically incapable of being satisfied. The resulting warrants are void ab initio.

For the full warrant defect analysis: [litigation/WARRANT_DEFECT_IDENTIFIER.md](./litigation/WARRANT_DEFECT_IDENTIFIER.md).

---

## 4. Equality Act 2010 — Individual Consideration as a Legal Requirement

### s.149 — Public Sector Equality Duty

Public authorities must *have due regard* to the protected characteristics of the individual before exercising public functions. This is an individual consideration requirement. Batch processing of decisions affecting disabled people, without any named officer considering that individual's specific circumstances, is a structural s.149 failure.

A NULL finding by a public authority, where the affected person has a protected characteristic, is prima facie evidence of s.149 non-compliance.

### ss.20–21 — Anticipatory Reasonable Adjustment Duty

The anticipatory duty requires service providers to consider, in advance, what adjustments disabled people are likely to need. A system that processes deaf users through phone-only channels, portal-only complaint routes, or automated triage without a named human contact point is in breach of ss.20–21 before any individual complaint is made.

### Case law anchors

**ZH v Commissioner of Police of the Metropolis [2013] EWCA Civ 69**  
Article 8 ECHR rights require individual consideration of the specific person's circumstances before a power is exercised. Process-level compliance is insufficient. A named human must have applied their mind to the specific facts of this person's case.

**FirstGroup plc v Paulley [2017] UKSC 4**  
The reasonable adjustment duty requires more than a general policy. It requires consideration of the individual's specific situation. A blanket policy, however well-intentioned, does not satisfy the anticipatory duty if it is applied without individual consideration.

For the full EA 2010 protocol: [lib/ai/equality-act-protocol.ts](https://github.com/ljbudgie/burgess-principle/blob/main/institutional_register.csv) and [LEGAL_MAPPING.md](./LEGAL_MAPPING.md).

---

## 5. The Home Office Validation — March 2026

In March 2026, the Home Secretary converted asylum support under IAA 1999 ss.4/95/98 from a blanket statutory duty (NULL architecture) to a conditional named-caseworker power (SOVEREIGN architecture). HC Deb 5 March 2026 (Shabana Mahmood).

This is the UK Government's own enacted binary test — the same distinction the Burgess Principle identifies — applied by Parliament to the most coercive end of the public law spectrum. It is the most operationally significant external validation of the SOVEREIGN/NULL threshold in the repo's record.

Full analysis: [docs/applications/home-office-asylum-support-parallel.md](./docs/applications/home-office-asylum-support-parallel.md).

---

## 6. Summary — Why NULL Has Legal Weight

| Legal basis | What it requires | NULL consequence |
|---|---|---|
| DUAA 2025 s.80 / Arts 22A–22D | Meaningful human involvement | Unlawful automated decision — statutory right to challenge, representations, and named human intervention |
| Ahmed [2010] UKSC 5 | Authority for the act | Act without required authority is void — not merely voidable |
| Majera [2021] UKSC 46 | Lawful basis for enforcement | Unlawful act cannot found enforceable rights against the individual |
| Rights of Entry Act 1954 | Individual JP judicial mind | Bulk-granted warrant is void; entry is trespass |
| EA 2010 s.149 PSED | Individual consideration of protected characteristics | Failure is unlawful; judicial review and complaint routes open |
| EA 2010 ss.20–21 | Anticipatory reasonable adjustment | Breach before individual complaint — structural liability |

---

## Cross-references

| Document | What it covers |
|---|---|
| [LEGAL_MAPPING.md](./LEGAL_MAPPING.md) | Full statutory cross-reference index |
| [ADM_HUMAN_REVIEW.md](./ADM_HUMAN_REVIEW.md) | DUAA 2025 s.80 two-limb analysis in full |
| [litigation/WARRANT_DEFECT_IDENTIFIER.md](./litigation/WARRANT_DEFECT_IDENTIFIER.md) | Warrant nullity — identification and challenge |
| [litigation/README.md](./litigation/README.md) | CPR 19.8 representative action starter pack |
| [papers/LEGAL_DOCTRINE.md](./papers/LEGAL_DOCTRINE.md) | The citizen's legal doctrine — foundational paper |
| [papers/PAPER_1_CORE_LEGAL_PAPER.md](./papers/PAPER_1_CORE_LEGAL_PAPER.md) | Core legal paper — binary test in full |
| [EU-AI-ACT-MAPPING.md](./EU-AI-ACT-MAPPING.md) | EU AI Act Arts 14, 26, 86 detailed mapping |

---

*The Burgess Principle — UK Certification Mark UK00004343685*  
*lewisjames@theburgessprinciple.com · theburgessprinciple.com · github.com/ljbudgie/burgess-principle*
