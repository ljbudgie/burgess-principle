# GIT_AS_GOVERNANCE.md — Git as Sovereign Governance Substrate

**The Burgess Principle**
UK Certification Mark No. UK00004343685
May 2026

-----

## The Claim

This repository does not use Git for version control. It uses Git as a sovereign, auditable governance substrate.

Every native Git primitive — commit, hash, diff, tag, branch, blame, log, fork, revert — maps directly onto a governance function that the Burgess Principle requires. None of these mappings were engineered after the fact. They were recognised. Git already had the properties. The framework made them legible.

The result is that the entire institutional record of the Burgess Principle — its origin, its doctrinal development, its deployment across 26+ institutions, its evidence base, its corrections, and its founding family — is held in a governance structure that no institution controls, no institution can quietly revise, and anyone can independently verify.

-----

## The Primitive Map

Every Git primitive serves a governance function within this repository. The left column is what Git calls it. The right column is what it becomes.

|Git primitive                  |Governance function                                                                                                                                                                                                                                                                                                 |
|-------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|**Commit**                     |A named act of accountability. A human decided that the state of the record should change, and attached their identity and a timestamp to that decision.                                                                                                                                                            |
|**Commit hash (SHA-1/SHA-256)**|Cryptographic proof that the record existed in this exact state at this exact time. Content-addressable and tamper-evident. The institutional roll entry.                                                                                                                                                           |
|**Commit message**             |The named-human attestation of what was changed and why. The equivalent of the reasons given when a decision is made on the record.                                                                                                                                                                                 |
|**Signed commit (GPG/SSH)**    |Verified named-human identity. The commit is not merely attributed — it is cryptographically bound to a specific key held by a specific person.                                                                                                                                                                     |
|**Diff**                       |The audit trail. Not a summary. Not a description. The exact changes, line by line, character by character. What was there before. What is there now. What was added. What was removed. Immutable.                                                                                                                  |
|**Git log**                    |The institutional register. Chronologically ordered, cryptographically chained, publicly readable. Every decision, every change, every author, every timestamp.                                                                                                                                                     |
|**Tag**                        |A formal declaration. In this repository, a tagged release (v2.2.0, v2.3.3) is a named moment at which the framework was declared complete to that standard. The tag cannot be moved without creating a new, visible record.                                                                                        |
|**Branch**                     |A parallel governance track. Drafts, experiments, and proposed changes exist on branches. They do not enter the canonical record until a human merges them. The distinction between draft and canonical is structural.                                                                                              |
|**Pull request**               |A proposal requiring human review before it enters the canonical record. The SOVEREIGN test in action: a named human must review the specific facts of the specific change before it is accepted. The PR history — comments, approvals, rejections — is itself part of the permanent record.                        |
|**Merge**                      |The act of a named human accepting a change into the canonical record. The merge commit records who accepted it and when.                                                                                                                                                                                           |
|**Fork**                       |The sovereign right to diverge. Any person can take the full record and build independently, without requiring permission, while preserving the complete lineage of where their version came from. Sovereignty without severance.                                                                                   |
|**Revert**                     |A transparent correction. Unlike institutional quiet edits — where a policy is revised and the original disappears — a Git revert creates a new commit that undoes a previous one. Both the original decision and the correction are permanently visible. The institution cannot pretend the mistake did not happen.|
|**Blame**                      |Attribution. Who wrote each line, when, and in which commit. The question “who decided this?” has an answer for every line of every file.                                                                                                                                                                           |
|**Public repository**          |The open institutional register. Not held behind a login. Not subject to a records retention policy. Not controlled by the institution it documents. Verifiable by anyone with a browser.                                                                                                                           |
|**Distributed copies**         |Resilience against institutional destruction of records. Every clone is a full copy of the entire history. The record survives the loss of any single server, any single account, any single jurisdiction.                                                                                                          |

-----

## What This Means in Practice

### The founding record cannot be altered

FOUNDING.md was committed on 28 April 2026. The commit hash, the timestamp, the author, and the content are permanently part of the canonical history. The Burgess family — Lewis, Norman, Jake, George, and Helen — are in the record. That record cannot be edited, backdated, or removed without creating a visible, traceable break in the hash chain.

The sentence in FOUNDING.md — *“The timestamp of this commit is the date from which this founding record is true”* — is not a rhetorical claim. It is a statement about the cryptographic properties of the medium in which it was written.

### Every doctrinal change is auditable

When Paper XI was added, the diff shows exactly what was introduced. When the binary test was refined, the diff shows the previous wording and the new wording. When a template was corrected, the correction is visible alongside the original. No doctrinal change can be made invisibly. The governance substrate does not permit it.

### The institutional register is self-hosting

LIVE_AUDIT_LOG.md and INSTITUTIONAL_REGISTER.md are governance documents held inside a governance substrate. The register of institutions challenged under the Burgess Principle is itself subject to the same audit trail, the same immutable history, and the same public verifiability as every other file. The framework audits institutions. Git audits the framework.

### The certification mark has a provenance chain

The first reference to UK00004343685 in this repository is traceable to a specific commit. Every subsequent reference is traceable to its own commit. The chain of usage — from first filing reference through deployment in letters, templates, and papers — is independently verifiable from the Git history alone.

### Corrections strengthen rather than weaken the record

In institutional governance, corrections are often treated as embarrassments to be buried. In Git, a correction is a revert or an amendment — a new commit that openly acknowledges the previous state and replaces it. The framework’s willingness to correct itself in public is not a vulnerability. It is the demonstration that the governance substrate works.

-----

## The Deeper Point

Git was designed for software version control. Its properties — content-addressable storage, cryptographic hashing, immutable append-only history, distributed redundant copies, named attribution at every decision point — were engineering choices made for code integrity.

Those same properties are exactly what a governance record requires.

The Burgess Principle did not bolt governance onto Git. It recognised that Git already was governance infrastructure — that the same cryptographic and structural guarantees that prevent silent changes to a codebase also prevent silent changes to an institutional record, a doctrinal history, a founding declaration, or an evidence base.

The repository is not documentation about governance. It is governance, executed in a medium that enforces its own integrity.

-----

## The Burgh Connection

LINEAGE.md traces the word *Burgess* to its root: a named individual with civic standing in a chartered town, admitted to the roll through individual assessment, never in bulk.

Git’s commit log is the modern roll. Each commit is an individual entry. Each entry names its author. Each entry is assessed (reviewed, merged, or rejected) before it joins the canonical record. The roll is public. The roll is permanent. The roll is ordered.

The burgh required a sponsor, a hearing, and a roll.
The framework requires a human, a consideration, and a record.
Git provides the record. The human provides the consideration. The commit provides the hearing.

The word, the framework, and the medium converge on the same structure.

-----

*UK Certification Mark <a href="https://trademarks.ipo.gov.uk/ipo-tmcase/page/Results/1/UK00004343685">UK00004343685</a> · MIT Licence*
*github.com/ljbudgie/burgess-principle*
