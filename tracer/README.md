# 🔍 Tracer — Defect Schema Library

The `tracer/` directory contains the **Tracer Protocol**, a library of
predefined "Facial Defects" that can render a corporate warrant or contract
**Void Ab Initio** under the Burgess Principle.

## What's here

| File | Purpose |
|---|---|
| `tracer.py` | Python module defining `DEFECT_SCHEMA` and helper functions (`get_defect`, `list_defects`) for looking up known defect types. |
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
2. Record the reasoning text that documents those issues.
3. Pass the reasoning text and its SHA-256 hash to `verify_scrutiny.py` to
   produce a `SOVEREIGN` or `NULL` result.

## Quick example

```python
from tracer.tracer import list_defects, get_defect

# See all known defect IDs
print(list_defects())        # ['DEFECT_01', 'DEFECT_02', ...]

# Look up a specific defect
defect = get_defect("DEFECT_01")
print(defect["title"])       # Bulk Approval Without Scrutiny
print(defect["axiom"])       # Violates 'The Judicial Mind.' ...
```
