# Release Notes — v2.5.1

## On the Record: Academic Publication, Accessibility, and a Transparent Ledger

Released: 31 May 2026

v2.5.1 is a credibility-and-accessibility release. It puts the framework on the
academic record, widens the statutory convergence it rests on, makes the live
audit evidence public and honest, and strengthens the accessibility footing of
the templates people actually send — all around the same narrow test: was a
named human able to personally review the specific facts before a decision
affected an identified person?

For adopters and a sceptical professional audience (academics, trade-union
officials, NGO directors), this release is about being checkable: cite-able
references, a transparent findings ledger framed as a path to sovereignty rather
than a scoreboard, and accessibility commitments stated plainly in the templates.

## Draft GitHub Release Description

### Release Signing Warning

Before publishing the GitHub Release, the maintainer must regenerate
`signed-update-manifest.json` with the offline Ed25519 PWA update-signing private
key. Keep that private key offline and never commit it to the repository. Follow
`SOVEREIGN_MODE.md` under "Signed update envelope" for the signing process.

### What's New

- Academic publication: SSRN abstract 6759778 and ORCID iD 0009-0001-8691-3366,
  with a "Cite as" block added to the whitepaper header.
- Case study "The Burgess Test — The Liability Transfer Chain" published on
  Zenodo — DOI 10.5281/zenodo.20449193.
- Legal convergence: Medical Devices Regulations 2002 added as the fifth
  statutory framework (MHRA FOI2026/00527).
- Live NULL findings ledger published at `audits/LIVE_AUDIT_LOG.md`
  (15-institution audit: 11 NULL, 0 SOVEREIGN, 4 AMBIGUOUS).
- Accessibility: Equality Act 2010 (ss.20/29) reasonable-adjustment line added to
  29 letter templates — footer coverage rises from 12 to 41 templates.
- New template `THIRD_PARTY_REFERRAL_REVIEW_WITH_BURGESS_PRINCIPLE.md` for
  decisions based on a third-party assessor (medical / occupational health / work
  capability / expert report), applying the binary test to both the assessment
  and the institution's reliance on it.
- Reframed institution statistics toward a path-to-sovereignty framing (help,
  not shame); removed brittle hardcounts in favour of the live register.
- Bumped package, API, PWA, Vercel-facing, and local install metadata to v2.5.1.

### Why It Matters

- The framework is now cite-able and on the academic record, which matters for
  the regulators, researchers, and advocates it is meant to serve.
- A wider statutory base (now five converging frameworks) strengthens its claim
  to operationalise existing law rather than invent a new standard.
- The public, honestly-framed findings ledger lets a sceptical reader verify the
  evidence instead of taking a number on trust.
- More templates now state reasonable-adjustment and email-only preferences,
  which is central to the framework's disability-rights purpose.

### Upgrade Path

- Pull the v2.5.1 release.
- Reinstall local Python tooling where needed with `pip install -e ".[local]"` or
  the platform install script in `scripts/`.
- For Sovereign Vault users, run `npm ci` in `enforcement/sovereign-vault/` and
  rebuild with `npm run build`.
- Refresh any cached PWA assets so the service worker moves to the v2.5.1 cache.
- Complete the release-signing step in the warning above before publishing the
  GitHub Release and enabling signed PWA update activation for the tagged
  release.

### Adoption Next Steps

- If you are affected by a decision now, start with `START_HERE.md` and the
  templates.
- If a decision relies on a third-party assessor (medical, occupational health,
  work capability, or an expert report), use
  `templates/THIRD_PARTY_REFERRAL_REVIEW_WITH_BURGESS_PRINCIPLE.md`.
- If you are building a system that acts on identified people, add the Burgess
  gate before decision logic and block NULL or AMBIGUOUS results for individual
  human review.
- To cite the framework, use the SSRN abstract (6759778) and the Liability
  Transfer Chain DOI (10.5281/zenodo.20449193).
