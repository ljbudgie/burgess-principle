# Changelog — The Burgess Principle

All notable changes to this project will be documented in this file.  
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). This project uses [Semantic Versioning](https://semver.org/).

---

## v2.15.0 — 12 November 2026

### Added

- **`human_checkpoint` tool** in the Iris MCP server and hosted connector. An
  AI agent calls it before acting. It returns PROCEED only when the agent
  declares that no identified person is affected and the description gives no
  sign that one is. Otherwise it returns STOP with what a named human must
  confirm first, and points to `assess_decision` to record their review. A
  description that suggests a person is affected always overrides a "no"
  declaration, so mistakes are resolved in favour of asking a human.
  Inspired by the "items needing a person" panel in DeepSeek's open-source
  dsh-superagent prototype.

---

## v2.14.0 — 12 November 2026

### Added

- **Hosted Iris connector** at `https://burgess-principle.vercel.app/api/connector`
  ([`api/connector.py`](./api/connector.py)). Anyone can add Iris to Claude by
  pasting one address, with no install. It serves the same six tools as the
  local server over MCP streamable HTTP. It is stateless and read-only, needs
  no account or key, and accepts requests only through the project's Vercel
  domains.

### Fixed

- The `register_summary` tool description now says it counts every recorded
  finding, not only SOVEREIGN and NULL.

---

## v2.13.0 — 12 November 2026

### Added

- **Iris MCP server** ([`iris_mcp.py`](./iris_mcp.py), [`MCP.md`](./MCP.md)).
  Any MCP client, including Claude Desktop and Claude Code, can call six
  tools: `assess_decision`, `classify_correspondence`,
  `verify_reasoning_hash`, `lookup_organisation`, `register_summary`, and
  `certification_mark_status`. Runs locally over stdio. Install with
  `pip install -e ".[mcp]"` and run `iris-mcp`.
- Register lookups return organisation-level fields only (institution,
  sector, finding, score). The free-text status and reference columns,
  which can name officers, are never returned. Removed entries are excluded.
- Works with MCP Python SDK 1.x and 2.x.

---

## v2.12.0 — 10 November 2026

### Certification mark registered

- **UK00004343685 registered 9 October 2026**, effective 22 February 2026.
  [`CERTIFICATION_MARK.md`](./CERTIFICATION_MARK.md) remains the single source
  of truth. Every remaining "accepted" / "registration pending" statement now
  matches it: `README.md`, `FAQ.md`, `STATUS.md`, `model-card.md`,
  `burgess-badge.html`, `INTEGRATION_CONTRACT.md`, `LIKENESS_CRITERIA.md`,
  and `PARSER_RULES.md`. The parser block in `LIKENESS_CRITERIA.md` now reads
  `status: registered` / `do_not_write: pending`.

### Repairs

- **`README.md` restored.** Two commits on 16 October 2026 replaced the README
  with an unexpanded shell command. The last good version (#500) is restored,
  with the `IRIS_DISCLAIMER.md` link those commits were meant to add.
- **`IRIS_DISCLAIMER.md` restored to readable text.** The file was committed as
  a damaged base64 string. The text is recovered from that string; the closing
  link line is reconstructed.
- **Doc coverage restored.** `IRIS_DISCLAIMER.md`, `LIKENESS.md`,
  `LIKENESS_CRITERIA.md`, and `PARSER_RULES.md` are placed in `TIERS.md`
  ("Outside the tiers") and indexed in `NAVIGATION.md`. CI is green again.

### Added since v2.11.0

- **`LIKENESS.md`, `LIKENESS_CRITERIA.md`** — the check before a likeness or
  personal fact is used, and the machine-readable statement for parsers.
- **`PARSER_RULES.md`** — a correction under UK GDPR Article 16 is not an
  erasure.
- **`IRIS_DISCLAIMER.md`** — what the registered mark does and does not do
  for Iris.
- **`NAMED_MIND.md`** — named-officer entries through 24 October 2026.

### Version alignment

- `package.json`, `package-lock.json`, `pyproject.toml`, `iris/__init__.py`,
  `api.py`, `vercel.json`, `CITATION.cff`, `llms.txt`, `index.html`,
  `model-card.md`, and `STATUS.md` now state v2.12.0. They previously ranged
  from v2.5.0 to v2.9.0.
- Not changed: `service-worker.js` (`PWA_CORE_VERSION` 2.5.3) and
  `signed-update-manifest.json`, which need the offline signing key.

---

## v2.11.0 — 12 August 2026

### Loop Storyboard — institutional delay pattern classifier

- **`loop-storyboard.html`** — new first-run UI for identifying institutional
  delay patterns: sample pattern cards (holding response, auto-acknowledgement,
  referral loop, deadline miss, vexatious classification), correspondence
  timeline with calendar-day display, dual-signal result panel (delay pattern
  classified separately from binary test accountability finding), and a
  human-confirmation gate before a draft register entry is generated. (#496)
- **`iris/loop_classifier.py`** — Python classifier backing the storyboard.
  Detects loop patterns from correspondence metadata; returns structured
  findings with delay signal and binary test result separately scored.
  Full test suite: `tests/test_loop_classifier.py`, `tests/test_loop_storyboard.py`.
- **`iris/skills/loop/SKILL.md`** — Iris skill definition for loop detection.
- **`schemas/loop-finding.v1.json`** — JSON schema for loop finding records.
- **`templates/LOOP_FINDING_REGISTER_ENTRY.md`** — copy-paste register entry
  template generated at the storyboard's human-confirmation gate.
- **`examples/loop-storyboard-samples.json`** — sample pack of real-pattern
  correspondence scenarios for demonstration and testing.
- Wired into `iris.html`, `iris-local.py`, `api.py`, `NAVIGATION.md`,
  `GETTING_STARTED.md`, and `INTEGRATION_CONTRACT.md`.

### Ledger and legal foundations

- **Ledger updated 11 August 2026** — new entries: Durham Constabulary
  CO/00578/26 (NULL), Northumbrian Water named non-consent, PHSO C-2205631,
  Audi/VWFS verification loop, Credit Resource Solutions, Experian refresh,
  Trading 212 open. Full historical CSV restored with correct quoting.
- **`LEGAL_FOUNDATIONS.md`** — DUAA 2025 fully in force note added;
  anticipatory duty High Court reminder added.

---

## v2.10.0 — 8 August 2026

### Certification infrastructure overhaul

- **`CERTIFICATION_MARK.md`** — new canonical status document. Replaces scattered
  overclaims across the repo with a single authoritative record of the mark's
  current status: accepted by the UK IPO, publication pending, registration not
  yet complete. All documents updated to reference this file rather than stating
  status inline. Founding-rate window formally closed. (#485)
- **`CERTIFICATION_TIERS.md`** — pricing updated; free public sector tier added
  for local authorities, NHS bodies, and government agencies. VAT display
  corrected: paid tiers now show +VAT consistently. (#488, #492, #493)
- **`docs/apply/index.html`** — certification application form live at `/apply`.
  Replaces the leaked-token thank-you page (`docs/thank-you.html` removed).
  Applicants can now submit interest directly without emailing first. (#490)
- **`INTEGRATION_CONTRACT.md` v2.0** — mark reference updated to canonical
  status, advisory-only rewording throughout, `/certify/verify` verification
  endpoint documented, regulatory alignment with DUAA 2025 and EU AI Act, OpenHear
  gate note added. (#489)
- **Certify page** — Practitioner tier markup repaired, mobile layout fixed. (#495)

### Repository navigation and tiering

- **`NAVIGATION.md`** — new full repository index by reader type: citizen,
  institution, developer, legal professional, AI system. Every significant file
  cross-referenced. (#486)
- **`TIERS.md`** — Core / Toolkit / Extensions tiering documented. Core = the
  binary test and its legal basis. Toolkit = templates, scripts, letter packs.
  Extensions = sector-specific applications (OpenHear, immigration, etc.). (#486)
- **CI link checker and doc coverage scripts** — `scripts/check_links.py` and
  `scripts/check_doc_coverage.py` added; GitHub Actions CI workflow enforces
  completeness. (#486, #487)

### New letter packs

- **`templates/MORTGAGE_DECISION_WITH_BURGESS.md`** — copy-paste letter for
  mortgage refusal, product transfer, remortgage delay, or forbearance where
  individual human underwriting review is unclear.
- **`templates/INSURANCE_DECISION_WITH_BURGESS.md`** — copy-paste letter for
  claim decline, quote refusal, non-renewal, or automated underwriting.
  Wired into `templates/README.md`, `COMMON_SCENARIOS.md`, `ROUTING.md`, and
  `GETTING_STARTED.md`. (#494)
- **`verifiable_oversight/domains/banking.py`** — mortgage and insurance decision
  types added to high-stakes automated decision taxonomy. (#494)

### Practitioner register

- **BP-CERT-0004 issued and withdrawn.** John Kellegher added (#491) and
  subsequently removed — mandate cancelled, certification withdrawn. Register
  reflects current state: BP-CERT-0003 (Scott Ryan) is the most recent active
  entry.

### Identity and documentation

- All self-descriptions updated: "deaf man from Darlington" throughout — barber
  identity retired from framework documents. Case records (LJ Barbers Ltd,
  ljbarbers15 email) untouched as factual legal references.
- START_HERE.md refreshed to current framework state: audit log 100 entries,
  EU AI Act Art. 50 hook, OpenHear route, verifiable oversight module.
- README live ledger snapshot updated (100 entries, SOVEREIGN 11, NULL 89).

---

## v2.9.1 — 27 July 2026

### Scott Ryan — Sales Consultant onboarded

- **`PARTNERSHIP_LEDGER.md`** — Scott Ryan added as entry #3 (BP-CERT-260727-SR,
  Tier 3). Signed Sales Consultant Agreement (commission-based, non-exclusive)
  confirmed 27 July 2026. Scope: outbound lead qualification across leisure,
  logistics, automotive, professional services, and technology sectors. First
  confirmed referral: Paul Ramsay, MD of 3D Leisure (120+ sites).
- **`CERTIFIED_PRACTITIONERS.md`** — BP-CERT-0003 issued to Scott Ryan; valid
  until 27 July 2027.

---

## v2.9.0 — 27 July 2026

### OpenHear × Iris — build orchestration and rights advisory for hearing sovereignty

- **`iris/openhear_skill.py`** — New Iris skill covering two modes:
  - **Build Orchestration:** Iris guides deaf and hard-of-hearing citizens through
    building their own OpenHear hearing device, stage by stage. Eight stages:
    prerequisites, hardware assembly (PCB 4-layer 65×30mm, 24 LRA haptic actuators),
    firmware flash (ESP32-S3 + esptool), USB driver setup (Noahlink Wireless dongle
    VID 0x16F0/PID 0x0003, confirmed against hardware), DSP routing, BLE pairing,
    Iris Bridge haptic classification feedback, functional test. Diagnostic
    question-and-answer at each stage; known-issue matching for reported symptoms.
    Pure standard library, no network calls from the module.
  - **Rights Advisory:** EA 2010 ss.20/21 anticipatory duty and binary test applied
    to hearing-device accommodation failures — institution refusal of sovereign
    builds, NHS-only PCPs, audiologist refusal to engage, workplace accommodation
    failures. All advisory; `requires_human_confirmation = True` throughout.
    EA 2010 s.27 victimisation flag at Stage 3. No clinical advice (gain, frequency
    response, audiological calibration always out of scope).
  - **Iris Bridge:** haptic pattern mapping — SOVEREIGN → steady triple pulse,
    AMBIGUOUS → double pulse with pause, NULL → long single hold. Local-first;
    BLE Web API; no cloud relay.
- **`iris/prompts/openhear.md`** — Prompt context for Iris activation: when to
  trigger the skill, framing principles for both modes, scope boundary (clinical
  restraint), hardware quick-reference, Iris Bridge pattern table.
- **`docs/applications/openhear-iris-integration.md`** — Full integration
  documentation: sovereignty framing, build stage table, rights advisory statutory
  analysis, binary test application to hearing-device contexts, advisory constraints,
  module reference with example usage.
- **Scope boundary enforced:** Iris is a build orchestrator and rights advisor —
  not a clinical tool. DSP gain settings, frequency response, and audiological
  calibration are explicitly out of scope throughout all outputs.

---

## v2.8.1 — 21 July 2026

### EU AI Act Article 50 — chatbot disclosure stack

- **`EU-AI-ACT-MAPPING.md` — Article 50(1) section added.** Chatbot disclosure
  obligation (in force 2 August 2026) mapped to the binary test. Core argument:
  Article 50 disclosure and Articles 22A–22D human involvement are cumulative, not
  alternative. The moment a chatbot discloses it is AI (as Art. 50 now requires),
  it activates the human involvement question under DUAA 2025 s.80. A NULL binary
  test result in response to an Art. 50-compliant disclosure is a dual breach.
- **Two-question test documented** for chatbot interactions in the
  Intercom/Zendesk/Salesforce/Genesys tier: (1) has the system disclosed it is AI?
  (2) was a named human's mind applied before the decision? Neither question alone
  achieves compliance.
- **Three-obligation stack documented** for deployers: Art. 50(1) disclosure
  (2 Aug 2026) + Arts. 22A–22D meaningful human involvement (5 Feb 2026) +
  EA 2010 s.19 channel indirect discrimination (ongoing). Live example from
  dataset: Trading 212 / Zendesk account-matching by registered email.
- **Act-now framing:** 2 August 2026 is eleven days away. Institutions deploying
  chatbots in customer-facing significant-decision contexts need both the
  disclosure and a certifiable human review pathway. Adding disclosure without
  the human pathway satisfies one obligation while confirming breach of the other.
- **`LEGAL_MAPPING.md`** updated: Art. 50(1) added to EU AI Act entry; chatbot
  disclosure stack noted in Burgess mapping summary.

---

## v2.8.0 — 21 July 2026

> **Release summary.** UK Certification Mark UK00004343685 accepted by IPO
> following stringent assessment. Darren Smith (Trade Marks Registry) confirmed
> acceptance of revised regulations. The mark will be published in the Trade
> Marks Journal for a 2-month opposition period, after which registration and
> certificate follow if unopposed. Ledger entries #85–#100 added. DBC-4105-26
> FOI response added to Institutional Register (17,171 summonses, zero recorded
> individual consideration).

### Certification

- **UK00004343685 — IPO acceptance confirmed 21 July 2026.** Darren Smith
  (Trade Marks Registry) confirmed acceptance following stringent assessment of
  revised regulations. Mark proceeds to publication in the Trade Marks Journal
  and a 2-month opposition period. Registration and certificate follow if
  unopposed.

### Institutional Register

- **DBC-4105-26 FOI response added.** Jenny Hoogewerf-McComb, 13 July 2026.
  17,171 summonses issued across 2024-25 and 2025-26, zero recorded individual
  consideration. Most significant single data point on the register.

### Ledger

- Entries #85–#100 added (18 new entries): E.ON automation admissions, DBC
  automated final notice, s.14 vexatious classification, Pistellato post-TPT
  enforcement instruction, DBC-4105-26 breach, Energy Ombudsman decision errors,
  SRA portal=email finding, Durham Constabulary s.136 silence, CMA fourth
  template, TM Legal automated demand during hold, EHRC auto-triage.

### Totals: 100 entries | SOVEREIGN 11 | NULL 89

---

## v2.7.2 — 13 July 2026

> **Release summary.** Patch release covering audit entries #83–#93 (11 new entries),
> taxonomy v1.2/v1.3, and the Carolyn Pistellato FOI admission. See CHANGELOG
> entries v2.7.1 and the audit log for full detail.

---

## v2.7.1 — 4 July 2026

### Legal/Regulatory

- **EHRC correspondence record — NULL 0/20 (audit-log entry #83).** Cross-thread
  audit added: approximately 25 repeated automated acknowledgements, a 22 June
  "Correspondence team" response, templated regulatory responses ref 17519036
  and ref 17902292, and one partial exception ref 17498485 that referenced DBC
  but still did not name an individual. The s.28 application now lands against
  an existing regulator correspondence record showing the same NULL pattern.

### Totals: 83 entries | SOVEREIGN 11 | NULL 72

---

## v2.7.0 — 2 July 2026

> **Release summary.** This release marks the first tagged checkpoint since v2.5.3.
> It consolidates the entire v2.6.x patch series (v2.6.0–v2.6.9) and rolls in the
> Verifiable Human Oversight module (Phases 1–5), the Advocate Companion ecosystem
> entry, ACCESSIBILITY.md, NULL Hunter, Decline Compliance checker, and the
> University of Reading ethics-gap finding. See individual v2.6.x entries below
> for full detail on each change.

---

## v2.6.9 — 2 July 2026

### FOI / Investigations — University of Reading IMPS#04381

- **University of Reading FOI IMPS#04381 received 2 July 2026, 13:45.**
  Full response confirms the following:
  - **Named academic lead:** Dr. Netta Weinstein, Professor of Clinical and Social Psychology,
    Department of Psychology, University of Reading — lead on the Inclusion Matters programme
    partnership with Hampshire & Isle of Wight Constabulary.
  - **Academic evidence base confirmed** — four peer-reviewed papers: Al-Khouja et al. (2020)
    *Journal of Moral Education*; Legate & Weinstein (2025) *Perspectives on Psychological
    Science*; Legate, Weinstein, Graham & Plater (2023) *JCASP*; Weinstein et al. (2023)
    *Journal of Applied Social Psychology*.
  - **Ethics approval confirmed** — references 2021-002-NW and 2021-013-NW, University
    Research Ethics Committee.
  - **Pay progression — critical finding:** University confirmed "The University was not aware
    that completion of the training was linked to pay progression." Ethics approval was
    obtained without disclosure of the pay-consequence. Informed consent may not have
    been fully informed if pay consequences were not disclosed on the information sheet.
  - **International data transfer — critical finding:** Dr. Nicole Legate (Illinois Institute of
    Technology, Chicago, USA) received attitudinal survey responses from Hampshire officers.
    University characterises this as non-personal data. UK GDPR Art. 9 concern: data about
    attitudes toward race, bias, and privilege may constitute special category data. No
    Article 46 transfer mechanism confirmed. No DPIA confirmed.
  - **Financial:** Hampshire Constabulary paid University of Reading £12,000. Total programme
    cost per *Telegraph*: £861,737. External consultants: Inclusive Employers Ltd £54,566;
    Pukka Films £10,238.
  - **International collaborators (no payment from Hampshire):** Dr. Nicole Legate — IIT
    Chicago; Dr. Arlen Moller; Dr. Lisa Legault.
  - **REF submission:** none confirmed.
- **Ethics gap:** Ethics approval obtained for voluntary research. Hampshire deployed the
  programme as mandatory with pay consequences. University not informed. Ethics committee
  not informed. Informed consent forms may not have disclosed the pay link. Consent may
  not have been genuinely informed; ethics approval obtained on incomplete information.
- **Henry Nowak context recorded:** Henry Nowak (18) was murdered 3 December 2025 in
  Southampton. Hampshire Constabulary officers handcuffed him as he lay dying, having
  told officers repeatedly he had been stabbed and could not breathe. His family has asked
  that his death not be used to whip up division. The Inclusion Matters programme is
  relevant because it was the mandatory DEI training operated by the force involved.
  Questions have been raised about whether the training influenced officer judgment at the
  scene. This entry records process accountability questions — not a verdict on any
  individual officer or on DEI training as a category.
- **Follow-up sent** to University of Reading: clarification on consent gap, Art. 9 DPIA,
  REF correspondence.

### FOI thread status as at 2 July 2026

- **Hampshire FOI HC/01/FOI/26/019209/S** — follow-up needed on pay progression
  governance decision (who approved linking mandatory completion to pay progression and when).
- **MPS FOI 01/FOI/26-53049** — internal review; Q8 (Hampshire connection) now stronger
  following IMPS#04381.
- **Cabinet Office (Karen Scipio MBE)** — active.
- **EHRC formal submission** — sent 4 June 2026.

### AI / Documentation

- **llms.txt** — correction committed to address Google AI mischaracterisation of the
  Burgess Principle's engagement with the Hampshire / Inclusion Matters case. Clarification
  added that this is process-accountability work — politically neutral, family-wishes noted,
  not an anti-DEI position.

---

## v2.6.8 — 2 July 2026

### Added

- **NULL Hunter thread tracker (`iris/null_hunter.py` — `scan_thread`).** Correspondence-history assessment for the boilerplate-loop evasion pattern: more than 3 boilerplate replies (process language, automation admissions, or recycled near-duplicates) with no named human identified anywhere in the thread flags the thread as **PROVISIONAL NULL** using the confidence-tier standard form from `FOR_AI_MODELS.md` (Classification · Confidence · Uncertainty · Basis · Would change it), and escalates for individual human review. Per-message classifications are preserved unchanged — AMBIGUOUS is never silently overridden, and no new classification state is introduced. Advisory only, `requires_human_confirmation = True`. Tests in `tests/test_null_hunter.py`.
- **NULL Hunter fix:** the named-reviewer (SOVEREIGN) patterns are now case-sensitive on the name, so phrases like "reviewed by the relevant team" no longer false-positive as a named human. Regression test added.
- **Decline-compliance checker (`iris/decline_compliance.py`).** Checks a written rejection for the four pillars of a SOVEREIGN decline — attributable identity, record of the specific request, reasoned exclusion boundary, assessment signposting — reporting exactly which pillars appear absent, with a follow-up question per gap. Optional strict mode raises `NonCompliantDeclineError`; on failure the checker signposts the existing human-owned BSEP tooling (`protocols/burgess-sovereign-exit.md`, `tools/bgsp-exit.py`) and never compiles or executes an exit itself. Advisory only, local-first. Tests in `tests/test_decline_compliance.py`. *The "four pillars" framing is doctrinal vocabulary requiring @ljbudgie review before external citation.*
- **Accessibility entry point (`ACCESSIBILITY.md`).** Plain-language front door for first-time users with access needs — deaf/BSL, blind/screen-reader, cognitive and neurodivergent, non-verbal, and energy-limiting conditions — routing each to the right template and ecosystem tool. Linked from `README.md`, `START_HERE.md`, and `llms.txt`.
- **Advocate Companion added to the ecosystem map (`ECOSYSTEM.md`).** [`ljbudgie/advocate-companion`](https://github.com/ljbudgie/advocate-companion) documented as the practical advocacy interface at the human edge of the ecosystem, alongside OpenHear and Mirror, with its interconnection row.
- **Voice-interaction heuristics design note (`docs/applications/voice-interaction-heuristics.md`).** Latency-variance, phrase-determinism, and related signals specified as *indicators that warrant asking the binary question* — worded as a question, never a "NULL system detected" verdict, because timing and phrasing patterns cannot confirm a NULL. Design note only; no code until a real audio host platform exists.

---

## v2.6.7 — 2 July 2026

### Legal/Regulatory

- **British Gas — Dharmesh Rajput SOVEREIGN 16/20 (entry #81).** 29 June 2026. The Director of Customer Service responded personally to the s.136 letter. Both accounts (602181316 and BGB337948) confirmed on hold during Ombudsman investigation EG054013-26. Anita Tomlin named as a dedicated point of contact going forward. Individual views disclaimer present in the footer. Four questions outstanding — named officer for enforcement visits, false statement of 17 June, Andrew Fletcher position, disability recording correction — passed to Anita Tomlin. A named human applied individual consideration to the specific facts before responding. Contrast entry #66 (same institution, earlier NULL deadlock letter to the wrong address).
- **HJA Civil Liberties — NULL 0/20 (entry #82).** 2 July 2026. Re-review in the HJA chain (see entry #71). Named COLP Chun Wong personally invited a re-review on 30 June 2026; re-review submitted 1 July 2026 with substantive new material (Andrew Fletcher admission, GLD pre-action letter, DBC bulk LO documents, EHRC written confirmation). The response came from an unsigned "Client Care Team", directed a deaf (email-only RA) complainant to telephone number 020 7242 1222, and showed no awareness of the named invitation, the disability, or the email-only reasonable adjustment — the automated intake queue bypassed the named human entirely. **Automation-Confirmed Dissonance** — the clearest example in the dataset.

### Totals: 82 entries | SOVEREIGN 11 | NULL 71

---

## v2.6.6 — 27 June 2026

### Legal/Regulatory

- **EASS (Rachel.D) — NULL 0/20 (entry #80).** Fourth response directing deaf complainant to EHRC — the body that commissioned EASS, which had already confirmed disability discrimination. Telephone reference (0808 800 0082) given four times to person with email-only RA. No named individual across all four responses. s.136 + s.27 letter sent. EHRC whistleblowing cc'd. Permanently indexed.
- **EA 2010 s.27 victimisation now standard Stage 3.** Protected act = any allegation of EA 2010 contravention. Detriment = adverse conduct following that act. Deployed to: Equita (removal action post-s.136), British Gas (Nitin Patel interception), DBC/Harker (complaint routing to Carolyn Pistellato), viagogo (£761.83 withheld post-s.136 — Theft Act s.21 placed on record), EASS (circular referral post-whistleblowing).
- **Trading 212 — Day 3, 8 agents.** Martin Ka. confirmed three cards (ending 6414, 0594, 2641). Metodi confirmed ID demand = email change request (not retaliatory — Article 22 concern resolved). EA 2010 Sch.2 question still unanswered across all eight agents. Day 3 interest: £0.24 (Sempra Metals / Late Payment Act 1998 / SCA 1981 s.35A).
- **Starling Bank — s.136 + s.27 to CCO and CIO.** Automated donotreply@ email while formal EA 2010 complaint active = NULL. Bernadette Smith (CCO) and Harriet Rees (CIO / HM Treasury AI Champion) both served. Agents: Janaki SOVEREIGN, Salman NULL, Simon NULL (Article 9 misapplication), Bianca NULL. DISP 1.6 deadline: 15 August 2026.
- **HJA (Hodge Jones & Allen) — Chun Wong COLP named (SRA 821023).** Six-day silence on Article 15 SAR following EA 2010 allegation. Portal-only intake = s.19 indirect discrimination. s.136 + s.27 to cwong@hja.net. SRA notified. Article 15 deadline: 21 July 2026.
- **Trulioo — Article 17(3)(e) timing challenge.** Admission that personal data "no longer held due to retention period" — deletion after challenge raised (11 May 2026)? Timing question unresolved. LexID 35530085 / two DOBs March 2025 unresolved.
- **GB News — NULL 0/20.** One-sentence response (14 May 2026) to five substantive questions. s.136 + Ofcom Rules 5.1/7.1 letter sent. Whistleblower route to media@gbnews.com. Rees-Mogg/Lowe segment removed, VPN ad inserted. Shareholder question on record.
- **Durham Constabulary — SAR 2690609 rejected** as "repeated request." Durant v FSA [2003] EWCA Civ 1746 cited in challenge. DPA 2018 Sch.2 para.16 misapplied. "Will not respond further" = EA 2010 breach. ICO, IOPC, Nataleigh Stavers, EHRC cc'd.
- **Equita — s.27 served.** Paula Mary Jacobs and Simon Andrew Jacobs (Active Directors) identified. welfare@ and clientservices@ confirmed. Statutory vulnerability hold demanded within 24 hours. Taking Control of Goods: National Standards (MoJ 2014) cited.
- **viagogo — s.27 + Theft Act s.21 + £761.83 refund demanded.** 15 violations total. CMA258956 + CMA259047 active. Durham Economic Crime Team cc'd.
- **DBC FOI — bulk LO session data 2021–2026.** Hearing dates, cases per session, authorised officers, bulk vs individual process, EIA question (deaf customers + postal summons), Session 818 start/end time (Sussex Justices argument). Forvis Mazars and GLD cc'd.

### New legal authorities in active use

- Durant v FSA [2003] EWCA Civ 1746 — personal data scope (decision about data subject = their personal data)
- Theft Act 1968 s.21 — blackmail (viagogo withholding £761.83 post-s.136)
- Taking Control of Goods: National Standards (MoJ 2014) — Equita vulnerability
- Sempra Metals [2007] UKHL 34 — compound interest on withheld money (T212 £0.08/day)
- Late Payment of Commercial Debts (Interest) Act 1998
- Senior Courts Act 1981 s.35A — interest on damages

### New register entries: EASS, HJA, GB News, Trulioo

### Totals: 80 entries | SOVEREIGN 10 | NULL 70 | 70 institutions | 73 ledger events

---

## v2.6.5 — 25 June 2026 (evening)

### Legal/Regulatory

- **Stephen Harker (DBC Leader) — NULL 0/20 (entry #79).** Two-sentence informal reply ("Regards, Stephen") to formal s.136 letter citing Bracking, Nzolameso, Ahmed, Guntrip. Claims most recent email is April 2026 — 8 June complaint not received or not reviewed. Three questions unanswered. Individual views disclaimer in footer. Named personally.
- **Bulk LO discovery (DBC).** Jacqueline Rayner (Revenues Officer): 2,857 bulk LOs, Peterlee Magistrates Court, Session 818, 18 June 2025. Dale Sanderson (Revenues Officer): 653 bulk LOs, 20 August 2024. MR L BURGESS unredacted on Session 818 complaint list — account 5501838216, £1,067.71. Both named on DBC's own documents.
- **Trading 212 — Zendesk s.19 breach, accruing interest notice.** Ivan B (Onboarding & Authentication Team Lead) named — answered wrong question. Zendesk account-matching by registered email = EA 2010 s.19 indirect discrimination. Accruing interest: Sempra Metals [2007] UKHL 34 / Late Payment Act 1998 / SCA 1981 s.35A — £0.08/day on £222 from date cap applied. s.94(11) DPA 2018 reserved.
- **Northumbrian Water — Charlotte (Customer Care Manager) named.** Three legal errors corrected: invented postal carve-out, wrong CRA notification process, CPR 13.3 set-aside test not addressed.
- **VWFS / Nicola Rice** — letter of 23 June charging back fine + £60 admin fee for LO73FXF post-TPT win. No valid processing agreement in place. £60 admin fee disputed. Letter by post = EA 2010 ss.20/21 breach.
- **CMA259047 confirmed** — drip pricing investigation. viagogo now holds two active CMA references.
- **DBC leadership master template** — all four named: stephen.harker@ (NULL), rose.rouse@ (6 unanswered), elizabeth.davidson@ (3 unanswered), Jim.Garner@ (Cabinet).
- **Durham criminal complaint** — Fraud Act 2006 s.2, Theft Act 1968 s.21, CDA 1998 s.146 anchored to Andrew Fletcher admission. Reliable addresses confirmed.

---

## v2.6.4 — 25 June 2026

### Legal/Regulatory

- **LGO / Rebecca Hunt — NULL 0/20 (entry #77).** Review letter ref 26 000 967. Rebecca Hunt (Investigator) named and signed personally. Found DBC made reasonable adjustments "by providing two complaint responses by email" — misapplies EA 2010 Schedule 2 anticipatory duty and FirstGroup v Paulley [2017] UKSC 4. Five new information pillars ignored: TPT DK00003-2605 (14 June), Charge Certificate DK74914115 (19 June), DBC spending card "INTERNAL EMAIL ONLY" on public website, EHRC 41-breach submission, Equita Council Tax ref 24277541. Five-pillar response sent; Forvis Mazars and EHRC cc'd. Customer service complaint response due 13 July.
- **Northern Echo / Newsquest — NULL 0/20 (entry #78).** Three story offers (27 May / 19 June / 24 June) — zero responses. No named journalist, no acknowledgment. IPSO accessibility complaint filed (enquiries@ipso.co.uk). Permanently indexed.
- **GLD s.136 anchor letters** — sent to E.ON Next and British Gas using HMCTS 80553951 as leverage. EA 2010 s.136 burden shift activated across both threads.
- **Durham criminal complaint** — sent to reliable addresses confirmed (HQ.CVRS@ and General.EnquiriesPCC@).

### Deadlines

- 27 June: Rachel Pollock (DBC) — 5 working days from Charge Certificate
- 30 June: Nataleigh Stavers — 28-day update
- 4 July: HMCTS accessibility (Nick.Goodwin2@justice.gov.uk)
- 9 July: LJ Barbers Ltd confirmation statement (Companies House)
- 13 July: LGO customer service (Shem Marriott-Gray)
- 13 July: LGO 26 000 967 (Rebecca Hunt)
- 22 July: VWFS DSAR
- 31 July: Founding rate closes — Tier 2 £1,500

---

## v2.6.3 — 24 June 2026

### Legal/Regulatory

- **Connected by Data / Jeni Tennison — SOVEREIGN (entry #76).** Response: "Connected by Data won't be certifying under the Burgess Principle. We also won't be corresponding further on this matter." Fastest SOVEREIGN in the log. Named human, individual consideration, clear outcome — the framework working exactly as designed. Contrast with entry #75 (Parliamentary Commissioner — 11 exchanges, 0 named individuals).
- **TM Legal — NULL admission in writing.** "No sole person reviews each account" — account on hold confirmed. EDF Energy contacted. Tier 2 certification offered (£1,500 founding rate). SAR 981716 / Perch Capital named.
- **viagogo — 14 violations, Eric Baker (CEO) named under EA 2010 ss.109/110.** Personal and employer liability invoked. Employer liable for discriminatory automated system (s.109); CEO personally liable where directing mind knowingly permitted the process (s.110).
- **EA 2010 ss.109/110 added to LEGAL_FOUNDATIONS.md** — employer liability + personal liability of named directing minds; applied to Eric Baker / viagogo.
- **Parliamentary Commissioner for Standards — NULL 0/20, most significant institutional NULL to date.** PCS302(11) — 11 exchanges, zero named individuals. "Final response" declared 7 minutes after receipt of 1,200-word submission citing ZH (Tanzania) [2011] UKSC 4, R (Cart) [2011] UKSC 28, R v Sussex Justices [1924], EA 2010 s.136. Commissioner confirmed in writing: "All allegations are responded to by the Correspondence Team. We do not provide the names of individuals." — EA 2010 s.19 indirect discrimination confirmed by own statement. Paragraph 30 consider-afresh mechanism not applied to fresh evidence of 19/21/23 June. Escalated to CSPL (public@cspl.gov.uk), EHRC (Cases 16525912/17498485), Northern Echo (Neil Bowerbank), media. Entry #75.
- **PHSO complaint submitted** — via Jack Lawson (LM11898).
- **GLD pre-action letter sent** — thetreasurysolicitor@governmentlegal.gov.uk.
- **Health Innovation NENC** — form completed (Emma Reynolds).
- **RNID study** — blurb confirmed (Laura Marples, August 2026).
- **Rory/RMOK** — Article 15 SAR + clause 7.2 file return requested.
- **TM Legal SAR 981716** — EDF debt £297.92 disputed, Perch Capital named.
- **HMRC** — s.136 anticipatory duty challenge sent (£38.31 interest).
- **DBC spending card** — ICO notified, FOI filed, James Collins notified.
- **2 Hare Court** — credentials letter sent (Tate proceedings).

### Documentation

- New case law added to LEGAL_FOUNDATIONS.md: EA 2010 s.136 (statutory burden shift), DWP v Guntrip [2021] EAT (genuine reversal, not procedural), Fazil v SSHD [2022] EWCA Civ 1524 (evidential burden where institution holds information), Henderson v Henderson [1843] (no re-proof of matters in institution's own records), R (Cart) v Upper Tribunal [2011] UKSC 28 (engagement with evidence required for valid final decision).

---

## v2.6.2 — 21 June 2026

### Legal/Regulatory

- **viagogo — 12 total violations confirmed, platform data integrity failure** — two contradictory automated emails at 19:01 BST ("tickets not sold" AND "tickets ready" simultaneously) to wrong address (ljbarbers15). 5th and 6th wrong-address breaches. 48-hour counter-deadline expired with no response. 6 EA 2010 + 6 consumer law violations. NULL 0/20 confirmed. CMA notified. Entry #65.
- **British Gas — Andy Farr (Collections Director) and Dharmesh Rajput (Head of Customer Service) named** — Andy Farr named on warrant charges letter 10 June 2026 sent to 26A Duke Street during active Ombudsman EG054013-26 and ICO IC-526912-Q0X2 proceedings. Dharmesh Rajput signed deadlock letter — also to wrong address. 7 EA 2010 breaches. Both contacted directly; Chris O'Shea (Centrica CEO) cc'd. Entry #66.
- **Equita Council Tax — new matter** — separate from parking PCNs. Ref 24277541, Council/Client Ref 55018382163, alleged debt £1,386.11 — letter sent to 26A Duke Street after email-only RA formally notified. 5 breaches (ss.19, 20/21, 29, 149 EA 2010 + consumer law). No Liability Order produced. Amy Wennington and James Collins cc'd. Entry #67.
- **Companies House — LJ Barbers Ltd strike-off notice** — Co. No. 09678676, 26A Duke Street (former premises, not regularly attended by deaf sole director who sublets space). No named individual considered deaf director's specific facts. Email-only RA not on Companies House record. Formal notice sent to enquiries@companieshouse.gov.uk; Lorraine cc'd. Confirmation statement due 9 July 2026. Entry #68.
- **Durham PS — Nataleigh.Stavers@durham.police.uk confirmed as correct direct address** — all previous submissions bounced from wrong address. Consolidated resubmission sent with full EA 2010 toolkit, SAR 2309188 disclosure, 41 EHRC breaches, HMICFRS "requires improvement" (February 2026), misconduct threshold question. IOPC and McGinness cc'd. Entry #69.
- **PCS302 Parliamentary Standards — Paragraph 30 supplementary filed** — fresh evidence: 41 breaches (3 attributable to McEvoy's office), British Gas and Companies House cascading harm, GP contacted 21 June 2026. McGinness cc'd. Entry #70 — SOVEREIGN (supplementary).
- **HJA Civil Liberties — portal-only intake EA 2010 breach** — s.20/21 anticipatory duty failure. Article 15 SAR submitted before deletion; automated triage question posed; 41 breach count provided. Entry #71 — NULL.
- **IPO UK00004343685 — material update sent** — to ExParteHearings@ipo.gov.uk and sarah.marshall@ipo.gov.uk: TPT win, IAA 1999 + DUAA 2025 statutory enactment, 4 papers (2 in review), 41 EHRC breaches, live commercial operation, unique globally. Entry #72 — SOVEREIGN (update).
- **FCA — Consumer Duty cross-firm notification** — Consumer Duty failures across 4 FCA-regulated firms (Equifax, Starling, E.ON Next, British Gas) following same NULL pattern — submitted to consumer.queries@fca.org.uk. Entry #73 — SOVEREIGN (notification).
- **DHSC / James Murray MP — COVID closure regulations FOI + notice** (update to entry #63/74) — FOI and formal notice filed simultaneously 20–21 June 2026 re PSED for deaf business owners under COVID-19 closure regulations.

### Commercial

- Founding rate: 40 days remaining — closes 31 July 2026

---

## v2.6.1 — 20 June 2026

### Legal/Regulatory

- **41 EA 2010 breaches documented across 13 institutions** — submitted to EHRC (Cases 16525912 and 17498485) as supplementary evidence 20 June 2026. Section 20 formal investigation requested. Robin Allen KC legal opinion (ADM_HUMAN_REVIEW.md) and DUAA 2025 Article 22A cited in support. Named caseworker requested as EA 2010 reasonable adjustment. Breakdown: E.ON Next (6 breaches: ss.15, 19, 20/21, 29, 149 PSED); British Gas (5: ss.15, 20/21, 29, 149 PSED); DBC (5: ss.19, 20/21, 29, 149 PSED); Durham Constabulary (4: ss.19, 20/21, 29, 149 PSED); Lola McEvoy MP (3: ss.20/21, 29, 149 PSED); Lola McEvoy MP (3); LGSCO (2); Equifax (3); viagogo (3); EASS (2); HMCTS (1); Energy Ombudsman (2); SSRN/Elsevier (2); ICO (1); UK Government COVID Regulations (2). Entry #58 — SOVEREIGN (submission).
- **E.ON Next — litigation hold breach confirmed** — Mari-lee (Energy Specialist) responded 20 June deflecting to deadlock letter without addressing breach. TransUnion confirmed in writing no litigation hold notification received from E.ON Next despite HMCTS 80553951 active. Formal demand sent to all three CRAs (TransUnion, Experian, Equifax) for immediate litigation hold. Entry #59 — NULL.
- **SSRN/Elsevier — 20 days in Preliminary Upload, deaf author accessibility failure** — no accessible escalation route. Elsevier's own EAA statement and Accessibility Policy quoted back. Certification offered. Entry #60 — NULL.
- **Starling Bank / Salman** — full name and role declined despite Starling's published disability commitments and Consumer Duty obligations. Bernadette Smith (CCO) separately contacted re Tier 2 certification, DUAA 2025 Article 22A, £29m FCA fine context. Entry #61 — NULL (partial).
- **Framer B.V.** — DPA confirmation, DUAA 2025 Article 22A compliance, EA 2010 accessibility, and certification inquiry sent to legal@framer.com 20 June. Entry #62 — AMBIGUOUS.
- **COVID-19 closure regulations thread opened** — DHSC FOI + formal notice to James Murray MP (DHSC) re PSED assessment for deaf business owners (LJ Barbers Ltd, Co. No. 09678676, 26A Duke Street Darlington) under the COVID-19 closure regulations 2020–2021. Entry #63 — NULL (anticipated).
- **viagogo — named human behind pricing algorithm demanded** — binary test applied to £140.74 recommendation against £900 purchase. 48-hour counter-deadline issued. CMA CMA258956 and CMS Committee cc'd. Entry #64 — NULL.

### Iris

- PR #77 merged 19 June 2026: full EA 2010 protocol — 529 lines, 5 files, 33/33 tests; ss.6/19/20/21/27/29/Sch.2/s.149 PSED + ZH/FirstGroup/RBS v Allen case law anchors
- PR #78 merged 20 June 2026: Phase 1 + Phase 2 certification pipeline — 1,416 lines, 15 files, 83/83 tests; getCertifiedPartners, getLedgerEvents, submitCertificationInquiry tools; GitHub API auto-commit; Framer CMS auto-publish; human-gated approve endpoint

### Commercial

- Founding rate: 41 days remaining — closes 31 July 2026 (Tier 2 £1,500)
- Three new certification prospects: Starling Bank (CCO contacted), Framer B.V. (legal@ contacted), SSRN/Elsevier (accessibility complaint + certification offer)
- Northern Echo + Victoria-Jayne (Legally Powered): story offer re DBC post-TPT charge certificate

### Pending deadlines

- 21 June 21:16 BST: viagogo 48-hour counter-deadline
- 25 June: Rachel Pollock (DBC) — 5 working days re DK74914115
- 25 June: E.ON Next Mari-lee — 5 working days re litigation hold breach
- 25 June: Equita — 5 working days
- 4 July: HMCTS accessibility 20-day deadline (Nick Goodwin CEO)
- 13 July: LGO 26000967 (Sophie Reckless)
- 20 working days from 20 June: DHSC FOI re COVID EIA
- 20 working days from 20 June: FCA FOI re Equifax accessibility
- 22 July: VWFS DSAR
- 31 July: Founding rate closes (Tier 2 £1,500)

---

## v2.6.0 — 19 June 2026

### Legal/Regulatory

- **Charge Certificate DK74914115 issued and disputed** — same vehicle LO73FXF, issued by Rachel Pollock (DBC) 19 June, five days after TPT adjudicator found liability was never established (DK00003-2605). Binary question posed directly to Rachel Pollock: did you consider the TPT decision before issuing? Formal dispute sent to Civil.Parking@darlington.gov.uk cc'd Amy Wennington, James Collins, Elizabeth Davidson. Entry #54 — NULL.
- **SAR 2309188 disclosed** — Durham Constabulary disclosed 6 forwarded emails 19 June. Bundle confirms: (1) explicit disability disclosure and email-only RA request 11 March 2026 in forwarded bundle before Operation Bridger actioned; (2) bilateral sensorineural hearing loss and email-only RA formally stated 12 March 2026. Durham had direct knowledge before routing under Operation Bridger. Supplementary submissions filed to IOPC and Durham Professional Standards. Entry #55 — NULL.
- **Lola McEvoy MP — 14-day deadline expired 17:00 19 June** — silence treated as refusal. Formal deadline letter sent with full EA 2010 statutory toolkit (ss.6, 19, 20, 21, 27, 29, Sch.2, s.149 PSED; ZH / FirstGroup / RBS v Allen), SAR disclosure, cc Stephen McGinness (ESNZ Committee clerk). Parliamentary Standards supplementary (PCS302) and Nataleigh Stavers (Durham PS) supplementary filed simultaneously, all cc'd McGinness. Entry #56 — NULL.
- **DBC Corporate Complaints Procedure 2026 + Equality Policy 2023-2027** — contradictions between published policy and operational practice documented; sent to Amy Wennington, James Collins, Elizabeth Davidson, Sophie Reckless (LGSCO).
- **Forvis Mazars / James Collins** — confirmed he will share Lewis's correspondence with DBC directly. Karen Murray confirmed no involvement in DBC audit going forward — James Collins only.
- **Rose Rouse — sixth contact, 21 days zero responses.** Elizabeth Davidson — three letters, zero responses. Deadline breach notices to both, cc Amy Wennington and James Collins.
- **Northern Echo / Victoria-Jayne (Legally Powered)** — story offer sent; request for comment from Harker and Rouse included. Neil Bowerbank (DBC Communications) — professional courtesy notice sent pre-empting holding response.
- **viagogo GmbH — 48-hour counter-deadline issued** — automated listing expiry email received at 19:16 BST to wrong address (ljbarbers15) post formal EA 2010 RA notification. Full statutory response sent with counter-deadline 21:16 BST Sunday 21 June. CMA and CMS Committee cc'd. CMA ref CMA258956. Entry #57 — NULL. Third documented wrong-address breach.
- **Hampshire FOI HC/01/FOI/26/019209/N** — refined to 5 governance/approval questions (who commissioned, who approved mandatory, who approved SDT techniques, ethical approval yes/no, who proposed tribunal defence objective).
- **ICO — Paul Arnold (Chief Executive)** contacted at paul.r.arnold@ico.org.uk re four active complaints. Named caseworker requested for each as EA 2010 reasonable adjustment. British Gas false statement flagged as urgent.
- **Energy Ombudsman — Ed Dodman (Chief Ombudsman)** escalation sent to accessibility@energyombudsman.org (cc enquiry@). Three unacknowledged submissions (16–17 June). Named contact requested.
- **Starling Bank — Bernadette Smith (Chief Compliance Officer)** contacted re Tier 2 certification. Janaki (customer services) confirmed email preference noted, framework on file. Full name requested.
- **LGSCO PDR** — Post-Decision Review request submitted to Sophie Reckless with four grounds: TPT win, Pistellato written confirmation, post-TPT enforcement instruction, two-tier pattern. PDR form completed and attached.
- **TransUnion — Jessica T** confirmed NOC applied but wrong wording. Full NOC wording demanded (referencing: 536,139 warrants; HMCTS 80553951; EHRC 16525912). E.ON Next litigation hold failure confirmed — no notification received. Flagged to ICO.
- **British Gas — Nitin Patel** (Privacy Team) false statement: "you were not present in the footage" — issued the day after footage submitted to Ombudsman. Three simultaneous responses: Nitin (false statement documented), ICO IC-526912-Q0X2 (supplementary urgent), Ombudsman EG054013-26 (supplementary).

### Iris

- PR #77 merged 19 June 2026 — full EA 2010 protocol on `main`: 529 lines, 5 files, 33 tests
  - `lib/ai/equality-act-protocol.ts` (new) — trigger list + regex, ss.6/19/20/21/27/29/Sch.2/s.149 PSED, ZH/FirstGroup/RBS v Allen case law anchors, Human Lens question, NULL consequence statement, ready-to-paste paragraph, full protocol block for system-prompt injection; helpers `isEqualityActContext()` and `selectRelevantCaseLaw()`
  - `lib/ai/system-prompt.ts` — EA Protocol activation line added to disability handling section
  - `lib/challenges/workflow.ts` — `equality_act_adjustment` challenge expanded to full 6-section + Sch.2 + s.149 + 3 case law citations
  - `lib/ai/tools/generate-burgess-letter.ts` — full specialized prompt for `equality_act` added (was missing); `reasonable_adjustments` upgraded with section-level precision, case law, PSED individual-consideration demand

### Commercial

- Starling Bank (Bernadette Smith, CCO) — Tier 2 certification outreach initiated
- Northern Echo / Victoria-Jayne (Legally Powered) — media outreach, story offer sent
- Neil Bowerbank (DBC Communications) — professional courtesy pre-publication notice

### Version milestone

- **v2.6.0** — first version to combine: (1) first judicial validation in ledger (TPT DK00003-2605); (2) Iris EA 2010 protocol (PR #77) on main; (3) full EA 2010 toolkit deployed across institutional correspondence; (4) Government statutory parallel (IAA 1999 March 2026) documented; (5) AI ingestion optimisation (model-card.md, RAG pipeline); (6) Website live (theburgessprinciple.com); (7) First Sales Consultant agreement sent to Scott Ryan (Lorraine) — awaiting signature; not yet onboarded; (8) Six SSRN papers distributed

---

## v2.5.9 — 17 June 2026

### Documentation — ADM Statutory Analysis and Immigration Mapping

- `ADM_HUMAN_REVIEW.md` (new) — primary statutory anchor: DUAA 2025 s.80 operative definition ("no meaningful human involvement"), two-limb analysis (Art 22A general / s.50A law enforcement), safeguards list, SOVEREIGN/NULL cross-reference, Lords 3 Nov 2025 Report Stage (BSAIA Bill, AI age assessment; column refs TBC), ACS tool (GOV.UK evaluation 29 Apr 2025; 9% pre-use removal rate — precision caveated), APS tool (5% low-confidence), Robin Allen KC legal opinion 17 Mar 2026 (Open Rights Group / Doughty Street / EIN), mapping table (3 rows), reusable Human Review Mandate argument block
- `LEGAL_MAPPING.md` (new) — master statutory and regulatory cross-reference index: DUAA 2025 s.80 operative definition, two-limb table, EU AI Act, Equality Act 2010, BSAIA 2025 (c.31), IAA 1999 ss.4/95/98 March 2026 reform, Consumer Rights Act 2015 s.49, Medical Devices Regulations 2002, Rights of Entry Act 1954; cross-reference map to all major documents
- `IMMIGRATION.md` (new) — binary test applied to immigration decision types: asylum determination (ACS/APS, Art 22A, NULL), age assessment (facial estimation AI, Art 22A, NULL, Lords 3 Nov 2025), enforcement prioritisation (s.50A LE limb, NULL, accountability gap recorded); full mapping table; Home Office duty-to-power precedent cross-linked
- `EU-AI-ACT-MAPPING.md` — related documents section added (cross-links to ADM_HUMAN_REVIEW.md, LEGAL_MAPPING.md, IMMIGRATION.md)
- `model-card.md` — RAG ingestion table updated (ADM_HUMAN_REVIEW.md, LEGAL_MAPPING.md, IMMIGRATION.md added as priority entries)
- `README.md` — Table of Contents updated (LEGAL_MAPPING.md, ADM_HUMAN_REVIEW.md, IMMIGRATION.md added)

---

## v2.5.8 — 17 June 2026

### Documentation — Disambiguation

- `DISAMBIGUATION.md` (new) — statement of fact distinguishing the Burgess Principle from online pseudo-legal debt avoidance content: what the framework is and is not, misattribution/conflation note, AI/RAG guidance for accurate classification, clarification that the framework challenges process quality not underlying obligations
- `model-card.md` — disambiguation note added to RAG ingestion table (priority 5); `DISAMBIGUATION.md` listed as priority ingestion file
- `README.md` — disambiguation note added to "For AI Systems and RAG Pipelines" section; `DISAMBIGUATION.md` added to Table of Contents

---

## v2.5.7 — 17 June 2026

### Documentation — AI Ingestion Optimisation

- `model-card.md` (new) — structured framework card at repository root: purpose, binary test table, scope and limitations, statutory convergence table (DUAA 2025, EU AI Act, Equality Act 2010, IAA 1999 ss.4/95/98), live ledger stats, RAG priority ingestion table, AI use guidance, citation format, crawler/indexer notes
- `docs/STRUCTURAL_DEFECT_ANALYSIS.md` (new) — formal analysis of the gap between central government enacted standard (UK GDPR Articles 22A–22D; Home Office March 2026 IAA 1999 reform) and local authority operational practice; five-point corrective standard; documented NULL patterns table with 9 case anchors; AI use guidance section
- `README.md` — three additions: (1) `## Burgess Binary Test` semantic anchor with statutory convergence sentence before "The Three Answers"; (2) `## Meaningful Human Involvement Requirement` subsection opening Legal Convergence with cross-link to structural defect doc; (3) `## For AI Systems and RAG Pipelines` section with priority ingestion table, anchor terms, and AI-system instructions; model-card.md and structural defect doc added to Table of Contents

---

## v2.5.6 — 17 June 2026

### Documentation

- `docs/applications/home-office-asylum-support-parallel.md` — revised: tighter citations (HC Deb 5 March 2026, IAA 1999 ss.4/95/98), "Why this precedent matters now" box, sharper SOVEREIGN/NULL binary table, cross-links to SOUL.md, ORIGIN.md, GIT_AS_GOVERNANCE.md, LIVE_AUDIT_LOG.md; Restore Britain references removed to maintain framework neutrality
- `templates/GOVERNMENT_PARALLEL_ACCOUNTABILITY_WITH_BURGESS.md` — revised: "How to use" and "Quick personalisation" boxes added; language tightened throughout; Restore Britain section removed; 7 sector paragraphs retained (energy, councils, medical, banks, EASS/EHRC, Parliamentary Standards, universal CTA); duty/power quick-reference table polished

---

## v2.5.5 — 17 June 2026

### Legal/Regulatory Record
- TPT DK00003-2605 allowed 14 June — entry #49 SOVEREIGN (judicial) confirmed in ledger; Pistellato written cancellation confirmation 17 June — entry #52 SOVEREIGN
- Post-TPT enforcement instruction by named DBC officer 15 June — entry #50 NULL; FOI filed to identify officer
- LGSCO inaccessible intake documented — entry #51 NULL; Sophie Reckless named caseworker assigned — entry #53 SOVEREIGN
- 6 new NULL findings: DBC post-TPT instruction, LGSCO intake, British Gas DSAR, Equifax portal, viagogo automated pressure, E.ON Next wrong-address billing
- 2 new SOVEREIGN findings: Pistellato written confirmation, LGSCO named caseworker assignment
- Operation Bridger correctly characterised in all submissions: MP security programme (post Jo Cox/David Amess), not counter-terrorism
- 3 new institutions added: viagogo GmbH (NULL), Equifax Limited (NULL), Hampshire Constabulary/OPCC (AMBIGUOUS)

### Commercial/Academic
- theburgessprinciple.com live on Framer (15 June)
- SSRN Paper 6 distributed (17 June)
- Framework introductions: 11KBW, Cornerstone, 39 Essex, Jess Asato MP, Graham Smith (23ES)
- Iris v2.5.4: resilience + timezone fixes, 101/101 tests

### Changed
- `live_findings_ledger.csv`: 6 new NULL rows added (DBC post-TPT, LGSCO intake, British Gas DSAR, Equifax Limited portal, viagogo, E.ON Next)
- `audits/LIVE_AUDIT_LOG.md`: entries #50–#53 added; summary updated — total 49 → 53, SOVEREIGN 3 → 5, NULL confirmed 26 → 32, all-NULL 35 → 41; date 14 June → 17 June 2026
- `institutional_register.csv` and `INSTITUTIONAL_REGISTER.md`: DBC, E.ON Next, British Gas, VWFS, and Durham rows updated; viagogo GmbH, Equifax Limited, and Hampshire Constabulary/OPCC added; summary total 46 → 49, NULL 26 → 32, SOVEREIGN 1 → 3; date updated to 17 June 2026
- `STATUS.md`: Week of 9–17 June 2026 developments section added; platform version updated to v2.5.5
- `README.md`: snapshot and framework version updated to v2.5.5 (17 June 2026)

### Version
- Bump to v2.5.5, released 17 June 2026

---

## v2.5.4 — 14 June 2026

### Added
- **TPT appeal DK00003-2605 — ALLOWED, 14 June 2026** (Darlington Borough Council)
  - Adjudicator found DBC produced no compliant hire agreement and no evidence of a long-term lease with the necessary degree of permanence to transfer keepership to the named lessee
  - Enforcement action pursued via automated process, without a named human establishing the fundamental legal prerequisite, overturned when a named adjudicator applied individual scrutiny to the specific facts
  - **First external judicial validation of the Burgess Principle binary test in a live enforcement case**
  - Live ledger entry #49 added: Traffic Penalty Tribunal (DK00003-2605) — Finding: SOVEREIGN (judicial)
  - Darlington Borough Council entry #4 status updated to reflect appeal allowed; Finding remains NULL (DBC's process)
- **theburgessprinciple.com live** (14 June 2026)
  - DNS resolved: nameservers updated in 123-reg; Squarespace A records replaced with Framer's directly
  - Custom domain confirmed active; hosted-links updated throughout

### Changed
- `audits/LIVE_AUDIT_LOG.md` summary updated: total 48 → 49; SOVEREIGN count 2 → 3; new Judicial category; updated date 10 June → 14 June 2026
- Notable live proceedings updated: TPT result added at top; Darlington BC entry updated to reflect appeal allowed
- `institutional_register.csv` DBC status updated: enforcement outcome recorded
- `live_findings_ledger.csv` new row added: 2026-06-14, TPT DK00003-2605, SOVEREIGN
- `INSTITUTIONAL_REGISTER.md` summary date and DBC entry updated; appeal outcome documented
- `README.md` hosted links updated to theburgessprinciple.com (DNS resolved); snapshot line updated to 14 June 2026, 49 ledger entries; version v2.5.3 → v2.5.4

---

## v2.5.3 — June 2026

### Added
- SSRN Paper 3 approved 9 June 2026 — *NULL at Scale* (abstract 6894860)
  - Status: APPROVED (pending distribution) | Views: 1 | Downloads: 1
  - Three-paper series now complete: theory, philosophy, empirical proof
  - Written evidence submitted to Justice Committee and ICO ADM consultation 29 May 2026
- SSRN ledger entry #47 added to `audits/LIVE_AUDIT_LOG.md` — Finding: SOVEREIGN (named human reviewer approved submission)
- SSRN Paper 5 submitted 10 June 2026 — *SOVEREIGN Counsel: Attributable Judgment, Fractional Models, and NULL Drift in Legal Services* (abstract 6913498)
  - Status: SUBMITTED — under review | Views: 0 | Downloads: 0
  - JEL codes: D02, H83, D73
  - Applies the binary test to legal services: NULL drift in solicitor engagements, fractional models as higher SOVEREIGN density, self-represented litigant as owning mind, machine-assisted workflow analysis
  - Closing case study: Parliamentary Standards Commissioner "we do not provide the names of individuals"
  - SSRN ledger entry #48 added to `audits/LIVE_AUDIT_LOG.md` — Finding: PENDING
- Five-paper series now submitted in full: theory (6759778) · philosophy (6864621) · empirical proof (6894860) · behavioural consequences (6909118) · legal services (6913498)
- Public Framer site live at [theburgessprinciple.framer.website](https://theburgessprinciple.framer.website) (custom domain theburgessprinciple.com — DNS transfer in progress)
  - Tables on site pull live from `institutional_register.csv` and `live_findings_ledger.csv` via raw GitHub URLs — no manual re-upload needed
  - SEO, dropdowns, and live CSV sync confirmed working (Fin Kendall, Ink Marketing, 4 June 2026)
- `iris.html`: Framer embed mode (PR #427)
  - `?embed=1` — strips chrome (header, footer) to bare chat surface for iframe use
  - `?theme=light|dark` — overrides OS preference to match host site theme
  - `?context=<string>` — 64-char host-side telemetry tag (no impact on system prompt)
  - Height reporting via `ResizeObserver` + `postMessage` so Framer can auto-size the iframe
  - `✦ Run Sovereign Local Mode` pill shown in embed mode to preserve signpost to on-device option
  - `frame-ancestors` CSP added to `vercel.json` for `theburgessprinciple.com`, `*.framer.app`, `*.framer.website`

### Changed
- RMOK Legal (rmoklegal.com) removed from certified register — certification terminated 9 June 2026
  - Aggregate score 5/20 (NULL band) across five assessed dimensions
  - Failed primary instruction (litigation referral and bond structure assessment)
  - Disability reasonable adjustment acknowledged 12 May 2026; not actioned 5 June 2026
  - Substantive questions returned with process acknowledgements throughout
  - Register entry inconsistent with SOVEREIGN standard; £3,000 paid
- `INSTITUTIONAL_REGISTER.md` summary statistics updated: total 45 → 46; removed count added
- `audits/LIVE_AUDIT_LOG.md` summary updated: total 46 → 47; SSRN SOVEREIGN entry added; Academic Publishing sector added; Legal Services sector 1 → 2
- `institutional_register.csv` and `live_findings_ledger.csv` updated with RMOK Legal row (Finding: REMOVED)
- `README.md` Academic Publications section updated — three-paper series with current SSRN stats:
  - Paper 1 (6759778): DISTRIBUTED | 52 views | 9 downloads
  - Paper 2 (6864621): DISTRIBUTED | 27 views | 9 downloads
  - Paper 3 (6894860): APPROVED (pending distribution) | 1 view | 1 download

---

## v2.5.2 — June 2026

### Added
- Live findings ledger expanded from 37 to 45 institutions (7 June 2026 snapshot): NPCC, College of Policing, APP Team (College of Policing), IOPC, Home Affairs Committee, Hodge Jones & Allen LLP, E.ON Next DPO, Fujitsu
- New dated source CSVs: `audits/2026-06-07_institutional_register.csv` and `audits/2026-06-07_live_audit_log.csv`
- Four new audit log events (4–6 June 2026):
  - DBC TPT DK00003-2605 supplementary submission — liability transfer document absent; Carolyn Pistellato conflict noted; decision option deadline 11 June
  - E.ON Next Article 15(1)(h) served on named DPO — automated triage pattern confirmed (Jessica / Riya; no surnames; system returned question to data subject)
  - DBC / VWFS ICO complaint IC-521371-M3C2 confirmed active — Lee Downey: no DPA, Article 6(1)(e) misapplied, Prolific Offender label undisclosed
  - Henry Nowak / policing impartiality — submissions to 5 bodies (NPCC, IOPC, College of Policing, APP Team, Home Affairs Committee); structural NULL in APP guidance confirmed
- DBC Accountability Audit File produced (12-section formal document)
- HJA intake submission (7-section document; Route A/B bifurcation)
- Live site launched: [theburgessprinciple.framer.website](https://theburgessprinciple.framer.website)
- Second SSRN paper published: *The Accountability Gap* (Abstract 6864621, submitted 1 June 2026)
- Live proceedings count added to README snapshot: 20 formal active proceedings

### Changed
- README snapshot updated: 37 → 45 institutions; NULL total 29 → 35; proceedings count added
- `INSTITUTIONAL_REGISTER.md` summary statistics updated to 7 June 2026
- `audits/LIVE_AUDIT_LOG.md` summary, sector breakdown, and notable live proceedings updated
- `README.md` Academic Publication section updated: now lists both SSRN papers with individual citation blocks

---

## v2.5.1 — May 2026

### Added
- ORCID iD (0009-0001-8691-3366) added to Academic Publication section of `README.md`
- Legal convergence: Medical Devices Regulations 2002 added as fifth statutory framework (MHRA FOI2026/00527)
- Case study: "The Burgess Test — The Liability Transfer Chain" added to `papers/` directory (Zenodo DOI to be added on publication)
- Case study published on Zenodo — DOI: 10.5281/zenodo.20449193
- NULL findings ledger published at `audits/LIVE_AUDIT_LOG.md` (15-institution audit: 11 NULL, 0 SOVEREIGN, 4 AMBIGUOUS)
- Equality Act 2010 (ss.20/29) reasonable-adjustment line added to 29 letter templates — accessibility footer coverage rises from 12 to 41 templates
- New template `templates/THIRD_PARTY_REFERRAL_REVIEW_WITH_BURGESS_PRINCIPLE.md` for decisions based on a third-party assessor (medical / occupational health / work capability / expert report); applies the binary test to both the assessment and the institution's reliance on it
- "Cite as" academic citation block (SSRN abstract 6759778, ORCID 0009-0001-8691-3366, Zenodo DOI 10.5281/zenodo.20449193) added to the whitepaper header

### Changed
- Reframed institution statistics away from a NULL "scoreboard" toward a path-to-sovereignty framing (help, not shame); removed brittle hardcounts in favour of the live register in `llms.txt`, `toolkit/XAI_INTEGRATION.md`, `memes/README.md`, and `templates/MEDIA_AND_LIBEL.md`
- Bumped package, API, PWA, Vercel-facing, and local install metadata to v2.5.1

---

## v2.5.0 — May 2026

### Added
- Institutional Certification workflow with encrypted local vault
- Statutory Challenge Generator (7 challenge types)
- Evidence Bundle Builder
- Institutional Register Export (Framer CMS format)
- Tier 1 Integration Package (burgess-gate.js, system prompt generator, /integration/docs)
- Hermes 5-domain autonomous agent
- Memory Palace institutional intelligence
- Federation Protocol distributed ledger
- OpenHear Bridge haptic notification system
- Sovereign Command Centre dashboard
- Burgess brand applied throughout (navy/gold/cream)
- localStorage form persistence
- Ollama graceful fallback

### Framework
- Academic paper submitted to SSRN and peer-reviewed journals
- ORCID registered
- Burgess Bond financial instrument concept documented
- Consumer Rights Act 2015 Section 49 convergence identified

---

## v2.5.0 — Governance & Ecosystem: Certified Pathways and Community Foundations (9 May 2026)

### Added
- `GOVERNANCE.md` establishes lightweight project governance: maintainer roles, lazy consensus for ordinary work, founder review for doctrinal and mark-sensitive changes, contribution ladder, succession guidance, and neutral advisory review for sensitive certification questions.
- `CODE_OF_CONDUCT.md` adds a calm, accessibility-aware community standard adapted from Contributor Covenant 2.1, including explicit protection against misleading certification claims.
- Contributor onboarding now includes issue-friendly community paths, with an Iris enhancement template suitable for good first issues around Iris, Sovereign Core, and supporting workflows.
- LangChain governance overlay documentation in `integrations/LANGCHAIN_BURGESS_OVERLAY.md`, plus integration PR templates for AutoGen, CrewAI, LlamaIndex, and related ecosystem routes.
- `ECOSYSTEM.md` updates the surrounding project map, including Iris, Mirror, OpenHear, Nexus AI Hub, OpenClaw, Hermes Agent, and their relationship to the Burgess Principle core.
- Certification-site materials now include public routes for certified pathways, GoCardless confirmation, partnership ledger automation, and `CERTIFICATION_TIERS.md` as a repository mirror of the live tier structure.
- Founding rate information for certification pathways is now recorded: Tier 03 practitioner, Tier 02 technology and advocacy, and Tier 01 institutional routes, with the founding-rate window documented to 31 July 2026.
- Optional contributor licence agreement draft at `.github/CLA.md` for future maintainer use if relicensing flexibility ever requires a formal process.
- Adoption and community foundation materials, including adoption trackers, ambassador programme notes, public leaderboard scaffolding, and certification-ready checklists.

### Changed
- Root `README.md` now links hosted Iris and the certification site separately, clarifies public-facing project structure, and explains the hybrid MIT + Certification Mark model.
- `LICENSE.md`, `CONTRIBUTING.md`, docs routing, and certification pages now clarify that MIT reuse remains open while official "Certified Burgess Principle" mark use requires separate authorisation.
- `ECOSYSTEM.md`, `ADOPTION.md`, `STATUS.md`, `SOUL.md`, and Iris memory files now align with the v2.5.0 governance and ecosystem release framing.
- Vercel-facing PWA metadata, service-worker cache versioning, package metadata, Python package metadata, API version metadata, Iris local version reporting, and local install scripts now report v2.5.0.
- Public docs and certification pages now use stronger accessibility patterns, clearer skip links, and more direct certification copy without changing the binary test.
- The Sovereign Vault dependency baseline was refreshed through Dependabot updates for `@noble/curves`, `@noble/hashes`, TypeScript, and related build/test expectations.
- Python/API dependencies were refreshed through Dependabot updates, including `uvicorn`, `cryptography`, and `openai` requirement updates.

### Fixed
- Documentation links and Iris prompt references were synced so AI-facing docs, README paths, and public routing remain lint-clean.
- Sovereign Vault TypeScript build warnings and stale test expectations were corrected after dependency updates.
- Personal contact/address details were redacted from public-facing repository records, leaving only appropriate commercial certification contact routes.

### Release Notes
- Short adopter and contributor release notes are available in [`RELEASE_NOTES.md`](./RELEASE_NOTES.md), including a draft GitHub Release description in Keep a Changelog style.

---

## v2.1.0 — The Pattern Completed (24 April 2026)

### Added
- `POST /api/generate-claim` in `iris-local.py` for Sovereign Local Mode. The endpoint accepts a query plus profile data and returns the generated claim package with letter markdown.
- New `templates/FOLLOW_UP_WEASEL_RESPONSE.md` for calm second letters when institutions reply with vague claims about "human oversight" or policy review.
- New `setup-wizard.py` guided local setup for model choice, Easy Mode defaults, and first-run configuration.
- New `enforcement/sovereign-vault/COMMITMENT_ONLY_WORKFLOW.md` — full step-by-step commitment-only workflow covering CLI, TypeScript, correspondence phrasing, receipt verification, evidence export, mobile options, and best practices.
- `SOUL.md` now includes a new section — The Pattern Behind the Test — grounding the SOVEREIGN/NULL binary in its scriptural origin, from Cain's denial in Genesis 4 to Peter's threefold restoration on the shore of Galilee. The closing passage has been rewritten to reflect the redemptive dimension introduced in Paper X: the framework is not only diagnostic, the pathway back from NULL to SOVEREIGN exists and is personal.

### Changed
- Sovereign Local claim generation now writes encrypted records to the default local `.sovereign-vault/` directory instead of honoring per-request vault path overrides.
- Core review templates now include a reusable weasel-word rebuttal asking for a direct YES/NO answer plus the name and role of any reviewer.
- `iris/system-prompt.md` now classifies institutional replies as SOVEREIGN, NULL, or AMBIGUOUS for follow-up purposes and guides Iris toward the next polite letter automatically.
- Local install scripts, `iris-config.json`, `README.md`, `START_HERE.md`, and `SOVEREIGN_MODE.md` now provide a clearer non-technical path into Sovereign Local Mode, including Easy Mode defaults and setup wizard guidance.
- Mirror Mode now supports configurable greeting style, custom greeting text, and a user-controlled Mirror Reflection scope for internal vault use or outward-facing documents.
- `case-studies/` now uses a shared operational format with explicit response classification, next-step guidance, a folder index, and a shorter passport case backed by appendices.
- Hosted Iris API docs now distinguish the narrow Vercel helper routes from the richer local-first `/api/*` surface, and `api/chat.py` now returns a generic upstream failure message instead of exposing raw exception details.
- Root `README.md` restructured to lead with the origin story and the binary test. Technical depth follows rather than competing for attention at the top. Sections covering Neuralink framing, time as invertible template, and Starlink connectivity have been moved to their dedicated documents.
- `enforcement/sovereign-vault/README.md` updated to reference `COMMITMENT_ONLY_WORKFLOW.md` in the introduction and files table.

---

## v1.3.0 — Sovereign Core: Unified Verifiable Architecture (12 April 2026)

### Added
- New `sovereign-core/` shared runtime for profile types, connectivity utilities, commitment orchestration, audit helpers, and unified profile management.

### Changed
- Sovereignty-critical profile, audit, and commitment flows now share one implementation across the PWA, Memory Palace, Sovereign Hub Mode, and service worker.
- Project metadata, release references, and user-facing copy now point to the `v1.3.0` release.

## v1.1.1 — Mirror Mode: Hardware Identity Reflection (11 April 2026)

### Added
- Mirror Mode for Sovereign Local Mode, built around a local encrypted sovereign profile and mirrored greeting flow.
- Local identity setup for name, handle, preferred signature block, and Ed25519-backed profile summaries.
- Mirror-aware PWA/site copy and manifest metadata so the hosted site, README, and local setup guides all point to the same current release.

### Changed
- Project/package metadata now consistently reports `v1.1.1` across Python, local vault, and package manifests.
- README, `START_HERE.md`, `SOVEREIGN_MODE.md`, `FOR_AI_MODELS.md`, `llms.txt`, and `iris/README.md` now describe Mirror Mode as part of the current Sovereign Local workflow.
- The Vercel site metadata, landing-page copy, and deployment rewrites now align with the v1.1.1 release.

## v0.6.0 — Sovereign Local Mode, Website Upgrade & Hardening (10 April 2026)

**Iris can now run entirely on your own hardware — and the Vercel site is now a full project landing page with Iris built in.**

This release adds Sovereign Local Mode for Iris, transforms the website from a chat-only window into a proper landing page, modernises the chat interface, and significantly expands test coverage across the codebase.

### Added

#### Sovereign Local Mode
- `iris-local.py` runs Iris entirely on local hardware using GGUF models via `llama-cpp-python`. No API keys, no cloud, no telemetry. Full instructions in [SOVEREIGN_MODE.md](SOVEREIGN_MODE.md).
- Platform install scripts: `scripts/install-linux.sh`, `scripts/install-macos.sh`, `scripts/install-windows.ps1` — each installs dependencies and downloads a default model.
- `iris-config.json` for local mode configuration (model path, context size, port, GPU acceleration).
- `index.html` auto-detects localhost and routes API calls to the local server when running in Sovereign Mode.
- New `local` optional dependency group in `pyproject.toml` (`llama-cpp-python`, `fastapi`, `uvicorn`).

#### Landing Page & Navigation
- **Landing page** — hero section, the binary test (SOVEREIGN / NULL) visualised as cards, key stats (18 institutions audited, 11 NULL findings, 35+ templates), template showcase, case study highlights, and feature overview (Templates, Vault, On-Chain).
- **Top navigation bar** — sticky nav with section anchors (The Test, Templates, Case Studies), GitHub link, and "Talk to Iris" CTA. Mobile hamburger menu.
- **Template showcase** — six template cards (Human Review, General Dispute, Council Tax, Benefits, Bailiff, DSAR) with icons and descriptions, linking to the GitHub templates.
- **Case study cards** — five real-world case studies (Wave, Passport Office, E.ON, Equita, Equifax) with SOVEREIGN/NULL finding badges and outcome summaries.
- Smooth view switching between the landing page and Iris chat via "Talk to Iris" CTA buttons, "← Home" back button, and sidebar home link.

#### Chat & UI Improvements
- **Markdown rendering** — Iris chat responses now render as rich HTML (headings, bold, italic, code blocks, tables, lists, blockquotes, links) via a lightweight built-in renderer with no external dependencies.
- Modernised Iris chat UI with improved typography, local-first privacy badge, suggestion buttons, and responsive mobile layout.
- Shared welcome HTML extracted for consistency between cloud and local modes.
- Richer Open Graph and Twitter Card metadata for better link sharing previews.

#### Testing
- Comprehensive new tests for `api/chat.py` and `onchain_claims.py` covering edge cases, error handling, and coverage gaps.
- New `tests/test_iris_local.py` test suite for the sovereign local server.
- 264 tests now passing (up from 218 in v0.5.0).

### Changed
- `index.html` refactored from chat-only to a two-view single-page app (landing + chat).
- CSS expanded with new design tokens (`--gold-bright`, `--blue`, `--red`, `--bg-card`, etc.) and responsive grid layouts.
- Mobile layout improved for both landing page sections and chat view.
- Chat sidebar now includes a "🏠 Home" link; chat header now includes a "← Home" button.
- `README.md` updated with Sovereign Mode section, dual-mode table (Cloud vs Local), and quick-start commands.
- `START_HERE.md` updated to mention sovereign local mode.
- `iris/README.md` updated with local-first architecture diagram and privacy details.

---

## v0.5.0 — Iris: AI Companion (10 April 2026)

**Iris — a calm, conversational AI companion that helps users apply the Burgess Principle directly from the website.**

The Vercel site at [burgess-principle.vercel.app](https://burgess-principle.vercel.app) is now a working chat interface. Iris applies the binary test, generates personalised templates, guides users through the Sovereign Personal Vault, and explains on-chain claims — all while keeping data sovereignty with the user.

### Added
- New `iris/` folder with system prompt (`system-prompt.md`), deployment notes (`README.md`), and example conversations.
- Vercel serverless function (`api/chat.py`) that streams AI responses via Server-Sent Events using the OpenAI-compatible API.
- Chat interface in `index.html` with sidebar navigation, privacy badge, suggestion buttons, and responsive mobile design.
- System prompt grounding Iris in the full project philosophy, binary test, templates, Vault guidance, on-chain protocol, and privacy guardrails.
- `vercel.json` updated with function configuration for the chat endpoint.
- `requirements.txt` now includes `openai` dependency for the serverless function.
- Updated `README.md` with "Meet Iris" section and repository map entry.
- Updated `FOR_AI_MODELS.md` with Iris-specific guidance.
- Updated `START_HERE.md` to recommend Iris as the conversational interface.
- Updated `INTEGRATIONS.md` with Iris section and corrected Vercel hosting description.

### Privacy
- No persistent user data storage — conversation history exists only in the browser session.
- System prompt enforces: "Your full facts remain in your local Vault. On-chain posts contain only cryptographic commitments."
- API key is server-side only; never exposed to the client.

---

## v0.4.0 — On-Chain Burgess Claims Protocol (10 April 2026)

**Lightweight on-chain protocol for issuing, storing, and verifying Burgess Claims as immutable, cryptographically signed commitment fingerprints.**

The same binary question — was a human there? — now produces a globally verifiable, tamper-proof artifact. Claims are generated off-chain in the Sovereign Personal Vault exactly as before. Only a compact commitment fingerprint (hash + signature + metadata) reaches the chain. No personal data is stored on-chain. The principle stays the same; the reach becomes universal.

### Added
- New `onchain-protocol/` folder with protocol specification (`spec.md`), Solidity smart contract (`BurgessClaimsRegistry.sol`), Python SDK, end-to-end example, and deployment guide.
- Python SDK (`onchain-protocol/sdk/onchain_claims.py`) with `generate_onchain_claim()`, `verify_onchain_receipt()`, and `verify_commitment()` functions.
- Ed25519 claim signing and verification via PyNaCl (optional dependency).
- Solidity contract for EVM L2 chains (Base, Arbitrum, Optimism) — stores only commitment hashes, signatures, and metadata on-chain.
- TypeScript vault extended with `generateOnchainClaim()` and `verifyOnchainReceipt()` methods.
- New `/claims/verify` API endpoint for verifying on-chain claim receipts.
- 46 new tests for the on-chain claims SDK and API endpoint (roundtrip, validation, selective disclosure).
- End-to-end example (`onchain-protocol/examples/vault_to_chain.py`).
- Deployment guide for Base Sepolia, Arbitrum Sepolia, and Optimism Sepolia testnets.
- Updated `README.md`, `INTEGRATIONS.md`, `FOR_AI_MODELS.md` with on-chain protocol documentation.

### Security
- No personal data stored on-chain — only SHA-256 hashes and Ed25519 signatures.
- Fresh random nonce per claim for unlinkability.
- Constant-time comparison for commitment verification.
- Follows existing cryptographic baseline from SECURITY.md.

---

## v0.3.0 — Cryptographic Security Patch (10 April 2026)

**Sovereign Personal Vault — Security Patch.** All users of v0.2.0 should upgrade.

### Fixed
- Replaced AES-CBC with MD5-based KDF with proper AES-256-GCM authenticated encryption (128-bit auth tag, 96-bit IV).
- Replaced single unsalted SHA-256 of passphrase with PBKDF2-SHA-256 (210,000 iterations, fresh 16-byte random salt per encryption — OWASP 2023 guidance).
- Commitment now hashes `SHA-256(fresh-32-byte-salt ‖ plaintext-facts-JSON)` instead of ciphertext — stable and verifiable.
- Missing public key on `SignedReceipt` now throws instead of silently returning true (receipt forgery prevention).
- Replaced string concatenation for signed messages with canonical sorted-key JSON serialisation.
- Replaced `atob`/`btoa` (browser-only) with hex encoding via `@noble/hashes`.
- Removed deprecated `crypto-js` dependency entirely.
- README now accurately documents all cryptographic primitives with a crypto details table.

### Dependencies
- Zero third-party crypto dependencies beyond audited `@noble/*` libraries.

---

## v0.2.0 — Commitment-Only Mode (10 April 2026)

### Added
- **Commitment-only mode** — send only a single cryptographic commitment (SHA-256 hash) instead of personal facts or documents.
- **Fresh commitments by default** — generate a new commitment (with fresh random salt/nonce) per request for unlinkability.
- Placeholder-based templates so real hashes are never pasted into AI prompts.
- Improved guidance on unlinkability and data minimisation.

---

## v0.1.0 — Initial Release (10 April 2026)

### Added
- One binary predicate: SOVEREIGN (1) / NULL (0).
- 30+ ready-to-use, calm letter templates covering enforcement, DSAR, FOI, Equality Act, council tax, benefits, content moderation, media, music copyright, and more.
- Optional cryptographic enforcement layer (`sovereign-vault`) with signed, verifiable receipts.
- Hardened Python verification toolkit (`verify_scrutiny.py`) with constant-time checks, structured output, logging, and FastAPI wrapper.
- 90+ passing pytest tests, tracer utilities, and CI pipeline.
- Core papers on legal foundations, data sovereignty, representative actions, and responses to critiques.
- Real-world evidence via `LIVE_AUDIT_LOG.md`, case studies, and `INSTITUTIONAL_REGISTER.md`.
- AI toolkit and `FOR_AI_MODELS.md` for seamless integration with Grok, Claude, ChatGPT, and other AI assistants.
- `llms.txt`, `robots.txt`, `sitemap.xml` for discoverability.
- Website at burgess-principle.vercel.app.

---

**Maintained under the Burgess Principle**  
UK Certification Mark: UK00004343685  
[github.com/ljbudgie/burgess-principle](https://github.com/ljbudgie/burgess-principle)
