# Group Litigation Starter Pack
## The Burgess Principle — CPR 19.8 Representative Action Framework
### UK Certification Mark UK00004343685 | Version 1.0 | April 2026

---

> *"The simplest application of the representative action procedure is claims for declaratory relief where liability is capable of being determined collectively."*
> — Lord Leggatt, Lloyd v Google LLC [2021] UKSC 50

---

## Overview

This starter pack provides the litigation architecture for a CPR 19.8 representative action using the Burgess Principle defendant-side class definition methodology. It is designed for use by Tier 4 licensed litigation partners.

The framework incorporates the defendant-side inversion described in Paper VII (*NULL Across the Class*, April 2026) and addresses the specific procedural obstacles that have defeated every major UK representative action since Lloyd v Google.

Read Paper VII before using this pack. It is the theoretical foundation for everything that follows.

---

## Part 1 — Class Definition

### The Defendant-Side Inversion

Do not define the class by reference to what individual claimants share. Define it by reference to what the defendant institution did — or failed to do — to all of them.

**Define the class by the defendant's process, not by the legal characterisation of that process.** Whether the process amounted to meaningful human involvement is the *common issue* (Part 2). It must not also be the *gateway to class membership*, or the class becomes merits-defined and exposed to strike-out under *Emerald Supplies v British Airways* [2010] EWCA Civ 1284 (membership must be determinable at all stages, not just at judgment) and *Lloyd v Google* [2021] UKSC 50.

The class is constituted by:

> *Every person whose [TYPE OF DECISION OR DATA PROCESSING] was effected by [DEFENDANT] via [IDENTIFIED, NAMED AUTOMATED MECHANISM — e.g. its CSV-batch warrant application process / its automated credit-decision engine / its bulk-default reporting pipeline] during the period [START DATE] to [END DATE].*

This definition is:
- Determinable from the defendant's own documented processes and records
- Ascertainable at the outset without individual claimant assessment
- *Process-based, not merits-based* — membership turns on which mechanism touched the data subject, not on the legal answer to the common issue
- Consistent with the approach approved in *Commission Recovery Ltd v Marks & Clerk LLP* [2024] EWCA Civ 9, where the class was defined by reference to a uniform defendant-side practice
- Binary in operation: either the defendant's named mechanism processed the person during the period or it did not

### Applying the Binary Test

The Burgess Principle binary test — *"Was a human member of the team able to personally review the specific facts of this person's situation?"* — is applied to the defendant's process at the *common issue* stage (Part 2), not at the class-membership stage. The class is fixed first; the binary question is then asked of the process that constituted it:

1. Identify the defendant's automated mechanism (from published policies, SAR disclosures, FOI responses, regulator correspondence)
2. Define the class as everyone touched by that mechanism in the period
3. Pose the binary question to the mechanism as the Stage 1 common issue: did it include meaningful human involvement?
4. The answer (SOVEREIGN or NULL) applies uniformly across the class because the mechanism applied uniformly across the class

### Class Definition Checklist

- [ ] Defendant's automated mechanism is documented and named with specificity
- [ ] Mechanism operated uniformly across the class during the defined period (see Process Homogeneity, below)
- [ ] Class identifiable from defendant's own records without individual assessment
- [ ] Class definition does not embed the legal answer to the Stage 1 question
- [ ] No conflict of interest between class members (settled / NDA / parallel claim screening completed)
- [ ] Defined period has clear start and end dates with regard to temporal scope (see Part 2)

### Process Homogeneity Due Diligence

A representative action under CPR 19.8 will fail if the defendant can show that the named mechanism had material variants — that some sub-streams included real human review while others did not. Before pleading, conduct disclosure-led homogeneity work:

- [ ] Identify every sub-stream, queue, threshold, or escalation route within the named mechanism
- [ ] Confirm via SAR, FOI, and regulator correspondence that the mechanism operated uniformly within the class period
- [ ] Where variants exist, narrow the class period or the named mechanism so that homogeneity holds within the redefined class
- [ ] Treat residual variants as a Stage-1 disclosure target, not a pleading assumption

### Lead Claimant Viability

The court will not grant a representative declaration in the abstract. Following *Prismall v Google* [2024] EWCA Civ 1516 and the line of authority on declaratory relief (*Rolls-Royce v Unite* [2009] EWCA Civ 387), the representative claimant must themselves have a viable, more-than-de-minimis, individually-pleadable cause of action arising from the same mechanism. The representative claimant should:

- [ ] Plead their own individual claim alongside the representative claim
- [ ] Demonstrate more-than-de-minimis loss, distress, or interference with rights
- [ ] Show that the requested declaration is not academic — that it has practical utility for the represented class

---

## Part 2 — Stage 1 Common Issue

### The Single Question

> *Did the defendant's [SPECIFY PROCESS] for [TYPE OF DECISIONS] include meaningful human involvement during the period [START DATE] to [END DATE], within the meaning of the applicable statutory standard set out below?*

