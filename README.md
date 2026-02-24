# The Burgess Principle

**A citizen-initiated legal doctrine — free and open for anyone to cite.**

## What It Is

The Burgess Principle establishes that facially defective warrants under the **Rights of Entry (Gas and Electricity Boards) Act 1954** are void *ab initio*, with downstream remedies for credit contamination and reasonable adjustments for protected characteristics.

## Open Source

The principle itself is **free and may be cited by anyone**. The goal is maximum truth reaching maximum people.

## Methodology & Toolkit — Open Source

The methodology and toolkit are **fully open source**, licensed under the [MIT License](LICENSE). Free for anyone to use, adapt, and build upon.

Integrated with [OpenClaw](https://openclaw.im) — the open-source AI automation platform for law.

## Auto-Pilot (GitHub Actions)

The Hunter scanning system runs **autonomously every 24 hours** via GitHub Actions, with no manual intervention required.

### How it works

- A scheduled workflow (`.github/workflows/daily_hunter_scan.yml`) triggers at **midnight UTC** every day.
- It runs `src/batch_scanner.py` against the warrant data in `examples/warrants_sample.csv`.
- Any warrant found to be defective under the **Rights of Entry (Gas and Electricity Boards) Act 1954** is flagged as **VOID AB INITIO** and written to `void_warrants_report.csv`.
- The report is uploaded as a **GitHub Actions Artifact** so you can download it at any time.

### Downloading the daily "Kill List"

1. Go to the **Actions** tab in this repository.
2. Click the latest **Daily Hunter Scan** workflow run.
3. Scroll to the **Artifacts** section at the bottom of the run summary.
4. Download **`void_warrants_report`** — this is your Kill List CSV.

### Running on demand

Click the **Run workflow** button on the [Daily Hunter Scan](../../actions/workflows/daily_hunter_scan.yml) workflow page to trigger an immediate scan.

## Live Site

[https://ljbudgie.github.io/Burgessprinciple/](https://ljbudgie.github.io/Burgessprinciple/)

## Contact

For media enquiries: [lewis@burgessprinciple.co.uk](mailto:lewis@burgessprinciple.co.uk)

## Legal

&copy; 2026 Lewis Burgess. Licensed under the [MIT License](LICENSE).  
Registered trademark application UK00004343685
