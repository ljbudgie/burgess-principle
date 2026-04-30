# Contamination Chain Mapper
## The Burgess Principle — Enforcement Chain Tracing Tool
### UK Certification Mark UK00004343685 | Version 1.0 | April 2026

---

## Purpose

This tool traces the downstream contamination chain from a void or unlawfully obtained enforcement instrument. Every institution that acted on the void instrument — processed data based on it, reported it to credit bureaus, instructed bailiffs under it, or registered a CCJ from it — is part of the chain. Each link is a potential defendant or regulatory complaint target.

---

## How Contamination Works

When an enforcement instrument (warrant, liability order, CCJ) is void ab initio, it never existed in law. But institutions act on it as if it were valid. Each institution that does so inherits the nullity:

- Data processed on the basis of a void instrument is processed without lawful basis
- Credit data reported on the basis of a void instrument is inaccurate
- Enforcement costs charged under a void instrument are unjustly enriched
- A CCJ registered on a void liability order is itself void

The contamination travels downstream silently. The claimant may not know how far it has reached until SAR responses are returned from every institution in the chain.

---

## Step 1 — Map the Originating Instrument

| Field | Detail |
|---|---|
| Instrument type | Warrant / Liability order / CCJ / Other |
| Issuing body | Court name and location |
| Date issued | |
| Reference number | |
| Defect identified | Unsigned / Batch processed / Named / Other |
| Binary test result | NULL — no individual judicial review |
| Evidence of defect | Written admission / Facial examination / Expert evidence |

---

## Step 2 — Trace Every Downstream Institution

For each institution in the chain, complete the following:

### Institution 1 — Energy Company / Applicant

| Field | Detail |
|---|---|
| Name | |
| Role | Obtained the warrant / instructed enforcement |
| Actions taken under void instrument | Forced entry / Meter change / Equipment installation |
| Data shared with third parties | Yes / No — identify recipients |
| Credit bureau data reported | Yes / No |
| PSR status acknowledged | Yes / No |
| Reasonable adjustment provided | Yes / No |
| SAR filed | Yes / No / Date |
| SAR response received | Yes / No / Date |
| Regulatory complaint filed | ICO / Ofgem / FCA — reference number |

---

### Institution 2 — Enforcement Agent / Bailiff

| Field | Detail |
|---|---|
| Name | |
| Role | Executed entry under void warrant |
| Actions taken | Entry / Goods removed / Costs charged |
| Fees charged | Amount |
| Bodycam footage held | Yes / No / Requested |
| SAR filed | Yes / No / Date |
| SAR response received | Yes / No / Date |

---

### Institution 3 — Credit Reference Agencies

File SARs with all three simultaneously. Do not wait for one before filing another.

| Agency | SAR Filed | Date | Response Received | Adverse Data Found |
|---|---|---|---|---|
| Experian | ☐ | | ☐ | ☐ |
| Equifax | ☐ | | ☐ | ☐ |
| TransUnion | ☐ | | ☐ | ☐ |

For each adverse entry found:

| Entry Type | Date Registered | Basis | Correction Requested | ICO Complaint Filed |
|---|---|---|---|---|
| Default | | | ☐ | ☐ |
| CCJ | | | ☐ | ☐ |
| Missed payment | | | ☐ | ☐ |
| Debt sale | | | ☐ | ☐ |

---

### Institution 4 — Debt Purchaser / Collector

| Field | Detail |
|---|---|
| Name | |
| Debt purchased from | |
| Amount claimed | |
| Basis of debt | Original liability order / CCJ |
| SAR filed | Yes / No / Date |
| Notice of void instrument served | Yes / No / Date |
| Response received | Yes / No |

---

### Institution 5 — Court (for CCJ registration)

| Field | Detail |
|---|---|
| Court name | |
| CCJ reference | |
| Date registered | |
| Basis | Liability order reference |
| Set aside application filed | Yes / No / Date |
| Grounds | Void underlying instrument — no individual judicial review |

---

### Institution 6 — Data Regulator (ICO)

| Field | Detail |
|---|---|
| Complaint reference | |
| Complaint filed | Date |
| Basis | Art.5(1)(a) accuracy / Art.22C safeguards / Art.22A automated processing |
| Response received | Yes / No / Date |
| Outcome | |
| Pre-action protocol issued | Yes / No / Date |

---

## Step 3 — Contamination Chain Summary

Once all SARs are returned and all institutions mapped, complete this summary:

```
ORIGINATING INSTRUMENT: [Type] issued by [Court] on [Date]
DEFECT: [Unsigned / Batch processed / Other]
BINARY TEST RESULT: NULL

CONTAMINATION CHAIN:

[Energy Company] ──→ Obtained void warrant
       │
       ├──→ Instructed [Enforcement Agent] → Forced entry on [Date]
       │         │
       │         └──→ Bodycam footage: [Held / Requested / Disclosed]
       │
       ├──→ Reported to [Credit Bureau(s)] → Adverse data registered on [Date(s)]
       │         │
       │         └──→ Correction requested: [Yes / No / Date]
       │
       ├──→ Debt sold to [Debt Purchaser] on [Date] for [Amount]
       │         │
       │         └──→ Notice of void instrument served: [Yes / No / Date]
       │
       └──→ CCJ registered at [Court] on [Date]
                 │
                 └──→ Set aside application: [Filed / Pending / Outcome]

REGULATORY COMPLAINTS:
- ICO: [Reference] — [Status]
- Ofgem: [Reference] — [Status]
- FCA: [Reference] — [Status]

TOTAL INSTITUTIONS IN CHAIN: [Number]
TOTAL ADVERSE DATA ENTRIES: [Number]
ESTIMATED AGGREGATE HARM: [See Damages Matrix]
```

---

## Step 4 — Priority Actions by Institution

| Institution | Priority Action | Deadline | Status |
|---|---|---|---|
| Energy company | Pre-action protocol letter | 14 days from notice | |
| All credit bureaus | Art.16 correction request | Simultaneous | |
| ICO | Complaint (data accuracy) | As soon as possible | |
| Debt collector | Notice of void instrument | Before any payment | |
| Court | CCJ set aside application | As soon as possible | |
| Ofgem / FCA | Regulatory complaint | As soon as possible | |

---

## Key Principle

Do not settle with the energy company alone. Settlement with the originating institution does not resolve the contamination downstream. Ensure any settlement agreement includes:

- Withdrawal of all adverse credit data from all three bureaus
- Written confirmation to all debt purchasers that the debt is extinguished
- Written confirmation to the court that the CCJ basis is void
- Data deletion obligations under Art.17 UK GDPR
- Confirmation of compliance within a specified period

Without these, the settlement resolves the claim against the energy company while leaving the claimant's credit file and downstream data intact.

---

*All Tiers | UK Certification Mark UK00004343685*
*Lewis James Burgess | lewisjames@theburgessprinciple.com | github.com/ljbudgie/burgess-principle*
