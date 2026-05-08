# Burgess Principle & NIST AI Risk Management Framework

**Alignment and Implementation Guide**

This document maps the Burgess Principle to the NIST AI RMF (Version 1.0, September 2023) to help organisations implement meaningful human involvement in AI systems.

---

## Executive Summary

The NIST AI RMF emphasises governance, transparency, and continuous monitoring of AI systems. The Burgess Principle operationalises the human-involvement component by asking: "Was a human member of the team able to personally review the specific facts of my specific situation?"

| NIST Phase | Burgess Role | Metric |
|---|---|---|
| **Govern** | Establish accountability: Who is the named human reviewer? | SOVEREIGN classification ≥ X% |
| **Map** | Understand decision logic: What facts are reviewed by human vs. algorithm? | AMBIGUOUS findings prompt clarification |
| **Measure** | Verify oversight effectiveness: Did individual review actually occur? | SOVEREIGN/NULL ratio; audit trail completeness |
| **Manage** | Respond to gaps: If NULL, escalate or redesign | Corrective actions triggered by NULL findings |
| **Monitor** | Track compliance: Is meaningful human involvement sustained? | Track SOVEREIGN % trend; investigate regressions |

---

## 1. NIST Govern Function & Human Oversight

### GOVERN 1.1 — Map AI system(s) and component(s)

**NIST expectation:** The organisation maps the system's scope, including decision points and human touchpoints.

**Burgess integration:** For each decision point, document:
1. **Is this decision made by algorithm alone, or is there human review?**
2. **If human review, who reviews and what specific facts do they review?**

**Implementation:**
- Create a decision-tree audit: List each automated decision (e.g., "credit scoring," "loan approval," "content moderation")
- For each, identify: "Is there a human review step before the decision affects the individual?"
- For each human review step, record: name / role of reviewer (or process to assign), specific facts reviewed (or criteria), timing

**Example documentation:**
```
Decision: Credit application approved/rejected
Automated step: Scoring algorithm produces recommendation
Human review step: YES
Reviewer: Credit Officer (rotating pool, name recorded per decision)
Facts reviewed: Credit history, income, debt-to-income ratio, reason for loan
Timing: Human review required before communication to applicant
Classification: SOVEREIGN (individual review confirmed) or AMBIGUOUS (process unclear)
```

### GOVERN 1.2 — Create a governance structure

**NIST expectation:** The organisation establishes governance, roles, and accountability for AI systems.

**Burgess integration:** The governance structure must assign responsibility for verifying SOVEREIGN classification:

- **Role:** Human-Involvement Accountability Officer (or equivalent)
- **Responsibility:** Ensure each significant decision gets classified (SOVEREIGN/NULL/AMBIGUOUS)
- **Process:** Monthly or quarterly audit of decision records; escalate NULL findings for corrective action
- **Reporting:** Present SOVEREIGN % and NULL findings to executive leadership

**Governance question:** "Can we name the human who reviewed each significant decision, describe what they reviewed, and confirm individual involvement?"

If the answer is no, the system is not yet Burgess-compliant.

### GOVERN 2.1 — Establish oversight and accountability

**NIST expectation:** The organisation establishes mechanisms to ensure human oversight of AI system performance.

**Burgess integration:** the Burgess test *is* the verification mechanism for human oversight:

1. **For each significant decision affecting an individual:**
   - Assign Burgess classification (SOVEREIGN / NULL / AMBIGUOUS)
   - SOVEREIGN: Document the named reviewer and specific facts reviewed
   - NULL: Trigger escalation or system redesign
   - AMBIGUOUS: Request clarification from decision-maker

2. **Create an audit trail:**
   - Individual affected → Classification → Outcome
   - Example: "John Smith, loan application. Classification: SOVEREIGN (Sarah Chen, Credit Officer, reviewed income docs and credit report, 12 May 2026, before offer sent)."

3. **Monthly reporting:**
   - SOVEREIGN decisions: X%
   - NULL decisions: Y%
   - AMBIGUOUS (requiring clarification): Z%
   - Corrective actions for NULL: implemented / pending

**Accountability metric:** SOVEREIGN % ≥ 95% (organisational policy call, but high threshold signals robust human involvement).

---

## 2. NIST Map Function & Decision Logic Transparency

### MAP 1.1 — Understand AI system use and interaction context

