# Public Leaderboard: Burgess-Ready vs. Burgess-Deficient Systems

**Transparency in AI governance: Which institutions have verified individual human review?**

*Last updated: May 8, 2026*

---

## Executive Summary

This leaderboard tracks organisations and systems against a simple binary:

- **🟢 BURGESS-READY**: Organisation has documented SOVEREIGN (individual human review) classification ≥ 95% for significant decisions affecting individuals
- **🟡 BURGESS-ACKNOWLEDGED**: Organisation has adopted the framework but is still implementing (target ≥ 85% SOVEREIGN)
- **🔴 BURGESS-DEFICIENT**: Organisation has NOT demonstrated individual human review; decisions appear to be automated bulk-processing

This leaderboard is **not** a judgment of institutional quality overall. It is a specific, verifiable measure: Does this organisation ensure that humans individually review decisions *before* they affect specific people?

---

## Burgess-Ready Systems (🟢)

### Verified: Individual Review Confirmed ≥95%

| System/Organisation | Sector | Key Decisions | SOVEREIGN % | Evidence | Verified Date |
|---|---|---|---|---|---|
| **Wave Utilities** | Water/Retail | Billing disputes, meter adjustments, enforcement escalations | 100% (2/2 resolved cases) | Public case study; settlement documented | April 27, 2026 |
| **OpenClaw (Burgess Governance Module)** | Open Intelligence | Access control, contributor status, community decisions | Target: 90%+ (implementing) | PR #68692; governance module in code | April 18, 2026 |
| **FastLogic Lending Ltd (Post-Redesign)** | FinTech / Credit | Self-employed applicant affordability | 89% (77/89 retroactive cases approved; 12 reversed) | FCA improvement direction; case study | May 2026 |

---

## Burgess-Acknowledged Systems (🟡)

### In Progress: Adoption Underway, Target ≥85%

| System/Organisation | Sector | Implementation Status | Timeline | Accountability |
|---|---|---|---|---|
| **NousResearch / Hermes Agent** | AI Agents | Governance framework for agent decision-making | PR #12265 (open, 99.1k stars) | Awaiting maintainer integration |
| **The Burgess Principle Limited** | Governance/Certification | Internal certification & licensing operations | Q3 2026 (UK00004343685) | Founder/Director accountability |

---

## Burgess-Deficient Systems (🔴)

### Documented: Automated Decisions Without Individual Human Review

Systems that have been formally asked whether individual human review occurred *before* decisions affected individuals, and the answer was "no" (NULL) or evasive (AMBIGUOUS unresolved).

| System/Organisation | Sector | Decision Type | Classification | Regulator | Status |
|---|---|---|---|---|---|
| **E.ON Next (Warrant Issuance)** | Energy | Forced entry warrants | NULL | ICO, EHRC, Ombudsman | Ongoing (case EG021819-26) |
| **British Gas (Meter Freeze)** | Energy | Automated meter freeze + billing adjustment | NULL | Ombudsman | Ongoing (case EG037844-26) |
| **HMCTS / Judiciary (Warrant Processing)** | Justice System | Unsigned warrant issuance | NULL (system admits no individual review) | ICO, EHRC | Submitted to court review |
| **Passport Office (Biometric Processing)** | Identity | Passport biometric verification & issuance | NULL at issuance stage | ICO, Article 22 challenge | Ongoing (case reference: CASE_STUDY_PASSPORT.md) |
| **Equita (Bulk Enforcement)** | Collections | Enforcement statements, council tax notices | NULL (processed in bulk) | LGO, ICO | Ongoing (6 DBC cases) |
| **OpenAI Ireland Limited** | AI / Language | Article 15 Data Subject Access Request (DSAR) processing | NULL (automated authentication denial; no named human) | ICO | Complaint filed IC-4999654-T1Q8 |
| **Amazon (Ad Insertion)** | Streaming / Platform | Ad placement in paid subscriptions (Article 22 GDPR violation) | NULL (algorithmic insertion) | ICO, FCA | Complaint pending (April 26, 2026) |
| **Equifax (Credit File Management)** | Finance / Credit | CCJ (County Court Judgment) entries; automated case closure | NULL (closure without individual review of dispute) | ICO, FCA | Ongoing |
| **Lowell Financial Ltd (Debt Recovery)** | Finance / Collections | Purchased debt portfolio enforcement | NULL (bulk pipeline) | Ombudsman | Resolved (ceased enforcement) |

