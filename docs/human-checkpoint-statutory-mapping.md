# human_checkpoint — statutory trigger mapping

This note maps the deterministic trigger patterns in `human_checkpoint` to the UK regimes that already require a named human to review the specific facts of an identified person before the action proceeds.

The mapping is descriptive only. It does not expand the tool’s behaviour. It exists so a reader can see why a given trigger forces STOP.

| Trigger pattern | Regime | Why a named human is required |
|---|---|---|
| disconnect, cut off, terminat, suspend (supply) | Ofgem supply rules / Electricity Act / Gas Act | Disconnection of supply to an identified premises requires prior review of the specific circumstances. |
| credit check, credit search, credit report | UK GDPR Article 22 (automated decision-making) | A credit decision that produces legal or similarly significant effects on a person requires meaningful human involvement. |
| refuse, declin, den, reject (refund, claim, application) | UK GDPR Article 22; Equality Act 2010 s.20 (where disability is engaged) | Refusal of a benefit, refund or service that affects an identified person requires review of the specific facts. |
| collect the debt, debt, arrears, default | FCA Consumer Duty; Consumer Credit Act | Enforcement or collection against an identified person requires assessment of individual circumstances. |
| close the account, cancel the account, block the account | FCA Consumer Duty; Payment Services Regulations | Closure or restriction of an account belonging to an identified person requires prior review. |
| charge, fine, penalt, surcharge | Consumer Rights Act; sector-specific charging rules | Imposition of a charge or penalty on an identified person requires confirmation that the specific facts justify it. |
| enforc, bailiff, warrant, summons, liability order | Civil Procedure Rules; Enforcement regulations | Enforcement action against an identified person requires a named decision-maker with authority over the specific facts. |
| evict, repossess | Housing Act; Consumer Credit Act | Possession or repossession affecting an identified occupier requires individual review. |
| benefit, eligib, appeal (social security) | Social Security Act; DWP decision-making rules | Benefit decisions and appeals require a named decision-maker who has reviewed the specific facts. |
| complaint | Sector complaint-handling rules (e.g. FCA DISP, Ofgem, Ofcom) | A complaint about an identified person’s case requires a named handler who has reviewed the facts. |

## Notes

- The regex in `iris_mcp.py` is deliberately broad. A match always routes to a named human, even if the calling agent declared the action safe.
- This table is not exhaustive and is not legal advice. It records the existing statutory expectation that the tool operationalises.
- Canonical status of the certification mark remains in `CERTIFICATION_MARK.md`.
