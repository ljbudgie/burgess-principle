"""
tracer.py — The Tracer Protocol (Module 03)
============================================
Part of The Burgess Principle: Omni-Sovereign Architecture
Phase 2 Tracer Protocol Upgrade (Grok Co-Developed)

Purpose:
    Hunt publicly available warrant documentation for known facial defects
    as catalogued in DEFECT_SCHEMA.md. Returns a structured defect report
    for each document URL supplied.

Defect categories (see DEFECT_SCHEMA.md for full definitions):
    1. BULK_APPROVAL   — Bulk approval without individual judicial scrutiny.
    2. RUBBER_STAMP    — Reliance on supplier affidavits without independent
                         verification.
    3. PROCEDURAL      — False safety claims or incomplete address data.
    4. DOWNSTREAM_TAINT — Defects that cascade to credit agencies or billing
                          systems.

Usage:
    python tracer.py --urls <url1> [<url2> ...]
    python tracer.py --file  urls.txt          # one URL per line

Requirements:
    pip install requests beautifulsoup4 lxml
"""

import argparse
import json
import re
import sys
from dataclasses import dataclass, field, asdict
from typing import List, Optional

import requests
from bs4 import BeautifulSoup

# ---------------------------------------------------------------------------
# Defect signature patterns
# Each pattern is a compiled regex matched against normalised page text.
# ---------------------------------------------------------------------------

DEFECT_SIGNATURES = {
    "BULK_APPROVAL": [
        re.compile(r"\bbulk\b.{0,40}\b(warrant|application|process)", re.I),
        re.compile(r"\bbundle[sd]?\b.{0,40}\bwarrant", re.I),
        re.compile(r"\bbatch(ed|ing)?\b.{0,40}\bwarrant", re.I),
        re.compile(r"\b\d{2,}\s+warrants?\b.{0,40}\b(minut|second)", re.I),
        re.compile(r"without\s+individual\s+judicial", re.I),
        re.compile(r"rubber[\s-]stamp", re.I),          # overlaps — intentional
    ],
    "RUBBER_STAMP": [
        re.compile(r"rubber[\s-]stamp", re.I),
        re.compile(r"\baffidavit\b.{0,60}\bwithout\b.{0,30}\bverif", re.I),
        re.compile(r"supplier.{0,40}(declaration|affidavit).{0,40}accept", re.I),
        re.compile(r"no\s+independent\s+verif", re.I),
        re.compile(r"taken\s+on\s+(trust|face\s+value)", re.I),
    ],
    "PROCEDURAL": [
        re.compile(r"(incorrect|wrong|false|incomplete)\s+(address|postcode)", re.I),
        re.compile(r"safety\s+(risk|hazard).{0,40}(false|fabricat|unfound)", re.I),
        re.compile(r"\bgas\s+escape\b.{0,60}\bunsubstantiat", re.I),
        re.compile(r"address.{0,20}(mismatch|missing|blank|omit)", re.I),
        re.compile(r"(sworn|stated).{0,40}(incorrect|false|mislead)", re.I),
    ],
    "DOWNSTREAM_TAINT": [
        re.compile(r"(credit|cra|equifax|experian|transunion).{0,60}\bdefect", re.I),
        re.compile(r"default.{0,40}(tainted|invalid|void)", re.I),
        re.compile(r"(billing|invoice|account).{0,60}(bulk|batch).{0,40}(error|defect|wrong)", re.I),
        re.compile(r"(ccj|county\s+court\s+judgment).{0,60}(void|nullity|invalid)", re.I),
        re.compile(r"cascad\w*.{0,30}(defect|error|taint)", re.I),
        re.compile(r"(defect|error|taint).{0,30}cascad", re.I),
    ],
}

# HTTP request timeout in seconds
REQUEST_TIMEOUT = 15

# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

@dataclass
class DefectHit:
    """A single pattern match found in a document."""
    category: str
    pattern: str
    excerpt: str            # surrounding text (up to 200 chars)


@dataclass
class TracerReport:
    """Full defect report for one URL."""
    url: str
    status: str             # "ok", "http_error", "connection_error", "parse_error"
    http_code: Optional[int] = None
    title: Optional[str] = None
    hits: List[DefectHit] = field(default_factory=list)
    defect_flags: List[str] = field(default_factory=list)   # unique categories triggered
    summary: str = ""


# ---------------------------------------------------------------------------
# Core scanning logic
# ---------------------------------------------------------------------------

def fetch_page(url: str) -> tuple:
    """
    Fetch the page at *url*.

    Returns (status, http_code, html_text).
    status is one of "ok", "http_error", "connection_error".
    """
    try:
        resp = requests.get(url, timeout=REQUEST_TIMEOUT, headers={
            "User-Agent": (
                "TracerProtocol/2.0 (Burgess Principle Defect Scanner; "
                "https://github.com/ljbudgie/Burgessprinciple)"
            )
        })
        if resp.ok:
            return "ok", resp.status_code, resp.text
        return "http_error", resp.status_code, resp.text
    except requests.RequestException as exc:
        return "connection_error", None, str(exc)


