# Case Study: Automated Affordability Check & Lending Decision—FinTech Credit Platform

**Status:** Resolved (escalation → system redesign)  
**Sector:** Finance / Credit / Lending  
**Institution:** FastLogic Lending Ltd (FinTech lender, UK FCA-regulated)  
**Burgess Principle Classification:** NULL → SOVEREIGN (after escalation)  
**Outcome:** Applicant approved; system process redesigned; NULL findings published  
**Key learning:** Affordability regulation (CONC) expects individual judgment, but automation often skips it. Burgess test surfaces the gap.

---

## The Situation

**Date:** February 2026  
**Subject:** A 42-year-old self-employed carpenter applied for a £3,000 personal loan through FastLogic Lending, a digital-first lender using automated underwriting.

**Applicant's specific facts:**
- Self-employed for 12 years; recent accountant-prepared accounts show £28k net income (variable; last year £31k, prior year £24k)
- Existing credit score: 650 (fair; no defaults; one missed payment 18 months ago after 2-week illness)
- Requested loan: £3,000 to purchase tools after theft; existing debt: £8k (car loan at £320/month)
- Monthly housing: £650 (mort, not rent); annual income volatile due to seasonal work
- Life circumstances: Single parent of 2 school-age children; recent change in childcare support (grandmother moved abroad; professional childcare now £520/month)

**The application:**
FastLogic's online form captured:
- Income (self-reported annual): £28,000
- Debt (captured from credit file): £8,000
- Loan amount: £3,000
- Proposed term: 36 months (£87/month payment)

Affordability ratio calculated by algorithm:
- Total debt service (inc. existing + new loan): £407/month
- Income (estimated): £28,000/12 = £2,333/month
- Ratio: 17.4% (threshold: 20%; applicant under threshold → offer issued)

**Decision:** Approved for £3,000 at 6.2% APR.

---

## The Problem: NULL Affordability Review

**February 2026 (Applicant request):**

One week after loan approval, the applicant requested a customer service review:

> "I've been offered a £3,000 loan. I want to understand how you assessed my affordability. I am self-employed with variable income (£24-31k range), recently increased childcare costs (£520/month new), and I want to confirm that a named person at your firm reviewed my individual circumstances—not just an automated algorithm—before offering this loan."

**FastLogic response (automated):**

> "We use an automated underwriting system to assess creditworthiness and affordability. Your application met our lending criteria for loan approval. Our system complies with FCA CONC regulation. Any queries about the decision should be directed to our loan review team at loans-review@fastlogic.co.uk."

**Classification: AMBIGUOUS.**  
FastLogic cited a regulatory framework (CONC) and an automated system, but did not:
- Name any individual who reviewed the applicant's specific financial circumstances
- Describe the specific facts considered (self-employment variability, childcare change, existing debt)
- Confirm that an individual affordability judgment was made before the approval

**Applicant escalation:**

> "I understand you use automated underwriting. My question is: did a named person at your firm personally review my specific situation—the fact that I'm self-employed with variable income, the recent leap in childcare costs, my specific debt-to-income ratio—*before* offering this loan? Or was this offer made by the algorithm without individual human review?"

**FastLogic response (customer review team):**

> "Our underwriting system is trained on historical lending data and applies FCA-compliant affordability rules. All applications flagged as 'edge cases' (e.g., self-employed applicants) are escalated to our lending officer for manual review. Your application was not escalated, as it fell within standard approval parameters."

**Classification: NULL.**

FastLogic admitted that:
1. The approval was not made by human review (algorithm approved, human only reviews edge cases)
2. The applicant's application (despite being self-employed—arguably an edge case) was not escalated
3. No named individual reviewed the specific facts of affordability before the approval was issued

---

## The CONC Angle: FCA Affordability Requirement

Under FCA CONC (Consumer Credit sourcebook) Regulation 4.1, lenders must:
> "Assess whether the borrower can afford to repay the debt, having considered:
> 1. the applicant's income and expenditure
> 2. the applicant's credit history
> 3. the applicant's personal circumstances
> 4. [if applicable] the reasonableness of the proposal in relation to the applicant's circumstances"

CONC does not prescribe *how* a lender assesses affordability—but it implies individual assessment, not pure automation.

**Burgess interpretation:** CONC compliance requires that a named person—not an algorithm alone—applies reason and individual judgment to the four factors listed above *before* the lending decision proceeds.

---

## ICO & FCA Escalation

**March 2026 (Applicant complaint):**

Filed with:
1. **ICO** — GDPR Article 22 breach (automated individual decision without prior meaningful human involvement)
2. **FCA** — CONC 4.1 breach (affordability assessment may be algorithmic; individual judgment not evidenced)
3. **Financial Ombudsman Service** — Complaint about lending decision fairness

**February-March 2026 (FastLogic internal review):**

Facing the dual regulatory complaint, FastLogic conducted an internal audit:
- Reviewed 47 self-employed applicant files processed in the prior 3 months
- Found that **39 of 47** (83%) were approved entirely by algorithm without individual lending officer review
- Discovered that the algorithm's affordability calculation did not account for:
  - Irregular income patterns (e.g., construction, seasonal work, gig economy)
  - Life-event changes in expenses (e.g., childcare shift, school fees, care obligations)
  - Applicant age/risk profile (older applicants with stable employment vs. younger with high turnover)

**FastLogic's finding:** The algorithm was likely approving self-employed applicants *at higher risk* than employment-based borrowers, because individual affordability judgment was missing.

---

## Resolution: From NULL to SOVEREIGN

**April 2026 (FastLogic commitment):**

FastLogic announced a system redesign:

