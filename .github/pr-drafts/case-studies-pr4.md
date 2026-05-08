# PR 4 Draft: New Case Studies

## Proposed Branch

phase3/case-studies-healthcare-finance

## Scope

Focused, single-concern PR containing two new case studies.

## Files to Include

- case-studies/CASE_STUDY_HEALTHCARE_TRIAGE.md
- case-studies/CASE_STUDY_FINANCIAL_LENDING.md

## Commit Message

docs(case-studies): add healthcare triage and financial lending studies

## Pull Request Title

Add healthcare triage and financial lending case studies

## Minimal Command Sequence

Run these commands from repository root:

```bash
git checkout -b phase3/case-studies-healthcare-finance

git add \
  case-studies/CASE_STUDY_HEALTHCARE_TRIAGE.md \
  case-studies/CASE_STUDY_FINANCIAL_LENDING.md

git commit -m "docs(case-studies): add healthcare triage and financial lending studies"

git push -u origin phase3/case-studies-healthcare-finance
```

Then open draft PR:

```bash
gh pr create \
  --base main \
  --head phase3/case-studies-healthcare-finance \
  --title "Add healthcare triage and financial lending case studies" \
  --body-file .github/pr-drafts/case-studies-pr4-body.md \
  --draft
```
