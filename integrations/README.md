# Integrations — Burgess Principle in AI Frameworks

**Integration patterns and PR templates for the most impactful AI platforms**

---

## Overview

This directory contains:

- **[LANGCHAIN_BURGESS_OVERLAY.md](./LANGCHAIN_BURGESS_OVERLAY.md)** — Production-ready governance layer for LangChain chains and agents; copy-paste code + PR template
- **Integration modules for:** LlamaIndex, AutoGen, CrewAI, OpenClaw, Hermes (coming)
- **High-visibility PR templates:** Ready to submit to major AI frameworks

---

## What Is This For?

When you build an AI chain or agent, you often include:

- LLM calls
- Tool invocations
- Decision logic that affects individuals

**The question:** When does a human *actually review* the decision before it affects someone?

**The answer:** Burgess Principle governance layer tracks this. It classifies every decision:

- **SOVEREIGN** = Named person reviewed specific facts before decision
- **NULL** = No individual review; decision was automated
- **AMBIGUOUS** = Process unclear; unclear if human reviewed

---

## Why Integrate?

### For Users

They get **transparency:** Can ask "who reviewed my case?" and get a named, identifiable answer.

### For Teams Building AI

- **Regulatory compliance** — GDPR 22, DUAA 2025, EU AI Act now expect this
- **Liability reduction** — Named reviewers + audit trail = defensible decisions
- **Competitive advantage** — "Burgess-Ready" certification signals trustworthiness
- **Market signal** — Early adopters capture the "ethical AI" segment

### For the Ecosystem

Early integration into major frameworks (LangChain, LlamaIndex, AutoGen, CrewAI, OpenClaw, Hermes) sets the standard. The first framework to make Burgess governance the *default* wins the market for responsible AI.

---

## Integration Modules (Status)

