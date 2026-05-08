# PR 5 Draft: Additional Integration Templates

## Proposed Branch

phase3/integrations-template-pack

## Scope

Focused, single-concern PR containing remaining integration templates and reference case study.

## Files to Include

- integrations/PR_TEMPLATE_LLAMAINDEX.md
- integrations/PR_TEMPLATE_AUTOGEN.md
- integrations/PR_TEMPLATE_CREWAI.md
- integrations/CASE_STUDY_OPENCLAW_INTEGRATION.md

## Commit Message

docs(integrations): add LlamaIndex, AutoGen, CrewAI templates and OpenClaw case study

## Pull Request Title

Add integration templates for LlamaIndex, AutoGen, CrewAI and OpenClaw case study

## Minimal Command Sequence

Run these commands from repository root:

```bash
git checkout -b phase3/integrations-template-pack

git add \
  integrations/PR_TEMPLATE_LLAMAINDEX.md \
  integrations/PR_TEMPLATE_AUTOGEN.md \
  integrations/PR_TEMPLATE_CREWAI.md \
  integrations/CASE_STUDY_OPENCLAW_INTEGRATION.md

git commit -m "docs(integrations): add LlamaIndex, AutoGen, CrewAI templates and OpenClaw case study"

git push -u origin phase3/integrations-template-pack
```

Then open draft PR:

```bash
gh pr create \
  --base main \
  --head phase3/integrations-template-pack \
  --title "Add integration templates for LlamaIndex, AutoGen, CrewAI and OpenClaw case study" \
  --body-file .github/pr-drafts/integrations-pr5-body.md \
  --draft
```
