# Publish Sequence for Phase 3 PR Splits

Use this order to keep reviews small and reduce merge conflicts.

## Recommended Order

1. PR 1: LangChain integration foundation
2. PR 2: Adoption infrastructure docs
3. PR 3: Papers (whitepaper + NIST mapping)
4. PR 4: Case studies (healthcare + lending)
5. PR 5: Remaining integration templates
6. PR 6 (optional): PR drafting toolkit under `.github/pr-drafts`

## Why this order

- PR 1 establishes integration baseline language.
- PR 2 adds implementation/adoption layer for organisations.
- PR 3 and PR 4 add evidence + theory after practical docs exist.
- PR 5 completes broader ecosystem template pack.

## Commands (safe routine for each PR)

```bash
# 0) Ensure clean working view
git status

# 1) Create PR branch
#    (Use branch from each draft file)

# 2) Add only listed files
#    (Use git add paths exactly as in draft)

# 3) Commit
#    (Use draft commit message)

# 4) Push
git push -u origin <branch>

# 5) Open draft PR
gh pr create --base main --head <branch> --title "..." --body-file .github/pr-drafts/<body-file>.md --draft
```

## Branch + Body Files

- PR 1: phase3/langchain-governance-overlay, body embedded in .github/pr-drafts/langchain-pr1.md
- PR 2: phase3/adoption-infrastructure-docs, body .github/pr-drafts/adoption-pr2-body.md
- PR 3: phase3/research-papers-docs, body .github/pr-drafts/papers-pr3-body.md
- PR 4: phase3/case-studies-healthcare-finance, body .github/pr-drafts/case-studies-pr4-body.md
- PR 5: phase3/integrations-template-pack, body .github/pr-drafts/integrations-pr5-body.md
- PR 6 (optional): phase3/pr-drafts-tooling-cleanup, body .github/pr-drafts/pr-drafts-pr6-body.md

## Notes

- Keep each PR docs-only and single concern.
- If a file appears in a prior merged PR, skip it in later PRs.
- If you hit branch contamination, start a fresh branch from main and re-add only target files.

## Tracking

- Use `.github/pr-drafts/PHASE3_PR_CHECKLIST.md` to track each PR from branch creation to merge.
