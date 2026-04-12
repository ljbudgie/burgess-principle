# Start Here

Welcome 👋

If you're feeling stressed, overwhelmed, or unseen by a system — you're in the right place.

If you want one canonical entry point first, start with [`CHOOSE_YOUR_PATH.md`](./CHOOSE_YOUR_PATH.md).

> **Need help right now?** Talk to **[Iris](https://burgess-principle.vercel.app)**, the AI companion for the Burgess Principle — or pick a [template](./templates) that matches your situation and send it today. On a phone in Sovereign Mode, tap **+ New Claim** to jump straight into the mobile claim builder, voice capture, encrypted phone vault flow, and optional **Mirror Mode** identity layer. You don't need to read anything else first. You can also clone the repo and drop it into [Grok](https://grok.com), [Claude](https://claude.ai), [ChatGPT](https://chat.openai.com), or any AI assistant — describe what happened and it will write a personalised letter for you.

The Burgess Principle gives you **one calm question** to ask any institution:

> **"Was a human member of the team able to personally review the specific facts of my situation?"**

That's it. No legal training. No confrontation. Just a clear, written record that speaks for itself.

You can also explore the principle on the website and talk to **Iris**, the AI companion: **[burgess-principle.vercel.app](https://burgess-principle.vercel.app)**

> 🛡️ **Iris keeps everything on your hardware by default — sovereign by design.** Your conversations stay in your browser. Nothing is stored on any server unless you explicitly send a message.

> 📱 **Phone-first workflow:** install the PWA from your local Sovereign Mode session, save your claim profile once, optionally enable Mirror Mode in **Claim profile & phone settings**, then generate, sign, save, export, and restore Burgess Claims entirely from the phone.

---

## Non-technical quick start

1. **Need help immediately?** Start with the hosted PWA: [burgess-principle.vercel.app](https://burgess-principle.vercel.app).
2. **Want full offline privacy later?** Run one of the install scripts in `scripts/`, then optionally run `python3 setup-wizard.py` for a guided local setup.
3. **Choose the small starter model first.** Phi-3 Mini is the easiest local starting point on ordinary laptops.
4. **If downloads are slow, RAM is tight, or antivirus interrupts setup, do not force it.** Check the troubleshooting notes in [SOVEREIGN_MODE.md](SOVEREIGN_MODE.md) and come back calmly.
5. **If an institution replies with vague wording instead of a straight answer, use the dedicated follow-up template**: [`templates/FOLLOW_UP_WEASEL_RESPONSE.md`](templates/FOLLOW_UP_WEASEL_RESPONSE.md).
6. **After your first local setup, export one Backup Bundle** so your profile, vault, Memory Palace state, receipts, and hub settings can be restored on another device.

---

## What do I do first?

### 1. I need to write a letter right now

Head to the [`/templates`](./templates) folder. Pick the one that matches your situation:

- **[General request for human review](templates/REQUEST_FOR_HUMAN_REVIEW.md)** — works for almost anything
- **[Follow-up after a vague "human oversight" reply](templates/FOLLOW_UP_WEASEL_RESPONSE.md)** — use when they still avoid a direct YES/NO answer
- **[General dispute with any organisation](templates/GENERAL_DISPUTE_WITH_BURGESS_PRINCIPLE.md)** — universal dispute letter
- **[Council tax or penalty charge](templates/COUNCIL_TAX_PCN_TEMPLATE.md)**
- **[Benefits claim dispute](templates/BENEFITS_CLAIM_HELP.md)**
- **[Bailiff threat](templates/BAILIFFS_THREAT_TEMPLATE.md)**
- **[Data subject access request (DSAR)](templates/DSAR_WITH_BURGESS_PRINCIPLE.md)**
- **[Freedom of Information request](templates/FOI_WITH_BURGESS_PRINCIPLE.md)**
- **[Automated decision challenge (Article 22)](templates/ARTICLE_22_WITH_BURGESS_PRINCIPLE.md)**
- **[Equality Act / disability adjustments](templates/EQUALITY_ACT_WITH_BURGESS_PRINCIPLE.md)**
- **[Crypto exchange freeze / withdrawal hold](templates/CRYPTO_EXCHANGE_ACCOUNT_RESTRICTION_WITH_BURGESS.md)**
- **[Cryptographic proof / on-chain notice](templates/CRYPTOGRAPHIC_PROOF_AND_ONCHAIN_NOTICE_WITH_BURGESS.md)**

Not sure which one? Start with the **[templates index](templates/README.md)** or the **[Common Scenarios guide](templates/COMMON_SCENARIOS.md)** for a quick comparison, or drop the whole repo into [Grok](https://grok.com), [Claude](https://claude.ai), [ChatGPT](https://chat.openai.com), or any AI assistant and describe your situation — it will pick the right template for you.

### 2. I want to see real results first

The [case studies index](./case-studies/README.md) shows the principle in action and tells you which template or workflow matches each case:

- **[Wave Utilities](case-studies/CASE_STUDY_WAVE.md)** — both accounts resolved to £0.00 after a single human review
- **[Passport Office](case-studies/CASE_STUDY_PASSPORT.md)** — Article 22 challenge to automated passport issuance
- **[E.ON Next](case-studies/CASE_STUDY_EON.md)** — forced entry under unsigned warrant challenged
- **[Equita](case-studies/CASE_STUDY_EQUITA.md)** — five enforcement cases with disability gatekeeping
- **[Equifax](case-studies/CASE_STUDY_CREDIT_FILE.md)** — credit file entries registered without individual verification

### 3. I want to understand the idea first

- Read the [README](README.md) — it explains the origin story, how the principle works, and real-world results.
- Read [SOUL.md](SOUL.md) — it explains the deeper philosophy behind the framework and why it exists.

### 4. I want step-by-step guidance

Check out the [tutorials](./tutorials) folder for walkthroughs — including how to challenge any institutional action in five steps, how to file a Subject Access Request, and how to assert a reasonable adjustment.

### 5. I want to go deeper

These resources are for people who want to explore the framework, doctrine, and strategy behind the principle:

| Resource | What's inside |
| --- | --- |
| [`/papers`](./papers) | Foundational papers, doctrine archive, and licensing notes — see the folder guide for what is current vs publication-era wording |
| [`LIVE_AUDIT_LOG.md`](LIVE_AUDIT_LOG.md) | Chronological record of every institutional interaction and finding |
| [`INSTITUTIONAL_REGISTER.md`](INSTITUTIONAL_REGISTER.md) | Every institution tested, with sector, response, and SOVEREIGN/NULL finding |
| [`/case-studies`](./case-studies/README.md) | Indexed real-world examples, current findings, and recommended starting points |
| [`/enforcement`](./enforcement) | Optional cryptographic enforcement tools (Sovereign Personal Vault) |
| [`/onchain-protocol`](./onchain-protocol) | On-chain Burgess Claims — post commitment fingerprints to an EVM L2 for public verifiability (v0.4.0) |
| [`/toolkit`](./toolkit) | AI integration and knowledge base |
| [`/marketing`](./marketing) | Commercial strategy, user stories, and outreach |

### 6. I want cryptographic proof or on-chain verification

The [Sovereign Personal Vault](enforcement/sovereign-vault/) lets you generate commitments and signed receipts entirely on your own device. As of v0.4.0, you can also post a compact commitment fingerprint (hash + signature, no personal data) to an EVM L2 for neutral timestamping and public verifiability. The binary test — SOVEREIGN or NULL — stays the same; the on-chain layer simply makes it globally auditable. See [onchain-protocol/spec.md](onchain-protocol/spec.md) for the protocol and [CHANGELOG.md](CHANGELOG.md) for details.

---

## You don't need to read everything

If you're here because something happened to you, start with a template. That's what they're for.

Take care.
