# DEFECT SCHEMA: Tracer Protocol Hunting Library
**Phase 2 — The Tracer Protocol (Grok Co-Developed)**  
*The Burgess Principle — Facial Defect Catalogue*

---

## Overview

This schema defines the four primary categories of **facial defects** that the Tracer Protocol (`tracer.py`) hunts for in warrant documentation and related legal records. A "facial defect" is a flaw that is visible on the face of the document itself — no extrinsic evidence is required to establish its existence.

A warrant exhibiting **any** of these defects is, under the Burgess Principle, a candidate for challenge as **void ab initio** (void from the beginning).

---

## Category 1 — Bulk Approval Without Scrutiny

**Axiom:** *The Judicial Mind* — a warrant cannot be valid unless a judicial officer applied their mind to the specific facts of that individual case.

### Definition
Warrants processed in batches without individual judicial review. This occurs when a Justice of the Peace or Magistrate signs multiple warrant applications in a single sitting, spending insufficient time on each to genuinely consider the evidence.

### Indicators
- Warrant issued as part of a named "bundle" or "batch" application.
- Timestamps showing multiple warrants signed within seconds of each other.
- No record of individual hearing or individual consideration on the face of the order.
- Court lists showing 50+ warrant applications listed for a single brief session.

### Legal Basis
- *R v Sussex Justices, Ex parte McCarthy* [1924] 1 KB 256 — justice must be seen to be done.
- Rights of Entry (Gas and Electricity Boards) Act 1954, s.2 — magistrate must be "satisfied" on the specific facts.
- *R (on the application of ClientEarth) v Secretary of State* — administrative decisions require genuine engagement with the facts.

### Tracer Keywords
`bulk`, `bundle`, `batch`, `warrants in minutes`, `without individual judicial`, `rubber-stamp`

---

## Category 2 — Rubber-Stamping

### Definition
The issuing magistrate accepted the energy company's written statement or sworn affidavit at face value, without requiring any independent corroboration or inviting the affected party to respond.

### Indicators
- Warrant application supported solely by a supplier-prepared statement.
- No evidence of independent witness, meter reading, or site visit recorded.
- Blanket approval of all applications in a bundle without differentiated reasoning.
- Affidavit language that is templated / identical across multiple applications.

### Legal Basis
- *R v Inland Revenue Commissioners, ex parte National Federation of Self-Employed* [1982] AC 617 — requirement for genuine independent scrutiny.
- European Convention on Human Rights, Article 8 — right to respect for the home; any derogation must be necessary and proportionate.
- UK Human Rights Act 1998, s.6 — public authorities must act compatibly with Convention rights.

### Tracer Keywords
`rubber-stamp`, `affidavit`, `without independent verification`, `taken on trust`, `supplier declaration accepted`

---

## Category 3 — Procedural Lies / Errors

**Definition:** False safety claims or incomplete address data on the face of the warrant application.

### Indicators
- The address on the warrant does not match the property in question (wrong postcode, wrong flat number, etc.).
- Safety justification (e.g., "gas escape", "suspected tampering") that is demonstrably false or unsubstantiated.
- Sworn statements that contain material inaccuracies.
- Missing mandatory fields (e.g., occupier's name, meter serial number) required by the issuing authority's own procedure.

### Legal Basis
- Perjury Act 1911 — false sworn statements are criminal.
- *R v Bow Street Metropolitan Stipendiary Magistrate, ex parte Government of the USA* [2000] 2 AC 216 — material error in warrant application can invalidate the warrant.
- Magistrates' Courts Act 1980, s.1 — informations must be laid truthfully.

### Tracer Keywords
`incorrect address`, `false safety`, `gas escape unfounded`, `wrong postcode`, `address mismatch`, `stated incorrectly`

---

## Category 4 — Downstream Taint Propagation

### Definition
A defective warrant that is void ab initio cannot create any valid downstream legal consequence. If a debt, CCJ, default notice, or credit entry was generated as a consequence of actions taken under such a warrant, those downstream records inherit the taint of the original nullity.

### Indicators
- A default or CCJ registered against a property owner following entry under a defective warrant.
- Billing entries that reference meter readings taken during an unlawful entry.
- Credit agency records (Experian, Equifax, TransUnion) reflecting the balance arising from contested warrant enforcement.
- Court enforcement orders issued on the basis of a tainted original warrant.

### Legal Basis
- *Bunnings Group v CEVA Logistics* — void instruments cannot found valid downstream obligations.
- Data Protection Act 2018 / UK GDPR, Article 17 — right to erasure of inaccurate personal data.
- Consumer Credit Act 1974, s.140A — unfair relationships; courts may set aside obligations flowing from an unfair original act.
- *Durkin v DSG Retail Ltd* [2014] UKSC 21 — rescission of foundational agreement rescinds linked obligations.

### Tracer Keywords
`credit`, `default`, `CCJ`, `tainted`, `void`, `cascade`, `billing error`, `Experian`, `Equifax`, `TransUnion`

---

## Defect Severity Matrix

| Category | Defect Type | Standalone Challenge? | Strength |
|---|---|---|---|
| 1 — Bulk Approval | Structural nullity | ✅ Yes | ⭐⭐⭐⭐⭐ |
| 2 — Rubber-Stamp | Evidential nullity | ✅ Yes | ⭐⭐⭐⭐ |
| 3 — Procedural Error | Factual nullity | ✅ Yes | ⭐⭐⭐ |
| 4 — Downstream Taint | Derivative nullity | ⚠️ Requires Category 1–3 finding | ⭐⭐⭐⭐⭐ |

---

## Usage with Tracer

The Tracer (`tracer.py`) maps each regex signature group to one of the four categories above. A document that triggers **Category 1 or 2** alongside **Category 4** represents the highest-priority defect combination — a structurally void warrant with live downstream consequences.

```
python tracer.py --urls <url> --output json
```

See `tracer.py` module docstring for full usage instructions.

---

*Schema version: 2.0 — Phase 2 Tracer Protocol Upgrade (Grok Co-Developed)*  
*© 2026 Lewis Burgess. Licensed under the MIT License.*
