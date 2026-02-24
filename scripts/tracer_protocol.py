"""
Tracer Protocol — Forensic Web Scanner
Part of the Omni-Sovereign Architecture
"""

import urllib.request
import urllib.error
from datetime import datetime, timezone

TARGET_URLS = [
    "https://github.com/ljbudgie/Burgessprinciple",
    "https://raw.githubusercontent.com/ljbudgie/Burgessprinciple/main/README.md",
    "https://raw.githubusercontent.com/ljbudgie/Burgessprinciple/main/LEGAL_DOCTRINE.md",
]

KEYWORDS = [
    "Burgess",
    "OpenClaw",
    "Void Ab Initio",
    "Sovereign",
]


def scan_url(url):
    """Fetch the content of a URL and return it as a string, or None on error."""
    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "TracerProtocol/1.0 (+https://github.com/ljbudgie/Burgessprinciple)"},
        )
        with urllib.request.urlopen(req, timeout=15) as response:
            return response.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as exc:
        print(f"  [ERROR] HTTP {exc.code} when accessing {url}")
    except urllib.error.URLError as exc:
        print(f"  [ERROR] Could not reach {url}: {exc.reason}")
    except Exception as exc:  # noqa: BLE001
        print(f"  [ERROR] Unexpected error for {url}: {exc}")
    return None


def run_tracer():
    timestamp = datetime.now(tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    print("=" * 60)
    print("  TRACER PROTOCOL — FORENSIC WEB SCANNER")
    print(f"  Scan initiated: {timestamp}")
    print("=" * 60)

    for url in TARGET_URLS:
        print(f"\n[TARGET] {url}")
        content = scan_url(url)

        if content is None:
            print("  [RESULT] Unreachable — skipped.")
            continue

        content_lower = content.lower()
        detected = [kw for kw in KEYWORDS if kw.lower() in content_lower]

        if detected:
            for kw in detected:
                print(f"  [DETECTED] '{kw}'")
        else:
            print("  [RESULT] No target keywords detected.")

    print("\n" + "=" * 60)
    print("  Scan complete.")
    print("=" * 60)


if __name__ == "__main__":
    run_tracer()
