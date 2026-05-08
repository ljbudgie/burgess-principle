# Burgess-Ready Certification Checklist

**For organisations implementing the Burgess Principle as operational governance**

*Use this checklist to verify readiness for UK00004343685 Tier 1 Certification (Premium) or Tier 2 Governance License (Standard)*

---

## Pre-Implementation: Planning & Governance

- [ ] **Leadership buy-in:** Executive/board commitment to individual human review as a governance principle
- [ ] **Legal review:** Your jurisdiction (UK/EU/other) and relevant frameworks (GDPR, DUAA, AI Act, sector-specific regulation) assessed
- [ ] **Scope definition:** Identify which decisions/systems will be subject to Burgess classification (e.g., credit approval, content moderation, triage)
- [ ] **Responsible party:** Name the individual/team accountable for oversight (e.g., Chief Compliance Officer, Data Protection Officer)
- [ ] **Budget:** Estimate cost of implementation (staff training, system changes, audits)

---

## Implementation: Decision Mapping & Process Design

### Decision Audit

- [ ] **List all significant decisions** affecting individuals in your scope (e.g., "credit approval," "content removal," "triage assignment")
- [ ] **For each decision, document:**
  - [ ] Current process (automated, human-led, hybrid)
  - [ ] Decision output (e.g., "Approve/Deny")
  - [ ] Where in the process does (or should) human review occur?
  - [ ] Who is the named human reviewer (or role if rotating)?
  - [ ] What specific facts about the individual must be reviewed?

### Process Design

- [ ] **Human review checkpoint:** Insert individual human review step *before* the decision affects the individual
  - [ ] Document: name/role of reviewer (or process to assign)
  - [ ] Document: specific facts reviewed (e.g., "income documents," "transaction history," "person's communication preference")
  - [ ] Document: timing (must occur before decision output reaches individual)

- [ ] **Classification protocol:** Design how you will classify each decision as SOVEREIGN / NULL / AMBIGUOUS
  - [ ] SOVEREIGN template: "Decision by [Name, Role], reviewed [Specific Facts], on [Date], before [Decision Output] was issued"
  - [ ] NULL escalation: If a decision would be NULL (no human review), what is the corrective action?
  - [ ] AMBIGUOUS clarification: Process for requesting reviewer name and specific facts reviewed

- [ ] **Audit trail:** System to record each decision's classification and evidentiary basis
  - [ ] Example: Database field for "Burgess Classification," "Named Reviewer," "Facts Reviewed," "Review Date"

---

## Operational Integration

### Decision Records

- [ ] **For each significant decision affecting an individual, record:**
  - [ ] Date of decision
  - [ ] Individual affected (anonymised ID acceptable)
  - [ ] Decision type (e.g., "credit approval")
  - [ ] Decision output (approve/deny/etc.)
  - [ ] Burgess Classification: SOVEREIGN / NULL / AMBIGUOUS
  - [ ] If SOVEREIGN: Named reviewer, specific facts reviewed, review date
  - [ ] If NULL: Escalation action taken
  - [ ] If AMBIGUOUS: Clarification requested and response

- [ ] **Sample audit (monthly minimum):**
  - [ ] Check 30–50 recent decisions
  - [ ] Verify SOVEREIGN % (target: ≥95%)
  - [ ] Investigate any NULL findings
  - [ ] Track corrective actions

### Training & Documentation

- [ ] **Staff trained on:**
  - [ ] Burgess Principle (binary test, definitions)
  - [ ] Organisation's implementation (which decisions, which roles, escalation protocol)
  - [ ] Classification process (how to document SOVEREIGN decisions)

- [ ] **Documentation created:**
  - [ ] Operating procedures: step-by-step guide to Burgess classification
  - [ ] Decision templates: standard forms for reviewers
  - [ ] Escalation protocol: what to do when NULL identified
  - [ ] Training slides/videos

