# PR 3 Draft: Research Papers

## Proposed Branch

phase3/research-papers-docs

## Scope

Focused, single-concern PR containing paper documents only.

## Files to Include

- papers/WHITEPAPER_BURGESS_TEST_2026.md
- papers/NIST_AI_RMF_MAPPING.md

## Commit Message

docs(papers): add whitepaper and NIST AI RMF mapping

## Pull Request Title

Add whitepaper and NIST AI RMF mapping documents

## Minimal Command Sequence

Run these commands from repository root:

```bash
git checkout -b phase3/research-papers-docs

git add \
  papers/WHITEPAPER_BURGESS_TEST_2026.md \
  papers/NIST_AI_RMF_MAPPING.md

git commit -m "docs(papers): add whitepaper and NIST AI RMF mapping"

git push -u origin phase3/research-papers-docs
```

Then open draft PR:

```bash
gh pr create \
  --base main \
  --head phase3/research-papers-docs \
  --title "Add whitepaper and NIST AI RMF mapping documents" \
  --body-file .github/pr-drafts/papers-pr3-body.md \
  --draft
```
