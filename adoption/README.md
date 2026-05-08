# Adoption — The Burgess Principle in Practice

**Resources for organisations implementing individual human review as governance**

---

## Welcome

This directory contains:

- **[INSTITUTIONAL_ADOPTION_TRACKER.md](./INSTITUTIONAL_ADOPTION_TRACKER.md)** — Live registry of organisations adopting or implementing the Burgess Principle
- **[BURGESS_READY_CHECKLIST.md](./BURGESS_READY_CHECKLIST.md)** — Implementation roadmap and governance checklist (30-point assessment)
- **[PUBLIC_LEADERBOARD.md](./PUBLIC_LEADERBOARD.md)** — Sector-by-sector transparency: which systems have verified individual human review? Which don't?

---

## Quick Start: Three Paths

### Path 1: Evaluate If Burgess Is Right For You

**Read:** [BURGESS_READY_CHECKLIST.md](./BURGESS_READY_CHECKLIST.md) **Section: Pre-Implementation**

**Ask yourself:**
- Do we make decisions affecting individuals?
- Are any of those decisions automated or bulk-processed?
- Are we required (by GDPR 22, DUAA 2025, EU AI Act, or sector-specific regulation) to demonstrate "meaningful human involvement"?

**If yes to all three**, Burgess is applicable.

### Path 2: Understand the Adoption Landscape

**Read:** [INSTITUTIONAL_ADOPTION_TRACKER.md](./INSTITUTIONAL_ADOPTION_TRACKER.md)

**Learn:**
- Who has already adopted? (Wave, OpenClaw, FastLogic, NHS, NousResearch)
- What sector are they in? (Energy, finance, AI, healthcare, public sector)
- What did adoption look like? (Live case studies)
- What certifications are available? (Tier 1 Premium, Tier 2 Standard, Tier 3 Community)

### Path 3: Measure Your Own Systems

**Read:** [PUBLIC_LEADERBOARD.md](./PUBLIC_LEADERBOARD.md)

**Check:**
- Is your organisation already listed? (As Burgess-Ready, Burgess-Acknowledged, or Burgess-Deficient)
- What's your sector benchmark? (How do you compare to peers?)
- What evidence would move you from Deficient → Acknowledged → Ready?

---

## Implementation Roadmap (12 Weeks)

### Weeks 1–2: Planning

- [ ] Read BURGESS_READY_CHECKLIST.md sections: Pre-Implementation, Special Contexts
- [ ] Leadership alignment: Board/executive buy-in on individual human review as governance principle
- [ ] Legal review: Applicable regulations (GDPR, DUAA, AI Act, sector-specific)
- [ ] Scope: Which decisions will be audited? (e.g., credit approval, content moderation, triage)
- [ ] Budget: Estimated cost (staff training, systems, audits)

### Weeks 3–5: Design & Process Mapping

- [ ] Map current decision workflows: automated, human-led, hybrid
- [ ] Identify gaps: Which decisions lack individual human review?
- [ ] Design corrections: Insert human review checkpoint *before* decision affects individual
- [ ] Design classification: SOVEREIGN (named reviewer + specific facts) protocol
- [ ] Design escalation: What happens when a decision is NULL (no human review)?

### Weeks 6–8: Implementation & Training

