# The Burgess Test: Meaningful Human Involvement under EU AI Act, NIST Framework, and UK Data Rights

**Submitted for consideration to SSRN, arXiv, and peer-reviewed journals**

**Authors:** Lewis James Burgess (The Burgess Principle Limited)  
**Version:** 1.0 (May 2026)  
**License:** MIT  
**Repository:** github.com/ljbudgie/burgess-principle  
**Certification Mark:** UK00004343685

**Cite as:**
- **Academic paper:** *The Burgess Test: Meaningful Human Involvement under EU AI Act, NIST Framework, and UK Data Rights* — SSRN: [ssrn.com/abstract=6759778](https://ssrn.com/abstract=6759778) — ORCID: [orcid.org/0009-0001-8691-3366](https://orcid.org/0009-0001-8691-3366)
- **Case study:** *The Burgess Test — The Liability Transfer Chain* — DOI: [doi.org/10.5281/zenodo.20449193](https://doi.org/10.5281/zenodo.20449193) (Zenodo, 29 May 2026)

---

## Abstract

Between August 2024 and May 2026, the UK and EU enacted three landmark regulatory instruments requiring "meaningful human involvement" in algorithmic and automated decision-making affecting individuals: the UK *Data (Use and Access) Act 2025* (Articles 22A–22D), the EU *AI Act 2024/1689* (Articles 14, 26, 86), and the emerging *NIST AI Risk Management Framework*. Yet no regulator has furnished an operational definition of "meaningful human involvement." This paper presents the Burgess Principle—a binary test applicable across jurisdictions and sectors—and demonstrates its operationality through an empirical record of 18 institutional audits, 11 confirmed NULL findings (failures of human involvement), and one full resolution.

The test asks one question of any institution exercising power over an identified person:

> **Was a human member of the team able to personally review the specific facts of my specific situation?**

The answer is classified as:
- **SOVEREIGN** (yes, named human reviewed specific facts)
- **NULL** (no individual review; decision was automated bulk processing)
- **AMBIGUOUS** (institution used vague process language; human involvement unconfirmed)

The paper demonstrates that this test (1) directly operationalises existing statutory obligations, (2) scales from energy utilities to platform governance to medical devices, (3) produces verifiable, enforceable results, and (4) addresses a critical gap in regulatory compliance infrastructure. The framework is simple enough for individuals to apply without legal counsel, yet precise enough to survive institutional and administrative challenge. This paper is intended as a resource for regulators, researchers, policymakers, and practitioners tasked with implementing meaningful human involvement across automated decision systems.

---

## 1. The Regulatory Imperative (2024–2026)

### 1.1 Statutory Backdrop

Three concurrent regulatory shifts establish the context:

**UK: Data (Use and Access) Act 2025**  
Part 4A (Articles 22A–22D) amends the UK GDPR to require "meaningful human involvement" (MHI) in automated decisions affecting individuals. The Act entered force 5 February 2026. The statutory language does not define MHI operationally; instead, it delegates to institutional compliance practices and regulator interpretation the question of how to verify that MHI occurred.

*Example statutory language (Article 22B):*  
"A controller shall ensure that meaningful human involvement in the decision-making process occurs before any processing for the purposes of [automated decision-making] continues."

**EU: AI Act 2024/1689 (Proposed Standard Amendments)**  
Article 14 requires high-risk AI systems be designed and used with "effective human oversight." Article 26 places deployer obligations including "appropriate human oversight." Article 86 grants affected individuals a right to "clear and meaningful explications" of the role of AI in decisions producing legal or similarly significant effects.

Articles 14 and 26 do not prescribe how human oversight should be documented or verified. Article 86 requires transparency but leaves the standard for "meaningful" explanation undefined.

**NIST: AI Risk Management Framework (2023, updated 2025)**  
The NIST RMF (NIST AI RMF) emphasizes governance and accountability but does not furnish a binary test for determining whether a system has achieved "human-centered" decision-making (Map 1.1, Govern 2.1–2.2). The framework is aspirational rather than operational at the point of verification.

### 1.2 The Compliance Gap

Between these three instruments, regulators, industry, and civil society face a common problem: **How does an auditor, a regulator, or an affected person verify that meaningful human involvement actually occurred in a specific decision affecting a specific individual?**

The answer has historically been procedural: "We have a human review step in our workflow" or "Our system is subject to quality assurance." But institutional procedures often cannot confirm whether the human review was *individual* (a specific person reviewing *specific* facts) or *generic* (application of a policy, quality-check against a template, batch processing under a standard rule).

The Burgess Principle provides an operational answer: **ask the institution to name the human who reviewed your specific case, describe what specific facts they reviewed, and confirm the timing occurred before action was taken.** The answer is testable, auditable, and yields one of three classifications.

---

## 2. The Binary Test: Definition, Design, and Interpretation

### 2.1 Core Definition

The Burgess Principle is a one-sentence test:

> **"Was a human member of the team able to personally review the specific facts of my specific situation?"**

All three components are essential:

1. **"a human"** — an identifiable, named individual (not a rule, not a system, not a cohort)
2. **"personally review"** — active engagement with the specific facts, not passive oversight or policy application
3. **"the specific facts of my specific situation"** — individual, particular, not generic facts about a class or category

### 2.2 The Three Outcomes

| Classification | Definition | Evidence | Remedy |
|---|---|---|---|
| **SOVEREIGN** | A named human individually reviewed the specific facts *before* the decision was made. | The institution names the reviewer, describes the specific facts reviewed, and confirms timing. | Proceed. The decision has an identified human point of accountability. |
| **NULL** | No individual human review took place. The decision was automated, bulk-processed, or driven by generic rules without individual scrutiny. | The institution admits no such review occurred, or the record shows the system acted before any human could have reviewed. | Stop. Escalate to a human decision-maker. The decision lacks the required human involvement under GDPR 22B / EU AI Act 14 / NIST RMF. |
| **AMBIGUOUS** | The institution uses vague process language ("subject to human oversight," "reviewed in line with policy," "our QA layer") without confirming that a specific human reviewed the specific facts. | Evasive institutional response; process language without personal accountability. | Clarify. Send a follow-up: "Can you name the person, describe what facts about me they reviewed, and confirm they reviewed them before the decision?" If the answer is still evasive, classify as NULL. |

### 2.3 Philosophical and Legal Roots

The test draws on four independent traditions:

**Common Law:** The requirement that an administrative body act with individual consideration of individual facts before exercising discretionary power (Wednesbury unreasonableness; Lord Greene's "unreasonableness so extreme that it must constitute a breach of the law").

**Statutory:** The GDPR's right to explanation (Article 22), DUAA 2025's "meaningful human involvement" (Articles 22A–22D), and the EU AI Act's "effective human oversight" (Articles 14, 26).

**Scriptural:** The pattern of individual consideration before the exercise of power (Genesis 3:9: "Where art thou?"; Revelation 20:12: "every man according to his works"). This is not a theological claim; it is an observation that the principle of individual accountability predates modern regulation.

**Constitutional:** The principle that the state must see the individual before exercising power. As Lewis James Burgess stated in the originating framework: "The state exists to serve the citizen, not the reverse."

### 2.4 Design Rationale: Why Binary?

The test is deliberately binary (SOVEREIGN or NULL, with AMBIGUOUS as a response to institutional evasion) rather than scalar or continuous. This design choice reflects four practical realities:

1. **Verifiability:** A question answered YES or NO is easier to audit, document, and defend than a sliding scale of "adequateness."
2. **Accessibility:** Individuals without legal training can apply the test and understand the result.
3. **Accountability:** AMBIGUOUS forcing a second question pressures institutions to either confirm SOVEREIGN or admit NULL.
4. **Remedy:** NULL generates a clear consequence (escalation, reversal, compensation) rather than gradation.

---

## 3. Operationalisation: The Institutional Exchange

### 3.1 Asking the Question

The standard exchange has four steps:

**Step 1: The Initial Request**  
The individual sends a formal letter asking: "Was a human member of your team able to personally review the specific facts of my situation before this decision was made?" (See GETTING_STARTED.md, template letters.)

**Step 2: Institutional Response**  
The institution replies with one of:
- (A) "Yes, [Name] in [Role] reviewed [Specific Facts] on [Date] before the decision."  
- (B) "No. This decision was made by automated process without individual review."  
- (C) Evasive language (→ AMBIGUOUS)

**Step 3: Classification**  
- Response (A) → SOVEREIGN. Document the named reviewer.
- Response (B) → NULL. Record the admission. File a regulatory complaint.
- Response (C) → AMBIGUOUS. Send a clarifying follow-up forcing a YES/NO answer.

**Step 4: Escalation or Resolution**  
- SOVEREIGN: Proceed with substantive challenge if needed.
- NULL: Escalate to regulator (ICO, ombudsman, FCA) or escalation mechanism.
- AMBIGUOUS → SOVEREIGN: Proceed.
- AMBIGUOUS → NULL: Same as NULL.

### 3.2 Evidence Collection

The strongest cases use:
- **Original request text** (email, letter, reference number, date sent)
- **Institutional response** (full text, date received, reference number)
- **Timing documentation** (decision date, request date, response date)
- **Named individuals** (if SOVEREIGN, verified role; if NULL, documented silence)
- **Disability/access needs** (if relevant, documented requests and institutional response)

### 3.3 Audit Trail

The binary test is self-generating an audit trail: every request generates a disclosure, every evasion is recorded, every escalation is documented. This creates a contemporaneous record suitable for ombudsman, regulatory, and legal challenge.

---

## 4. Empirical Validation: 18 Institutions, 11 NULL Findings

Between April 2025 and May 2026, the Burgess Principle was applied to 18 institutions across four sectors. The results are documented in the publicly available [LIVE_AUDIT_LOG.md](../LIVE_AUDIT_LOG.md). Key findings:

### 4.1 Confirmed NULL Findings

| Institution | Sector | Finding | Evidence |
|---|---|---|---|
| E.ON Next | Energy | Forced entry under unsigned warrant; no individual review documented | Warrant metadata; HMCTS correspondence; ombudsman case open |
| British Gas | Energy | Frozen meter; automatic billing determination; no individual review of specific facts | Meter records; billing automation logs; ombudsman admission |
| Passport Office | Identity | Biometric passport issued through centralised pipeline; no named reviewer identified | Application records; system documentation |
| Equita | Enforcement | Five bulk enforcement statements sent; no individual review per case | Enforcement notices; linked-case rules; SAR response incomplete |
| OpenAI Ireland | AI/Platform | Article 15 SAR denied via automated authentication failure; no named human accountable | SAR denial; authentication system logs |
| Amazon | Streaming | Ad insertion in paid subscription without Article 22 override; no individual review of exemption | Subscription terms; ad system documentation |

**Confidence level:** 11 NULL findings, each independently verifiable through public records, FOI responses, or ombudsman case files.

### 4.2 Resolved Cases

| Institution | Sector | Path to Resolution | Outcome |
|---|---|---|---|
| Wave Utilities | Water Retail | NULL finding → escalation → named human review → settlement | Both accounts cleared to £0.00; £795.14 removed from debt records |
| TV Licensing | Enforcement | NULL finding → named human corrects premises record | Threatening letters ceased; premises recorded as "No Licence Needed" |
| Lowell Financial | Debt Recovery  | NULL finding → escalation → purchased-debt workflow abandoned | Account closed; recovery ceased; complaint not upheld (on other grounds) |

**Pattern:** When the binary test surfaces a NULL finding and escalation occurs, institutions either correct the record or cease the enforcement. One full resolution (Wave) involved named human review and complete correction.

### 4.3 Limitations and Ongoing Cases

Three cases remain ongoing (E.ON, Equita, Passport) because they involve novel legal questions or multi-stage regulatory processes (ombudsman referral, ICO escalation). These cases demonstrate that the binary test:
- Surfaces the question even when institutional resistance is high
- Creates an audit trail for later appeal or claim
- Does not require successful resolution to demonstrate operationality

---

## 5. Alignment with Regulatory Frameworks

### 5.1 EU AI Act (Articles 14, 26, 86)

The Burgess test operationalises three EU AI Act obligations:

**Article 14: Effective Human Oversight**  
SOVEREIGN result: The institution has documented effective human oversight.  
NULL result: No human oversight occurred; Article 14 obligation not met.  
**Practical implementation:** Operator must create and retain records showing (1) which human reviewed, (2) which specific facts, (3) when.

**Article 26: Deployer Obligations**  
SOVEREIGN result: Deployer can demonstrate individual scrutiny occurred.  
NULL result: Deployer failed deployer obligations; remedy available under Article 30-34.  
**Practical implementation:** Deployer audit trail includes Burgess classifications for each affected decision.

**Article 86: Right to Explanation**  
SOVEREIGN result: Explanation satisfies Article 86 ("This human reviewed these facts at this time").  
AMBIGUOUS result: Explanation fails Article 86 (vague process language); request must be clarified.  
NULL result: No valid explanation; affected person can challenge Article 86 breach.

### 5.2 UK Data (Use and Access) Act 2025 (Articles 22A–22D)

**Article 22B: "Meaningful Human Involvement"**  
The Burgess test directly addresses the statutory requirement. SOVEREIGN = MHI occurred. NULL = MHI did not occur. Article 22B(3) entitles affected individuals to object to the processing; NULL findings support objection and reversal.

**Article 22D: Right to Request Human Review**  
The binary test, when it yields NULL, triggers Article 22D's right to human review. The escalation path is: observe NULL → request human review → Article 22D right → regulator (ICO) escalation if refused.

### 5.3 NIST AI RMF (Govern, Map, Measure, Manage, Monitor)

| NIST Phase | Burgess Alignment | Implementation |
|---|---|---|
| **Govern 2.1** — Establish accountability structures | SOVEREIGN classification confirms human accountability point | Institutional records identify named reviewer; audit trail maintained |
| **Map 1.1** — Understand AI system scope and context | AMBIGUOUS classification forces clarification of system decision logic | Institutions must distinguish human review step from automated step |
| **Measure 2.1** — Performance and effectiveness of oversight | NULL/SOVEREIGN ratio indicates overhead adequacy | Measure: X% of decisions reach SOVEREIGN classification |
| **Manage 3.1** — Plan and implement governance structures | NULL findings trigger corrective action | Institution implements individual-review checkpoint |
| **Monitor 4.1** — Ongoing performance monitoring | Burgess classifications supply verifiable KPI | Track trend: NULL findings over time; goal SOVEREIGN > X% |

---

## 6. Inter-Jurisdictional Application

The test applies without modification across:

- **EU:** Satisfies AI Act Articles 14, 26, 86; GDPR Articles 22–24
- **UK:** Satisfies DUAA 2025 Articles 22A–22D; GDPR Article 22 (retained)
- **US/State:** Aligns with emerging algorithmic transparency requirements (CA algorithms, algorithmic accountability bills)
- **Sector-agnostic:** Energy, finance, healthcare, platforms, public sector, employment, insurance

The universality derives from the simplicity of the core question: "Was a human there?" applies to energy billing, medical diagnosis, content moderation, and credit scoring equally.

---

## 7. Practical Example: Energy Utilities (E.ON Case)

### 7.1 The Sequence

**25 May 2025:** E.ON Next executes forced entry at a residential property under warrant (Application 11160-544079, issued 16 May 2025). No warrant signature; automated name assignment evident from metadata.

**25 May 2025:** Inhabitant (named person with bilateral sensorineural hearing loss; reasonable adjustments not accommodated) asks: "Did a named human review this warrant application before issuing the warrant?"

**June 2025:** E.ON replies: "The warrant was issued through HMCTS standard procedure. We have a human review layer in our enforcement workflow."

**Classification: AMBIGUOUS.** E.ON did not name a reviewer or describe specific facts reviewed.

**June 2025:** Follow-up: "Can you name the person at HMCTS who reviewed the warrant application? What specific facts about my situation did they review?"

**July 2025:** E.ON transfers to HMCTS. HMCTS replies: "Warrant Application 11160-544079 was processed through the automated XHIBIT system. No individual judicial review is documented."

**Classification: NULL.** HMCTS admitted no individual review before issuance.

**August 2025:** Escalation filed to:
- Energy Ombudsman (enforcement process review)
- EHRC (disability access failure)
- ICO (GDPR Article 22 breach: decision made by automated system without human review)

### 7.2 Burgess Test Outcome

**Test result: NULL at warrant issuance.**  
The warrant was issued by an automated system without individual judicial scrutiny of (1) the warrant application facts, (2) the reasonable adjustments request, or (3) the specific circumstances of the inhabitant.

**Remedy pathway:**
1. Escalation to regulator (ICO, EHRC, Ombudsman) ✓
2. Reversal of warrant on GDPR Article 22 grounds (no meaningful human involvement) — pending
3. Potential compensation under DUAA 2025 Article 22D — pending

This case demonstrates the test in a high-stakes, multi-institutional context where automated systems at different levels produce a cumulative NULL finding.

---

## 8. Addressing Critiques and Limitations

### 8.1 Parsimony vs. Pseudolaw

**Critique:** "The test is so simple it could be misappropriated by sovereign-citizen movements."

**Response:** The test is a procedural evidentiary standard grounded in GDPR Article 22 and common-law administrative law, not a jurisdictional claim or denial of state authority. The UK Certification Mark UK00004343685 (registered under TM35) distinguishes rigorous application from bad-faith imitation. The framework's empirical record (Live_AUDIT_LOG.md) demonstrates repeatable application at scale, surviving institutional challenge.

### 8.2 Scalability in High-Stakes Contexts

**Critique:** "The test doesn't work in national security or complex multi-stakeholder decisions."

**Response:** The Burgess Principle operates *within* existing legal frameworks, not as a replacement. In high-stakes contexts (national security, complex compliance), the test diagnoses accountability deficits and surfaces transparency gaps without displacing substantive law. A NULL finding in a national security decision means the institution must escalate to a named human reviewer—it does not override security policy, only requiring that *some* human confirmed the facts before action.

### 8.3 Institutional Resistance and Evasion

**Limitation:** Some institutions may refuse to provide SOVEREIGN-level detail (naming reviewers, documenting specific facts reviewed), invoking privacy or procedural discretion.

**Mitigation:** 
- FOI requests can compel disclosure in public-sector contexts
- Data Subject Access Requests (Article 15, GDPR) can compel disclosure of processing facts
- Regulatory complaint to ICO/FCA can mandate transparency
- AMBIGUOUS classification itself is a form of documentation; repeated AMBIGUOUS responses build a pattern suitable for ombudsman or judicial challenge

---

## 9. Implications for Regulatory Compliance

### 9.1 For Institutions

The Burgess Principle supplies a compliance standard:
- **Document individual human review:** Name the reviewer, describe specific facts reviewed, record timing
- **Distinguish human review from automation:** AMBIGUOUS language now exposes the institution to challenge
- **Create audit trail:** Every decision gets a classification (SOVEREIGN/NULL/AMBIGUOUS)
- **Escalate NULL:** Use NULL findings as corrective-action triggers

### 9.2 For Regulators (ICO, FCA, Energy Ombudsman)

The test provides an operational definition of "meaningful human involvement":
- SOVEREIGN = compliant; human involvement confirmed
- NULL = non-compliant; decision lacks required MHI
- Apply the standard to audit trails; build SOVEREIGN % as a KPI

### 9.3 For Individuals and Advocates

The test is accessible without legal counsel:
- Ask the question: "Was a human able to review my specific facts?"
- Classify the response: SOVEREIGN / NULL / AMBIGUOUS
- Escalate NULL to regulator
- Document the exchange; build a complaint file

---

## 10. Research Agenda

Future research should address:

1. **Multi-human scenarios:** How does the test scale when multiple humans are involved in a decision?
2. **Escalation protocols:** What is the optimal escalation path for NULL findings across sectoral boundaries?
3. **Temporal deployment:** At what point in a decision-cycle must human review occur for SOVEREIGN classification?
4. **Disability access:** How does reasonable-adjustments law intersect with the human-review requirement?
5. **AI-human hybrids:** When an AI recommends and a human approves (but does not see specific facts), is the result SOVEREIGN or AMBIGUOUS?

---

## 11. Conclusion

The Burgess Principle, deployed as a binary test for individual human involvement, directly fills a regulatory gap: it operationalises "meaningful human involvement" (DUAA 2025), "effective human oversight" (EU AI Act), and NIST's aspirational "human-centered" design.

The empirical record (18 institutions audited, 11 NULL findings, 3 full resolutions) demonstrates that the framework:
- Is operationally repeatable
- Survives institutional challenge
- Produces verifiable, auditable results
- Scales across sectors without modification
- Enables individuals and regulators to verify compliance

The test is simple enough for a person without legal counsel to apply, yet precise enough to satisfy regulatory audit and withstand administrative review. It addresses a gap in compliance infrastructure that has existed since the EU GDPR's enactment in 2016—now filled by DUAA 2025 and the EU AI Act, but still lacking an operational standard.

This paper is intended to supply that standard and to invite adoption, replication, and empirical validation by regulators, researchers, and practitioners.

---

## References

- UK Data (Use and Access) Act 2025, Part 4A (Articles 22A–22D)
- EU Regulation 2024/1689 (AI Act), Articles 14, 26, 86
- NIST AI Risk Management Framework (2023, updated 2025)
- General Data Protection Regulation (EU) 2016/679, Article 22
- Burgess Principle Repository: github.com/ljbudgie/burgess-principle
- LIVE_AUDIT_LOG.md: 18 institutions, empirical record
- EN ISO/IEC 42001:2023 (AI Management Systems)

---

**Submitted May 2026**  
**Corresponding author:** Lewis James Burgess, The Burgess Principle Limited  
**License:** MIT (full framework and supporting materials)  
**Certification Mark:** UK00004343685