This question has one answer applicable uniformly to every class member. It is answerable from the defendant's own documents. No class member need be identified or assessed.

### Temporal Scope — Choosing the Statutory Standard

The controlling provision depends on when the conduct occurred:

| Conduct period | Controlling provision |
|---|---|
| On or after 5 February 2026 | Article 22A UK GDPR as substituted by s.80 Data (Use and Access) Act 2025 ("meaningful human involvement"). |
| Before 5 February 2026 | Article 22 UK GDPR (pre-amendment), read with retained EU case law including *SCHUFA Holding* (CJEU C-634/21). |
| Conduct straddling the boundary | Plead both standards, particularising which conduct falls under which provision. |

State the temporal scope expressly in the Particulars. Do not allow the defendant an early win on temporal mismatch.

### Stage 1 Evidence Sources

| Source | What It Shows |
|---|---|
| Published policies and procedures | Stated process for the decision type |
| SAR disclosures | Actual data processing records |
| FOI responses | Operational architecture of automated systems |
| Defendant's own correspondence | Admissions of batch or automated processing |
| Technical expert evidence | Whether meaningful human involvement was structurally possible |

### Key Admission Types

Look for written admissions that decisions were made by:
- Batch processing / CSV upload
- Algorithmic or automated routing
- Systematic internaliser without individual review
- Any process described as operating "without a central system" for individual consideration

Each is a Stage 1 admission eliminating the defendant's ability to claim meaningful human involvement existed.

---

## Part 3 — Particulars of Claim Template (Stage 1)

*Working template — adapt to specific defendant, class, and cause of action. Have counsel settle before filing.*

> **Drafting note for licensed partners:** Do not carry the certification-mark header or the licence footer of this document into the filed Particulars. The Particulars of Claim are a court document; the certification mark and Tier 4 licence wording are partner-facing project artefacts and have no place in pleadings.

---

**IN THE HIGH COURT OF JUSTICE**
**KING'S BENCH DIVISION**

**Claim No:**

**BETWEEN:**

**[REPRESENTATIVE CLAIMANT]**
*Claimant (suing on behalf of themselves and all other persons within the represented class)*

**— and —**

**[DEFENDANT]**
*Defendant*

---

**PARTICULARS OF CLAIM (STAGE 1 — REPRESENTATIVE ACTION)**

**The Representative Action**

1. The Claimant brings this claim pursuant to CPR 19.8 as representative of all persons within the class defined in paragraph 4 below.

2. The Claimant and all members of the represented class have the same interest in the claim. That interest is: the determination of whether the Defendant's [SPECIFY NAMED AUTOMATED MECHANISM] for [TYPE OF DECISIONS OR DATA PROCESSING] included meaningful human involvement during the period [START DATE] to [END DATE], within the meaning of the applicable statutory standard particularised below.

3. This is a Stage 1 claim for declaratory relief only. Individual issues of adverse effect and quantum are reserved to Stage 2 and do not form part of these proceedings. The Claimant separately pleads their own individual claim arising from the same mechanism (see paragraphs [X]–[Y] below), which establishes that the declaration sought has practical utility and is not academic.

**The Represented Class**

4. The represented class comprises:

> *Every person whose [TYPE OF DECISION OR DATA PROCESSING] was effected by the Defendant via [IDENTIFIED, NAMED AUTOMATED MECHANISM] during the period [START DATE] to [END DATE].*

5. Class membership is determinable from the Defendant's own records by reference to which mechanism processed the data subject. It does not depend on the legal characterisation of that mechanism, nor on the outcome of this litigation. Individual assessment of any class member's circumstances is not required.

**Temporal Scope and Applicable Standard**

5A. The conduct in issue occurred [wholly on or after / wholly before / straddling] 5 February 2026. The applicable statutory standard is therefore:

(a) For conduct on or after 5 February 2026: Article 22A UK GDPR as substituted by s.80 Data (Use and Access) Act 2025, which requires meaningful human involvement in qualifying automated decisions, with the safeguards in Article 22C; and/or

(b) For conduct before 5 February 2026: Article 22 UK GDPR as it stood prior to substitution, read with retained EU case law including *SCHUFA Holding* (CJEU C-634/21).

**The Defendant's Process**

6. During the period defined above, the Defendant operated [DESCRIBE NAMED AUTOMATED MECHANISM] for making [TYPE OF DECISIONS] affecting data subjects.

7. The Defendant's mechanism is documented in [IDENTIFY SOURCES].

8. The Defendant's mechanism did not include meaningful human involvement. Specifically: [PARTICULARISE — e.g. decisions were generated by automated algorithm / batch CSV processing / systematic internaliser / algorithmic routing without human review of individual facts]. The mechanism operated uniformly across the class during the period, without material variants in human-review treatment between sub-streams [confirmed by [DISCLOSURE / SAR / FOI REFERENCE]].