**NIST expectation:** The organisation understands what the AI system does, who it affects, and how it interacts with human decision-making.

**Burgess integration:** The "interaction context" must clearly distinguish human-led decisions from algorithm-led decisions.

**Questions to resolve during mapping:**

1. **When does the human review occur?**
   - Before the algorithm runs (human sets parameters)
   - After the algorithm recommends (human approves/rejects)
   - Before the decision reaches the individual (human verifies outcome)
   - Or: never (fully automated)

2. **What specific facts does the human review?**
   - The input facts about the individual (e.g., income, age, location)
   - The algorithm's recommendation and confidence score
   - The individual's own submission or appeal
   - Edge cases or exceptions flagged by QA

3. **Does the human review reach the level of *individual consideration*, or is it policy application?**
   - Individual consideration: "I looked at John's specific situation and made a judgment."
   - Policy application: "John's case matched rule set X, which mandates outcome Y."

**Burgess classification during Map:**
- If human review reaches *individual* level: potential SOVEREIGN
- If human review is policy application only: likely AMBIGUOUS (clarify with human reviewer)
- If no human review occurs: NULL

### MAP 1.2 — Understand intended use

**NIST expectation:** The organisation understands the AI system's intended use, beneficiaries, and risks.

**Burgess integration:** Specify the intended use of human review:

- **Use:** "Meaningful human involvement to ensure automated credit decisions are informed by individual circumstances"
- **Beneficiaries:** Credit applicants, particularly those with non-standard profiles (self-employed, recent immigrants, credit history gaps)
- **Risks:** "If human review does not reach individual consideration level, applicants with non-standard profiles are systematically disadvantaged" (AMBIGUOUS or NULL finding)

---

## 3. NIST Measure Function & Oversight Effectiveness

### MEASURE 1.1 — Verify performance and effectiveness

**NIST expectation:** The organisation measures whether AI system performance meets expectations, including human oversight effectiveness.

**Burgess integration:** The Burgess test provides a direct metric for human-oversight effectiveness:

**Metric: SOVEREIGN Classification Rate**
- Definition: The percentage of individual decisions for which the organisation can demonstrate a named human reviewed specific facts before the decision was made
- Target: ≥ 95%
- Calculation: (SOVEREIGN decisions / total significant decisions) × 100

**Metric: NULL Escalation Rate**
- Definition: The percentage of NULL findings that trigger escalation or corrective action
- Target: 100% (every NULL should escalate)
- Calculation: (NULL findings escalated / total NULL findings) × 100

**Metric: AMBIGUOUS Resolution Time**
- Definition: Average time to resolve AMBIGUOUS classifications into SOVEREIGN or NULL
- Target: < 7 days
- Calculation: Average days from AMBIGUOUS classification to clarification and re-classification

### MEASURE 2.1 — Evaluate oversight and monitor processes

**NIST expectation:** The organisation evaluates whether human oversight processes are functioning as designed.

**Burgess implementation:** Monthly audit of decision records:

**Sample audit:**
```
May 2026 Credit Decisions Audit (n = 127 decisions affecting individuals):

SOVEREIGN:    112 decisions (88%)
  — Named human, specific facts, timing documented ✓

AMBIGUOUS:      8 decisions (6%)
  — Process unclear; human reviewer contacted for clarification ✓

NULL:           7 decisions (6%)
  — No human review before decision reached individual ✗
  — Corrective action: System redesigned; human review checkpoint added
  — Status: Implemented for June onward

Next month target: SOVEREIGN ≥ 95%
```

---

## 4. NIST Manage Function & Corrective Action

### MANAGE 1.1 — Plan AI system performance management

**NIST expectation:** The organisation plans how to manage AI system performance, including responding to issues.

**Burgess integration:** Plan for NULL findings as a corrective-action trigger:

**NULL Response Protocol:**
1. **Immediate:** Notify affected individual; explain the NULL finding
2. **Escalation:** Escalate to human decision-maker for individual review
3. **Root cause:** Investigate why human review did not occur (system design, training gap, workload, technical failure)
4. **Corrective action:** Redesign workflow, add checkpoint, retrain staff, or escalate to management
5. **Prevention:** Implement control to prevent recurrence

