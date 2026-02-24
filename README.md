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

## Hunter Protocol (Batch Scanning)

The **Hunter Batch Scanner** lets OpenClaw agents and users process thousands of warrants at once, automatically identifying those that are *Void Ab Initio* under the Burgess Principle.

### How it works

1. **Prepare a CSV file** with one warrant per row.  
   Required columns: `warrant_id`, `act`, `issuing_court`, `issue_date`, `subject_address`.  
   Optional columns: `facial_validity`, `protected_characteristics`, `reasonable_adjustment`, `notes`.  
   See [`examples/warrants_sample.csv`](examples/warrants_sample.csv) for a ready-made template with mixed valid and defective entries.

2. **Run the scanner:**

   ```bash
   python src/batch_scanner.py examples/warrants_sample.csv
   ```

   By default the report is written to `void_warrants_report.csv` in the current directory.  
   Use `--output` to specify a different path:

   ```bash
   python src/batch_scanner.py input.csv --output results/void_warrants.csv
   ```

3. **Read the report.**  
   The output CSV contains only the defective warrants, with an extra `void_reasons` column that explains each identified facial defect.

### Defects detected

| Check | Description |
|---|---|
| Missing mandatory fields | `warrant_id`, `act`, `issuing_court`, `issue_date`, or `subject_address` absent |
| Wrong enabling Act | Act cited is not the *Rights of Entry (Gas and Electricity Boards) Act 1954* |
| Explicit invalidity flag | `facial_validity` column set to `false` / `invalid` / `defective` |
| Unknown issuing court | Court recorded as `none`, `unknown`, or `n/a` |
| Missing reasonable adjustment | Protected characteristics present but no reasonable adjustment recorded (Equality Act 2010 / CRPD) |

### Requirements

Python 3.10 or later (uses only the standard library — no additional packages needed).

---

## Contact

For media enquiries: [lewis@burgessprinciple.co.uk](mailto:lewis@burgessprinciple.co.uk)

## Legal

&copy; 2026 Lewis Burgess. Licensed under the [MIT License](LICENSE).  
Registered trademark application UK00004343685
