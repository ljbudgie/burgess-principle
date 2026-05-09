# Release Notes — v2.5.0

## Governance & Ecosystem: Certified Pathways and Community Foundations

Released: 9 May 2026

v2.5.0 matters because the Burgess Principle now has clearer public governance,
community expectations, certification pathways, and ecosystem routing around the
same narrow test: was a named human able to personally review the specific facts
before a decision affected an identified person?

For adopters, this release makes the boundary easier to trust: repository
materials remain MIT-open, while official "Certified Burgess Principle" use and
the UK Certification Mark **UK00004343685** remain separately governed.

For contributors, it creates a calmer path into the project: governance rules,
conduct standards, good-first-issue style routes, integration overlays, and
certification documents are now easier to find and review.

## Draft GitHub Release Description

### Release Signing Warning

Before publishing the GitHub Release, the maintainer must regenerate
`signed-update-manifest.json` with the offline Ed25519 PWA update-signing private
key. Keep that private key offline and never commit it to the repository. Follow
`SOVEREIGN_MODE.md` under "Signed update envelope" for the signing process.

### What's New

- Added `GOVERNANCE.md` for roles, lazy consensus, sensitive-change escalation,
  neutral advisory review, certification-mark boundaries, and succession.
- Added `CODE_OF_CONDUCT.md` with accessibility-aware community standards.
- Added contributor and onboarding routes, including Iris enhancement issues
  suitable for good first contributions.
- Added LangChain governance overlay documentation and integration templates for
  agent/RAG ecosystems.
- Updated `ECOSYSTEM.md` with Iris, Mirror, OpenHear, Nexus AI Hub, OpenClaw, and
  Hermes Agent relationships.
- Clarified founding certification rates, certification tiers, partnership ledger
  routes, and post-payment certification-site flow.
- Clarified the hybrid MIT + Certification Mark model across README, licence,
  contributing, docs, and certification materials.
- Bumped package, API, PWA, Vercel-facing, and local install metadata to v2.5.0.

### Why It Matters

- Adopters can use the MIT-open core without implying certification.
- Organisations seeking certified use now have clearer public pathways and
  stronger neutrality safeguards.
- Contributors have clearer expectations for conduct, governance, issue routing,
  and doctrinal escalation.
- Agent-framework maintainers have concrete overlay material for adding the
  SOVEREIGN / NULL / AMBIGUOUS check without replacing their existing systems.

### Upgrade Path

- Pull the v2.5.0 release.
- Reinstall local Python tooling where needed with `pip install -e ".[local]"` or
  the platform install script in `scripts/`.
- For Sovereign Vault users, run `npm ci` in `enforcement/sovereign-vault/` and
  rebuild with `npm run build`.
- Refresh any cached PWA assets so the service worker moves to the v2.5.0 cache.
- Complete the release-signing step in the warning above before publishing the
  GitHub Release and enabling signed PWA update activation for the tagged
  release.
- Review `GOVERNANCE.md`, `CODE_OF_CONDUCT.md`, `LICENSE.md`, and
  `CERTIFICATION_TIERS.md` before making public certification claims.

### Adoption Next Steps

- If you are affected by a decision now, start with `START_HERE.md` and the
  templates.
- If you are building a system that acts on identified people, add the Burgess
  gate before decision logic and block NULL or AMBIGUOUS results for individual
  human review.
- If you maintain an AI framework, adapt the LangChain overlay pattern or the
  integration templates to your stack.
- If your organisation can evidence named human review, review
  `CERTIFICATION_TIERS.md` and the certification site before applying for
  official mark use.
