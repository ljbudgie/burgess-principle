# Named-mind index

The institutional register scores a body. The binary test scores a person.

A unit signature, a "we", or a role without a name is not a mind on the file.
A named officer who puts one sentence on the file is an exhibit. Keep the
sentence. Do not restate the week.

This file is not a private case dump and not a replacement for
[`INSTITUTIONAL_REGISTER.md`](./INSTITUTIONAL_REGISTER.md). It is the missing
unit: the officer.

Standing language for the letter itself: [`REGISTER.md`](./REGISTER.md).

An entry in this file is only as strong as its **record class**. A Commons
column is official for what was said in the House. An officer's email is
official for what that officer wrote. They are not interchangeable. Do not
file a press line under a Hansard code. Do not file a Hansard column as if
it decided a live account.

---

## Record class — required on every entry

Use one class. If two records exist, make two entries.

| Class | What it is | Locator you must keep | What a court or regulator can treat it as |
| --- | --- | --- | --- |
| **P** Parliamentary | Spoken in the House, written answer, or written ministerial statement | `HC Deb date, vol, col` / `HL Deb …` / `HC 12345` UIN / `HL 1234` / `HCWS` / `HLWS` | Official Report of that utterance. Not a decision on a named account. |
| **C** Committee / Assembly | Select committee, GLA committee, PCC panel, appointed auditor letter that is a published report | Committee name, session, paper number (`HC 2025-26 274`) or minute date and item | Evidence to that body, or that body's published finding. |
| **F** FOI / EIR | A numbered information-rights reply | Force/council reference + date + whether signed by a name or a unit | What that public authority said it held, or did not hold, on that date. |
| **L** Named letter | Email or letter that names the officer and the file | Date, time, from-address, subject, account or case number. Keep the `.eml` or PDF. | What that officer put on that file. This is the usual exhibit. |
| **S** Statute / scheme / code | The rule the officer cited or should have cited | Act + section, licence condition, NAO Code paragraph, Editors' Code clause | The law or code. Not proof that the officer applied it. |
| **X** No official record | Speech, press release, social post, "Team" footer, unit signature | URL + date, or "none" | AMBIGUOUS until a P, C, F or L record exists. Do not cite as a decision. |

### Locator rules

- **P.** Volume and column, or UIN, or `HCWS`. Add the hansard.parliament.uk URL if you have it. The URL does not replace the code.
- **F.** The authority's own reference (DBC-4186-26, HC/01/FOI/26/019981/V, HMC-4717015). A covering mailbox is not the locator.
- **L.** Date and time in the sender's timezone, plus the account or case number the officer used. If they later call the same text the written response, say so in the entry.
- **S.** Pin the subsection. Section 13A is not enough. Section 13A(1)(c) or 13A(2) is.
- **X.** Leave the name on the clock table if you must. Do not promote it to a finding.

### Entry template

Copy this block. Empty fields stay empty. Do not invent a Hansard code.

```
Officer:
Role / body:
Record class: P | C | F | L | S | X
Locator:
Date:
Sentence kept: "…"
Pattern: dual-role | subsection-swap | min-term | role-without-name | other
Clock:
Next official step:
```

A bundle tab is: class + locator + the sentence. That is the whole exhibit.

---

## Four patterns that recur

These are reusable. The names below are the specimens, not the only instances.

### 1. Dual role

The same named officer authorises the enforcement spend and decides the
welfare question on the accounts in that spend.

```
Officer: Wendy Tarelli
Role / body: Revenues and Benefits Manager, Darlington Borough Council
Record class: F + L
Locator: FOI DBC-4186-26 (11 September 2026); paper reminder 16 September 2026 account 55018335332 / summons 268/7584060; nominated correspondent thread 24 September 2026
Date: 28 May 2026 (authorisation) / 11 September 2026 (disclosure) / 16 September 2026 (signed reminder)
Sentence kept: authoriser of the £990 HMCTS line, "Application fees for Council Tax Liability Orders." Same name on the 16 September paper reminder to Nicola Patterson.
Pattern: dual-role
Clock: internal review window on the FOI; Equita hold requested 24 September 2026
Next official step: appointed auditor — arrangements by which policy is reached (class S, NAO Code); do not treat the paper reminder as a new merits decision
```

Why it matters: that is an arrangement, not a policy preference.

### 2. Subsection swap

The officer agrees the Act gives a power, then quotes a different subsection
to stop using it.