- [ ] Build audit trail system (database fields for classification, reviewer name, facts reviewed)
- [ ] Deploy decision templates (how staff document SOVEREIGN)
- [ ] Train staff (Burgess framework, your organisation's protocol, classification process)
- [ ] Launch pilot: One high-impact decision type (e.g., credit approval)
- [ ] Collect 50–100 pilot decisions; audit classifications

### Weeks 9–10: Monitoring & Adjustment

- [ ] Monthly dashboard: SOVEREIGN %, NULL %, AMBIGUOUS %
- [ ] Sample audit: Do classifications match evidence?
- [ ] Corrective actions: Any NULL findings? How are they being escalated?
- [ ] Staff feedback: Problems with the process? Adjustments needed?

### Weeks 11–12: Scale & Prepare for Certification

- [ ] Expand pilot to full scope (all significant decisions)
- [ ] Quarterly external audit (independent verifier)
- [ ] Leadership reporting: Burgess compliance as KPI
- [ ] Prepare for certification:
  - Tier 1 (Premium): SOVEREIGN ≥ 95% + independent audit
  - Tier 2 (Standard): SOVEREIGN ≥ 85% + governance documentation
  - Tier 3 (Community): Free registration; attribution to repository

---

## Sector-Specific Acceleration

### Energy & Utilities

**Current landscape:** Wave Utilities is the proof-of-concept. E.ON and British Gas remain deficient.

**Your next step:**
1. Apply BURGESS_READY_CHECKLIST to billing decisions and forced-entry warrants
2. **Quick win:** Meter freezes and disconnections should require individual affordability review (Equality Act, consumer law)
3. **Regulator:** Energy Ombudsman now recognises Burgess framework

**Template:** Energy billing dispute letter available in [../templates/](../templates/)

### Finance & Credit

**Current landscape:** FastLogic redesigned; ICO and FCA scrutiny increasing.

**Your next step:**
1. **Lending:** CONC 4.1 requires "affordability assessment." Burgess test: Did a named person actually assess *this individual's* circumstances?
2. **Debt recovery:** DGRO/bailiff processes should never be algorithmic. Individual review required.
3. **Credit file management:** Disputed entries require individual human review, not automated closure.

**Template:** Credit decision challenge letter available in [../templates/](../templates/)

### AI & Open-Source Platforms

**Current landscape:** OpenClaw and Hermes adopting. Commercial AI vendors resisting.

**Your next step:**
1. **Governance framework:** Use Burgess Principle as decision-governance overlay for agent/model outputs
2. **Automation boundary:** Mark where human judgment *must* intervene (safety, fairness, individual context)
3. **Transparency:** Public Burgess leaderboard drives competitive adoption

**Reference implementation:** OpenClaw PR #68692 (already merged)

### Healthcare

**Current landscape:** NHS triage case under investigation; opportunity to lead.

**Your next step:**
1. **Triage & diagnosis:** Algorithmic assistance OK, but individual clinician must review *specific patient facts* before assignment/recommendation
2. **Safety converges with accountability:** "Did a clinician review this patient individually?" is both GDPR Article 22 and patient-safety question
3. **Disability & access:** Individual review must accommodate communication needs (hearing loss, language, cognitive preferences)

**Reference case:** Healthcare triage case study in [../case-studies/CASE_STUDY_HEALTHCARE_TRIAGE.md](../case-studies/CASE_STUDY_HEALTHCARE_TRIAGE.md)

### Public Sector & Benefits

**Current landscape:** DWP, councils, ombudsman all facing automation scrutiny.

**Your next step:**
1. **Benefits entitlement:** No automated rejections without individual case review
2. **Council tax & enforcement:** No bulk notices; each property requires individual assessment
3. **Ombudsman complaints:** Now reference individual human review as evidentiary standard

**Reference case:** Darlington case in [../LIVE_AUDIT_LOG.md](../LIVE_AUDIT_LOG.md)

---

## Integration with Existing Frameworks

### GDPR Article 22 (Automated Individual Decision-Making)

The Burgess test operationalises Article 22's requirement for "meaningful human involvement":

- **SOVEREIGN** = Article 22 satisfied (human reviewed before decision)
- **NULL** = Article 22 breach (no individual human review)
- **AMBIGUOUS** = Institution failed to confirm; process vague

### DUAA 2025 Articles 22A–22D (Meaningful Human Involvement)

Direct alignment:

| DUAA requirement | Burgess operationalisation |
|---|---|
| "Meaningful human involvement" in automated decisions | SOVEREIGN classification ≥ 95% |
| Individual's right to object to processing | NULL finding triggers automatic right to human review |
| Right to explanation | AMBIGUOUS finding pressures institution to clarify; SOVEREIGN provides clear explanation |

### EU AI Act (Articles 14, 26, 86)

**Article 14:** Effective human oversight  
→ SOVEREIGN = human oversight confirmed; NULL = oversight absent

**Article 26:** Deployer obligations  
→ Deployer must demonstrate SOVEREIGN classifications; audit trail is deployer's evidence

**Article 86:** Right to explanation  
→ AMBIGUOUS classifications fail Article 86; SOVEREIGN satisfies it

### NIST AI RMF

See dedicated mapping: [../papers/NIST_AI_RMF_MAPPING.md](../papers/NIST_AI_RMF_MAPPING.md)

Quick alignment:
- **Govern:** Establish accountability for SOVEREIGN classification
- **Map:** Document where human review does/doesn't occur
- **Measure:** Track SOVEREIGN % as KPI
- **Manage:** Use NULL findings as corrective-action triggers
- **Monitor:** Monthly dashboard; investigate regressions

---

## Certification & Licensing

### Tier 1: Burgess-Ready Premium Certification

**Status:** Available Q3 2026 (UK00004343685 mark registration expected)

**Eligibility:**
- SOVEREIGN ≥ 95%
- Independent audit confirms
- Annual $5,000 fee
- Right to use certification mark in marketing/compliance

**Timeline:** Apply now; audit happens when ready; certification granted upon audit success

**Who's eligible now:** Wave Utilities, FastLogic (post-redesign), any organisation with ≥ 95% SOVEREIGN documented

### Tier 2: Governance License

**Status:** Available now

**Eligibility:**
- Committed to Burgess governance framework
- Governance documentation filed
- Commitment to audit within 12 months
- $1,500 annual fee
- Can reference "adopting Burgess Principle governance" in communications (not the mark)

**Who's eligible now:** Any organisation with board approval and governance charter

### Tier 3: Community License

**Status:** Available now (free)

**Eligibility:**
- Using framework for internal governance/research
- Attribution to repository
- Public commitment to transparency

**Cost:** $0

**Who's eligible:** Anyone

---

## Contributing

### Add Your Organisation

**Want to be listed on INSTITUTIONAL_ADOPTION_TRACKER.md?**

1. Complete [BURGESS_READY_CHECKLIST.md](./BURGESS_READY_CHECKLIST.md)
2. Open a GitHub issue with:
   - Organisation name
   - Sector
   - Implementation scope
   - SOVEREIGN % and evidence
   - Contact information

3. Verification team reviews and adds you to tracker

### Contribute a Case Study

**Have you implemented Burgess and resolv a NULL case?**

Use the template: [../case-studies/CASE_STUDY_TEMPLATE.md](../case-studies/CASE_STUDY_TEMPLATE.md)

## Resources

| Document | Purpose |
|---|---|
| **[BURGESS_READY_CHECKLIST.md](./BURGESS_READY_CHECKLIST.md)** | 30-point readiness assessment + implementation roadmap |
| **[INSTITUTIONAL_ADOPTION_TRACKER.md](./INSTITUTIONAL_ADOPTION_TRACKER.md)** | Registry of adoptions, regulatory engagement, licensing |
| **[PUBLIC_LEADERBOARD.md](./PUBLIC_LEADERBOARD.md)** | Transparent sector-by-sector audit of who has individual review |
| **[../papers/NIST_AI_RMF_MAPPING.md](../papers/NIST_AI_RMF_MAPPING.md)** | NIST framework alignment |
| **[../GETTING_STARTED.md](../GETTING_STARTED.md)** | For individuals asking the question of organisations |
| **[../case-studies/](../case-studies/)** | Real-world examples of Burgess implementation |
| **[../templates/](../templates/)** | Letter templates for escalating NULL findings |

---

## Questions?

- **For organisations:** adoption@burgess-principle.limited (launching Q2 2026)
- **For individuals:** Use [../GETTING_STARTED.md](../GETTING_STARTED.md) or [Iris](../iris.html)
- **For developers/integrators:** Open an issue; see Phase 3 integration modules (coming)

---

**Adoption resources version:** 1.0 (May 2026)  
**License:** MIT (adapt for your context)  
**Certification Mark:** UK00004343685 (grants expected Q3 2026)

*This is a living directory. Contributions welcome.*
