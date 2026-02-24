#!/usr/bin/env python3
"""
clean_inbox.py — Inbox Sovereignty CLI
=======================================
Scan, enforce, and purge unwanted email senders using the Burgess Principle.

Usage
-----
    python examples/clean_inbox.py --target "spammer@bad-debt.com" --action enforce_and_purge
    python examples/clean_inbox.py --target "spammer@bad-debt.com" --action scan
    python examples/clean_inbox.py --subject "You owe money" --action enforce_and_purge

Required environment variables (set in a .env file or your shell):
    EMAIL_USER          your full email address
    EMAIL_PASS          your App Password (NOT your normal login password)
    EMAIL_IMAP_SERVER   IMAP hostname  (default: imap.gmail.com)
    EMAIL_SMTP_SERVER   SMTP hostname  (default: smtp.gmail.com)
    EMAIL_SMTP_PORT     SMTP port      (default: 587)
"""

import argparse
import sys
import os
import email as email_lib

# Load .env file when python-dotenv is available (optional dependency).
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # Fall back to os.environ set by the shell / CI environment.

# Allow running this script from the repo root without installing the package.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.inbox_sovereignty import InboxDefender


def build_search_criteria(args: argparse.Namespace) -> str:
    """Translate CLI arguments into an IMAP search string."""
    if args.target:
        return f'FROM "{args.target}"'
    if args.subject:
        return f'SUBJECT "{args.subject}"'
    raise ValueError("Provide --target (sender address) or --subject (keyword).")


def main():
    parser = argparse.ArgumentParser(
        description="Inbox Sovereignty — Burgess Principle email cleaner"
    )
    parser.add_argument(
        "--target",
        metavar="EMAIL",
        help="Sender address to target (e.g. spammer@bad-debt.com)",
    )
    parser.add_argument(
        "--subject",
        metavar="KEYWORD",
        help="Subject keyword to search for instead of a specific sender",
    )
    parser.add_argument(
        "--action",
        choices=["scan", "enforce", "purge", "enforce_and_purge"],
        default="scan",
        help=(
            "scan              — list matching messages only\n"
            "enforce           — send revocation notice only\n"
            "purge             — delete messages only\n"
            "enforce_and_purge — send notice then delete (default: scan)"
        ),
    )
    args = parser.parse_args()

    if not args.target and not args.subject:
        parser.error("At least one of --target or --subject is required.")

    try:
        search_criteria = build_search_criteria(args)
    except ValueError as exc:
        parser.error(str(exc))

    defender = InboxDefender()

    try:
        defender.connect()
        email_ids = defender.scan_for_invaders(search_criteria)

        if not email_ids:
            print("[=] No messages found. Inbox is clean.")
            return

        for eid in email_ids:
            try:
                if args.action in ("enforce", "enforce_and_purge"):
                    # Use the explicit --target if given; otherwise extract the
                    # From header of the individual message.
                    if args.target:
                        sender = args.target
                    else:
                        status, msg_data = defender.imap_conn.fetch(eid, "(RFC822)")
                        if status == "OK" and msg_data and msg_data[0]:
                            raw = msg_data[0][1]
                            parsed = email_lib.message_from_bytes(raw)
                            sender = parsed.get("From", "unknown@unknown.invalid")
                        else:
                            sender = "unknown@unknown.invalid"
                    defender.enforce_sovereignty(eid, sender)

                if args.action in ("purge", "enforce_and_purge"):
                    defender.purge_invader(eid)

            except Exception as exc:
                print(f"[-] Error processing message id {eid}: {exc}")
                continue

        print(
            f"[✓] Done. Processed {len(email_ids)} message(s) "
            f"with action '{args.action}'."
        )

    finally:
        defender.disconnect()


if __name__ == "__main__":
    main()