```
Officer: Baldev Singh
Role / body: Revenues and Benefits Team Leader, Darlington Borough Council
Record class: L + S
Locator: emails 10 and 11 September 2026, 15:56; account 5501838216; LGFA 1992 s.13A(1)(c) against s.13A(2)
Date: 11 September 2026
Sentence kept: "The Section 13a Discretionary Relief will not be dealt with, until the Council Tax Support review has been completed." Also: both emails are the Council's written response to the appeal.
Pattern: subsection-swap
Clock: VTE two months from 11 September 2026 if this is the s.16(7) notification — ~11 November 2026
Next official step: fresh VTE notice on the 11 September letters. VT00041152 is dead. Do not restart "consideration" with a third letter.
```

Why it matters: a policy precondition the Act does not contain, in the
officer's own name, on the section 16 clock.

### 3. Minimum term treated as an ending

A date that ends a commitment period is written as if it ended the contract.

```
Officer: Matthew Brown
Role / body: Customer and Legal Manager, The Bannatyne Group
Record class: L
Locator: email 11 September 2026, 16:52; DAR2380553; attachments Membership / Welcome
Date: 11 September 2026
Sentence kept: minimum term ended 9 January 2026 and then continued indefinitely; no historic T&Cs version against an acceptance timestamp; termination set at 1 November 2026 after written cancellation 3 September 2026.
Pattern: min-term
Clock: SAR statutory month (SAR is not completed by this bundle)
Next official step: clause and version that turns 3 September notice into 1 November; no collector while the SAR is open
```

Why it matters: January is not a discharge. The missing timestamp is the
exhibit on the terms themselves.

### 4. Role without a name

A decision is admitted. The officer who approved it is given only as a rank.
The letter is signed by a unit.

```
Officer: none on the face (Deputy Chief Constable, unnamed)
Role / body: Hampshire and Isle of Wight Constabulary
Record class: F (unit-signed — treat as X until a name exists)
Locator: HC/01/FOI/26/019981/V, 11 September 2026, Public Access Joint Information Management Unit
Date: 11 September 2026
Sentence kept: pay-progression link agreed by the People Board and approved by the Deputy Chief Constable; no Equality Impact Assessment.
Pattern: role-without-name
Clock: internal review, 2 months
Next official step: name the Deputy Chief Constable and produce the People Board record, or confirm not held
```

Why it matters: AMBIGUOUS until the name exists. Internal review is the next
act, not a second essay.

---

## Named review that closed with a payment (12 October 2026)

```
Officer: Jon White
Role / body: Complaints Manager, Valuation Office Agency (part of HMRC)
Record class: L
Locator: email 12 October 2026, 15:43 UTC; HMC-4717015; valuationofficecomplaints@hmrc.gov.uk; address 26A Duke Street, Darlington, DL3 7AJ
Date: 12 October 2026
Sentence kept: named officer; accepted failings on the reasonable adjustment; confirmed email route via formhelpvo@hmrc.gov.uk; confirmed no penalty issued; apologised; offered £200. Payment accepted same day. Certification ask sent same day.
Pattern: other (named review + redress)
Clock: BACS form to transactionsservicesteamvo@hmrc.gov.uk; certification decision still open
Next official step: confirmation the £200 has been paid; the name of the person who decides whether the free standard is wanted on the complaints process
```

Why it matters: a public body named the officer, accepted the adjustment gap, and paid. That is the exhibit others can read.

UK Certification Mark UK00004343685 entered the register 9 October 2026 (effective 22 February 2026). That is a status change on the mark, not a named-mind finding. Do not file it as an officer's sentence.

---

## What this file refuses

It does not score an institution from a single email.
It does not treat a minimum-term date as a termination.
It does not invent a Deputy Chief Constable's name.
It does not invent a Hansard volume for a person who did not speak.
It does not claim a refused recovery hold is automatically unlawful.
It does not treat a price-cap notice as a confession.
It does not treat a class-X press report as a decision, or as proof that a
named closer would have changed a targeting outcome.
It does not treat an OPCC-upheld police complaint as certification of the mark.
It does not treat a VTE strike-out on prematurity as a decision on 13A.
It does not treat an OPCC closure email as the Force's 28ZA notification.
It does not treat a Group Portal flag as certification of the mark.
It does not replace [`REGISTER.md`](./REGISTER.md).

I reviewed this. I decided this. I am accountable for these sentences.