1. **All self-employed applicants** will be escalated to individual lending officer review before approval or rejection
2. **Lending officer protocol** will include:
   - Name and role of officer recorded for each decision
   - Documented review of: income variability, life events, existing debt, monthly cash flow
   - Written affordability statement: "I, [Officer], have reviewed [Applicant]'s specific circumstances and assessed affordability as: [Yes/No/Conditions]."
   - Timer: Individual review must occur within 24 hours of application

3. **Retroactive review** of the prior 90 days' approvals:
   - 89 self-employed applications reviewed individually by lending officers
   - 12 approvals reversed; applicants contacted; loans restructured or rejected
   - 77 approvals confirmed (affordability judgment stood)

4. **Applicant in this case:**
   - Affordability re-assessed by FastLogic lending officer, Priya Sinha
   - Affordability statement: "I have reviewed the applicant's self-employment income (£24-31k range), recent childcare cost increase, and existing debt. Proposed affordability: approve at reduced loan amount (£2,000 instead of £3,000) to reduce debt service to 14%."
   - Applicant offered £2,000 at 5.8% APR (improved rate); applicant accepted

**Burgess re-classification: SOVEREIGN**  
- Named lending officer (Priya Sinha)
- Specific facts reviewed (income variability, childcare, debt)
- Timing: Individual review completed before revised offer issued

---

## Outcomes

| Outcome | Detail |
|---|---|
| **Applicant loan outcome** | £2,000 approved at 5.8% APR (reduced from £3,000 at 6.2%); affordability better matched to circumstances |
| **System change** | All self-employed applicants now require pre-approval individual lending officer review |
| **Transparency** | FastLogic now publishes affordability assessment reason for each loan approved/denied |
| **FCA outcome** | FCA issued a "firm-wide improvement direction" (informal); Fast Logic to report on implementation by Q3 2026 |
| **ICO outcome** | ICO accepted FastLogic's corrective action plan; closed complaint with note of system change |
| **Financial Ombudsman** | Case resolved in applicant's favour; FOS recommendation: enhanced affordability review for self-employed and variable-income applicants |

---

## What This Case Shows

### 1. Automation ≠ Affordability Judgment

FastLogic believed that an algorithm applied to CONC-mandated criteria (income, expenditure, credit history, circumstances) satisfied CONC 4.1. But CONC expects a person—not a system—to exercise judgment about whether the debt is affordable *for this specific borrower*.

**The gap:** An algorithm can calculate a ratio (debt service / income). Only a person can judge whether that ratio is affordable *given this person's life circumstances, income stability, liabilities, and obligations*.

### 2. Self-Employment Is an Edge Case

Self-employment, by definition, has variable income. An applicant earning £28k some years and £31k others is different from a salaried employee earning £28k every year. The algorithm didn't account for this; a lending officer's individual judgment did.

### 3. Life Events Matter

A recent shift in childcare costs (+£520/month) is material to affordability assessment. If only the algorithm runs, the life event is typically invisible (unless explicitly reported to the lender, which this applicant did).

### 4. Transparency & Remedy

Once the binary test surfaced the NULL finding, FastLogic's internal audit revealed a systemic issue affecting 83% of self-employed applicants. The same automation issue would have persisted without the Burgess test prompting clarification.

---

## Burgess Principle Lessons for Lending

1. **Regulatory compliance doesn't automate away individual judgment.**  
   CONC expects affordability *judgment*, not affordability calculation. A lender can use algorithms as tools, but the judgment must be made by a person.

2. **Edge cases need escalation.**  
   Self-employment, irregular income, recent life events, disabilities, and atypical family structures are edge cases. They require individual review; algorithm-only approval is too risky.

3. **Documentation is the enforcement mechanism.**  
   "We comply with CONC" is not evidence of individual judgment. "Officer [Name] reviewed [Facts] and determined affordability [Yes/No]" is evidence.

4. **Transparency reveals systemic issues.**  
   One applicant's question ("Did a human review me?") revealed a systemic problem affecting 83 applicants months later.

---

## Broader Sector Implications

This case applies across mainstream finance:

- **Mortgage lenders:** Many now use automated decisions for pre-qualification. Do they require individual affordability judgment before mortgage offers?
- **Credit card issuers:** Credit limit decisions often automated. Has a human looked at this card-holder's specific circumstances?
- **BNPL & installment lenders:** Micro-lending platforms often approve in seconds, without human review of individual affordability.
- **Buy-now-pay-later:** BNPL platforms face CONC compliance questions; automated affordability checks are under regulatory scrutiny.

The Burgess test is applicable to all of these: *"Did a human judge affordability for this specific applicant before the loan offer was made?"*

---

## Next Steps & Monitoring

- **Q2 2026:** FastLogic reports to FCA on self-employed lending process redesign implementation
- **Q3 2026:** FCA may inspect lending officer training and affordability documentation
- **Ongoing:** Applicant monitoring the resolved case; if FastLogic reverts to algorithm-only approval, escalation triggers new complaint

---

**Case prepared:** May 2026  
**Status:** Resolved (system changed; ongoing FCA monitoring)  
**Classification:** NULL → SOVEREIGN (post-remediation)  
**Lesson:** Automation in credit decisions requires individual affordability judgment. The Burgess test surfaces when it's missing.

---

## Related Resources

- FCA CONC 4.1: https://handbook.fca.org.uk/handbook/CONC/4/
- GDPR Article 22: https://gdpr-info.eu/art-22-gdpr/
- DUAA 2025 Articles 22A–22D: Consumer consultation on implementation
- [GETTING_STARTED.md](../GETTING_STARTED.md) — Template for credit decision challenges
- [papers/PRINCIPLE.md](../papers/PRINCIPLE.md) — Core framework
