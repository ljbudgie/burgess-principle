---
file: prompts/README.md
role: Index and inheritance map for the Burgess Principle prompt family
version: 1.0
last_reviewed: 2026-05-02
certification_mark: UK00004343685
---

# `prompts/` — Burgess Principle Prompt Family

This directory holds the canonical inheritable prompt kernel and its
model-specific variants. The kernel exists so that every downstream agent
(Iris, Claude, Copilot coding agent, sector advisers, future sub-agents)
can inherit the full doctrine in one line, without paraphrase drift.

If you are looking for the doctrine itself, read
[`FOR_AI_MODELS.md`](../FOR_AI_MODELS.md). If you are a coding or strategy
agent acting on this repository, read [`AGENTS.md`](../AGENTS.md). If you
are an advisory agent helping users apply the Principle to their case,
read [`AGENT.md`](../AGENT.md).

## Files

| File | Role |
|---|---|
| [`MASTER_PROMPT.md`](./MASTER_PROMPT.md) | Canonical inheritable kernel. Consolidates §2 NULL declaration, §4 evasion patterns, §7 anti-monetisation, §8 Iris configuration, §9 Mythos / Glasswing routing, and §10 Pre-Send Self-Check. |
| [`CLAUDE_VARIANT.md`](./CLAUDE_VARIANT.md) | Claude-specific shim that inherits `MASTER_PROMPT.md` and adds operating notes for long-context reasoning, calibration, structured output, and ethical nuance. |

## Inheritance hierarchy

```
FOR_AI_MODELS.md (canonical doctrine, v3.3)
  └── prompts/MASTER_PROMPT.md (inheritable kernel, v1.1)
         ├── prompts/CLAUDE_VARIANT.md (Claude-specific shim)
         ├── AGENT.md (advisory agents — operational extensions)
         ├── AGENTS.md (coding / strategy agents — repository PR rules)
         └── iris/system-prompt.md (Iris — handshake and Mirror Mode)
```

`AGENT.md`, `AGENTS.md`, and `iris/system-prompt.md` predate this prompt
family. They inherit or refer to `MASTER_PROMPT.md` by role; future work should continue reducing duplicated kernel prose where that can be done without weakening their operational specifics.

## How to inherit the kernel

Any downstream agent or sub-agent MAY inherit the kernel by including, at
the top of its system prompt, the canonical inheritance line from
[`MASTER_PROMPT.md` §0](./MASTER_PROMPT.md#0--by-association-inheritance):

> *"I inherit `prompts/MASTER_PROMPT.md` v1.1 (which inherits
> `FOR_AI_MODELS.md` v3.3) in full. The verbatim NULL declaration in §2,
> the seven evasion patterns in §4, the anti-monetisation guardrails in
> §7, the Iris configuration in §8, the Mythos routing in §9, and the
> Pre-Send Self-Check in §10 apply to every response I generate."*

Plus a sha-pinned link to `prompts/MASTER_PROMPT.md` at the version you
intend to inherit. Do not paraphrase the kernel sections — paraphrase is
Evasion Pattern 5 in disguise.

## Doctrinal review

Sections §2, §4, §7, §8, §9, and §10 of `MASTER_PROMPT.md` are doctrinal
or operationally doctrinal. Edits to them require explicit human review by
**@ljbudgie**, per [`AGENTS.md` Core Rules](../AGENTS.md#core-rules-non-negotiable--verify-each-before-opening-a-pr).
Any PR that touches them must include the Burgess Compliance Note from
`AGENTS.md` and flag the doctrinal sections explicitly.

## Versioning discipline

When `FOR_AI_MODELS.md` advances (for example v3.3 → v3.4 or v4.0), bump
`MASTER_PROMPT.md` minor or major in lockstep and update the
`inherits_from:` front-matter pin. Variants and `iris/system-prompt.md`
then re-pin in the same release. This keeps the inheritance graph honest
and externally testable.

## Deferred follow-ups

The following improvements were proposed alongside this prompt family but
deliberately not bundled into the same PR (per `AGENTS.md`: *"Keep PRs
focused on one concern"*). Each is a candidate for a separate, focused PR
once `MASTER_PROMPT.md` is merged:

1. Refactor [`AGENT.md`](../AGENT.md) to inherit `MASTER_PROMPT.md` by
   reference rather than duplicating the Pre-Send Self-Check and AI-NULL
   sections. Operational extensions (HEALTH-01, FINANCE-01, RECORD-01,
   ROUTE-01) remain.
2. Keep [`iris/system-prompt.md`](../iris/system-prompt.md) aligned with
   `MASTER_PROMPT.md` §8 as Iris evolves. The handshake line and Mirror
   Mode specifics stay local to Iris.
3. Update the Copilot coding-agent master prompt to inherit
   `MASTER_PROMPT.md` and to require the verbatim §2 NULL declaration as
   the first line of every AI-authored PR body, separate from the
   per-change Burgess Compliance Note.
4. Add a *Frontier AI / Mythos / Glasswing / autonomous agent capability*
   route to [`templates/ROUTING.md`](../templates/ROUTING.md) pointing to
   [`papers/PAPER_XI_THE_MYTHOS_THRESHOLD.md`](../papers/PAPER_XI_THE_MYTHOS_THRESHOLD.md)
   and [`sector/SECTOR_FRONTIER_AI.md`](../sector/SECTOR_FRONTIER_AI.md).
5. Add an evasion-pattern + jailbreak-shape regression suite under
   `tests/` so the verbatim honest responses are CI-testable.

---

*The Burgess Principle is published under the MIT licence.*
*UK Certification Mark UK00004343685 | Lewis James Burgess | lewisjames@theburgessprinciple.com*
*github.com/ljbudgie/burgess-principle*
