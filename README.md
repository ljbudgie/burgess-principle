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

## Enforcer Protocol (Automated Notices)

The **Enforcer** module is the final piece of the automated legal defence suite (Hunter → Tracer → Enforcer). It takes the "Kill List" of defective warrants produced by the Hunter module and turns each entry into a formal legal notice ready for service.

### How it works

1. The Hunter module outputs a `void_warrants_report.csv` containing the warrant ID, issue date, identified defect, and issuing court.
2. The Enforcer module reads that CSV and generates one `Notice_Warrant_[ID].txt` file per row in an output `notices/` directory.
3. Each notice follows the standard **Notice of Void Warrant Ab Initio** template:

   > NOTICE OF VOID WARRANT AB INITIO.  
   > To [Court/Issuer]. Take notice that Warrant [ID] issued on [Date] is void ab initio due to [Defect]. Under the Burgess Principle, all entry is trespass. Immediate remedy required.

### Quick start

```bash
# Generate notices from the bundled sample data
python examples/generate_notices.py

# Generate notices from a Hunter-produced report
python examples/generate_notices.py path/to/void_warrants_report.csv
```

### Programmatic use

```python
from src.enforcer_module import LegalNoticeGenerator

generator = LegalNoticeGenerator(output_dir="notices")

# From a CSV file (Hunter output or warrants_sample.csv)
paths = generator.generate_from_csv("void_warrants_report.csv")

# Or from a list of dicts
warrants = [
    {"warrant_id": "WRT-001", "date": "2024-03-15",
     "defect": "Missing magistrate signature", "court_issuer": "Brighton Magistrates Court"},
]
paths = generator.generate_from_list(warrants)
```

## Contact

For media enquiries: [lewis@burgessprinciple.co.uk](mailto:lewis@burgessprinciple.co.uk)

## Legal

&copy; 2026 Lewis Burgess. Licensed under the [MIT License](LICENSE).  
Registered trademark application UK00004343685
