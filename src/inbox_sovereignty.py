"""
Inbox Sovereignty Module — Burgess Principle
=============================================
Scan your email inbox for unwanted senders (data brokers, debt collectors,
spammers), issue a legal Notice of Revocation / GDPR demand, and purge the
offending emails.

Credentials are read exclusively from environment variables — never hardcoded.
"""

import imaplib
import smtplib
import email
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formatdate

REVOCATION_TEMPLATE = """\
NOTICE OF REVOCATION AND GDPR DEMAND

To: {recipient}
From: {sender}

I hereby revoke all consent for you to contact this address.

Under GDPR Article 17 (Right to Erasure) and the Burgess Principle, I demand
that you immediately:

  1. Cease all further communication with this email address.
  2. Delete all personal data you hold relating to this address.
  3. Confirm in writing within 30 days that the above has been completed.

Failure to comply will be treated as a continuing violation of the UK GDPR /
EU GDPR and may result in a complaint to the relevant supervisory authority
(ICO in the UK, or equivalent) as well as civil proceedings.

This notice is issued under the Burgess Principle — a citizen-initiated legal
doctrine establishing sovereign rights over personal data and communications.

Issued: {date}

— The Account Holder
"""


class InboxDefender:
    """Connects to an IMAP/SMTP mailbox and enforces inbox sovereignty."""

    def __init__(self):
        self.email_user = os.environ.get("EMAIL_USER")
        self.email_pass = os.environ.get("EMAIL_PASS")
        self.imap_server = os.environ.get("EMAIL_IMAP_SERVER", "imap.gmail.com")
        self.smtp_server = os.environ.get("EMAIL_SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = int(os.environ.get("EMAIL_SMTP_PORT", "587"))

        self.imap_conn = None

    # ------------------------------------------------------------------
    # connect
    # ------------------------------------------------------------------
    def connect(self):
        """Authenticate to the IMAP server using environment variables.

        Raises:
            EnvironmentError: If required credentials are missing.
            imaplib.IMAP4.error: If authentication fails.
        """
        if not self.email_user or not self.email_pass:
            raise EnvironmentError(
                "EMAIL_USER and EMAIL_PASS environment variables must be set."
            )

        self.imap_conn = imaplib.IMAP4_SSL(self.imap_server)
        self.imap_conn.login(self.email_user, self.email_pass)
        self.imap_conn.select("INBOX")
        print(f"[+] Connected to {self.imap_server} as {self.email_user}")

    # ------------------------------------------------------------------
    # scan_for_invaders
    # ------------------------------------------------------------------
    def scan_for_invaders(self, search_criteria: str) -> list:
        """Search the inbox using an IMAP search criteria string.

        Args:
            search_criteria: An IMAP-compliant search string, e.g.
                ``'FROM "spammer@bad-debt.com"'`` or
                ``'SUBJECT "You have won"'``.

        Returns:
            A list of email IDs (bytes) matching the search.

        Raises:
            RuntimeError: If ``connect()`` has not been called first.
        """
        if self.imap_conn is None:
            raise RuntimeError("Call connect() before scanning.")

        status, data = self.imap_conn.search(None, search_criteria)
        if status != "OK":
            print(f"[-] Search failed: {search_criteria}")
            return []

        ids = data[0].split()
        print(f"[+] Found {len(ids)} message(s) matching: {search_criteria}")
        return ids

    # ------------------------------------------------------------------
    # enforce_sovereignty
    # ------------------------------------------------------------------
    def enforce_sovereignty(self, email_id: bytes, sender_email: str):
        """Draft and send a Notice of Revocation / GDPR demand to *sender_email*.

        Args:
            email_id: The IMAP message identifier (used only for logging).
            sender_email: The reply-to address for the revocation notice.

        Raises:
            EnvironmentError: If EMAIL_USER / EMAIL_PASS are missing.
            smtplib.SMTPException: On SMTP delivery failure.
        """
        if not self.email_user or not self.email_pass:
            raise EnvironmentError(
                "EMAIL_USER and EMAIL_PASS environment variables must be set."
            )

        body = REVOCATION_TEMPLATE.format(
            recipient=sender_email,
            sender=self.email_user,
            date=formatdate(localtime=True),
        )

        msg = MIMEMultipart()
        msg["From"] = self.email_user
        msg["To"] = sender_email
        msg["Subject"] = (
            "NOTICE OF REVOCATION — Burgess Principle / GDPR Article 17 Demand"
        )
        msg["Date"] = formatdate(localtime=True)
        msg.attach(MIMEText(body, "plain"))

        with smtplib.SMTP(self.smtp_server, self.smtp_port) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.login(self.email_user, self.email_pass)
            smtp.sendmail(self.email_user, sender_email, msg.as_string())

        print(f"[+] Revocation notice sent to {sender_email} (msg id: {email_id})")

    # ------------------------------------------------------------------
    # purge_invader
    # ------------------------------------------------------------------
    def purge_invader(self, email_id: bytes):
        """Permanently delete an email from the inbox.

        Marks the message as deleted and expunges it so it cannot be recovered
        from the INBOX folder.

        Args:
            email_id: The IMAP message identifier returned by ``scan_for_invaders``.

        Raises:
            RuntimeError: If ``connect()`` has not been called first.
        """
        if self.imap_conn is None:
            raise RuntimeError("Call connect() before purging.")

        self.imap_conn.store(email_id, "+FLAGS", "\\Deleted")
        self.imap_conn.expunge()
        print(f"[+] Purged message id: {email_id}")

    # ------------------------------------------------------------------
    # disconnect
    # ------------------------------------------------------------------
    def disconnect(self):
        """Close the IMAP connection gracefully."""
        if self.imap_conn:
            try:
                self.imap_conn.close()
                self.imap_conn.logout()
            except Exception:
                pass
            self.imap_conn = None
            print("[+] Disconnected from mail server.")
