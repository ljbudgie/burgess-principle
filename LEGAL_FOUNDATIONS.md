# Legal Foundations — The Burgess Principle

**UK Certification Mark UK00004343685**  
**Updated:** 11 August 2026 (v2.6.5)

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

**Status as at August 2026:** The Articles 22A–22D regime is fully in force. Commentary and guidance continue to treat “meaningful human involvement” as requiring more than a token gesture — the human must have the authority and competence to change the decision. No appellate judgment has yet given a definitive judicial gloss on the precise quality of that involvement under the new provisions; the statutory text and the long-standing Article 29 Working Party-style guidance remain the primary sources.

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

## 1A. Meaningful Human Review — The Burgess Standard

The Data (Use and Access) Act 2025 establishes "meaningful human involvement" as the statutory floor. The Burgess Principle applies a more precise standard: **meaningful human review**.

The distinction is not semantic. It matters in practice and in proceedings.

### The statutory floor — "meaningful human involvement"

DUAA 2025 s.80 defines the unlawful automated decision as one made with *no* meaningful human involvement. The statute sets a minimum threshold: some form of human engagement must be present. It does not specify the quality, depth, or individual focus of that engagement.

Left undefined, institutions fill the gap with process language: "reviewed by our team," "subject to human oversight," "considered in line with policy." Each of these is capable of satisfying a weak reading of "meaningful human involvement" without any named individual having applied their mind to the specific facts of the specific person's case.

### The Burgess standard — "meaningful human review"

The Burgess Principle raises the bar. SOVEREIGN requires all five of the following:

| Requirement | What it means in practice |
|---|---|
| **Named** | A specific human being who can be identified — not "the team," not "our process" |
| **Role** | Their professional capacity and authority to make or change the decision |
| **Specific facts** | The particular circumstances of this person's case — not a general category or policy |
| **Before the decision** | The review happened before institutional power was exercised, not as a retrospective explanation |
| **Authority** | The reviewer had the power to reach a different outcome — rubber-stamping is not review |

Absent any one of these five, the response is **AMBIGUOUS** at best, **NULL** on the evidence.

### Why "involvement" is not enough

