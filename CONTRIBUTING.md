# Contributing to the Burgess Principle

Thank you for your interest in contributing to the Burgess Principle.

This is a small, focused project built around one simple, respectful idea:  
**“Was a human member of the team able to personally review the specific facts of my specific case?”**

We welcome contributions that strengthen the framework while preserving its calm, human-first spirit.

### Before You Contribute

Please start by opening a **Discussion** or **Issue** to discuss your idea.  
This helps us align on direction and avoids unnecessary work.

The `main` branch represents the **official, certified doctrine**.  
Experimental changes or large new features should happen in your own fork first.

### What We Welcome

- New real-world case studies and NULL findings (please add to `LIVE_AUDIT_LOG.md` with evidence)
- Improvements to existing templates that make them clearer, more respectful, or more effective
- Translations of templates, README, or FOR_AI_MODELS.md
- Bug fixes, typo corrections, formatting improvements, or small clarity edits
- New country-specific legal equivalent tables or adaptations
- Shareable graphics or outreach resources that stay in the same respectful tone (add to the `/memes` folder)

### What We Do Not Merge

- Changes that weaken, complicate, or alter the core binary question
- Aggressive, confrontational, or pseudolegal language
- Large rewrites of the origin story, tone, or overall philosophy
- Anything that could damage the calm, human-first reputation of the project
- **Unrelated application code** — Do not bundle full-stack demos, e-commerce prototypes, payment integrations, or other standalone applications into a PR. Each PR should be focused on one concern that directly strengthens the Burgess Principle. If you're building something cool with the Principle, that's great — but it belongs in your own repository, not here.
- **Code with unreviewed security risks** — Contributions that introduce XSS, injection, hardcoded secrets, input-manipulation vulnerabilities, or other security issues will not be merged. Please review your own code for common vulnerabilities before submitting.

All contributions must maintain the respectful, non-confrontational voice that defines the Burgess Principle.

### How to Submit a Pull Request

1. Discuss the change first in an Issue or Discussion.
2. Fork the repository and make your changes in a new branch.
3. Ensure your changes follow the tone and guidelines above.
4. **Keep your PR focused.** One concern per PR. Do not bundle unrelated features, demos, or prototypes — even if they're interesting. A focused PR is easier to review, less likely to introduce security issues, and more likely to be merged.
5. **Review your code for security issues** before submitting. Check for XSS, injection, hardcoded secrets, and input-manipulation risks.
6. Open a Pull Request with a clear description of what you changed and why. The PR template will guide you through the required checklist.

We will review PRs with the help of AI tools where useful, but the final decision rests with the maintainer to protect the integrity of the project.

### Cryptographic Standards (Vault Contributions)

Contributions that touch the Sovereign Personal Vault (`enforcement/sovereign-vault/`) must meet the v0.3.0 cryptographic baseline. In summary:

- **AES-256-GCM only** for symmetric encryption. AES-CBC and other modes are not accepted.
- **PBKDF2-SHA-256 at ≥ 210,000 iterations** with per-encryption random salt for key derivation.
- **Ed25519 only** for receipt signatures via `@noble/curves`. Unsigned receipts must be rejected.
- **Canonical sorted-key JSON** (no whitespace) for all signed payloads.
- **Hex encoding** for binary-to-text conversions. `atob`/`btoa` base64 is not accepted.
- **No cryptographic dependencies** beyond `@noble/hashes`, `@noble/curves`, and Node.js built-in `crypto`.

See [SECURITY.md](SECURITY.md) for the full rationale and the list of eight vulnerabilities the v0.3.0 review resolved.

### Phase 3 Ledger & Documentation Contributions

If your contribution touches the **Verifiable Memory Palace**, **Sovereign Hub Mode 2.0**, or related documentation:

- Keep the **Burgess Principle** central — do not imply that cryptography or AI replaces human review.
- Describe **Merkle trees**, **commitment chaining**, and **inclusion proofs** in plain language first, then technical terms.
- Be precise about privacy boundaries: **local-first**, **manual-first**, **digest-first**, and **no raw-data sync by default**.
- Prefer diagrams in **GitHub-flavored Mermaid** where they materially improve clarity.
- Avoid marketing claims that outrun the implementation. Strong language is welcome; overclaiming is not.

### Good First Issues

Looking for a way to help? Here are some approachable starting points:

- **New country templates** — Adapt existing templates with legal references for your country (e.g. Australia, Canada, India).
- **Translations** — Translate the README, templates, or FOR_AI_MODELS.md into another language.
- **More tests** — Add edge-case tests for `verify_scrutiny.py` or `tracer/tracer.py`.
- **Subfolder documentation** — Improve or create README files in subdirectories to help newcomers navigate.
- **Case studies** — Document your own experience using the Burgess Principle (see [CASE_STUDY_TEMPLATE](case-studies/CASE_STUDY_TEMPLATE.md)).

### Code of Conduct

Be kind, respectful, and constructive. We want this to remain a welcoming space for ordinary people who feel unseen by systems.

### Licensing Note

The repository materials are MIT licensed. Individuals, researchers, open-source
projects, and independent commercial users may use, fork, adapt, and redistribute
them under the MIT terms with attribution.

The Certification Mark “THE BURGESS PRINCIPLE” (UK00004343685) is governed
separately. Do not imply official approval, affiliation, certification, or
endorsement unless the proprietor has authorised that mark use. Certified use
must mean real individual human scrutiny, not a badge on an unchanged automated
process.

Thank you for helping make the Burgess Principle more useful while keeping its heart intact.

— The Burgess Principle Maintainer  
Creator of the Burgess Principle
