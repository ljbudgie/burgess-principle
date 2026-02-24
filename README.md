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

## Digital Armor

The `src/protection_module.py` file implements the Burgess Principle as executable code for use by [OpenClaw](https://openclaw.im) agents to programmatically detect void warrants.

### Classes

- **`WarrantDefectIdentifier`** — evaluates warrant data and returns a verdict of `VOID AB INITIO` or `VALID`.
- **`SovereigntyShield`** — generates the standard Digital Armor legal assertion text.

### Usage

```python
from src.protection_module import WarrantDefectIdentifier, SovereigntyShield

# Evaluate a warrant
identifier = WarrantDefectIdentifier()
result = identifier.evaluate_warrant({
    "act": "Rights of Entry (Gas and Electricity Boards) Act 1954",
    "facial_validity": "wrong_address",
    "date": "2026-01-15",
    "issuer": "Example Utility Company",
})
print(result["status"])  # VOID AB INITIO
print(result["reason"])
print(result["defects"])  # ['wrong_address']

# Generate the sovereignty assertion
shield = SovereigntyShield()
print(shield.generate_assertion())
```

### Tests

```bash
python -m pytest tests/test_protection_module.py -v
```

## Contact

For media enquiries: [lewis@burgessprinciple.co.uk](mailto:lewis@burgessprinciple.co.uk)

## Legal

&copy; 2026 Lewis Burgess. Licensed under the [MIT License](LICENSE).  
Registered trademark application UK00004343685
