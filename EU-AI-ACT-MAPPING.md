# EU AI Act Mapping

This note maps the Burgess Principle to three provisions of Regulation (EU)
2024/1689. It is a plain-language compliance aid, not a substitute for legal
advice. The relevant obligations discussed here apply from **2 August 2026**.

## Article 14 — Human oversight

Article 14 requires high-risk AI systems to be designed and used with effective
human oversight. The Burgess Principle supplies a factual question for that
oversight: was a human member of the team able to personally review the specific
facts of the specific situation before the system acted?

A SOVEREIGN result means the record identifies a named human reviewer, the role
that person held, the facts personally reviewed, and the timing of the review. A
NULL result means the system processed the case without individual human review.
An AMBIGUOUS result means the organisation has described a process but has not
confirmed personal scrutiny of the specific facts.

The framework does not replace Article 14 controls. It helps show whether the
human oversight was real at the point where institutional power met an identified
person.

## Article 26 — Deployer obligations

Article 26 places obligations on deployers of high-risk AI systems, including use
in accordance with instructions, appropriate human oversight, monitoring, and
record-keeping. The Burgess Principle gives deployers a simple record to keep for
each affected person: who reviewed the specific facts, what they reviewed, and
whether that review happened before action was taken.

For deployers, a NULL finding should stop the decision from being treated as
individually considered. The proper next step is escalation to a named human
reviewer who can examine the specific facts before the action continues.
AMBIGUOUS process language should be resolved by asking for the reviewer’s name,
role, specific facts reviewed, and timing.

This makes Article 26 operational without turning the framework into a badge. The
question remains evidential: did individual human scrutiny happen or not?

## Article 50 — Transparency obligations for AI systems (chatbot disclosure)

### The obligation

Article 50(1) requires providers of AI systems intended to interact directly with
natural persons to ensure that those systems inform the person they are interacting
with an AI — unless this is obvious from context. This obligation applies from
**2 August 2026**.

The practical scope is wide. Customer service platforms built on Intercom, Zendesk,
Salesforce Service Cloud, Genesys, and equivalents are AI systems interacting
directly with natural persons. Where they handle complaints, billing disputes,
account changes, access decisions, or any request that produces effects for the
individual, Article 50(1) applies. From 2 August, failing to disclose is a breach
without further analysis.

### Why disclosure and human involvement stack

Article 50 and Articles 22A–22D do not operate independently. They stack.

The moment a chatbot discloses that it is an AI — as Article 50(1) now requires
— it simultaneously activates the human involvement question under Articles 22A–22D
(UK: DUAA 2025 s.80). Disclosure identifies the system as automated. If that
automated system is making or influencing a significant decision, the affected
person has an immediate right to meaningful human involvement before that decision
stands.

Compliance with Article 50 is therefore incomplete without also being able to
answer the binary test. An institution that discloses "you are talking to an AI"
and then cannot name a human reviewer who applied their mind to the specific facts
before the decision is compliant with Article 50 and simultaneously NULL under
Articles 22A–22D.

The two obligations are not alternative. They are cumulative.

### The two-question test for chatbot interactions

When engaging with a customer service chatbot from **2 August 2026**:

| Question | Legal basis | Expected answer | If absent |
|---|---|---|---|
| **1. Has the system disclosed it is AI?** | EU AI Act Art. 50(1) | Yes, before or at first interaction | Art. 50 breach — reportable to national market surveillance authority |
| **2. Was a named human's mind applied to the specific facts before the decision?** | DUAA 2025 Arts. 22A–22D / UK GDPR | Named person, role, specific facts, pre-decision timing, authority to differ | NULL — binary test result; escalation right activated |

A system can satisfy Question 1 and fail Question 2. Disclosure is not human
review. The binary test is the evidential standard for Question 2, and no amount
of transparency language in the disclosure satisfies it.

### The Intercom / Zendesk / Salesforce / Genesys tier

These platforms are the infrastructure layer for customer-facing AI decisions
across energy, banking, telecoms, and consumer services. Three obligations
currently stack for any deployer in this tier:

**Obligation 1 — Article 50(1) disclosure** (from 2 August 2026, EU AI Act)
The bot must say it is AI at the point of first interaction, not buried in terms.

**Obligation 2 — Meaningful human involvement** (in force 5 February 2026, DUAA 2025 s.80)
For any significant decision — refusal, enforcement action, account restriction,
complaint closure — a genuine human route must exist. Process language ("our team
reviews", "subject to human oversight") does not satisfy this. A named individual
who reviewed the specific facts before the decision was taken is required.

**Obligation 3 — EA 2010 s.19 indirect discrimination** (ongoing, UK only)
Where the platform's account-matching, authentication, or communication channel
applies a provision, criterion, or practice that puts disabled users at a
particular disadvantage, that is indirect discrimination regardless of the binary
test outcome on the underlying decision. Account-matching by registered email
address (where a deaf user's complaint email differs from their account email)
is a live example from the dataset — Trading 212 / Zendesk, entry #(see ledger).

### Act-now significance

The Article 50(1) deadline of 2 August 2026 is the hook. Institutions in this
tier that are not yet compliant have a short window. The prudent response is not
only to add the disclosure — it is to simultaneously audit the human review
pathway for significant decisions, because disclosure without that pathway
satisfies one obligation while confirming breach of the other.

The Burgess Principle provides institutions with the practical route: certify the
human review pathway under the binary test, so that when the chatbot discloses
it is AI, the institution can also demonstrate that a named human with authority
to differ is in the decision loop before significant effects are produced.

A certified institution deploying a chatbot can truthfully say: "This system is
AI. For decisions that significantly affect you, a named human reviewer with
authority to reach a different outcome will review the specific facts before the
decision stands." That is the combined compliance position. Neither obligation
alone achieves it.

---

## Article 86 — Right to explanation

Article 86 gives affected persons a right to obtain clear and meaningful
explanations of the role of a high-risk AI system in decisions that produce legal
effects or similarly significant effects. The Burgess Principle aligns with that
right by asking for the human point of accountability behind the decision.

An explanation that only says a case was handled under policy, quality checked,
or subject to human oversight does not answer the Burgess question. The person
needs to know whether a specific human reviewed their specific facts, before the
decision affected them.

From **2 August 2026**, this mapping should be read as a practical route for
framing Article 86 requests: ask for the AI system’s role, the human reviewer’s
name and role, the facts reviewed, and the timing of that review. If those facts
cannot be provided, the result is NULL or AMBIGUOUS rather than SOVEREIGN.

---

## Related documents

- [ADM_HUMAN_REVIEW.md](./ADM_HUMAN_REVIEW.md) — DUAA 2025 s.80 statutory analysis; two-limb mapping (Art 22A general / s.50A law enforcement); ACS/APS Home Office AI tools; reusable Human Review Mandate argument block
- [LEGAL_MAPPING.md](./LEGAL_MAPPING.md) — master statutory and regulatory cross-reference index
- [IMMIGRATION.md](./IMMIGRATION.md) — binary test applied to asylum determination, age assessment, and enforcement prioritisation