---

## Sector Analysis

### Energy & Utilities

| Organisation | Status | SOVEREIGN % | Trend | Notes |
|---|---|---|---|---|
| **Wave Utilities** | 🟢 Ready | 100% | ↑ | Proof of concept; full resolution achieved |
| **E.ON** | 🔴 Deficient | 0% | ← | Forced entry under unsigned warrant; no individual review |
| **British Gas** | 🔴 Deficient | 0% | ← | Automated meter shutdown without individual review |

**Sector trend:** Automation is dominant in metering and billing. Only Wave has demonstrated individual human review.

### Finance & Credit

| Organisation | Status | SOVEREIGN % | Trend | Notes |
|---|---|---|---|---|
| **FastLogic Lending** | 🟢 Ready | 89% | ↑ | Post-redesign; self-employed applicants now individually reviewed |
| **Equifax / Credit Files** | 🔴 Deficient | 0% | ← | Automated entry management without individual dispute review |
| **Lowell Financial** | 🔴 Deficient | 0% | ← | Bulk-purchased debt processed without individual affordability review |

**Sector trend:** Automation dominates lending and debt recovery. Regulatory pressure (FCA, ICO) prompting change.

### AI & Platforms

| Organisation | Status | SOVEREIGN % | Trend | Notes |
|---|---|---|---|---|
| **OpenClaw** | 🟡 Acknowledged | TBD (target 90%+) | ↑ (implementing) | Governance framework adopted; individual decisions now classified |
| **Hermes Agent (NousResearch)** | 🟡 Acknowledged | TBD (target 85%+) | ↑ (implementing) | Agent decision-making framework; PR open |
| **OpenAI (DSAR & Ad Serving)** | 🔴 Deficient | 0% | ← | Article 15 access denied via automation; ads inserted algorithmically |
| **Amazon** | 🔴 Deficient | 0% | ← | Paid subscription ad insertion without individual review |

**Sector trend:** Open-source projects leading adoption. Commercial AI/platform vendors resisting transparency.

### Healthcare

| System | Status | SOVEREIGN % | Regulator | Notes |
|---|---|---|---|---|
| **NHS Emergency Triage (Anonymised)** | 🔴 Deficient | 0% (at algorithm stage) | ICO, CQC | Manchester Triage Protocol applied without pre-algorithm clinician review |

**Sector trend:** Healthcare begins to face scrutiny; safety + individual review are converging concerns.

### Government & Public Sector

| System | Status | SOVEREIGN % | Regulator | Notes |
|---|---|---|---|---|
| **HMCTS Warrant Processing** | 🔴 Deficient | 0% | ICO, EHRC | Automated warrant issuance; unsigned documents |
| **Darlington Borough Council** | 🔴 Deficient | 0% (likely) | LGO, ICO | Bulk council tax notices; no individual review alleged |
| **DWP Benefits (Generalised)** | 🔴 Deficient (presumed) | TBD | DWP, ICO | No public Burgess testing yet; high automation suspected |

**Sector trend:** Government bulk-processing widespread; regulatory investigations active.

---

## How This Leaderboard is Maintained

### Verification Criteria

**🟢 BURGESS-READY (SOVEREIGN ≥ 95%):**
- Independent audit confirming classification
- OR public case study with verified outcome
- OR regulatory confirmation (ICO, FCA, ombudsman)
- + Governance documentation

**🟡 BURGESS-ACKNOWLEDGED (≥ 85%):**
- Public commitment + governance documentation
- Implementation underway (not yet audited)
- Target date for 95%+ SOVEREIGN

**🔴 BURGESS-DEFICIENT:**
- Formal inquiry ("Do you individually review decisions?")
- Response: "No" (NULL) OR evasive (AMBIGUOUS unresolved)
- Documented via public records, regulator, case study

### Evidence Standards

- **Case study:** Factual account from affected party, organisation, or regulator
- **Regulatory:** ICO decision, FCA directive, ombudsman ruling, CQC finding
- **Public records:** FOI response, court documents, signed commitments
- **Self-attestation:** Only with independent audit or third-party verification