| Framework | Status | Key Use Cases | PR Link |
|---|---|---|---|
| **LangChain** | ✅ READY | General-purpose chains, agents, Q&A | [LANGCHAIN_BURGESS_OVERLAY.md](./LANGCHAIN_BURGESS_OVERLAY.md) |
| **LlamaIndex** | 🏗️ IN PROGRESS | RAG systems, document analysis | (coming) |
| **AutoGen** | 🏗️ IN PROGRESS | Multi-agent systems | (coming) |
| **CrewAI** | ⏹️ QUEUED | Agent teams, role-based workflows | (coming) |
| **OpenClaw** | ✅ MERGED | Large multi-agent system (#68692) | [View PR](https://github.com/OpenClaw/openclaw) |
| **Hermes** | ⏳ PLANNED | Agent orchestration | (coming) |

---

## Integration Pattern (Reusable Template)

Every Burgess integration follows this pattern:

### 1. Classification Layer

```python
class BurgessClassification(Enum):
    SOVEREIGN = "SOVEREIGN"     # Named reviewer ✅
    NULL = "NULL"               # No reviewer ❌
    AMBIGUOUS = "AMBIGUOUS"     # Unclear process ⚠️
```

### 2. Audit Trail

```
decision_id | timestamp | classification | reviewer_name | facts_reviewed | output
-----------+-----------+----------------+---------------+----------------+---------
dec_12345  | 2026-05-01| SOVEREIGN      | Alice Wong    | [income, age]  | "approve"
dec_12346  | 2026-05-01| NULL           | (none)        | [data_points]  | "reject"
```

### 3. Escalation Gate

```python
if classification == NULL:
    raise ValueError("Decision blocked; human review required before execution")
```

### 4. Metrics Dashboard

```
Total decisions: 1,247
SOVEREIGN: 92.8% ✅
NULL: 5.1% ⚠️ (requires action)
AMBIGUOUS: 2.1% ⚠️ (clarify process)
```

---

## How to Use an Integration

### For LangChain Users (Right Now)

1. **Read:** [LANGCHAIN_BURGESS_OVERLAY.md](./LANGCHAIN_BURGESS_OVERLAY.md)
2. **Copy:** `burgess_config.py` code into your project
3. **Wrap:** Your chains with `BurgessChainWrapper`
4. **Deploy:** Flask dashboard + audit log
5. **Monitor:** Weekly SOVEREIGN % metrics

### For Framework Maintainers (Contribute)

1. **Review:** [LANGCHAIN_BURGESS_OVERLAY.md](./LANGCHAIN_BURGESS_OVERLAY.md) for pattern
2. **Adapt:** Pattern to your framework's architecture
3. **Implement:** Config classes, wrapper, audit logger, dashboard
4. **Test:** Unit + integration tests
5. **Submit:** PR with Burgess Compliance Note (template below)

---

## Burgess Compliance Note Template

Every integration PR must include:

```markdown
### Burgess Compliance Note

- **What changes:** Adds Burgess Principle governance layer to [FRAMEWORK] chains/agents
- **Effect on meaningful human involvement:** Strengthens — tracks whether individual humans reviewed decisions; escalates NULL decisions
- **Doctrinal sections touched:** None (implementation only; no doctrinal wording changed)
- **Risk and mitigation:** None — backwards compatible, opt-in, non-breaking
- **Burgess test applied to this change:** SOVEREIGN (reviewed by framework maintainers + @ljbudgie before merge)
```

---

## High-Visibility PR Targets (Priority Order)

### Tier 1: Force Multipliers (≥ 50k forks / stars)

| Project | Forks | Stars | Why | PR Title | Status |
|---|---|---|---|---|---|
| **LangChain** | 55.8k | 92.2k | Ubiquitous; immediate adoption potential | "Add Burgess Principle governance overlay for individual human review in chains/agents" | 🏗️ IN PROGRESS |
| **LlamaIndex** | 38.6k | 66.1k | RAG standard; high-stakes decisions | "Add Burgess classification layer to document-based decisions" | 🏗️ TODO |
| **AutoGen** | 32.3k | 29.9k | Multi-agent standard; complex workflows | "Add Burgess audit trail to agent decision checkpoints" | 🏗️ TODO |
| **OpenClaw** | 73.3k | 18.4k | Endorsed by Elon; massive visibility | "Add Burgess governance overlay to multi-agent decisions (#68692)" | ✅ MERGED |

### Tier 2: Sector-Specific Standards

| Project | Forks | Stars | Sector | PR Idea | Status |
|---|---|---|---|---|---|
| **Hermes Agent** | 12.5k | 8.3k | Agent orchestration | "Add Burgess decision audit to Hermes workflows" | 🏗️ TODO |
| **CrewAI** | 15.7k | 22.1k | Team-based agents | "Add Burgess audit trail to crew decision loops" | 🏗️ TODO |
| **Transformers (HF)** | 130k | 131k | ML/AI infrastructure | "Add Burgess decision classification option to pipelines" | 🏗️ MAJOR EFFORT |
| **Anthropic Claude models** | — | — | LLM provider | Integration via API; document best practices | 🏗️ PARTNER DISCUSSION |

### Tier 3: UK Public Sector & Disability Tech (High Impact + Regulatory Leverage)

| Project | Why | PR Idea | Status |
|---|---|---|---|
| **UK Cabinet Office AI Hub** | Government adoption = policy signal | "Burgess Principle governance for public-sector AI decisions" | 🏗️ OUTREACH |
| **Equality and Human Rights Commission open-source** | Disability tech + regulatory authority | "Burgess framework for accessible decision-making" | 🏗️ OUTREACH |
| **NHS Digital** | Healthcare triage case study live; immediate need | "Burgess governance for NHS triage algorithms" | 🏗️ OUTREACH |

---

## PR Workflow

### For Each High-Visibility PR

1. **Prepare** (1 week):
   - Fork repo
   - Create feature branch
   - Adapt integration module pattern
   - Write tests
   - Draft PR description

2. **Submit** (1 day):
   - Open PR with template (see below)
   - Tag framework maintainers + @ljbudgie
   - Include Burgess Compliance Note
   - Link to live case studies

3. **Iterate** (2–4 weeks):
   - Address code review
   - Refine examples
   - Validate backward compatibility
   - Respond to doctrinal questions (defer to @ljbudgie)

4. **Merge** (1 day):
   - Framework maintainers approve
   - CI passes
   - Merged to main

5. **Launch** (1 day):
   - Post-merge: announce in community
   - Add to PUBLIC_LEADERBOARD.md
   - Celebrate adoption milestone

---

## PR Template (Copy-Paste)

```markdown
# [Framework] — Add Burgess Principle Governance Overlay

## Summary

This PR adds a Burgess Principle governance overlay to [FRAMEWORK] chains/agents/decisions, enabling transparent tracking of whether individual humans reviewed decisions before they affect users.

## What

- Classification layer: `SOVEREIGN` (human reviewed) / `NULL` (automated) / `AMBIGUOUS` (unclear)
- Audit trail: JSON-based logging of all decisions
- Escalation gates: Blocks automated decisions if governance requires human review
- Metrics dashboard: Tracks SOVEREIGN %, NULL %, AMBIGUOUS %

## Why

**Compliance:**
- GDPR Article 22 (right not to be subject to automated decisions)
- DUAA 2025 Articles 22A–22D (meaningful human involvement)
- EU AI Act Articles 14/26/86 (effective human oversight)
- FCA/ICO guidance: individual human review as evidentiary standard

**Business:**
- Liability reduction via named reviewers + audit trail
- "Burgess-Ready" certification signals trustworthiness
- User adoption: people want to know "who reviewed my case?"

**Ecosystem:**
- First major framework to default Burgess governance wins "responsible AI" market

## How

1. Users instantiate `BurgessChainWrapper(your_chain, name, threshold_classification)`
2. Call `run_with_burgess(input_data, individual_context, reviewer_profile)`
3. Decision auto-classified; logged; escalated if NULL
4. Dashboard at `/burgess/metrics` shows SOVEREIGN %

## Example

```python
reviewer = ReviewerProfile(name="Alice", role="Officer", organisation="Bank")
output, classification = burgess_chain.run_with_burgess(
    input_data={"query": "assess creditworthiness"},
    individual_context="self-employed, age 42, irregular income",
    reviewer=reviewer,
)
# Output: "approved", <SOVEREIGN>
```

## Testing

- ✅ Unit tests: SOVEREIGN, NULL, AMBIGUOUS classification
- ✅ Integration tests: Audit log metrics, escalation logic
- ✅ Backward compatibility: Existing code unchanged

## Burgess Compliance Note

- **What changes:** Adds individual human review tracking to [FRAMEWORK]
- **Effect on meaningful human involvement:** Strengthens — chains now log who reviewed what; NULL decisions escalate; transparency dashboard
- **Doctrinal sections touched:** None (implementation only)
- **Risk and mitigation:** None — backwards compatible, opt-in, non-breaking
- **Burgess test applied to this change:** SOVEREIGN (reviewed by maintainers + @ljbudgie)

## Related

- Live case studies: [Wave Utilities (resolved)](../../case-studies/CASE_STUDY_WAVE.md), [FastLogic lending (resolved)](../../case-studies/CASE_STUDY_FINANCIAL_LENDING.md)
- Documentation: [Integration guide](./LANGCHAIN_BURGESS_OVERLAY.md)
- Institutional adoption tracker: [PUBLIC_LEADERBOARD.md](../../adoption/PUBLIC_LEADERBOARD.md)
- Regulatory mapping: [NIST_AI_RMF_MAPPING.md](../../papers/NIST_AI_RMF_MAPPING.md)
```

---

## Deployment & Scale-Up Roadmap

### Week 1: LangChain (Most Impactful)

- Submit LangChain PR
- Iterate + merge (target: 7–14 days)
- Post-merge: announce in r/langchain, HN, Twitter

### Weeks 2–3: Tier 1 Force Multipliers

- Submit LlamaIndex PR
- Submit AutoGen PR
- OpenClaw already merged

### Weeks 4–5: Tier 2 Sector-Specific

- Submit Hermes + CrewAI PRs
- Prepare Hugging Face Transformers integration

### Weeks 6–8: Ecosystem Traction

- Target: 3–5 PRs merged
- Public leaderboard updated with all adoptions
- Media + community announcements

### Weeks 9–12: Regulatory & Institutional

- NHS Digital integration (healthcare case study leverage)
- UK Cabinet Office outreach (government AI policy)
- Equality Commission partnership (disability + accessibility)

---

## Success Metrics

By end of Phase 3 (90 days):

- [ ] ≥ 3 integration PRs merged (LangChain, LlamaIndex, AutoGen)
- [ ] ≥ 150 GitHub stars (likely met; Wave + OpenClaw + new PRs)
- [ ] ≥ 5 institutional adoptions (Wave, FastLogic, OpenClaw, NHS, NousResearch target)
- [ ] Whitepaper published (ready for SSRN)
- [ ] Burgess Principle cited in regulatory guidance (ICO, FCA, CQC + ombudsmen)
- [ ] Certification mark granted (UK00004343685 grant expected Q3 2026)

---

## Contributing

### I Want to Adapt This Pattern for [Framework]

1. Copy [LANGCHAIN_BURGESS_OVERLAY.md](./LANGCHAIN_BURGESS_OVERLAY.md)
2. Replace `langchain` examples with your framework's API
3. Keep the structure: config → wrapper → audit → dashboard
4. Add sector-specific examples (credit, healthcare, moderation, etc.)
5. Open an issue with draft; we'll refine together
6. Submit PR to this repo with your adapted module

### I Want to Submit a PR to [High-Visibility Project]

1. Read [LANGCHAIN_BURGESS_OVERLAY.md](./LANGCHAIN_BURGESS_OVERLAY.md)
2. Adapt for your target framework
3. Use PR template above
4. Tag @ljbudgie for doctrinal review
5. Link to adoption tracker + case studies
6. We'll amplify the announcement

---

## Resources

| Resource | Link |
|---|---|
| **Burgess overview** | [../../README.md](../../README.md) |
| **GETTING_STARTED (for end users)** | [../../GETTING_STARTED.md](../../GETTING_STARTED.md) |
| **Regulatory mapping** | [../../papers/NIST_AI_RMF_MAPPING.md](../../papers/NIST_AI_RMF_MAPPING.md) |
| **Adoption readiness** | [../../adoption/BURGESS_READY_CHECKLIST.md](../../adoption/BURGESS_READY_CHECKLIST.md) |
| **Case studies** | [../../case-studies/](../../case-studies/) |
| **Institutional tracker** | [../../adoption/INSTITUTIONAL_ADOPTION_TRACKER.md](../../adoption/INSTITUTIONAL_ADOPTION_TRACKER.md) |

---

## Questions?

- **Technical:** Open an issue in the Burgess Principle repo
- **Regulatory/Doctrinal:** Tag @ljbudgie
- **PR strategy:** Discuss in issues; we coordinate timing + messaging
- **Ready to submit?** Let us know; we'll prepare draft + coordinate review

---

**Version:** 1.0 (Phase 3 Initial)  
**Status:** LangChain ready; others in progress  
**License:** MIT (adapt for your context)

*This is the force multiplier phase. One integrated PR early = exponential ecosystem adoption.*
