# US AI Civil Rights Act Mapping

This note maps the Burgess Principle to the key mechanisms of the proposed US
**Artificial Intelligence Civil Rights Act**. It is a plain-language compliance
aid, not a substitute for legal advice.

**Last reviewed:** 14 July 2026

## Status — proposed legislation, not enacted law

The Artificial Intelligence Civil Rights Act is a **bill**, not enacted law. It
was introduced by Senator Edward J. Markey as **S.5152** in the 118th Congress
on 24 September 2024 and referred to the Senate Committee on Commerce, Science,
and Transportation, where it did not progress. It was reintroduced in the 119th
Congress in December 2025 as **S.3308** (Senate) and **H.R.6356** (House).

Nothing in this document should be read as claiming the bill imposes any legal
obligation today. It imposes none. The value of this mapping is anticipatory:
if the bill (or a successor) is enacted, the binary test already supplies the
operational measure its mechanisms would need. Until then, this page tracks
convergence, nothing more.

## Covered algorithms in consequential decisions

The bill regulates algorithms used in consequential decisions — employment,
housing, healthcare, financial services, education, criminal justice, public
accommodations, and government services. This is exactly the territory where
the Burgess question applies: institutional power meeting an identified person.

For each such decision, the binary test asks whether a human member of the team
was able to personally review the specific facts of the specific situation
before the system acted. A SOVEREIGN result means the record identifies a named
human reviewer, the role that person held, the facts personally reviewed, and
the timing of the review. A NULL result means the algorithm processed the case
without individual human review. An AMBIGUOUS result means the organisation has
described a process but has not confirmed personal scrutiny of the specific
facts.

## Pre-deployment evaluations and impact assessments

The bill would require developers and deployers of covered algorithms to
conduct independently audited pre-deployment evaluations and post-deployment
impact assessments to identify and mitigate discriminatory outcomes.

The Burgess record — named reviewer, role, facts reviewed, timing — is the
individual-scrutiny evidence such audits would need. An aggregate bias audit
answers a statistical question; the binary test answers the individual one. An
assessment that cannot show whether any specific affected person received
individual human review has documented a process, not scrutiny. Recording the
SOVEREIGN / NULL / AMBIGUOUS classification per affected person turns an
abstract assessment obligation into a checkable evidential trail.

## Consumer notification and transparency

The bill would require individuals to be notified when a consequential decision
is made by an algorithm, with information about how the decision was made.

This aligns with the framing already used for Article 86 of the EU AI Act (see
[EU-AI-ACT-MAPPING.md](./EU-AI-ACT-MAPPING.md)): a notice that says a case was
handled under policy, quality checked, or subject to human oversight does not
answer the Burgess question. A notice that names no human who reviewed the
specific facts is NULL or AMBIGUOUS, not SOVEREIGN. The practical route is the
same in both jurisdictions: ask for the algorithm's role, the human reviewer's
name and role, the facts reviewed, and the timing of that review.

## Enforcement — FTC, state attorneys general, private right of action

The bill provides for enforcement by the Federal Trade Commission and state
attorneys general, and a private right of action for individuals harmed by
algorithmic discrimination.

For individuals, this would sit alongside the existing US civil-rights remedy
route discussed in
[papers/US_CONSTITUTIONAL_ADDENDUM.md](./papers/US_CONSTITUTIONAL_ADDENDUM.md)
— the 42 U.S.C. § 1983 civil rights lawsuit for deprivation of constitutional
rights under colour of law. That document covers the constitutional analysis
(Fourth and Fourteenth Amendment, the "rubber stamp" doctrine); this mapping is
not a duplicate of it. The connection is evidential: in either route, a NULL
finding — no named human applied their mind to the specific facts before the
decision — is the factual core a claimant would need to establish.

## Primary sources

- S.5152 (118th Congress, as introduced): [congress.gov/118/bills/s5152/BILLS-118s5152is.pdf](https://www.congress.gov/118/bills/s5152/BILLS-118s5152is.pdf)
- S.5152 bill record: [govinfo.gov/app/details/BILLS-118s5152is](https://www.govinfo.gov/app/details/BILLS-118s5152is)
- S.3308 (119th Congress, as introduced): [govinfo.gov/app/details/BILLS-119s3308is](https://www.govinfo.gov/app/details/BILLS-119s3308is)
- H.R.6356 (119th Congress): [congress.gov/bill/119th-congress/house-bill/6356](https://www.congress.gov/bill/119th-congress/house-bill/6356)

---

## Related documents

- [LEGAL_MAPPING.md](./LEGAL_MAPPING.md) — master statutory and regulatory cross-reference index
- [EU-AI-ACT-MAPPING.md](./EU-AI-ACT-MAPPING.md) — Art 14, 26, 86 detailed mapping (enacted EU law)
- [papers/US_CONSTITUTIONAL_ADDENDUM.md](./papers/US_CONSTITUTIONAL_ADDENDUM.md) — Fourth / Fourteenth Amendment analysis and the § 1983 civil rights remedy