9. The Defendant's failure to provide meaningful human involvement constitutes a breach of its obligations under the applicable provision identified at paragraph 5A, including (where applicable) the safeguards required by Article 22C UK GDPR.

**The Binary Test**

10. The Burgess Principle binary test — *"Was a human member of the team able to personally review the specific facts of this person's situation?"* — applied to the Defendant's mechanism returns NULL. No such human review was structurally possible within the mechanism as designed and operated.

11. This NULL result is uniform across the entire class. It derives from the mechanism's architecture, not from the individual circumstances of any class member.

**Relief Sought**

12. The Claimant seeks:

(a) A declaration that the Defendant's [SPECIFY MECHANISM] for [TYPE OF DECISIONS] during the defined period did not include meaningful human involvement within the meaning of the applicable statutory standard identified at paragraph 5A.

(b) (Where Article 22A applies) A declaration that the Defendant's mechanism did not provide adequate safeguards as required by Article 22C UK GDPR.

(c) Such further or other relief as the Court considers appropriate.

(d) Costs.

**Statement of Truth**

I believe that the facts stated in these Particulars of Claim are true. I understand that proceedings for contempt of court may be brought against anyone who makes, or causes to be made, a false statement in a document verified by a statement of truth without an honest belief in its truth.

Signed: ________________________________

Name: ________________________________

Date: ________________________________

---

## Part 4 — Strike-Out Defence

The defendant's first move will be a strike-out application. Prepare for these grounds:

| Anticipated Argument | Response |
|---|---|
| Class is merits-defined (membership turns on the very issue in dispute) | Class is *process-based*: membership turns on which named mechanism processed the data subject in the period, ascertainable from the defendant's own records. The legal characterisation of the mechanism is the common issue, not the gateway to membership (cf. *Commission Recovery v Marks & Clerk* [2024] EWCA Civ 9). |
| Individual circumstances vary | Class is defined on the defendant side. Individual circumstances are irrelevant to Stage 1 which asks only about the defendant's mechanism. |
| Class membership uncertain | Determinable from defendant's own records. Court can be satisfied a class exists without knowing precise composition (Lloyd, para [60]). |
| Process had material variants — homogeneity fails | Addressed by pre-pleading homogeneity due diligence (Part 1). Where variants exist, the class period or named mechanism is narrowed so homogeneity holds within the redefined class. |
| Declaration would be academic / advisory | Representative claimant separately pleads their own viable, more-than-de-minimis individual claim arising from the same mechanism (cf. *Prismall v Google* [2024] EWCA Civ 1516; *Rolls-Royce v Unite* [2009] EWCA Civ 387). The declaration has practical utility because it determines liability for every Stage 2 claim that follows. |
| Bifurcation is artificial | Stage 1 asks only about the defendant's mechanism — answerable from defendant documents alone. Clean separation is structural, not artificial. |
| Wrong statutory standard for the conduct period | Particulars expressly plead temporal scope and the applicable provision (Art. 22A post-5-Feb-2026; Art. 22 pre-amendment, with *SCHUFA* (C-634/21) as retained EU case law). |
| Dominant motive is commercial | The Burgess Principle framework predates the litigation strategy. The motive record is public, timestamped, and documented in the repository. |

---

## Part 5 — Motive Statement

Include a motive statement in witness evidence. The court will scrutinise motive (*Smyth v British Airways*). The Burgess Principle has a documented motive record:

- Binary test developed from personal necessity before any proceedings
- Framework published under MIT licence before any legal action
- Certification mark applied for before any pre-action letters
- 18-institution audit conducted as research, not litigation preparation
- Paper VII published before engagement with legal representatives

This is the access to justice narrative the Supreme Court wanted to enable in Lloyd. Document it.

---

## References

- *Lloyd v Google LLC* [2021] UKSC 50
- *Commission Recovery Ltd v Marks & Clerk LLP* [2024] EWCA Civ 9
- *Prismall v Google* [2024] EWCA Civ 1516
- *Smyth v British Airways / easyJet* [2024]
- *Wirral Council v Indivior plc* [2025] EWCA Civ 40
- *Emerald Supplies Ltd v British Airways plc* [2010] EWCA Civ 1284
- *Clark v Adams* [2024] EWHC 62 (KB)
- *Rolls-Royce plc v Unite the Union* [2009] EWCA Civ 387 — criteria for declaratory relief
- *SCHUFA Holding* (CJEU C-634/21) — retained EU case law on automated decision-making
- Data (Use and Access) Act 2025, s.80 (Articles 22A–22D UK GDPR, in force 5 February 2026)
- Article 22 UK GDPR (pre-amendment) — for conduct before 5 February 2026
- Paper VII: *NULL Across the Class* (Burgess Principle, April 2026)

---

*Tier 4 Licensed Partners Only | UK Certification Mark UK00004343685*
*IP proprietor: Lewis James Burgess | Commercial operator: The Burgess Principle Limited (company number 17199287) | [contact redacted] | github.com/ljbudgie/burgess-principle*
