# Specification vs Enforcement

**Status:** Current as of 24 August 2026  
**Purpose:** Explicitly state the boundary between the normative binary test and any executable or cryptographic implementation inside this repository.

This note answers the precise questions technical readers ask when they first examine the repo.

---

## 1. Canonical definition (Specification)

The normative core of the Burgess Principle is the binary test:

> Was a named human with authority applied to the specific facts of this specific case before the decision took effect?

- **Yes** → SOVEREIGN  
- **No** → NULL  
- Insufficient evidence → AMBIGUOUS (treated operationally as unresolved / lean NULL)

This definition lives in the core papers (particularly the legal/operational papers) and the founding record. It is the authoritative specification. Everything else in the repository is downstream of it.

---

## 2. What currently exists as executable / cryptographic logic

The repository contains supporting machinery that can:

- Record facts in a private, tamper-evident way (Verifiable Memory Palace / ledger style components)
- Produce signed receipts and selective disclosure
- Attest to whether a review occurred and bind that attestation cryptographically
- Maintain audit trails of commitments

These components improve **integrity**, **auditability**, and **proof**. They do not themselves perform the classification of an external institutional process as SOVEREIGN or NULL.

---

## 3. What is still enforced by human application

Live determination of the residual mark (SOVEREIGN / NULL / AMBIGUOUS) on external institutional processes is currently performed by human application of the binary test in real correspondence and proceedings.

The residual mark is then left on the formal record. That human-applied classification, once recorded, becomes part of the public evidence base of the framework.

---

## 4. What remains architectural

A fully executable, pre-execution runtime gate that can sit in front of an arbitrary external system and hard-deny state transitions on a NULL finding is still architectural.

The repository contains the specification and the proof/receipt layers. It does not yet contain a universal enforcer that can autonomously reach into third-party institutional systems and block progression.

---

## 5. Design intention

This separation is intentional at the present stage.

The standard was designed to be applied by a human mind first, then progressively instrumented. The executable and cryptographic layers are being grown around a test that already functions in live proceedings, rather than the reverse.

Future work may tighten the enforcement boundary. Until then, the distinction above is the accurate description of the current state of the repository.

---

*The Burgess Principle*  
UK Certification Mark UK00004343685  
github.com/ljbudgie/burgess-principle
