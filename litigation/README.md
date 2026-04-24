# Litigation

## The Burgess Principle — Tier 4 Litigation Partner Tools

### UK Certification Mark UK00004343685 | Version 1.1 | April 2026

-----

This directory contains the operational litigation tools for Tier 4 licensed partners. A signed Tier 4 licence agreement is required to use these tools commercially. See [LICENSING.md](../LICENSING.md) for terms.

The tools here are the practical implementation of the theoretical framework set out in [Paper VII](../papers/PAPER_VII_NULL_ACROSS_THE_CLASS.md). Read Paper VII first.

-----

## The Core Argument

Paper VII introduces a defendant-side class definition methodology for group litigation under CPR Part 19.8. The thesis: where an institution applies a single automated process to every person it acts against — issuing instruments, enforcing debts, processing data, exercising statutory powers — the Burgess Principle binary test can be applied to the *defendant’s process* rather than the *claimants’ circumstances*. If the process returns NULL (no individual human review of the specific facts of the specific case), it returns NULL for every person subjected to it simultaneously. That shared NULL is “same interest” under CPR 19.8, and the class defines itself from the defendant’s own documents without requiring claimants to prove common characteristics, common loss, or anything about themselves at all.

This avoids the cost, complexity, and case management burden of a Group Litigation Order. A representative action under CPR 19.8 asks one binary question of one defendant. Stage 1 is declaratory relief — was the process SOVEREIGN or NULL? — answerable from the defendant’s own records. Individual quantum follows at Stage 2 only after the systemic question is resolved.

-----

## Key Concept: Contamination Chain

A void originating instrument — an unsigned warrant, a bulk-processed liability order, an enforcement notice issued without individual judicial scrutiny — contaminates every downstream action, institution, and data entry built upon it. The debt passed to an enforcement agent, the credit file entry, the data shared with third parties, the fees added at each stage: all inherit the nullity of the source. The contamination chain is what connects a single defective instrument to multiple institutional defendants and multiple categories of loss.

-----

## The Disability Uplift

For claimants with disabilities (within the meaning of s.6 Equality Act 2010), the failure to apply individual human review is not only a process defect — it is a potential failure of the duty to make reasonable adjustments under ss.20–21 and may constitute discrimination arising from disability under s.15. Where a claimant has a Pre-action Protocol for Debt Claims vulnerability flag (the PSR — Priority Services Register — or equivalent), a recorded disability, or an asserted reasonable adjustment (such as email-only communication for hearing loss), and the defendant’s automated process made no accommodation for that individual’s circumstances, the quantum per class member increases significantly.

This is the highest-value element in many cases. Document PSR status, disability, and reasonable adjustment failures at intake for every claimant. The Equality Act claims run alongside the process nullity claims and compound the damages.

-----

## Tools in This Directory

|File                              |Purpose                                                                                                                              |Stage                          |
|----------------------------------|-------------------------------------------------------------------------------------------------------------------------------------|-------------------------------|
|<GROUP_LITIGATION_STARTER_PACK.md>|CPR 19.8 representative action framework — defendant-side class definition, Stage 1 particulars of claim template, strike-out defence|Pre-issue and Stage 1          |
|<DAMAGES_MATRIX.md>               |Quantum framework across four harm categories — direct enforcement, credit, data processing, systemic                                |Stage 2                        |
|<WARRANT_DEFECT_IDENTIFIER.md>    |Assessment tool for entry warrant facial defects and batch processing invalidity                                                     |Client intake                  |
|<CONTAMINATION_CHAIN_MAPPER.md>   |Traces downstream contamination from a void enforcement instrument across all institutions                                           |Client intake and claim scoping|

-----

## How the Tools Fit Together

### Client Intake

Start with the two intake tools for every new claimant:

1. **WARRANT_DEFECT_IDENTIFIER** — is the originating instrument void? If yes, everything built on it is contaminated.
1. **CONTAMINATION_CHAIN_MAPPER** — how far has the contamination travelled? Map every institution, file every SAR simultaneously.

At intake, also record: any disability or long-term health condition, any PSR or vulnerability flag, any previously asserted reasonable adjustment, any evidence that the defendant was aware of the claimant’s circumstances before processing. This information drives the Equality Act uplift at Stage 2.

### Building the Class

Once individual cases are assessed, use **GROUP_LITIGATION_STARTER_PACK** to:

- Define the class on the defendant side using the binary test
- Structure Stage 1 particulars of claim for declaratory relief
- Prepare for the strike-out application the defendant will file

### Quantifying Harm

Use **DAMAGES_MATRIX** at Stage 2 to quantify harm across all four categories for each class member. The four categories are:

1. **Direct enforcement loss** — fees, charges, overpayments, property damage from void instruments
1. **Credit contamination** — impaired credit files, declined applications, increased borrowing costs traceable to void entries
1. **Data processing breach** — unlawful processing, Article 22 failures, DSAR non-compliance, data shared downstream without lawful basis
1. **Systemic harm** — distress, anxiety, time spent, interference with private life, loss of autonomy from being processed as a data object rather than an individual

The Equality Act disability uplift applies across all four categories where the claimant’s protected characteristic was known or ought to have been known to the defendant.

-----

## The Foundation

These tools implement the defendant-side class definition methodology from Paper VII. The core logic:

- Define the class by what the defendant did, not by what claimants share
- The binary test applied to the defendant’s process returns NULL for every class member simultaneously
- NULL across the class is “same interest” under CPR 19.8
- Stage 1 asks one question answerable from the defendant’s own documents
- Personal data is the lowest common denominator — it is the common substrate connecting every class member to the defendant’s automated process
- The contamination chain maps the full downstream reach of the originating nullity

-----

## Tier 4 Licence

Using these tools commercially requires a signed Tier 4 agreement. Terms:

- Upfront: £1 or nil
- Ongoing: 2–5% of the firm’s net fee share on qualifying matters
- Trigger: Successful outcome only
- Process: One email → one agreement → one signature → public commit in this repository

Contact: ljbarbers15@gmail.com

-----

## Motive Record

The motive record for these tools is documented in Paper VII and the repository commit history. The framework predates the litigation strategy. The originator bears the same risk as the firm. This is access to justice, not a commercial vehicle.

-----

*Tier 4 Licensed Partners Only*
*Lewis James Burgess | ljbarbers15@gmail.com | github.com/ljbudgie/burgess-principle*
