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

## Media Sovereignty (Copyright Defense)

The **Media Sovereignty Module** (`src/media_sovereignty.py`) extends the Burgess Principle to digital media rights, allowing any sovereign individual to challenge automated or unsubstantiated copyright strikes on platforms such as YouTube, Spotify, and SoundCloud.

### How It Works

The module applies the same **Void Ab Initio** and Sovereignty logic used in warrant challenges to DMCA takedowns and copyright strikes:

- A claim that lacks a **wet ink signature** or a **sworn affidavit of ownership** is automatically marked **VOID**.
- An automated strike with no stated legal basis violates the claimant's Sovereignty rights under the Burgess Principle and is likewise **VOID**.

### Usage

```python
from src.media_sovereignty import MediaRightsDefender

defender = MediaRightsDefender()

claim = {
    "claimant": "ContentID_Bot",
    "platform": "YouTube",
    "work_title": "Morning Sunrise (Original Composition)",
    "legal_basis": "DMCA Section 512",
    "automated": True,
    "proofs": [],
}

result = defender.evaluate_copyright_claim(claim)
print(result)
# {'status': 'VOID', 'reason': "Claim is Void Ab Initio: missing required proofs: ..."}

counter_notice = defender.generate_counter_notice(claim)
print(counter_notice)
```

The counter-notice produced asserts rights under **Article 29 of the Magna Carta** and the Burgess Principle, demanding that all downstream consequences of the void claim (demonetisation, content removal, account penalties) be reversed forthwith.

### Sample Data

`examples/media_claim_sample.csv` contains representative DMCA takedown and copyright strike scenarios for testing and demonstration purposes.

## Contact

For media enquiries: [lewis@burgessprinciple.co.uk](mailto:lewis@burgessprinciple.co.uk)

## Legal

&copy; 2026 Lewis Burgess. Licensed under the [MIT License](LICENSE).  
Registered trademark application UK00004343685
