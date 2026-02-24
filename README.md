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

## Digital Armor — Security Module

The `src/protection_module.py` file provides a reusable **Digital Armor** module that codifies the Burgess Principle's warrant-defect logic into Python code. Any AI agent or automated system (including [OpenClaw](https://openclaw.im) agents) can import this module to "inherit" the legal protections of the Burgess Principle.

### How It Works

The module exposes a **Warrant Defect Identifier** — a binary logic tree that takes warrant details as input and returns a `"VOID AB INITIO"` determination when facial defects are found under the 1954 Act.

```python
from src.protection_module import assess_warrant

result = assess_warrant({
    "applicant_name": "Example Energy Ltd",
    "property_address": "1 Example Street",
    "warrant_date": "2025-06-01",
    "issuing_authority": "Anytown Magistrates Court",
    "notice_given_to_occupier": False,   # <-- defect
    "grounds_stated_on_face": False,     # <-- defect
    "officer_authorised": True,
    "protected_characteristics": ["autism"],
})

print(result["determination"])           # VOID AB INITIO
print(result["defects"])                 # list of identified defects
print(result["downstream_remedies_available"])  # True
```

Or use the class directly for more control:

```python
from src.protection_module import WarrantDefectIdentifier, WarrantDetails

wdi = WarrantDefectIdentifier()
details = WarrantDetails(
    notice_given_to_occupier=True,
    notice_period_days=3,
    grounds_stated_on_face=True,
    officer_authorised=True,
)
result = wdi.assess(details)
print(result.determination)  # APPARENTLY VALID
```

### Sovereignty Shield Header

`Sovereignty_Shield_Header.txt` contains a standard legal assertion statement that OpenClaw agents (or any other system) can prepend to their logs or outputs. It asserts the Burgess Principle, declares all void-ab-initio consequences unlawful, and places any relying party on notice. Simply include the file's contents at the top of any relevant output.

### How OpenClaw (and other AIs) Inherit the Protection

1. **Import** `src/protection_module.py` into your agent's codebase.
2. **Call** `assess_warrant()` (or instantiate `WarrantDefectIdentifier`) whenever your agent encounters a warrant claim.
3. **Prepend** the contents of `Sovereignty_Shield_Header.txt` to any output or log that may be used in proceedings involving 1954 Act warrants.

By doing so, the agent operates with explicit awareness of the Burgess Principle and can flag void-ab-initio warrants before they cause downstream harm.

---

## Contact

For media enquiries: [lewis@burgessprinciple.co.uk](mailto:lewis@burgessprinciple.co.uk)

## Legal

&copy; 2026 Lewis Burgess. Licensed under the [MIT License](LICENSE).  
Registered trademark application UK00004343685
