# 🔍 Tracer — Defect Schema Library

The `tracer/` directory contains the **Tracer Protocol**, a library of
predefined "Facial Defects" that can render a corporate warrant or contract
**Void Ab Initio** under the Burgess Principle.

It now also includes lightweight helpers for building **audit-ready trace
findings** and **structured trace reports**, which fits the repository's
current release focus on clearer evidence flows, standardized records, and
human-review auditability.

## What's here

| File | Purpose |
|---|---|
| `tracer.py` | Python module defining `DEFECT_SCHEMA` plus lookup and report helpers (`get_defect`, `list_defects`, `build_trace_finding`, `build_trace_report`). |
| `DEFECT_SCHEMA.md` | Human-readable reference listing every defect, its description, and the legal axiom it violates. |

## How it relates to `verify_scrutiny.py`

`verify_scrutiny.py` (in the project root) answers a binary question:
**Was individual scrutiny applied?** — returning `SOVEREIGN` (1) or `NULL` (0).

The Tracer module is the *investigative* companion. Use it to **identify and
log the specific defects** found in an institution's process, then feed the
results into `verify_scrutiny.py` to obtain a formal binary verdict.

**Typical workflow:**

1. Import defect definitions from `tracer.py` to catalogue issues found in a
   warrant or contract.
2. Build trace findings and a structured report describing the detected defects
   and supporting evidence.
3. Record the reasoning text that documents those issues.
4. Pass the reasoning text and its SHA-256 hash to `verify_scrutiny.py` to
   produce a `SOVEREIGN` or `NULL` result.

## Quick example

```python
from tracer.tracer import (
    build_trace_report,
    get_defect,
    list_defects,
)

# See all known defect IDs
print(list_defects())        # ['DEFECT_01', 'DEFECT_02', ...]

# Look up a specific defect
defect = get_defect("DEFECT_01")
print(defect["title"])       # Bulk Approval Without Scrutiny
print(defect["axiom"])       # Violates 'The Judicial Mind.' ...

# Build an audit-ready report for later review
report = build_trace_report(
    ["DEFECT_01", "DEFECT_03"],
    reasoning="Batch handling and false safety claims were documented.",
    evidence_by_id={
        "DEFECT_01": "Witness statement describing batch-approved warrants.",
        "DEFECT_03": "Transcript claiming a gas leak without corroboration.",
    },
)
print(report["defect_ids"])  # ['DEFECT_01', 'DEFECT_03']
```
