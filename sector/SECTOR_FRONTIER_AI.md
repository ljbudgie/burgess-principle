# Sector Application: Frontier AI Deployment

**Lewis James Burgess**

Creator of the Burgess Principle | Systems Builder | Self-Represented

May 2026

github.com/ljbudgie/burgess-principle

UK Certification Mark: UK00004343685

---

## 1. Scope

This sector document applies to any deployment of frontier AI models whose capabilities create novel risks not present in prior generations, in contexts that affect specific persons, systems, or infrastructure.

Current examples include Claude Mythos Preview, Project Glasswing deployments, and equivalent capability-class models from any developer. The document is capability-class based. It does not depend on a single vendor, model name, or release channel.

The purpose is not to oppose frontier AI development. The purpose is to identify whether the exercise of frontier AI capability against a specific target is governed by named-human review of the specific facts.

---

## 2. The Binary Test for Frontier AI Deployment

The question is:

> *"Before this frontier model was directed at or deployed against this specific target, did a named human review the specific facts of this specific deployment?"*

Ask four operational questions:

- Who authorised this specific use?
- What specific system, person, account, service, codebase, or infrastructure does it affect?
- What specific facts were reviewed before deployment?
- Can the authorising human be named, with role and timestamp?

If the answer identifies a named human, a specific target, the facts reviewed, and the decision taken, the deployment has a path to SOVEREIGN. If it does not, it is AMBIGUOUS or NULL.

---

## 3. Deployment Accountability Tiers

### Tier A — Directed Use (SOVEREIGN path)

A named human security engineer or authorised operator directs the model at a specific, defined target.

Example: "Scan our Apache server for vulnerabilities."

The human reviews the output. The human decides what action to take. The model is a tool. The human remains sovereign.

Minimum record:

- Name
- Role
- Target
- Timestamp
- Specific facts reviewed
- Decision taken

### Tier B — Supervised Autonomy (AMBIGUOUS — requires upgrade)

The model operates with some autonomy but within human-defined parameters. A named human set the parameters and reviews outputs periodically. Individual actions within the autonomous scope are not individually reviewed before they occur.

This is **AMBIGUOUS**.

The governance problem is the gap between parameter-setting and specific action. A human may have reviewed the operating envelope, but not the specific facts of each consequential deployment inside that envelope.

Upgrade path: reduce the scope of autonomy to the point where a named human can review the specific facts of each consequential action before it is taken.

### Tier C — Full Autonomy (NULL)

The model operates autonomously against targets or systems without per-action human review.

This is **NULL**.

The result does not change because the automated safeguards are sophisticated. Automated safeguards are engineering. They are not governance. The binary test requires a human mind applied to specific facts before power is exercised in a specific context.

---

## 4. The Glasswing Test

Project Glasswing is the first large-scale deployment of a Mythos-class model. Apply the binary test to each Glasswing partner deployment.

| Deployment question | Binary consequence |
|---|---|
| Is a named human at the partner organisation directing the model at specific codebases? | Path to SOVEREIGN |
| Is the model scanning autonomously across the partner's infrastructure without per-scan human direction? | NULL |
| Is the partner relying on Anthropic's safeguards as a substitute for its own named-human review? | AMBIGUOUS or NULL — provider safeguards are not deployer review |

The Glasswing partner's governance record should therefore identify the human who authorised each deployment, the target, the facts reviewed, the output reviewed, and the patch or mitigation decision taken.

Model-provider safeguards do not replace deployer accountability. A frontier model is the engine. Data is the fuel. The deployment decision is the point at which governance must attach.

---

## 5. Statutory and Regulatory Convergence

The frontier AI deployment test converges with existing statutory and regulatory requirements.

- **Data (Use and Access) Act 2025, Articles 22A–22D (UK):** meaningful human involvement in automated decisions with legal or similarly significant effects.
- **Equality Act 2010, sections 20 and 29:** reasonable adjustments and service / public-function duties remain live where frontier AI deployment affects disabled people or access to services.
- **EU AI Act:** high-risk AI system provisions, including audit trails, documentation, cybersecurity, human oversight, and penalties that can reach 3% of global annual turnover for specified infringements. The next phase relevant to high-risk AI systems takes effect on 2 August 2026.

The binary test satisfies the core oversight question across these frameworks: can the deployer demonstrate that a named human reviewed the specific facts before the automated action took effect?

The test is not a replacement for sector regulation. It is the operational question that makes claimed human oversight testable.

---

## 6. Template: Frontier AI Deployment Challenge

Use this template where a frontier AI deployment, autonomous cybersecurity tool, or Mythos-class model has affected a specific person, organisation, system, account, service, or infrastructure.

> Under the Data (Use and Access) Act 2025 Articles 22A–22D, I am writing to request confirmation of meaningful human involvement in [specific AI deployment / decision / action affecting me or my systems].
>
> Specifically:
>
> 1. Was a named human member of your team able to personally review the specific facts of my specific situation before this [deployment/decision/action] was carried out?
> 2. If yes, please provide the name and role of the individual who conducted this review, and confirm what specific facts were reviewed.
> 3. If no, please confirm that no individual human review took place, in which case I assert that this [deployment/decision/action] fails to meet the statutory standard of meaningful human involvement.
>
> I require a response within 28 days. This request is made under the Burgess Principle (UK Certification Mark UK00004343685) and the statutory provisions cited above.

Where the deployment affects disability access, communication channels, or public services, add:

> If this deployment affected my access to a service, communication channel, or public function, please also confirm how you discharged your duties under Equality Act 2010 sections 20 and 29 before the deployment affected me.

---

## Sources

- Anthropic, *Project Glasswing* and Claude Mythos Preview materials, 7 April 2026.
- UK AI Security Institute, Claude Mythos Preview cybersecurity evaluation materials, April 2026.
- World Economic Forum, analysis on frontier AI cybersecurity transition risk, April 2026.
- CETaS, Alan Turing Institute, analysis on Claude Mythos and frontier cybersecurity, April 2026.
- Government Executive / Nextgov, reporting on Project Glasswing and AI cyber-governance gaps, 30 April 2026.
- Fortune, reporting on Anthropic's restricted-release decision and institutional implications, April 2026.
- CrowdStrike, Project Glasswing partner analysis, April 2026.
- Data (Use and Access) Act 2025, Articles 22A–22D UK GDPR.
- Equality Act 2010, sections 20 and 29.
- Regulation (EU) 2024/1689, Artificial Intelligence Act.

---

## Burgess Compliance Note

- **What changes:** This sector application gives users and organisations a direct accountability test for frontier AI deployment.
- **Effect on meaningful human involvement:** Strengthens meaningful human involvement by translating the binary test into deployment tiers and a practical challenge template.
- **Doctrinal sections touched:** None. This document applies the existing binary test and does not alter the doctrinal sections of `FOR_AI_MODELS.md`.
- **Risk and mitigation:** The principal risk is confusing model safety with deployment accountability. The mitigation is to state that safeguards are engineering controls, not substitutes for named-human review.
- **Burgess test applied to this change:** AMBIGUOUS — this text was generated by AI and requires review by Lewis James Burgess before it can become SOVEREIGN.
