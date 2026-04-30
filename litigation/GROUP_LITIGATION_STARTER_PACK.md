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

The class is constituted by:

> *Every person whose personal data was processed by [DEFENDANT]'s [SPECIFY AUTOMATED PROCESS] during the period [START DATE] to [END DATE], in respect of which no meaningful human involvement in the decision-making process can be demonstrated by the defendant.*

This definition is:
- Determinable from the defendant's own documented processes
- Ascertainable at the outset without individual claimant assessment
- Consistent with the "general principle" in *Emerald Supplies v British Airways* [2010] EWCA Civ 1284 that membership must be determinable at all stages, not just at judgment
- Binary: either the defendant's process included meaningful human involvement or it did not

### Applying the Binary Test

The Burgess Principle binary test — *"Was a human member of the team able to personally review the specific facts of this person's situation?"* — applied to the defendant's process produces the class definition automatically:

1. Identify the defendant's automated process (from published policies, SAR disclosures, FOI responses)
2. Apply the binary test: did the process include meaningful human involvement?
3. If NULL — every person processed by that mechanism during the relevant period is in the class
4. The class definition is complete. No individual claimant assessment required.

### Class Definition Checklist

- [ ] Defendant's automated process is documented
- [ ] Process operated uniformly across the class during the defined period
- [ ] Binary test returns NULL for the process as a whole
- [ ] Class identifiable from defendant's own records without individual assessment
- [ ] No conflict of interest between class members
- [ ] Defined period has clear start and end dates

---

## Part 2 — Stage 1 Common Issue

### The Single Question

> *Did the defendant's [SPECIFY PROCESS] for [TYPE OF DECISIONS] include meaningful human involvement within the meaning of Article 22A of the UK GDPR (as substituted by s.80 Data (Use and Access) Act 2025, in force 5 February 2026) during the period [START DATE] to [END DATE]?*

This question has one answer applicable uniformly to every class member. It is answerable from the defendant's own documents. No class member need be identified or assessed.

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

2. The Claimant and all members of the represented class have the same interest in the claim. That interest is: the determination of whether the Defendant's [SPECIFY PROCESS] for [TYPE OF DECISIONS] included meaningful human involvement within the meaning of Article 22A of the UK GDPR during the period [START DATE] to [END DATE].

3. This is a Stage 1 claim for declaratory relief only. Individual issues of adverse effect and quantum are reserved to Stage 2 and do not form part of these proceedings.

**The Represented Class**

4. The represented class comprises:

> *Every person whose personal data was processed by the Defendant in connection with [TYPE OF DECISION] during the period [START DATE] to [END DATE], in circumstances where the Defendant's process did not include meaningful human involvement in the decision, within the meaning of Article 22A(1)(a) UK GDPR.*

5. Class membership is determinable from the Defendant's own records and does not depend on the outcome of this litigation. Individual assessment of any class member's circumstances is not required.

**The Defendant's Process**

6. During the period defined above, the Defendant operated [DESCRIBE AUTOMATED PROCESS] for making [TYPE OF DECISIONS] affecting data subjects.

7. The Defendant's process is documented in [IDENTIFY SOURCES].

8. The Defendant's process did not include meaningful human involvement within the meaning of Article 22A(1)(a) UK GDPR. Specifically: [PARTICULARISE — e.g. decisions were generated by automated algorithm / batch CSV processing / systematic internaliser / algorithmic routing without human review of individual facts].

9. The Defendant's failure to provide meaningful human involvement constitutes a breach of its obligations under Article 22C UK GDPR, which requires safeguards enabling data subjects to obtain human intervention and contest decisions.

**The Binary Test**

10. The Burgess Principle binary test — *"Was a human member of the team able to personally review the specific facts of this person's situation?"* — applied to the Defendant's process returns NULL. No such human review was structurally possible within the process as designed and operated.

11. This NULL result is uniform across the entire class. It derives from the Defendant's process architecture, not from the individual circumstances of any class member.

**Relief Sought**

12. The Claimant seeks:

(a) A declaration that the Defendant's [SPECIFY PROCESS] for [TYPE OF DECISIONS] during the defined period did not include meaningful human involvement within the meaning of Article 22A(1)(a) UK GDPR.

(b) A declaration that the Defendant's process did not provide adequate safeguards as required by Article 22C UK GDPR.

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
| Individual circumstances vary | Class is defined on the defendant side. Individual circumstances are irrelevant to Stage 1 which asks only about the defendant's process. |
| Class membership uncertain | Determinable from defendant's own records. Court can be satisfied a class exists without knowing precise composition (Lloyd, para [60]). |
| Bifurcation is artificial | Stage 1 asks only about the defendant's process — answerable from defendant documents alone. Clean separation is structural, not artificial. |
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
- Data (Use and Access) Act 2025, s.80 (Articles 22A–22D UK GDPR)
- Paper VII: *NULL Across the Class* (Burgess Principle, April 2026)

---

*Tier 4 Licensed Partners Only | UK Certification Mark UK00004343685*
*Lewis James Burgess | lewisjames@theburgessprinciple.com | github.com/ljbudgie/burgess-principle*
