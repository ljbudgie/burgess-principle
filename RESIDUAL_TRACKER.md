# Residual Tracker

UK Certification Mark UK00004343685

The residual mark on an advertising identifier is the same binary test as every other institutional process.

> Before an identifier keeps emitting, and before that emission is sold or reused, has a named human with authority applied their mind to *this* device and *this* purpose?
>
> If yes: **SOVEREIGN**.
> If no: **NULL**.

A default that stays on because "that is how the device ships" is not a decision. It is process.

---

## What this is

A **residual tracker** is an advertising ID, analytics ID, or location-adjacent identifier that keeps moving after the person thinks the interaction has ended.

It is the data-layer twin of the residual mark already used on correspondence: something left on the file that nobody named agreed to keep there.

OpenHear is residual *hearing* — signal the institution treated as unused. This file is residual *telemetry* — signal the device kept sending because no named human switched it off.

End state the framework is aiming at: **unwanted advertising identifiers off unless a named human turns them on for a stated purpose, in writing, with a date.**

This file is not a targeting guide. It does not describe how location data is used against anyone. It records only the accountability question and the public proof that the identifier can be disabled.

---

## Scoring

Apply [`INSTITUTION_AUDIT_TAXONOMY.md`](./INSTITUTION_AUDIT_TAXONOMY.md) unchanged.

| Evidence | Finding |
| --- | --- |
| Identifier on by default; no named officer for this fleet or this person | **NULL** |
| Broker or publisher reuses the stream with no named human for this purpose | **NULL** |
| Institution says "industry standard" or "the OS requires it" with no name | **NULL** |
| Named official confirms the identifier is disabled, with date | **SOVEREIGN** on that disablement |
| Person asks for ads/trackers off and is sent to a portal or a telephone queue | Accessibility / channel **NULL** if email-only was already on the file |

D2 still requires the specific facts of the specific device or account. A global privacy policy is D2 = 1.

---

## Public proof that disablement is a decision

On 4 September 2026 Reuters reported letters released by US Senator Ron Wyden. US military services stated they had disabled advertising identifiers on phones and computers after commercially available location data became a live risk to forces.

That is the point for this framework:

1. The identifier was optional.
2. Leaving it on was an unowned default.
3. A named official could turn it off and put the date on paper.

UK public bodies and regulated firms do not get a special exception. PECR and UK GDPR still require a lawful basis and, for non-essential cookies and similar identifiers, consent that is not buried in a default.

---

## What to put on the register

Record:

- device or service class (phone, laptop, app, smart TV);
- the identifier type if known (advertising ID, not a new exploit);
- whether a named human confirmed on / off, and the date;
- the channel used to ask (email-only remains the reasonable adjustment on this project);
- any onward reuse the institution admits in writing.

Do not record methods for extracting or weaponising location. The live findings ledger takes the correspondence fact, not the payload.

---

## Related files

- [`SPECIFICATION_VS_ENFORCEMENT.md`](./SPECIFICATION_VS_ENFORCEMENT.md) — residual mark as live determination
- [`INSTITUTION_AUDIT_TAXONOMY.md`](./INSTITUTION_AUDIT_TAXONOMY.md) — D1–D5 anchors
- [`LIVE_AUDIT_LOG.md`](./LIVE_AUDIT_LOG.md) — where a scored finding is written
- [`OPENHEAR_LICENSING_FRAMEWORK.md`](./OPENHEAR_LICENSING_FRAMEWORK.md) — residual hearing, same sovereignty idea
