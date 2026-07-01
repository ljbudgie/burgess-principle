# Verifiable Human Oversight

**Part of the Burgess Principle ecosystem**  
**Version:** 0.5.0 (Phase 5 — Mental Capacity Act 2005 capacity domain, extending Phase 4 email, banking & medical domains, institution registry, deadline engine, Iris integration)  
**Language:** Python 3.11+  
**Dependencies:** stdlib only for the core test and records. Ed25519 signing is an optional add-on requiring [PyNaCl](https://pypi.org/project/PyNaCl/) (`pip install PyNaCl`).

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
│   ├── decision_record.py   # Sealed record with SHA-256 fingerprint + signature
│   ├── signing.py           # Ed25519 RecordSigner + verify_record_signature (Phase 2)
│   ├── storage.py           # Append-only, hash-chained RecordStore (Phase 3)
│   ├── registry.py          # Institution + InstitutionRegistry (Phase 4B)
│   ├── deadlines.py         # Statutory deadline profiles + DeadlineEngine (Phase 4B)
│   └── verifier.py          # Integrity + logical consistency + signature validation
├── domains/
│   ├── base.py              # Abstract domain — extend to add new domains
│   ├── general.py           # No-extension baseline
│   ├── communication.py     # EA 2010 ss.20/21 channel accessibility
│   ├── email.py             # Sovereign email-only application (Phase 4A)
│   ├── legal.py             # Enforcement, bulk process, burden shift
│   ├── banking.py           # FCA DISP deadlines; automated credit decisions (Phase 4D)
│   ├── medical.py           # Clinical decision support; consent; MCA 2005 (Phase 4D)
│   └── capacity.py          # MCA 2005 CapacityAssessment — two-stage test (Phase 5)
├── integrations/
│   └── iris.py              # ConversationAssessor — mid-conversation assessment (Phase 4C)
├── templates/
│   └── decision_record.json # Template for manual record creation
├── examples/
│   ├── example_sovereign.py # LGO Rebecca Hunt — SOVEREIGN process, wrong law
│   ├── example_null.py      # EASS Rachel.D — NULL, circular referral
│   ├── example_ambiguous.py # Trading 212 — AMBIGUOUS pending answer
│   ├── example_signed.py    # Signed NULL record — Ed25519 non-repudiation
│   ├── example_storage.py   # Append-only oversight ledger — persist & verify (Phase 3)
│   ├── example_email.py     # Email domain — inbound/outbound assessment (Phase 4A)
│   ├── example_registry_deadlines.py  # Institution registry + deadline engine (Phase 4B)
│   ├── example_iris_conversation.py   # Iris mid-conversation assessment (Phase 4C)
│   ├── example_banking_medical.py     # Banking + medical domains (Phase 4D)
│   └── example_capacity.py            # MCA 2005 capacity assessment (Phase 5)
└── docs/
    └── specification.md     # Full specification with legal grounding
```

---

## Running the examples

From the repo root:

```bash
python verifiable_oversight/examples/example_null.py
python verifiable_oversight/examples/example_sovereign.py
python verifiable_oversight/examples/example_ambiguous.py
python verifiable_oversight/examples/example_signed.py   # requires PyNaCl
python verifiable_oversight/examples/example_storage.py  # append-only ledger
python verifiable_oversight/examples/example_email.py    # email inbound/outbound
python verifiable_oversight/examples/example_registry_deadlines.py  # registry + deadlines
python verifiable_oversight/examples/example_iris_conversation.py   # mid-conversation
python verifiable_oversight/examples/example_banking_medical.py     # banking + medical
```

No installation required for any example except the signed one — stdlib
only. The signed example additionally requires PyNaCl (`pip install PyNaCl`).

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
| `email` | Email-only application; inbound/outbound; no portal/telephone/CAPTCHA/app-only barriers; named individual for significant responses; RA confirmed before first substantive exchange |
| `legal` | Statutory basis; case reference; burden shift; bulk process presumption |
| `banking` | FCA DISP deadlines; solely-automated credit decisions (UK GDPR Art 22 / DUAA 2025 s.80) |
| `medical` | Clinical decision-support; consent; Mental Capacity Act 2005 (capacity + best interests); clinical AI / MHRA registration |
| `capacity` | `CapacityAssessment` — MCA 2005 two-stage test (s.2 diagnostic + s.3 functional), best interests (s.4), least restrictive option (s.1(5)), clinical-AI NULL detection |

To add a new domain, subclass `BaseDomain` and implement `name`, `guidance`, and optionally `validate_domain_metadata` and `_build_domain_metadata`.

---

## Cryptographic integrity

Every `DecisionRecord` is sealed with a SHA-256 fingerprint on creation. The fingerprint covers all content fields. Any change to the record after sealing will cause `verify_integrity()` to return `False`.

The `signature` field carries an Ed25519 signature over the fingerprint (Phase 2 — see *Cryptographic signing* below). The data model supports it without structural changes — the signing infrastructure connects to the existing [`CRYPTOGRAPHIC_IDENTITY.md`](../CRYPTOGRAPHIC_IDENTITY.md) architecture.

---

## Cryptographic signing (Phase 2)

The fingerprint proves a record has **not changed**. A signature proves **who
produced it**. A `RecordSigner` holds an Ed25519 private key, signs the sealed
record's fingerprint, and attaches the signature and public key so any third
party can verify the finding **offline, with no shared secret**.

```python
from verifiable_oversight import (
    BinaryTest, DecisionRecord, RecordSigner, Verifier, verify_record_signature,
)

record = DecisionRecord.create(
    subject="Fourth response — circular referral to EHRC",
    institution="EASS",
    binary_test=BinaryTest(context="No named individual across four responses."),
)

signer = RecordSigner.generate()   # or RecordSigner(private_key_hex)
signer.sign(record)                # populates record.signature / public_key / signed_at

record.is_signed                   # True
record.public_key                  # publish this for independent verification
verify_record_signature(record)    # True

Verifier().verify(record).signature_ok  # True

# Tamper-evidence: any change after signing breaks both integrity and signature.
record.subject = "Altered"
verify_record_signature(record)    # False
```

**What signing adds:**

- **Non-repudiation** — the record is bound to the holder of a published public key.
- **Independent verification** — a tribunal, ombudsman, or opposing institution
  can verify the signature with only the record and the public key.
- **Backward compatible** — the signature lives *outside* the canonical
  fingerprint, so signing never changes a record's fingerprint, and unsigned
  records behave exactly as in Phase 1 (`Verifier` reports `signature_ok=None`).

The signed message is domain-separated and reproducible:
`SIGNING_CONTEXT + b":" + fingerprint` (see `signing_message`). PyNaCl is required
only for signing/verification; the stdlib core continues to work without it.

Run the signed example:

```bash
pip install PyNaCl
python verifiable_oversight/examples/example_signed.py
```

---

## Record storage (Phase 3)

A single finding is useful. A durable, ordered *chain* of findings is
accountability infrastructure — a log of every SOVEREIGN/NULL assessment that
can be replayed, audited, and independently verified long after the moment it
was produced.

`RecordStore` is an **append-only, tamper-evident ledger** keyed by fingerprint.
It is **stdlib only** — records are persisted as JSON-Lines (one record per
line), so the ledger is human-readable, greppable, and trivially transmittable.

```python
from verifiable_oversight import BinaryTest, DecisionRecord, RecordStore, Verdict

store = RecordStore("oversight-ledger.jsonl")   # or RecordStore() for in-memory

record = DecisionRecord.create(
    subject="Fourth response — circular referral to EHRC",
    institution="EASS",
    binary_test=BinaryTest(context="No named individual across four responses."),
)

entry = store.append(record)        # returns the LedgerEntry (record + chain metadata)
store.get(record.fingerprint)       # retrieve by fingerprint
store.find(verdict=Verdict.NULL)    # filter by verdict / institution / domain
store.counts_by_verdict()           # {'SOVEREIGN': …, 'NULL': …, 'AMBIGUOUS': …}
store.verify_chain()                # True — the whole ledger is intact

# Re-opening a file-backed ledger loads it and re-verifies the chain automatically.
RecordStore("oversight-ledger.jsonl").verify_chain()   # True
```

**Three guarantees:**

- **Append-only** — records are only ever added, never edited or deleted in
  place. Appending an unsealed record, a tampered record (integrity failure), or
  a duplicate fingerprint raises `StorageError`.
- **Keyed by fingerprint** — every record is indexed by its SHA-256 fingerprint;
  the same finding cannot be stored twice, and any record is retrievable in one
  lookup.
- **Tamper-evident chain** — each entry stores the hash of the previous entry,
  forming a hash chain (domain-separated by `CHAIN_CONTEXT`) over the whole
  ledger. Altering, reordering, or truncating any past entry breaks the chain,
  which `verify_chain()` detects — on demand and automatically on load — over
  and above each record's own fingerprint and signature checks.

The chain hash is kept **separate** from the record fingerprint: the fingerprint
commits to a record's *content*, the chain hash commits to its *position in the
ledger*. So signing a record never affects the chain, and building the chain
never changes a record's fingerprint. Signed and unsigned records store
identically — storage is agnostic to whether a record carries a signature.

Run the storage example:

```bash
python verifiable_oversight/examples/example_storage.py
```

---

## Roadmap

- **Cryptographic signing** ✅ *(Phase 2)* — Ed25519 private key → `signature` field populated; public key attached for independent, offline verification
- **Record storage** ✅ *(Phase 3)* — append-only, hash-chained JSON-L ledger; records keyed by fingerprint; chain verified on load and on demand
- **Email domain** ✅ *(Phase 4A)* — sovereign email-only application; each outbound communication creates a record; each institutional response is assessed on receipt against the binary test and the non-negotiable accessibility requirements (no portal redirect, no telephone, no CAPTCHA, no app-only verification, named individual for every significant response, RA confirmed and recorded before the first substantive exchange)
- **Institution registry + deadline engine** ✅ *(Phase 4B)* — case-insensitive, alias-aware `InstitutionRegistry`; `DeadlineEngine` with statutory response profiles (FCA DISP 8 weeks, DSAR one month, and more) classifying a window as PENDING / DUE_TODAY / BREACHED
- **Iris integration** ✅ *(Phase 4C)* — `ConversationAssessor` creates and verifies records on a user's behalf mid-conversation: AMBIGUOUS while gathering, targeted follow-up questions for each missing element, and a definitive SOVEREIGN/NULL appended to the ledger on finalisation
- **Banking domain** ✅ *(Phase 4D)* — FCA DISP deadlines; solely-automated credit decision assessment (UK GDPR Art 22 / DUAA 2025 s.80)
- **Medical domain** ✅ *(Phase 4D)* — clinical decision support; consent; Mental Capacity Act 2005 (capacity assessment + best-interests determination)
- **Capacity domain** ✅ *(Phase 5)* — `CapacityAssessment` applies the binary test to Mental Capacity Act 2005 decisions: presumption of capacity (s.1(2)), decision- and time-specific two-stage test (s.2 diagnostic + s.3 functional), best interests by a named decision-maker (s.4), least restrictive option (s.1(5)), and NULL detection for clinical AI used without named clinician review (DUAA 2025 s.80 / UK GDPR Art.22)
- **Post-quantum companion** — hybrid Ed25519 + ML-DSA/SLH-DSA signatures, reusing the `onchain-protocol` provider architecture

---

## Legal grounding

This module implements the Burgess standard as described in the SSRN working paper series. See [`papers/SSRN_INDEX.md`](../papers/SSRN_INDEX.md) and [`LEGAL_FOUNDATIONS.md`](../LEGAL_FOUNDATIONS.md).

Key authorities: EA 2010 ss.6/19/20/21/27/136/149 · DUAA 2025 s.80 · Ahmed [2010] UKSC 5 · Majera [2021] UKSC 46 · ZH [2011] UKSC 4 · FirstGroup v Paulley [2017] UKSC 4