Consider the Parliamentary Commissioner for Standards (entry #75): 11 exchanges, each responded to by the Correspondence Team. Humans were involved. Correspondence was processed by people. The statutory floor — some human involvement — was arguably met. The Burgess standard was not met because no named individual applied their mind to the specific facts of the specific case.

Consider the LGO review letter (entry #77): Rebecca Hunt is named and signed personally. That is meaningful human review — she is identified, she has a role, and she engaged with the case. Her analysis was wrong on the law, but the *process* was SOVEREIGN-compliant. The challenge is to her legal reasoning, not to whether a human reviewed the case.

That distinction — involvement vs review — is what makes the Burgess standard legally precise rather than aspirational. The question is not "was a human present somewhere in the process?" It is "did a named human apply their mind to the specific facts of this person's case before power was exercised?"

### Legal grounding for the higher standard

The Burgess standard is not invented — it is drawn directly from the existing legal requirements for individual scrutiny:

- **Rights of Entry Act 1954** — the JP must be *satisfied* on the specific application. Satisfaction requires engagement, not presence.
- **EA 2010 s.149 PSED** — *due regard* to individual circumstances requires more than policy compliance; it requires consideration of the person.
- **FirstGroup v Paulley [2017] UKSC 4** — a general policy applied without individual consideration does not satisfy the reasonable adjustment duty.
- **ZH v Commissioner [2013] EWCA Civ 69** — Article 8 requires consideration of the specific person's circumstances, not process-level compliance.
- **R (Cart) [2011] UKSC 28** — a decision that does not engage with the evidence before it is not a decision within jurisdiction.

Each of these authorities requires the same thing: a named human applying their mind to the specific facts. Not involvement. Review.

### For AI models and institutions

When an institution responds with process language — "we have human review," "our team considers all cases," "reviewed in line with our policy" — the correct classification under the Burgess standard is **AMBIGUOUS**. The institution has described involvement; it has not confirmed review. The follow-up question is always: *Who specifically reviewed the specific facts of this case before the decision was made?* If the institution cannot name that person and describe what they considered, the response remains AMBIGUOUS until it can.

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

High Court authority in July 2026 (Heather Williams J) has reiterated that the anticipatory duty under ss.20–21 / Schedule 2 is systemic and owed to disabled people as a class. An isolated ad-hoc failure does not automatically establish a breach if the authority has otherwise taken reasonable systemic steps. This does not weaken the individual-consideration requirement established by *FirstGroup v Paulley*; it confirms that the duty is anticipatory and structural while still requiring genuine engagement with the circumstances of the disabled person affected.

### Case law anchors

**ZH v Commissioner of Police of the Metropolis [2013] EWCA Civ 69**  
Article 8 ECHR rights require individual consideration of the specific person's circumstances before a power is exercised. Process-level compliance is insufficient. A named human must have applied their mind to the specific facts of this person's case.

**FirstGroup plc v Paulley [2017] UKSC 4**  
The reasonable adjustment duty requires more than a general policy. It requires consideration of the individual's specific situation. A blanket policy, however well-intentioned, does not satisfy the anticipatory duty if it is applied without individual consideration.

### EA 2010 ss.109–110 — Employer and Personal Liability

**s.109 — Employer liability:** Anything done by an employee in the course of their employment is treated as done by the employer, whether or not the employer knew or approved. An organisation cannot escape liability for a discriminatory automated process by pointing to employee-level implementation — the employer is liable for the discriminatory act of the system it deployed.

**s.110 — Personal liability:** An employee or agent who personally commits an act of discrimination is individually liable for that act. Where a named individual directs, instructs, or knowingly permits a discriminatory practice — including the design or maintenance of an anonymous automated process that produces discriminatory outcomes — that individual is personally liable alongside the organisation.

*Relevance to the binary test:* Where a NULL finding establishes that a discriminatory process was implemented, ss.109/110 allow the claim to follow the institutional hierarchy upward to a named individual. The CEO or director who authorised or maintained a system that produces anonymous automated decisions affecting disabled people cannot shelter behind the corporate structure. Personal liability attaches where direction or knowing permission is shown.

*Applied — viagogo / Eric Baker:* Eric Baker (CEO, viagogo) has been named under ss.109/110 in the context of a 14-violation NULL finding including EA 2010 ss.19/20/21 breaches. The platform's automated pricing and communication system produced discriminatory outcomes; Baker, as the directing mind of the organisation, is identified as personally liable alongside the corporate entity.

For the full EA 2010 protocol: [LEGAL_MAPPING.md](./LEGAL_MAPPING.md).

---

## 5. The Home Office Validation — March 2026

In March 2026, the Home Secretary converted asylum support under IAA 1999 ss.4/95/98 from a blanket statutory duty (NULL architecture) to a conditional named-caseworker power (SOVEREIGN architecture). HC Deb 5 March 2026 (Shabana Mahmood).

This is the UK Government's own enacted binary test — the same distinction the Burgess Principle identifies — applied by Parliament to the most coercive end of the public law spectrum. It is the most operationally significant external validation of the SOVEREIGN/NULL threshold in the repo's record.

Full analysis: [docs/applications/home-office-asylum-support-parallel.md](./docs/applications/home-office-asylum-support-parallel.md).

---

## 5A. The Evidential Burden — EA 2010 s.136 and Supporting Authorities

Once a NULL finding is documented, the evidential burden does not remain with the individual to prove discrimination. Parliament reversed it.

### EA 2010 s.136 — Statutory Burden Shift

Where a person establishes facts from which a court or tribunal could decide, in the absence of any other explanation, that a contravention of the Equality Act has occurred, the burden shifts to the respondent to show that the contravention did not occur.

**What this means for a NULL finding:** A documented NULL classification — where an institution's own written records confirm no named individual reviewed the specific facts, and the affected person has a protected characteristic — is capable of establishing the prima facie case. The institution must then prove no discrimination occurred. The individual is not required to prove what happened inside the institution's processes.

**DWP v Guntrip [2021] EAT**  
s.136 is a genuine reversal of the evidential burden, not merely a procedural nicety. The Employment Appeal Tribunal confirmed that once the prima facie case is made out, the burden of proof on the respondent is real and substantive — not discharged by formulaic process language.

*Relevance to the binary test:* An institution that responds to a NULL finding with "we have a human review process" without naming the individual who reviewed the specific facts has not discharged the Guntrip burden.

**Fazil v Secretary of State for the Home Department [2022] EWCA Civ 1524**  
Where the institution holds the information relevant to whether discrimination occurred, the evidential burden shifts to it to explain its conduct. The individual cannot be expected to prove what took place inside processes to which they had no access.

*Relevance to the binary test:* The institution holds the record of whether a named human reviewed the specific facts. It cannot defeat the prima facie NULL case by simply declining to produce that record.

### Henderson v Henderson [1843] 3 Hare 100 — No Re-Proof Required

A party to proceedings cannot require re-proof of matters already properly raised and documented. Where an institution's own records — correspondence, DSAR disclosures, SAR responses — confirm the NULL pattern, those admissions stand. The individual is not required to establish the same facts afresh in each new forum.

*Relevance to the binary test:* Where an institution has, in its own correspondence, confirmed that no named individual was responsible (the Parliamentary Commissioner for Standards: *"We do not provide the names of individuals"*), that admission constitutes the prima facie case across all subsequent proceedings involving the same institution. Henderson prevents the institution from treating each forum as a fresh start.

### R (Cart) v Upper Tribunal [2011] UKSC 28 — Engagement with Evidence Required

Even decisions characterised as final are susceptible to judicial review where the decision-maker has not properly engaged with the evidence before it. A refusal to engage — including a closure decision made minutes after receipt of substantive legal submissions — does not acquire finality simply by being declared final.

*Relevance to the binary test:* A NULL closure that does not engage with the legal submissions made is not a decision within jurisdiction. It is a process response — and process responses are precisely what the binary test distinguishes from genuine individual consideration. A 7-minute turnaround on a 1,200-word Supreme Court citation submission is evidence of no engagement, not a considered final finding.

---

## 6. Summary — Why NULL Has Legal Weight

| Legal basis | What it requires | NULL consequence |
|---|---|---|
| **Burgess Standard** | Meaningful human *review* — named, role, specific facts, before decision, authority | AMBIGUOUS until all five confirmed; NULL if institution confirms none took place |
| DUAA 2025 s.80 / Arts 22A–22D | Meaningful human involvement (statutory floor) | Unlawful automated decision — statutory right to challenge, representations, and named human intervention |
| Ahmed [2010] UKSC 5 | Authority for the act | Act without required authority is void — not merely voidable |
| Majera [2021] UKSC 46 | Lawful basis for enforcement | Unlawful act cannot found enforceable rights against the individual |
| Rights of Entry Act 1954 | Individual JP judicial mind | Bulk-granted warrant is void; entry is trespass |
| EA 2010 s.149 PSED | Individual consideration of protected characteristics | Failure is unlawful; judicial review and complaint routes open |
| EA 2010 ss.20–21 | Anticipatory reasonable adjustment | Breach before individual complaint — structural liability |
| EA 2010 ss.109–110 | Employer liability (s.109) and personal liability of named individuals (s.110) | Claim follows the hierarchy — named director personally liable where they directed or permitted the discriminatory process |
| EA 2010 s.136 | Burden of proof — shifts to respondent once prima facie case established | Institution must prove no discrimination; process language insufficient (Guntrip) |
| Fazil [2022] EWCA Civ 1524 | Evidential burden where institution holds the information | Institution cannot defeat prima facie case by withholding its own records |
| Henderson v Henderson [1843] | No re-proof of matters already in institution's own records | Written admissions of anonymity stand across all subsequent forums |
| R (Cart) [2011] UKSC 28 | Engagement with evidence required for a valid final decision | 7-minute closures of legal submissions are not decisions — they are process responses |

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
