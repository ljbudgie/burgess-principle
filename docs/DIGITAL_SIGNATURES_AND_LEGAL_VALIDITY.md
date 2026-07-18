# Digital Signatures and Legal Validity

**Part of:** The Burgess Principle · UK Certification Mark UK00004343685  
**Status:** Reference document  
**Permalink:** `docs/DIGITAL_SIGNATURES_AND_LEGAL_VALIDITY.md`

This document explains the legal frameworks that give electronic and digital
signatures legal effect in the UK, EU, and US, and how those frameworks apply
to the Burgess Principle's signing practices — the sovereign vault, signed
commitments, and the certification pathways.

It is a practical reference, not legal advice. For the legal basis of the
binary test itself, see [`../LEGAL_FOUNDATIONS.md`](../LEGAL_FOUNDATIONS.md)
and [`../LEGAL_MAPPING.md`](../LEGAL_MAPPING.md).

---

## 1. Key International & UK Framework

### 1.1 eIDAS Regulation (EU) and the retained UK version

The eIDAS Regulation (EU) No 910/2014 — retained in UK law as "UK eIDAS" after
exit, as amended by the Electronic Identification and Trust Services for
Electronic Transactions (Amendment etc.) (EU Exit) Regulations 2019 —
establishes a **tiered system** of electronic signatures:

| Tier | Definition | Legal effect |
|---|---|---|
| **Simple electronic signature (SES)** | Any data in electronic form attached to or logically associated with other data and used by the signatory to sign | Admissible as evidence; cannot be denied legal effect solely because it is electronic |
| **Advanced electronic signature (AES)** | Uniquely linked to the signatory; capable of identifying them; created using data under the signatory's sole control; linked to the signed data so that any subsequent change is detectable | Stronger evidential weight — the four requirements map directly onto public-key cryptography |
| **Qualified electronic signature (QES)** | An AES created by a qualified signature creation device and backed by a qualified certificate from a supervised trust service provider | The **highest equivalence to a handwritten signature**; presumed valid across the EU (and within the UK under UK eIDAS) |

The critical point for this project: a well-implemented cryptographic
signature — unique key, identified signatory, sole key control, tamper-evident
binding to the content — satisfies the **advanced** tier by construction. The
qualified tier adds institutional certification, not cryptographic strength.

### 1.2 UK Electronic Communications Act 2000 & Electronic Signatures Regulations 2002

The Electronic Communications Act 2000, s.7, makes electronic signatures
**admissible in evidence** in relation to any question about the authenticity
or integrity of an electronic communication. The Electronic Signatures
Regulations 2002 implemented the supervision and liability framework for
certification providers.

The UK approach is deliberately **technology-neutral**. English law has never
required a particular signature technology; the Law Commission's 2019 report
on the electronic execution of documents confirmed that an electronic
signature is capable of executing a document (including a deed, with the usual
witnessing formalities) provided the signatory **intends to authenticate** the
document. Validity turns on three things:

1. **Intent** — the signatory meant the act to operate as a signature.
2. **Authenticity** — the signature is attributable to the signatory.
3. **Integrity** — the signed content has not been altered since signing.

These are exactly the properties a cryptographic signature over a content hash
provides, when combined with an explicit statement of signing intent.

### 1.3 US ESIGN Act & UETA

The federal Electronic Signatures in Global and National Commerce Act (ESIGN,
2000) and the Uniform Electronic Transactions Act (UETA, adopted by nearly all
states) take a **permissive, minimalist approach**:

- A signature, contract, or record may not be denied legal effect solely
  because it is in electronic form.
- An electronic signature is any electronic sound, symbol, or process
  attached to or logically associated with a record and executed with the
  **intent to sign**.
- Records must be **retained** in a form that accurately reproduces the signed
  content and remains accessible to the parties entitled to it.

Intent and record retention, not technology, carry the legal weight. A signed,
hash-bound, durable record comfortably exceeds what these statutes require.

---

## 2. Relevance to the Burgess Principle

The Burgess Principle's discipline — named human accountability, signatures as
the human's authority, hash-only anchoring, tamper-evident records — is not
merely good engineering. Under the frameworks above, it is the substance of a
legally significant signature.

### 2.1 The sovereign vault