- [ ] **Governance document:** Board-level policy or governance charter stating commitment to SOVEREIGN ≥X%

---

## Monitoring & Verification

### Metrics & Dashboard

- [ ] **Monthly dashboard showing:**
  - [ ] Total decisions classified
  - [ ] SOVEREIGN %
  - [ ] NULL %
  - [ ] AMBIGUOUS %
  - [ ] Escalations triggered
  - [ ] Corrective actions closed

- [ ] **Targets set:**
  - [ ] SOVEREIGN ≥ 95% (Tier 1) or ≥ 85% (Tier 2)
  - [ ] NULL escalation rate: 100% (every NULL reviewed for corrective action)
  - [ ] AMBIGUOUS resolution: < 7 days

### Quarterly Review

- [ ] **Conduct quarterly audit:**
  - [ ] Sample 100+ recent decisions
  - [ ] Verify classifications against evidence
  - [ ] Investigate trends (SOVEREIGN increasing/regressing?)
  - [ ] Report to leadership

- [ ] **Root cause analysis:**
  - [ ] If SOVEREIGN % dropping: Why? System design issue? Staff turnover? Increased volume?
  - [ ] If NULL % increasing: Corrective action stalled? New bypass mechanism?

### Annual External Verification (Tier 1 Certification)

- [ ] **Independent auditor engagement:**
  - [ ] Selection of auditor (Big 4, boutique compliance firm, or nominated ICO/regulator)
  - [ ] Audit scope: 12 months of decision records
  - [ ] Sample size: ≥500 decisions
  - [ ] Report: SOVEREIGN %, NULL findings, corrective action status

- [ ] **Audit findings:**
  - [ ] SOVEREIGN ≥ 95% confirmed
  - [ ] NULL findings documented and escalated
  - [ ] AMBIGUOUS clarifications processed
  - [ ] No systemic gaming or workarounds identified

---

## Governance & Accountability

### Leadership Accountability

- [ ] **Assign accountability:**
  - [ ] Role: Burgess Principle Officer (or similar title)
  - [ ] Responsibility: Oversee classification, audit, escalation, reporting
  - [ ] Reporting line: Executive sponsor (CRO, DPO, CTO)

- [ ] **Board reporting:**
  - [ ] Quarterly: SOVEREIGN %, NULL findings, corrective actions
  - [ ] Annual: External audit result, certification status

### Escalation & Corrective Action

- [ ] **NULL escalation process documented:**
  - [ ] Who decides next step? (leadership? regulator?)
  - [ ] What are the options? (reverse decision, redesign process, accept risk, escalate to regulator)
  - [ ] Timeline: How quickly must escalation be resolved?

- [ ] **Corrective actions tracked:**
  - [ ] When NULL identified: create task
  - [ ] Assign owner
  - [ ] Set deadline
  - [ ] Verify completion
  - [ ] Re-test (was corrective action effective?)

### Regulatory Readiness

- [ ] **Documentation ready for regulator scrutiny:**
  - [ ] Governance policy
  - [ ] Decision classification records
  - [ ] Audit results
  - [ ] Corrective actions log
  - [ ] Evidence of individual human review (reviewers named, specific facts documented)

- [ ] **Regulator communication plan:**
  - [ ] If ICO asks about Article 22 compliance: Can you show SOVEREIGN classifications?
  - [ ] If FCA asks about affordability: Can you name the officer who reviewed this applicant?
  - [ ] If CQC asks about triage: Did a clinician review this patient individually?

---

## Special Contexts

### High-Stakes Decisions (Finance, Healthcare, Safety)

- [ ] **Dual verification:** Critical decisions reviewed by two individuals independently
- [ ] **Named accountability:** Both reviewers' names recorded; decision maker identified
- [ ] **Documentation depth:** Specific facts reviewed, reasoning, confidence level

### Disability & Accessibility