**Example NULL response — Energy billing:**
```
NULL Finding: Meter frozen; billing adjustment made by automated reconciliation.
No human review of individual's circumstances documented.

Immediate action: Contact individual; reverse automatic charges; offer payment plan.

Root cause: High-volume month; billing automation triggered without QA checkpoint.

Corrective action: Added mandatory human review for >£X adjustments.

Prevention: Monthly audit of AMBIGUOUS/NULL classifications.
```

### MANAGE 3.1 — Manage AI system performance and effectiveness

**NIST expectation:** The organisation manages performance to ensure systems continue to function as intended.

**Burgess integration:** Use SOVEREIGN/NULL/AMBIGUOUS classifications as a performance metric:

- **If SOVEREIGN % drops:** Investigate why human involvement may be degrading
- **If NULL % increases:** Red flag; system may be automated beyond design intent
- **If AMBIGUOUS % persists:** Documentation process unclear; retrain staff or clarify procedures

---

## 5. NIST Monitor Function & Continuous Oversight

### MONITOR 4.1 — Feedback loop and continuous monitoring

**NIST expectation:** The organisation establishes a feedback loop to monitor system performance, risks, and effectiveness over time.

**Burgess integration:** Track Burgess classifications over time as a compliance KPI:

**Monitoring dashboard (example):**
```
Q2 2026 Burgess Compliance Dashboard

SOVEREIGN:  91%  ↑ (May: 88%)  Target: >95%
NULL:        5%  ↓ (May: 6%)   Target: <2%
AMBIGUOUS:   4%  → (May: 6%)   Target: <3%

Trend: SOVEREIGN improving. NULL escalation protocol effective.
Status: On track for Q3 target of 95%.

Risk: AMBIGUOUS plateau. Next action: Staff training on Burgess classification.
```

**Monitoring cadence:**
- Monthly: Classification counts and percentages
- Quarterly: NULL escalation outcomes; corrective actions closed
- Annually: Trend analysis; compare to regulatory benchmarks and peer organisations

---

## 6. Sector-Specific Applications

### 6.1 Banking & Financial Services

**Decision types:** Credit approval, overdraft facility, loan origination, fraud review

**Burgess checkpoints:**
- Credit scoring: Does a human review non-standard applicants individual circumstances? (e.g., self-employed, recent immigrant, credit gap)
- Fraud review: Does a named person examine specific transaction flags individually, or is the block automatic?
- Debt restructuring: Does a human consider the individual's hardship circumstances, or is the offer templated?

**Compliance example:**
```
Loan application from self-employed applicant denied by algorithm.
Burgess test: Was a human able to review this specific applicant's income docs and business model?
Result: AMBIGUOUS — "Subject to quality assurance process."
Follow-up: Who reviewed this file? What specific income facts?
Result: NULL — No individual review; algorithm decision final.
Escalation: Article 22 GDPR challenge; individual entitled to human review and explanation.
```

### 6.2 Healthcare & Medical AI

**Decision types:** Diagnostic recommendation, triage, treatment plan, denial of coverage

**Burgess checkpoints:**
- Diagnosis: Did a named clinician review the individual patient's symptoms, history, and context before accepting the algorithm's recommendation?
- Triage: Did a human clinician individually assess the patient's urgency, vulnerabilities, and specific circumstances?
- Coverage denial: Was the individual case reviewed by a human before the denial was issued?

**Compliance example:**
```
Automated diagnostic algorithm recommends testing for condition X.
Burgess test: Did a clinician review this specific patient's history and symptoms before adopting the recommendation?
Result: SOVEREIGN — Dr. Sarah Chen reviewed John's previous admissions, medications, and presenting symptoms before confirming the recommendation.
Outcome: Defensible clinical decision; individual had human consideration.
```

### 6.3 Public Sector & Benefits

**Decision types:** Benefit entitlement, council tax, enforcement, public ID

**Burgess checkpoints:**
- Benefit claim: Did a human review this specific applicant's circumstances, disabilities, caring responsibilities, before a decision?
- Council tax: Did anyone review this specific property's facts before issuing the notice or enforcement?
- ID document: Did a human verify this specific applicant's identity and eligibility before issuing the document?

**Compliance example:**
```
Benefit claim rejected automatically because income exceeded threshold by £5.
Burgess test: Did a human review this specific applicant's situation before rejection?
Result: NULL — Automated income check; no human review documented.
Escalation: Article 22 GDPR + DUAA 2025 Article 22B breach; individual entitled to human review.
Corrective action: Human assessment of individual circumstances; hardship exemption applied.
```

