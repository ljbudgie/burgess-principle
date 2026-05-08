# PR 6 Draft: PR Tooling Cleanup

## Proposed Branch

phase3/pr-drafts-tooling-cleanup

## Scope

Focused, single-concern PR for PR drafting/tooling artifacts under `.github/pr-drafts`.

## Files to Include

- .github/pr-drafts/langchain-pr1.md
- .github/pr-drafts/adoption-pr2.md
- .github/pr-drafts/adoption-pr2-body.md
- .github/pr-drafts/papers-pr3.md
- .github/pr-drafts/papers-pr3-body.md
- .github/pr-drafts/case-studies-pr4.md
- .github/pr-drafts/case-studies-pr4-body.md
- .github/pr-drafts/integrations-pr5.md
- .github/pr-drafts/integrations-pr5-body.md
- .github/pr-drafts/PUBLISH_SEQUENCE.md

## Commit Message

chore(pr): add phase3 pr-draft tooling pack

## Pull Request Title

Add Phase 3 PR drafting toolkit under .github/pr-drafts

## Minimal Command Sequence

Run these commands from repository root:

```bash
git checkout -b phase3/pr-drafts-tooling-cleanup

git add .github/pr-drafts/

git commit -m "chore(pr): add phase3 pr-draft tooling pack"

git push -u origin phase3/pr-drafts-tooling-cleanup
```

Then open draft PR:

```bash
gh pr create \
  --base main \
  --head phase3/pr-drafts-tooling-cleanup \
  --title "Add Phase 3 PR drafting toolkit under .github/pr-drafts" \
  --body-file .github/pr-drafts/pr-drafts-pr6-body.md \
  --draft
```

## Optional alternative

If you prefer not to keep these files in `main`, skip this PR and keep `.github/pr-drafts` as local-only helper artifacts.
