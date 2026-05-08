# PR 2 Draft: Adoption Infrastructure Documentation

## Proposed Branch

phase3/adoption-infrastructure-docs

## Scope

Focused, single-concern PR containing adoption infrastructure docs only.

## Files to Include

- adoption/README.md
- adoption/INSTITUTIONAL_ADOPTION_TRACKER.md
- adoption/BURGESS_READY_CHECKLIST.md
- adoption/PUBLIC_LEADERBOARD.md
- adoption/BURGESS_AMBASSADORS_PROGRAMME.md

## Commit Message

docs(adoption): add institutional tracker, readiness checklist, leaderboard, and ambassadors programme

## Pull Request Title

Add adoption infrastructure docs (tracker, checklist, leaderboard, ambassadors)

## Minimal Command Sequence

Run these commands from repository root:

```bash
git checkout -b phase3/adoption-infrastructure-docs

git add \
  adoption/README.md \
  adoption/INSTITUTIONAL_ADOPTION_TRACKER.md \
  adoption/BURGESS_READY_CHECKLIST.md \
  adoption/PUBLIC_LEADERBOARD.md \
  adoption/BURGESS_AMBASSADORS_PROGRAMME.md

git commit -m "docs(adoption): add institutional tracker, readiness checklist, leaderboard, and ambassadors programme"

git push -u origin phase3/adoption-infrastructure-docs
```

Then open draft PR:

```bash
gh pr create \
  --base main \
  --head phase3/adoption-infrastructure-docs \
  --title "Add adoption infrastructure docs (tracker, checklist, leaderboard, ambassadors)" \
  --body-file .github/pr-drafts/adoption-pr2-body.md \
  --draft
```