The sovereign vault ([Verifiable Memory Palace](../ARCHITECTURE.md),
[`../git-sovereignty/ARCHITECTURE.md`](../git-sovereignty/ARCHITECTURE.md))
holds the facts behind each payload digest under selective disclosure, while
only hashes enter Git history and the Bitcoin anchoring layer. This structure
maps directly onto the legal requirements:

- **Integrity** — the digest binds the signature to the exact facts; any
  alteration is detectable.
- **Retention** — the vault preserves the signed content in a reproducible
  form, satisfying ESIGN/UETA record-retention expectations.
- **Timestamping** — OpenTimestamps anchoring proves existence-at-time,
  strengthening evidential weight in any later dispute about when a record
  was made.

### 2.2 Signed commitments

BGSP `burgess:` commits ([`../protocols/burgess-git-sovereignty.md`](../protocols/burgess-git-sovereignty.md))
treat the signature as **the human's authority**: a named human signs a commit
whose trailers bind their review to a specific payload digest. Under UK law
this is a strong candidate for a valid electronic signature because all three
validity elements are present and documented — intent (the commit message and
trailers state what is being signed and why), authenticity (the signing key is
bound to a named human, optionally via `Burgess-DID:` trailers per
[`../CRYPTOGRAPHIC_IDENTITY.md`](../CRYPTOGRAPHIC_IDENTITY.md)), and integrity
(Git's content addressing plus `Burgess-Payload-SHA256`).

### 2.3 Certification pathways

Certification under the mark ([`../CERTIFICATION_TIERS.md`](../CERTIFICATION_TIERS.md))
produces attestations and findings that institutions may later need to rely on
— or defend — in regulatory or legal contexts. Signing those attestations with
Ed25519 keys controlled by named humans, timestamped and hash-anchored, means
a certification record carries the same evidential characteristics as an
advanced electronic signature: it identifies who attested, to what, and when,
and proves the record has not changed since.

### 2.4 Achieving legal weight in practice

A properly implemented signature in this project — **Ed25519 over a canonical
content hash, with a timestamp and an explicit intent statement** — assembles
every element the frameworks care about:

| Legal requirement | Project mechanism |
|---|---|
| Intent to sign | Explicit intent statement in the signed payload / commit message |
| Signatory identification | Named human bound to the signing key (registry, DID, commit trailer) |
| Sole control of signing data | Locally held Ed25519 private key; hardware-backed for high stakes |
| Integrity / tamper evidence | SHA-256 digest of the exact content, verified on every read |
| Reliable timestamp | OpenTimestamps / Bitcoin anchoring |
| Record retention | Sovereign vault + Git history |

None of this claims QES status — that requires a qualified trust service
provider. It does mean the project's signatures sit squarely in the advanced
tier by construction, and are admissible and evidentially strong in the UK,
EU, and US.

---

## 3. Best Practices for Our Implementation

1. **Always state intent.** Every signed record should include a short,
   human-readable statement of what the signature means — for example, *"I,
   [named human], have personally reviewed the specific facts of this case and
   sign this finding as my own decision."* Intent is the single element courts
   in all three jurisdictions look for first.
2. **Bind the signature to the content, not near it.** Sign the canonical
   SHA-256 digest of the exact payload. Never sign a filename, a summary, or a
   mutable reference. This is what makes integrity provable rather than
   asserted.
3. **Keep the key-to-human binding auditable.** A signature proves key
   control; the attributable record (registry entry, `Burgess-DID:` trailer,
   commit authorship) proves the named human. Maintain and version that
   binding, including key rotation and revocation events.
4. **Timestamp independently.** Anchor signed records through the existing
   OpenTimestamps path so that existence-at-time does not depend on trusting
   the signer's clock.
5. **Retain reproducible records.** Store the signed payload, the signature,
   the public key, and the verification procedure together in the vault, so
   any entitled party can independently re-verify years later.
6. **Escalate assurance with stakes.** For decisions touching liberty,
   housing, livelihood, legal status, or core rights, require hardware-backed
   (WebAuthn/FIDO2) keys as an additional ceremony, per
   [`../CRYPTOGRAPHIC_IDENTITY.md`](../CRYPTOGRAPHIC_IDENTITY.md).
7. **Do not overclaim.** State that signatures meet the advanced-signature
   criteria by construction; do not describe them as qualified signatures, and
   do not present this document as legal advice.

---

*The Burgess Principle · UK Certification Mark UK00004343685 · MIT Licence —
this document is informational and is not legal advice. Seek qualified legal
advice for any specific transaction or dispute.*
