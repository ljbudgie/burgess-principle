# Verifiable Human Oversight

**Part of the Burgess Principle ecosystem**  
**Version:** 0.1.0 (Phase 1 — MVP)  
**Language:** Python 3.11+  
**Dependencies:** stdlib only (no Pydantic, no third-party packages required for core)

---

## What this does

This module implements the **Burgess Binary Test** as executable, verifiable code.

It answers one question:

> "Was a named human being's mind applied to the specific facts of a specific person's case before institutional power was exercised?"

The answer is `SOVEREIGN`, `NULL`, or `AMBIGUOUS`. Every assessment produces a sealed `DecisionRecord` with a SHA-256 fingerprint — a tamper-evident record of the finding that can be transmitted, stored, and independently verified.

---

## Quick start

```python
from verifiable_oversight import BinaryTest, Verifier
from verifiable_oversight.domains import CommunicationDomain

domain = CommunicationDomain()

record = domain.create_record(
    subject="Fourth response — circular referral to EHRC",
    institution="EASS",
    binary_test=BinaryTest(
        named_person=None,
        role_and_authority=None,
        specific_facts_considered=None,
        pre_decision_timing=None,
        authority_to_differ=None,
        context="Four responses. No named individual. Circular referral.",
    ),
    channel="email (telephone number provided)",
    ra_on_record=True,
    ra_description="email-only communication",
    channel_accessible=False,
)

print(record)
# DecisionRecord(…) [NULL] EASS — Fourth response — circular referral to EHRC

verifier = Verifier()
report = verifier.verify(record)
print(report.is_valid)   # True — the NULL finding is correctly documented
print(record.fingerprint)  # SHA-256 fingerprint
```

---

## The five elements

All five must be present for `SOVEREIGN`. Any single absent element yields `NULL`.

| Element | What it requires |
|---|---|
| **Named person** | The full name of the individual — not "our team" |
| **Role and authority** | Their role AND the authority to reach a different outcome |
| **Specific facts considered** | Evidence this specific person's facts were reviewed |
| **Pre-decision timing** | Review happened *before* the decision was exercised |
| **Authority to differ** | Practical authority to reach a different conclusion |

**Process language does not satisfy any element.** "Reviewed by our team", "subject to human oversight", "considered by the relevant department" — zero elements. Ask directly: *"Please provide the full name and role of the individual who considered my specific case before this decision was made."*

---

## Structure

```
verifiable-oversight/
├── __init__.py              # Top-level package — import BinaryTest, DecisionRecord, Verifier here
├── core/
│   ├── binary_test.py       # Five-element engine → SOVEREIGN / NULL / AMBIGUOUS
│   ├── decision_record.py   # Sealed record with SHA-256 fingerprint
│   └── verifier.py          # Integrity + logical consistency validation
├── domains/
│   ├── base.py              # Abstract domain — extend to add new domains
│   ├── general.py           # No-extension baseline
│   ├── communication.py     # EA 2010 ss.20/21 channel accessibility
│   └── legal.py             # Enforcement, bulk process, burden shift
├── templates/
│   └── decision_record.json # Template for manual record creation
├── examples/
│   ├── example_sovereign.py # LGO Rebecca Hunt — SOVEREIGN process, wrong law
│   ├── example_null.py      # EASS Rachel.D — NULL, circular referral
│   └── example_ambiguous.py # Trading 212 — AMBIGUOUS pending answer
└── docs/
    └── specification.md     # Full specification with legal grounding
```

---

## Running the examples

From the repo root:

```bash
python verifiable-oversight/examples/example_null.py
python verifiable-oversight/examples/example_sovereign.py
python verifiable-oversight/examples/example_ambiguous.py
```

No installation required. stdlib only.

---

## Verdicts

| Verdict | Meaning |
|---|---|
| `SOVEREIGN` | All five elements present. Named human applied their mind to specific facts before the decision. |
| `NULL` | One or more elements absent. No evidence of meaningful human review meeting the Burgess standard. |
| `AMBIGUOUS` | Element status unknown — institution has not yet answered the direct question. Temporary state only. |

`NULL` ≠ illegal in all cases, but it is the prerequisite question before any legal challenge. A `NULL` process is a defective process. Under *Ahmed [2010] UKSC 5* and *Majera [2021] UKSC 46*, an unlawful institutional act cannot found enforceable rights against an individual regardless of what label is applied to it.

---

## Domains

Each domain extends the core test with domain-specific metadata and validation:

| Domain | What it adds |
|---|---|
| `general` | No extensions — pure binary test |
| `communication` | Channel vs RA compatibility; automated comms flag; regulatory framework |
| `legal` | Statutory basis; case reference; burden shift; bulk process presumption |

To add a new domain, subclass `BaseDomain` and implement `name`, `guidance`, and optionally `validate_domain_metadata` and `_build_domain_metadata`.

---

## Cryptographic integrity

Every `DecisionRecord` is sealed with a SHA-256 fingerprint on creation. The fingerprint covers all content fields. Any change to the record after sealing will cause `verify_integrity()` to return `False`.

The `signature` field is reserved for Ed25519 / post-quantum signing (Phase 2). The data model supports it without structural changes — the signing infrastructure connects to the existing [`CRYPTOGRAPHIC_IDENTITY.md`](../CRYPTOGRAPHIC_IDENTITY.md) architecture.

---

## Phase 2 roadmap

- **Cryptographic signing** — Ed25519 private key → `signature` field populated; public key published for independent verification
- **Record storage** — append-only SQLite or JSON-L log; records keyed by fingerprint
- **Iris integration** — Iris can create and verify records on behalf of a user in conversation
- **Email domain** — sovereign email application; each outbound communication creates a record; each institutional response is assessed on receipt
- **Banking domain** — FCA DISP deadlines; automated credit decision assessment
- **Medical domain** — clinical decision support; consent; Mental Capacity Act 2005

---

## Legal grounding

This module implements the Burgess standard as described in the SSRN working paper series. See [`papers/SSRN_INDEX.md`](../papers/SSRN_INDEX.md) and [`LEGAL_FOUNDATIONS.md`](../LEGAL_FOUNDATIONS.md).

Key authorities: EA 2010 ss.6/19/20/21/27/136/149 · DUAA 2025 s.80 · Ahmed [2010] UKSC 5 · Majera [2021] UKSC 46 · ZH [2011] UKSC 4 · FirstGroup v Paulley [2017] UKSC 4
