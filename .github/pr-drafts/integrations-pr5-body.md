### What this changes
- Adds framework-specific PR templates for:
  - LlamaIndex
  - AutoGen
  - CrewAI
- Adds OpenClaw integration case-study reference for implementation pattern and adoption signal.

### Why this matters
This package accelerates ecosystem adoption by giving maintainers reusable, framework-specific governance overlays and review-ready PR language.

### Validation
- Documentation-only changes
- No runtime code modified
- Consistent Burgess Compliance Note format retained across templates

### Risk and mitigation
- Scope risk mitigated by isolating remaining integration templates from LangChain PR
- Overclaim risk mitigated by positioning as templates/reference and preserving factual qualifiers

### Burgess Compliance Note
- **What changes:** Adds additional integration templates and an OpenClaw integration reference case.
- **Effect on meaningful human involvement:** **Strengthens** by lowering integration friction for named human-review checkpoints and escalation controls.
- **Doctrinal sections touched:** None.
- **Risk and mitigation:** Template/reference framing reduces implementation and overclaim risk.
- **Burgess test applied to this change:** **SOVEREIGN** (prepared for human-reviewed merge process).
