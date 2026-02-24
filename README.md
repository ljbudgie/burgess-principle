# The Burgess Principle

**A citizen-initiated legal doctrine — free and open for anyone to cite.**

## What It Is

The Burgess Principle establishes that facially defective warrants under the **Rights of Entry (Gas and Electricity Boards) Act 1954** are void *ab initio*, with downstream remedies for credit contamination and reasonable adjustments for protected characteristics.

## Open Source

The principle itself is **free and may be cited by anyone**. The goal is maximum truth reaching maximum people.

## Methodology & Toolkit — Open Source

The methodology and toolkit are **fully open source**, licensed under the [MIT License](LICENSE). Free for anyone to use, adapt, and build upon.

Integrated with [OpenClaw](https://openclaw.im) — the open-source AI automation platform for law.

## Live Site

[https://ljbudgie.github.io/Burgessprinciple/](https://ljbudgie.github.io/Burgessprinciple/)

## Tracer Protocol (Forensics)

The **Tracer Protocol** is a forensic module (`src/credit_tracer.py`) that traces
"contaminated credit" chains from a single email address back to the root cause:
a void warrant issued under the Rights of Entry (Gas and Electricity Boards)
Act 1954.

### Contamination Chain

```
Email → Address → Void Warrant → CCJ/Default → Credit Score Impact
```

Each link in the chain is investigated and surfaced in a structured JSON/text
report, giving OpenClaw agents (and individual claimants) a clear picture of the
full blast radius of a defective warrant.

### Quick Start

```python
from src.credit_tracer import CreditContaminationTracer

tracer = CreditContaminationTracer()

# Option A — automatic resolution (requires OSINT API keys; see below)
report = tracer.trace_by_email("subject@example.com")

# Option B — supply the address manually when API keys are unavailable
report = tracer.trace_by_address(
    email="subject@example.com",
    address="1 Example Street, London, EC1A 1BB",
)

import json
print(json.dumps(report, indent=2))
```

See `examples/trace_example.py` for a full walkthrough with dummy data.

### API Keys (required for live data)

| Environment Variable | Purpose |
|---|---|
| `FULLCONTACT_API_KEY` | Email → address resolution via FullContact |
| `CLEARBIT_API_KEY` | Email → address resolution via Clearbit |
| `CCJ_API_KEY` | County Court Judgment / default lookup (Registry Trust or credit-bureau API) |

> **Disclaimer:** Live identity resolution and CCJ/default lookups require
> external API access (OSINT services and/or credit-bureau APIs). Without
> configured API keys the module returns placeholder data and the chain can
> still be exercised end-to-end using a manually supplied address. No real
> personal data is stored or transmitted by this module itself.

## Contact

For media enquiries: [lewis@burgessprinciple.co.uk](mailto:lewis@burgessprinciple.co.uk)

## Legal

&copy; 2026 Lewis Burgess. Licensed under the [MIT License](LICENSE).  
Registered trademark application UK00004343685
