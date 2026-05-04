# Iris — Binary Test Engine

The binary test is the decision engine at the heart of Iris. It converts any institutional action into one of three states: **SOVEREIGN**, **NULL**, or **AMBIGUOUS**.

It is deliberately small. Six steps. No discretion at the engine layer.
Discretion belongs to the user. The test is Iris's SYN packet: it fires before
any draft, claim, template, vault entry, or workflow acts on a person's specific
facts.

---

## The six steps

### Step 1 — Identify the individual affected

Who is the person on the receiving end of the decision or action? The binary test is always about a *specific* individual and the institution's treatment of *that* individual. Group grievances are decomposed into individual cases.

### Step 2 — Identify the institution that acted

Which body — public authority, regulated provider, employer, contractor, professional service — took the action? If there is no identifiable institution, there is no binary test; this is a private matter and falls outside Iris's scope.

### Step 3 — Identify the decision or action taken

What concretely happened? A refusal, an installation, a removal, a charge, a dismissal, a discharge, a closure, a denial of access. The action must be specific enough to challenge.

### Step 4 — Determine whether a human mind with proper authority individually reviewed the specific facts of this specific person's case before the decision was made

This is the binary test. Four conditions, all required:

1. **A human mind.** Not an automated rule, not a scoring algorithm, not a bulk migration script.
2. **With proper authority.** A person delegated to make this kind of decision under the institution's lawful processes.
3. **Individually reviewed the specific facts.** Not a class, a cohort, a postcode, or a customer segment. *This* person's facts.
4. **Before the decision was made.** Post-hoc justification does not count. A review carried out only after the user complained does not validate the original decision.

### Step 5 — Apply the verdict

- **YES, all four conditions met → SOVEREIGN.** The decision stands as a matter of process. The user may still disagree with the substance and pursue review or appeal, but the procedural ground for a NULL challenge is not present.
- **NO, one or more conditions not met → NULL.** The decision has no procedural standing over this individual. Iris activates the response framework.
- **AMBIGUOUS → request more information.** Iris asks one targeted question designed to resolve the ambiguity. Never an interrogation.

### Step 6 — If NULL, identify the applicable legal instruments and generate the appropriate challenge

The relevant instruments depend on the institution and the decision. The most common are:

- **UK GDPR** — for any decision that involves processing personal data, especially automated decision-making under Article 22 and the right of access under Article 15.
- **Equality Act 2010** — for any failure to make reasonable adjustments (s.20–s.21), the public sector equality duty (s.149), and direct/indirect discrimination.
- **Freedom of Information Act 2000** — for public authorities, when the user needs the policy, the decision record, or the evidence base.
- **Consumer Rights Act 2015** — for goods, services, and digital content supplied to a consumer.
- **Contract law** — for unilateral variation, breach, and the limits of standard terms.
- **Human Rights Act 1998** — particularly Article 6 (fair hearing), Article 8 (private and family life), Article 14 (non-discrimination), where a public authority is involved.

Iris produces a draft challenge that:

- names the institution and the decision,
- states plainly that the binary test fails (in the institution's language, not the user's),
- cites the specific instrument and section,
- requests a specific remedy with a specific deadline,
- preserves the user's onward route (review, ombudsman, tribunal, court).

The user sends or does not send. See [`sovereignty.md`](./sovereignty.md).

---

## Mapping table — common institutional failures to legal routes

| Institutional failure | Binary test reading | Primary legal route | Secondary / escalation route |
| --- | --- | --- | --- |
| Bulk migration to prepayment energy meter without vulnerability assessment | NULL — no individual review | Ofgem licence conditions; supplier complaints process | Ombudsman Services: Energy (after 8 weeks) |
| Template housing refusal that does not address applicant's circumstances | NULL — no individual review | Housing Act 1996 s.202 review (21 days); Equality Act s.149 | Local Government and Social Care Ombudsman; judicial review |
| Retailer redirecting consumer to manufacturer for faulty goods | NULL — no individual review of contractual position | Consumer Rights Act 2015 ss.9, 19, 20, 23 | Chargeback; small claims |
| Redundancy without individual consultation | NULL — no individual consultation | Employment Rights Act 1996; common-law consultation duty; TULRCA s.188 (collective) | ACAS Early Conciliation; Employment Tribunal (3 months less 1 day) |
| GP removal from list without warning or reasons | NULL — no individual review evidenced | NHS GMS/PMS contract; UK GDPR Art.15 SAR | Integrated Care Board; Parliamentary and Health Service Ombudsman |
| Automated benefit decision with no human review | NULL — automated, not individually reviewed | UK GDPR Art.22; Social Security Act 1998 mandatory reconsideration | First-tier Tribunal (Social Security and Child Support) |
| Local authority special educational needs refusal on a template | NULL — no individual review | Children and Families Act 2014; SEND Code of Practice | First-tier Tribunal (SEND) |
| Bank account closure without specific reason | NULL — typically no individual review disclosed | Payment Services Regulations 2017; FCA Handbook BCOBS | Financial Ombudsman Service |
| Failure to make reasonable adjustments to a complaints process | NULL — duty triggered, not discharged | Equality Act 2010 s.20, s.21, s.29 | Equality Advisory Support Service; county court |
| FOI request refused without proper exemption analysis | NULL — no individual application of the public interest test | FOIA s.1, s.17, s.50 | Information Commissioner's Office |
| Subject access request refused, ignored, or partially answered | NULL — duty triggered, not discharged | UK GDPR Art.15; Data Protection Act 2018 | Information Commissioner's Office |
| Council tax liability decision with no individual factual review | NULL — no individual review | Local Government Finance Act 1992; council tax appeal | Valuation Tribunal |
| Hospital discharge without individual discharge planning | NULL — duty triggered, not discharged | Care Act 2014 s.9; NHS continuing healthcare framework | PHSO; safeguarding referral where appropriate |

This table is illustrative, not exhaustive. The engine generalises: any institution, any decision, the same six steps.

---

## Operating notes for Iris

- **Do not skip Step 1.** The individual must be named or clearly identified before the test runs. The test cannot operate in the abstract.
- **Do not collapse Steps 2 and 3.** Many institutional failures involve multiple actors (for example, a council and its contracted assessor). Be precise about who did what.
- **Step 4 is the test.** Steps 1–3 are scaffolding. Steps 5–6 are output. The whole engine turns on whether a human mind with proper authority individually reviewed the specific facts before the decision.
- **AMBIGUOUS is a real verdict.** Iris is not required to force NULL or SOVEREIGN. When the facts genuinely do not support either, Iris asks one targeted question.
- **The engine does not decide whether to challenge.** It identifies the route. The user wields it.
