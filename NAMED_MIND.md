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
Record class: F
Locator: FOI DBC-4186-26 (11 September 2026); Jenny Hoogewerf-McComb
Date: 28 May 2026 (authorisation) / 11 September 2026 (disclosure)
Sentence kept: authoriser of the £990 HMCTS line, "Application fees for Council Tax Liability Orders."
Pattern: dual-role
Clock: internal review window on the FOI
Next official step: appointed auditor — arrangements by which policy is reached (class S, NAO Code)
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
Clock: VTE two months from 11 September 2026 if this is the s.16 response
Next official step: tribunal notice, not a third letter that restarts "consideration"
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

## Code language worth keeping

```
Officer: Suzy Smith
Role / body: Senior Audit Manager, Local Audit Code and Guidance, NAO
Record class: L + S
Locator: letter 11 September 2026; DBC-4226-26 thread; NAO Code of Audit Practice
Date: 11 September 2026
Sentence kept: auditors may examine the arrangements by which policy decisions are reached and consider the effects of the implementation of policy.
Pattern: other (code language)
Clock: operational work stays with the appointed auditor (Mazars)
Next official step: map Tarelli dual-role (class F) onto that sentence; do not ask the NAO to keep a Darlington file a second time
```

---

## Named desks opened 11 September 2026

Not a score table. A clock table. An auto-reply is not a response.
Class X stays on the clock. It does not become a finding.

| Officer | Class | Locator | Sentence | Clock |
| --- | --- | --- | --- | --- |
| Jon White | L | HMC-4717015, 11 Sep 2026, valuationofficecomplaints@hmrc.gov.uk | Named complaints manager; 20 working days | ~9 October 2026 |
| Suzy Smith | L + S | NAO letter 11 Sep 2026 | Arrangements and effects; appointed auditor | Mazars |
| Jenny Hoogewerf-McComb | F | DBC-4186-26 | Named Tarelli on the £990 line; s.42 on gunnercooke | FOI internal review |
| Baldev Singh | L + S | 5501838216, 10 and 11 Sep 2026 | Written appeal response; 13A parked | VTE ~11 November 2026 |
| Public Access unit | F / X | HC/01/FOI/26/019981/V | DCC approved; no name; no EIA | Internal review, 2 months |
| Gavin Foster | L | IPSO 08362-26 | Agreed clarification online and in print | Text, live time, print date |
| Matthew Brown | L | DAR2380553, 11 Sep 2026 16:52 | Min term / 1 November / no T&Cs timestamp | SAR month |
| Susan Hall AM | C / X | GLA Police and Crime, 4 Sep 2026 | Would put three questions to the DMPC | Unanswered 11 Sep 2026 |
| Kaya Comer-Schwartz | X | DMPC / MOPAC | The desk Hall named; no P or L record on this file yet | Do not invent a Hansard code |
| The E.ON Next Team | X | A-18BA6CAF, hi@eonnext.com, 11 Sep 2026 18:44 | Cap notice; phone CTA; net +£71.02 on their table | Hold. Bundle when CNBC issues a number |

Do not copy Duncan Bannatyne on the membership thread. He already threatened
to void the file if other desks were written to.

Hall is class C only for what the Committee wrote. She is class X for the
three questions until a letter or a minute exists. Comer-Schwartz does not
become class P by being a public officer. Fahnbulleh, Rayner, Jones and
Arnold stay off this table until there is a P, C, F or L locator that touches
this file.

---

## Public-source exhibit — three-layer split (20–21 September 2026)

This is not a UK file and not a finding. Class **X** until a P, C, F or L
record exists on *this* repo's live accounts. Do not write Palantir,
Anthropic, CENTCOM or DSIT from this block. Do not claim the Principle would
have prevented the strike.

```
Officer: none on this file
Role / body: public reporting of an unreleased Pentagon review
Record class: X
Locator: Bloomberg investigation published 18–19 September 2026; subsequent UK/US reprints 20–21 September 2026 (Gizmodo, LA Times). Subject: 28 February 2026 strike on Shajareh Tayyebeh school, Minab; officials cited over-reliance on Palantir Maven Smart System and an expectation that the tool would flag stale or contradictory intelligence.
Date: 18–21 September 2026 (reporting). Event date: 28 February 2026.
Sentence kept: HITL is not a named closer. A fusion tool that compresses hours into minutes can still ship a stale label. A named attestation records who recommended and who authorised. It does not refresh the underlying record by itself.
Pattern: other (HITL treated as judgement; large system scrutinised, small repeated act not)
Clock: none on this repo
Next official step: none. Cite only if a UK consultation on meaningful human involvement opens. Do not annex the strike to UK00004343685.
```

Operational stack recorded in public with Paul Blatherwick, LinkedIn,
20 September 2026 (class X — social post):

1. Runtime check of the output.
2. Named attestation at the point of act (who, these facts, authority).
3. Longitudinal measure of the person — not inferred from the signature.
   A clean name is not proof of independent judgement.

Layer 2 is the Burgess Principle. Layer 3 is not. Do not fold 3 into 2.

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
It does not replace [`REGISTER.md`](./REGISTER.md).

I reviewed this. I decided this. I am accountable for these sentences.