### 6.4 Platform & Content Moderation

**Decision types:** Content removal, account suspension, recommendation ranking, ad targeting

**Burgess checkpoints:**
- Content removal: Did a human review the specific content in context (satire, commentary, jurisdiction) before removal?
- Account suspension: Did a human review the specific account's history and context before banning?
- Ad targeting: Was any human aware of the specific targeting decision, or was it pure automation?

**Compliance example:**
```
Video removed for copyright claim.
Burgess test: Did a human review the specific content for fair use, parody, or jurisdiction before removal?
Result: AMBIGUOUS — "Our trust and safety team reviewed the claim."
Follow-up: Can you name the reviewer and describe the specific facts they reviewed?
Result: NULL — No human review; automated DMCA process.
Escalation: Article 86 / Article 22 GDPR challenge; user entitled to human explanation and appeal.
```

---

## 7. Integration with NIST Compliance

### 7.1 Mapping to NIST Core Functions

| NIST Core Function | Burgess Principle Application |
|---|---|
| **GOVERN** | Create governance structure that assigns accountability for SOVEREIGN classification; establish NULL escalation protocol |
| **MAP** | Document where human review does and doesn't occur; distinguish individual consideration from policy application |
| **MEASURE** | Track SOVEREIGN % as primary KPI for human-involvement effectiveness; use NULL findings as audit triggers |
| **MANAGE** | Treat NULL as corrective-action trigger; implement system redesign or process improvement to achieve SOVEREIGN |
| **MONITOR** | Monthly/quarterly dashboard of SOVEREIGN/NULL/AMBIGUOUS classifications; track trends; identify regressions |

### 7.2 NIST Documentation Requirements

**Burgess-compliant documentation should include:**

1. **Governance charter:** "The organisation commits to SOVEREIGN classification for [X%] of significant decisions."
2. **Decision mapping:** For each AI system: decision types, human review points, named roles
3. **Classification records:** Each significant decision: SOVEREIGN/NULL/AMBIGUOUS + evidence
4. **Escalation log:** NULL findings → corrective action → outcome
5. **Monitoring dashboard:** Monthly SOVEREIGN % trend, NULL escalation rate, AMBIGUOUS resolution time
6. **Training records:** Staff trained on Burgess classification process

---

## 8. Compliance Checklist

- [ ] Governance structure assigns accountability for human-involvement verification
- [ ] Decision mapping completed; human review points identified and documented
- [ ] Classification protocol established; staff trained on SOVEREIGN/NULL/AMBIGUOUS
- [ ] Decision records created for each significant individual decision
- [ ] NULL escalation protocol implemented and tested
- [ ] Monthly audit process established
- [ ] Dashboard created; SOVEREIGN % tracked
- [ ] Annual trend analysis conducted
- [ ] NIST RMF functions mapped to Burgess operations
- [ ] External audit (regulatory, internal) planned using Burgess metrics

---

## 9. Quick Start: 30-Day Implementation

**Week 1: Assessment**
- Identify 3–5 high-impact AI decisions in your system
- For each, ask: "Do we have documented evidence of individual human review?"
- Classify existing decisions as SOVEREIGN/NULL/AMBIGUOUS

**Week 2: Design**
- Create decision-mapping template
- Design classification form (SOVEREIGN / NULL / AMBIGUOUS + evidence)
- Draft NULL escalation protocol

**Week 3: Pilot**
- Pick one high-volume decision type (e.g., credit approval)
- Run 50 retrospective classifications
- Calculate initial SOVEREIGN %

**Week 4: Scale**
- Integrate into incident/decision system
- Train staff on classification
- Publish first dashboard

**Result:** At end of week 4, you have a baseline SOVEREIGN % and a system to track it.

---

## References

- NIST AI Risk Management Framework (2023), https://airc.nist.gov/
- EU AI Act 2024/1689, Articles 14, 26, 86
- UK Data (Use and Access) Act 2025, Articles 22A–22D
- Data Protection Regulation (EU) 2016/679, Article 22
- Burgess Principle Repository, github.com/ljbudgie/burgess-principle

---

**Document version:** 1.0 (May 2026)  
**License:** MIT  
**Certification Mark:** UK00004343685