- [ ] **Accessible communication:** Individual review process accommodates communication needs (hearing loss, language, cognitive preferences)
- [ ] **Reasonable adjustments:** Burgess classification includes notation if individual requested adjustments in reviewing their case
- [ ] **Equality Act compliance:** Review process explicitly considers individual circumstances (e.g., disability-related funding needs, care obligations)

### Bulk vs. Individual

- [ ] **Clear boundary:** Distinguish automated batch decisions (never SOVEREIGN) from individual decisions (potential SOVEREIGN)
- [ ] **Example:** 
  - ❌ Batch email: "Your service is suspended effective today." = Automated, no individual review, NULL (unless urgent exception applied)
  - ✅ Individual decision: "Your account reviewed by [Sarah Chen]. Your specific situation qualifies for grace period. Suspension delayed." = Individual review, SOVEREIGN

---

## Common Implementation Pitfalls to Avoid

- [ ] **Pitfall:** Claiming "our algorithm considers individual facts" = SOVEREIGN
  - **Reality:** Only humans make individual judgments. Algorithms are tools. SOVEREIGN requires a person's name.

- [ ] **Pitfall:** Process documentation ("we have a quality assurance layer") = SOVEREIGN
  - **Reality:** Process documentation is good governance, but SOVEREIGN requires evidence that a specific person reviewed this specific case.

- [ ] **Pitfall:** Reviewer names withheld for privacy = Can't verify SOVEREIGN
  - **Reality:** Burgess requires attribution. Alternative: "Reviewed by [Role] on behalf of [Team]" or rotate reviewer names to separate individuals.

- [ ] **Pitfall:** "Escalation will happen if anyone complains" = NULL becomes nebulous
  - **Reality:** Escalation must be automatic for NULL findings, not contingent on user complaint.

- [ ] **Pitfall:** Very high SOVEREIGN % (99%+) without corresponding NULL cases
  - **Reality:** Suggests gaming (classifying NULLs as AMBIGUOUS, or not capturing all decisions). Red flag for auditor.

---

## Self-Assessment: Readiness Score

**For each section below, score 0–3:**
- 0 = Not planned
- 1 = In early planning
- 2 = In progress
- 3 = Complete and operational

| Area | Score (0–3) | Notes |
|---|---|---|
| **Governance & leadership** | — | — |
| **Decision mapping** | — | — |
| **Human review process design** | — | — |
| **Classification protocol** | — | — |
| **Audit trail system** | — | — |
| **Staff training** | — | — |
| **Monitoring & metrics** | — | — |
| **Escalation protocol** | — | — |
| **Documentation** | — | — |
| **External verification readiness** | — | — |

**Total:** ___ /30

- **27–30:** Ready for Tier 1 Certification (Premium)
- **20–26:** Ready for Tier 2 Governance License (Standard)
- **10–19:** In progress; return in 3 months
- **<10:** Schedule consultation with The Burgess Principle team

---

## Next Steps

1. **Complete this checklist** with your team
2. **Identify gaps** and prioritize them
3. **Set implementation timeline** (typically 3–6 months)
4. **Assign Burgess Principle Officer** to lead
5. **Consider pilot:** Start with one high-impact decision type before scaling
6. **Apply for certification/license** when ready (contact: adoption@burgess-principle.limited)

---

## Resources

- [GETTING_STARTED.md](../GETTING_STARTED.md) — User-facing guide to asking the question
- [NIST_AI_RMF_MAPPING.md](../papers/NIST_AI_RMF_MAPPING.md) — NIST integration guidance
- [PRINCIPLE.md](../papers/PRINCIPLE.md) — Core doctrinal framework
- [Case studies](../case-studies/) — Real examples of implementation
- [Template letters](../templates/) — Request formats for individuals

---

**Checklist version:** 1.0 (May 2026)  
**License:** MIT (adaptable for your context)  
**Certification Mark:** UK00004343685 (once granted, Q3 2026)

*Questions? Open an issue or contact: adoption@burgess-principle.limited*
