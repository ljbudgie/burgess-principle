# Run All Phase 3 PR Commands

Copy and run each block in order. Each block is scoped to one PR.

## PR 1 — LangChain integration foundation

```bash
git checkout -b phase3/langchain-governance-overlay

git add integrations/LANGCHAIN_BURGESS_OVERLAY.md integrations/README.md

git commit -m "docs(integrations): add LangChain Burgess governance overlay and index"

git push -u origin phase3/langchain-governance-overlay

gh pr create \
  --base main \
  --head phase3/langchain-governance-overlay \
  --title "Add LangChain Burgess governance overlay documentation" \
  --body-file .github/pr-drafts/langchain-pr1.md \
  --draft
```

## PR 2 — Adoption infrastructure docs

```bash
git checkout main

git checkout -b phase3/adoption-infrastructure-docs

git add \
  adoption/README.md \
  adoption/INSTITUTIONAL_ADOPTION_TRACKER.md \
  adoption/BURGESS_READY_CHECKLIST.md \
  adoption/PUBLIC_LEADERBOARD.md \
  adoption/BURGESS_AMBASSADORS_PROGRAMME.md

git commit -m "docs(adoption): add institutional tracker, readiness checklist, leaderboard, and ambassadors programme"

git push -u origin phase3/adoption-infrastructure-docs

gh pr create \
  --base main \
  --head phase3/adoption-infrastructure-docs \
  --title "Add adoption infrastructure docs (tracker, checklist, leaderboard, ambassadors)" \
  --body-file .github/pr-drafts/adoption-pr2-body.md \
  --draft
```

## PR 3 — Research papers

```bash
git checkout main

git checkout -b phase3/research-papers-docs

git add \
  papers/WHITEPAPER_BURGESS_TEST_2026.md \
  papers/NIST_AI_RMF_MAPPING.md

git commit -m "docs(papers): add whitepaper and NIST AI RMF mapping"

git push -u origin phase3/research-papers-docs

gh pr create \
  --base main \
  --head phase3/research-papers-docs \
  --title "Add whitepaper and NIST AI RMF mapping documents" \
  --body-file .github/pr-drafts/papers-pr3-body.md \
  --draft
```

## PR 4 — Case studies (healthcare + lending)

```bash
git checkout main

git checkout -b phase3/case-studies-healthcare-finance

git add \
  case-studies/CASE_STUDY_HEALTHCARE_TRIAGE.md \
  case-studies/CASE_STUDY_FINANCIAL_LENDING.md

git commit -m "docs(case-studies): add healthcare triage and financial lending studies"

git push -u origin phase3/case-studies-healthcare-finance

gh pr create \
  --base main \
  --head phase3/case-studies-healthcare-finance \
  --title "Add healthcare triage and financial lending case studies" \
  --body-file .github/pr-drafts/case-studies-pr4-body.md \
  --draft
```

## PR 5 — Remaining integration templates

```bash
git checkout main

git checkout -b phase3/integrations-template-pack

git add \
  integrations/PR_TEMPLATE_LLAMAINDEX.md \
  integrations/PR_TEMPLATE_AUTOGEN.md \
  integrations/PR_TEMPLATE_CREWAI.md \
  integrations/CASE_STUDY_OPENCLAW_INTEGRATION.md

git commit -m "docs(integrations): add LlamaIndex, AutoGen, CrewAI templates and OpenClaw case study"

git push -u origin phase3/integrations-template-pack

gh pr create \
  --base main \
  --head phase3/integrations-template-pack \
  --title "Add integration templates for LlamaIndex, AutoGen, CrewAI and OpenClaw case study" \
  --body-file .github/pr-drafts/integrations-pr5-body.md \
  --draft
```

## PR 6 — Optional PR tooling pack

```bash
git checkout main

git checkout -b phase3/pr-drafts-tooling-cleanup

git add .github/pr-drafts/

git commit -m "chore(pr): add phase3 pr-draft tooling pack"

git push -u origin phase3/pr-drafts-tooling-cleanup

gh pr create \
  --base main \
  --head phase3/pr-drafts-tooling-cleanup \
  --title "Add Phase 3 PR drafting toolkit under .github/pr-drafts" \
  --body-file .github/pr-drafts/pr-drafts-pr6-body.md \
  --draft
```

## Fast verification after each PR

```bash
git status
```

## Tracking

Use .github/pr-drafts/PHASE3_PR_CHECKLIST.md as the authoritative checklist while executing.