def extract_text(html: str) -> tuple:
    """
    Parse *html* with BeautifulSoup and return (page_title, plain_text).
    Strips script / style noise before extracting text.
    """
    try:
        soup = BeautifulSoup(html, "lxml")
    except Exception:
        soup = BeautifulSoup(html, "html.parser")

    # Remove non-content tags
    for tag in soup(["script", "style", "noscript", "head"]):
        tag.decompose()

    title = soup.title.string.strip() if soup.title and soup.title.string else ""
    text = " ".join(soup.get_text(separator=" ").split())   # collapse whitespace
    return title, text


def _get_excerpt(text: str, match: re.Match, window: int = 100) -> str:
    """Return *window* characters either side of a regex *match* in *text*."""
    start = max(0, match.start() - window)
    end = min(len(text), match.end() + window)
    excerpt = text[start:end]
    if start > 0:
        excerpt = "…" + excerpt
    if end < len(text):
        excerpt = excerpt + "…"
    return excerpt


def scan_text(text: str) -> List[DefectHit]:
    """
    Run all defect signatures against *text* and return every hit found.
    Duplicate pattern hits within the same category are deduplicated.
    """
    hits: List[DefectHit] = []
    seen: set = set()

    for category, patterns in DEFECT_SIGNATURES.items():
        for pattern in patterns:
            for match in pattern.finditer(text):
                key = (category, pattern.pattern, match.start())
                if key not in seen:
                    seen.add(key)
                    hits.append(DefectHit(
                        category=category,
                        pattern=pattern.pattern,
                        excerpt=_get_excerpt(text, match),
                    ))
    return hits


def build_summary(hits: List[DefectHit]) -> str:
    """Produce a human-readable one-line summary of defects found."""
    if not hits:
        return "No defects detected."
    flags = sorted({h.category for h in hits})
    return f"Defects detected — categories: {', '.join(flags)} ({len(hits)} hit(s) total)."


def trace_url(url: str) -> TracerReport:
    """Full pipeline: fetch → parse → scan → report."""
    report = TracerReport(url=url, status="ok")

    status, code, body = fetch_page(url)
    report.http_code = code

    if status != "ok":
        report.status = status
        report.summary = f"Could not retrieve page: {status} (code={code})."
        return report

    try:
        title, text = extract_text(body)
    except Exception as exc:
        report.status = "parse_error"
        report.summary = f"HTML parse failed: {exc}"
        return report

    report.title = title
    report.hits = scan_text(text)
    report.defect_flags = sorted({h.category for h in report.hits})
    report.summary = build_summary(report.hits)
    return report


# ---------------------------------------------------------------------------
# CLI entry-point
# ---------------------------------------------------------------------------

def _build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Tracer Protocol — Burgess Principle Phase 2\n"
            "Scans documents for warrant facial-defect signatures."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument(
        "--urls", nargs="+", metavar="URL",
        help="One or more URLs to scan.",
    )
    source.add_argument(
        "--file", metavar="FILE",
        help="Path to a text file containing one URL per line.",
    )
    parser.add_argument(
        "--output", choices=["text", "json"], default="text",
        help="Output format (default: text).",
    )
    return parser


def _load_urls_from_file(path: str) -> List[str]:
    with open(path, encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]


def _print_text_report(report: TracerReport) -> None:
    print(f"\n{'=' * 70}")
    print(f"URL   : {report.url}")
    print(f"Status: {report.status}  (HTTP {report.http_code})")
    if report.title:
        print(f"Title : {report.title}")
    print(f"Result: {report.summary}")
    if report.hits:
        print(f"\nDefect hits ({len(report.hits)}):")
        for i, hit in enumerate(report.hits, 1):
            print(f"  [{i}] [{hit.category}] {hit.excerpt}")


def main(argv: Optional[List[str]] = None) -> int:
    parser = _build_arg_parser()
    args = parser.parse_args(argv)

    if args.file:
        urls = _load_urls_from_file(args.file)
    else:
        urls = args.urls

    reports = [trace_url(url) for url in urls]

    if args.output == "json":
        print(json.dumps([asdict(r) for r in reports], indent=2))
    else:
        for r in reports:
            _print_text_report(r)
        flagged = sum(1 for r in reports if r.defect_flags)
        print(f"\n{'=' * 70}")
        print(f"Tracer complete. {flagged}/{len(reports)} document(s) flagged.")

    return 0 if all(r.status == "ok" for r in reports) else 1


if __name__ == "__main__":
    sys.exit(main())
