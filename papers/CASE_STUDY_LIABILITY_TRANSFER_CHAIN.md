# Case Study: The Burgess Test — The Liability Transfer Chain

**Author:** Lewis James Burgess, The Burgess Principle Ltd  
**ORCID:** [0009-0001-8691-3366](https://orcid.org/0009-0001-8691-3366)  
**Version:** v2.5.1 (May 2026), organisation-level public text 21 November 2026  
**Licence:** MIT (text) / Certification mark separately reserved

---

## Abstract

This case study documents the *Liability Transfer Chain*: the
institutional pattern by which responsibility for an automated or
algorithmically-mediated decision is passed between organisations
such that, when the Burgess Test is applied, no named human being
can be identified as having applied their mind to the specific facts
of a specific person's case before institutional power was exercised.

The worked example is the Phonak AutoSense OS / Medical Devices
Regulations 2002 chain, read alongside the organisation-level
findings in [`live_findings_ledger.csv`](../live_findings_ledger.csv)
and [`LIVE_AUDIT_LOG.md`](../LIVE_AUDIT_LOG.md).

## The Burgess Test

> *Was a named human being's mind applied to the specific facts of a
> specific person's case before institutional power was exercised?*

A binary outcome is recorded for each link in the chain:

- **SOVEREIGN** — a named human reviewer of the specific case is identified.
- **NULL** — no such named human reviewer is identified.
- **AMBIGUOUS** — the institution claims human involvement but cannot
  evidence it for the specific case.

## The Chain

1. **Manufacturer (Phonak / Sonova UK Ltd)** — algorithmic fitting via AutoSense OS.
   A subject access request did not evidence an individual clinical review of
   the specific patient's hearing profile.
2. **Regulator (MHRA)** — a freedom-of-information reply confirmed the device
   class and located clinical suitability with the audiology provider.
3. **Provider (an NHS audiology service)** — no evidence on the public record
   that an individual clinician reviewed device suitability for the specific
   patient.

At each link, responsibility is referred onward. The chain terminates
without a named human reviewer — a *NULL across the class*. The public
register records Phonak / Sonova UK Ltd and the MHRA as NULL.

## Finding

The Liability Transfer Chain is the operational mechanism by which
"meaningful human involvement", as required under the Data (Use and
Access) Act 2025 (Articles 22A–22D), the EU AI Act high-risk
oversight provisions, the NIST AI Risk Management Framework, the
Consumer Rights Act 2015 Section 49, and the Medical Devices
Regulations 2002, is rendered untestable in practice.

The Burgess Test makes the failure documentable.

## References

- `papers/BURGESS_TEST_2026.md` — paper documentation for the main academic paper
- `papers/WHITEPAPER_BURGESS_TEST_2026.md` — the long-form paper text (published on SSRN; not altered in the 21 November 2026 organisation-level pass)
- `papers/MEDICAL_DEVICE_DOCTRINE.md` — medical device convergence
- `LIVE_AUDIT_LOG.md` — organisation-level live findings ledger
- `README.md` — Legal Convergence section
