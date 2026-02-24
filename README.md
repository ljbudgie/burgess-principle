# The Burgess Principle

**A citizen-initiated legal doctrine — free and open for anyone to cite.**

## What It Is

The Burgess Principle establishes that facially defective warrants under the **Rights of Entry (Gas and Electricity Boards) Act 1954** are void *ab initio*, with downstream remedies for credit contamination and reasonable adjustments for protected characteristics.

## Open Source

The principle itself is **free and may be cited by anyone**. The goal is maximum truth reaching maximum people.

## Methodology & Toolkit — Open Source

The methodology and toolkit are **fully open source**, licensed under the [MIT License](LICENSE). Free for anyone to use, adapt, and build upon.

Integrated with [OpenClaw](https://openclaw.im) — the open-source AI automation platform for law.

## Live Site

[https://ljbudgie.github.io/Burgessprinciple/](https://ljbudgie.github.io/Burgessprinciple/)

## Auto-Pilot — Always Watching

The system now runs on an **hourly schedule** via GitHub Actions, effectively operating as a **24/7 Surveillance** mode. No longer limited to once a day — it is constantly active, scanning every hour around the clock.

> "What's stopping you from going 24/7?" — Nothing.

## Inbox Sovereignty

The **Inbox Sovereignty** module extends the Burgess Principle to your email inbox, letting you scan for "invaders" (data brokers, debt collectors, spammers), send them an automatic legal Notice of Revocation / GDPR Article 17 demand, and permanently purge their messages.

### Setup

**1. Install dependencies**

```bash
pip install -r requirements.txt
```

**2. Create a `.env` file** in the repository root (never commit this file):

```dotenv
EMAIL_USER=[REDACTED-EMAIL]
EMAIL_PASS=xxxx xxxx xxxx xxxx   # App Password — see below
EMAIL_IMAP_SERVER=imap.gmail.com
EMAIL_SMTP_SERVER=smtp.gmail.com
EMAIL_SMTP_PORT=587
```

> ⚠️ **Use an App Password, not your normal login password.**
>
> * **Gmail:** Google Account → Security → 2-Step Verification → App Passwords.  Generate one for "Mail / Windows Computer" (or any label you choose).
> * **Outlook / Hotmail:** Microsoft Account → Security → Advanced security options → App passwords.
> * **Other providers:** Consult your provider's documentation for IMAP app passwords or device-specific passwords.
>
> Your real password is never stored or transmitted by this script — only the App Password you generate.

**3. Add `.env` to `.gitignore`** (if not already present):

```bash
echo ".env" >> .gitignore
```

### Usage

```bash
# Scan only — list matching messages without taking action
python examples/clean_inbox.py --target "spammer@bad-debt.com" --action scan

# Send a revocation notice only
python examples/clean_inbox.py --target "spammer@bad-debt.com" --action enforce

# Delete matching messages only
python examples/clean_inbox.py --target "spammer@bad-debt.com" --action purge

# Send notice AND delete (full enforcement)
python examples/clean_inbox.py --target "spammer@bad-debt.com" --action enforce_and_purge

# Target by subject keyword instead of sender
python examples/clean_inbox.py --subject "final demand" --action enforce_and_purge
```

The revocation notice sent to the invader reads:

> *"NOTICE OF REVOCATION AND GDPR DEMAND. I hereby revoke all consent for you to contact this address. Under GDPR Article 17 (Right to Erasure) and the Burgess Principle, I demand you immediately cease all communication, delete all personal data you hold relating to this address, and confirm compliance in writing within 30 days."*

All credentials remain on your local machine — the script runs entirely in your own environment.

## Contact

For media enquiries: [lewis@burgessprinciple.co.uk](mailto:lewis@burgessprinciple.co.uk)

## Legal

&copy; 2026 Lewis Burgess. Licensed under the [MIT License](LICENSE).  
Registered trademark application UK00004343685
