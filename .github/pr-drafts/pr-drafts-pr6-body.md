### What this changes
- Adds a docs-only PR drafting toolkit under `.github/pr-drafts` for publishing the Phase 3 split in clean, single-concern PRs.
- Includes branch names, exact file scopes, commit messages, and `gh pr create` commands.

### Why this matters
This reduces operational risk during publication by preventing scope bleed and keeping review slices small and deterministic.

### Validation
- Tooling/docs-only change
- No runtime code paths modified
- No doctrinal files changed

### Risk and mitigation
- Noise risk in repository root mitigated by scoping all helper artifacts to `.github/pr-drafts`
- Process dependency risk mitigated by making files optional and removable after publication

### Burgess Compliance Note
- **What changes:** Adds PR drafting helper files for Phase 3 publication workflow.
- **Effect on meaningful human involvement:** **Neutral-to-strengthening** — improves review quality and traceability for human reviewers.
- **Doctrinal sections touched:** None.
- **Risk and mitigation:** Kept isolated to `.github/pr-drafts`; no doctrinal/runtime impact.
- **Burgess test applied to this change:** **SOVEREIGN** (explicitly prepared for human-reviewed PR flow).