### Dispute Process

**If an organisation disputes its categorisation:**
1. Submit written challenge with evidence
2. Independent review by Burgess Principle governance committee
3. Recategorisation if evidence warrants it
4. Public notation of dispute (if unresolved)

---

## What This Leaderboard Tells You

### For Consumers/Users:

- **🟢 Burgess-Ready system?** This organisation has verified that humans individually review decisions before you're affected. Higher confidence in fairness.
- **🔴 Burgess-Deficient system?** This organisation has chosen (or defaulted to) automation without individual human review. If a decision harms you, it may lack legal defensibility.

### For Regulators (ICO, FCA, CQC, etc.):

- **Audit lens:** Use Burgess classification as KPI for meaningful human involvement compliance
- **Comparative analysis:** Which sectors are leading? Which are lagging?
- **Enforcement trigger:** NULL findings → compliance action

### For Investors & Board Members:

- **Governance quality:** Burgess-ready organisations have documented individual accountability; lower legal/reputational risk
- **Regulatory trend:** Deficiency now often = regulator investigation later
- **Competitive advantage:** "Burgess-Ready" certification can differentiate in regulated sectors (finance, healthcare, energy)

---

## Key Observations (May 2026)

1. **Automation is the default.** Most organisations have NOT demonstrated SOVEREIGN classification. Only Wave and revised FastLogic have 85%+.

2. **Regulation is catching up.** ICO, FCA, CQC now audit individual human review as part of Article 22 / CONC / safety compliance.

3. **Open-source leading.** OpenClaw and Hermes adoption shows open-source projects embrace transparency faster than commercial platforms.

4. **Sector patterns:**
   - **Energy:** Automation without override (e.g., forced entry, meter freezes) = high NULL rate
   - **Finance:** Algorithmic credit/affordability decisions beginning to face scrutiny; regulation forcing redesign
   - **Platforms:** Resisting transparency; multiple NULL findings unpublic
   - **Healthcare:** Safety concerns + individual review = emerging convergence
   - **Public sector:** Bulk-processing widespread; regulator attention increasing

5. **Regulatory momentum:** Every NULL finding filed with ICO/FCA/ombudsman increases pressure on deficient systems to change.

---

## Future Leaderboard (Aspirational)

By **Q4 2026**, we expect:

| Sector | Burgess-Ready (🟢) | Burgess-Acknowledged (🟡) | Burgess-Deficient (🔴) |
|---|---|---|---|
| **Energy** | 3+ organisations | 2+ | 1–2 (under regulatory pressure) |
| **Finance** | 2+ (lenders, credit issuers) | 3+ | Declining (FCA pressure) |
| **AI/Open-source** | 2+ (LangChain, etc.) | 4+ (frameworks adopting) | Platform vendors under scrutiny |
| **Healthcare** | 0–1 (NHS redesign?) | 1+ | 0–1 (CQC oversight) |
| **Public sector** | 0 | 1+ (council, DWP pilots?) | 2–3 (ombudsman pressure) |

---

## Contribute to This Leaderboard

**Have evidence of a Burgess-Ready or Burgess-Deficient system?**

1. Open a GitHub issue with:
   - Organisation name
   - Sector
   - Evidence (case study, regulator finding, audit result, public commitment)
   - Links to supporting documentation

2. Or submit a pull request updating this file

3. Evidence will be independently verified before publication

---

## Disclaimer

This leaderboard is **informational only**. Categorisations reflect publicly available evidence and formal inquiries answered. It is not legal advice, and categorisation does not determine compliance with applicable law (GDPR, DUAA, AI Act, sector-specific regulation).

Organisations not listed may have adopted the Burgess Principle privately or may not yet have been formally inquired. Listing is not comprehensive; this is a *public record of documented cases*.

---

**Leaderboard version:** 1.0 (May 2026)  
**Maintained by:** The Burgess Principle Limited & Community  
**License:** Data published under MIT; attribution appreciated  
**Certification Mark:** UK00004343685

*Next update: June 1, 2026*  
*Questions?* Open an issue or contact adoption@burgess-principle.limited
