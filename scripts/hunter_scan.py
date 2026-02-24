"""
hunter_scan.py — Automated surveillance scan for the Burgessprinciple repository.

Fetches recent GitHub events for the repository using the GitHub REST API and
logs the findings with a timestamp. Uses only the Python standard library so no
extra dependencies are required.
"""

import datetime
import json
import os
import sys
import urllib.error
import urllib.request


def run_scan():
    timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
    print(f"[{timestamp}] Initiating Hunter Surveillance Scan...")

    repo = "ljbudgie/Burgessprinciple"
    url = f"https://api.github.com/repos/{repo}/events"

    req = urllib.request.Request(url)
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("User-Agent", "Burgessprinciple-HunterScan/1.0")

    # Use GITHUB_TOKEN if available to raise the unauthenticated rate limit.
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        req.add_header("Authorization", f"token {token}")

    try:
        with urllib.request.urlopen(req) as response:
            if response.status == 200:
                data = json.loads(response.read().decode())
                print(
                    f"[{timestamp}] Scan successful. "
                    f"Found {len(data)} recent event(s)."
                )
                if data:
                    latest = data[0]
                    print(
                        f"[{timestamp}] Latest activity: "
                        f"{latest.get('type')} at {latest.get('created_at')}"
                    )
            else:
                print(
                    f"[{timestamp}] Warning: Unexpected status code "
                    f"{response.status}"
                )
    except urllib.error.HTTPError as e:
        print(f"[{timestamp}] CRITICAL ERROR: HTTP {e.code} — {e.reason}")
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"[{timestamp}] CRITICAL ERROR: Network error — {e.reason}")
        sys.exit(1)

    print(f"[{timestamp}] Hunter Surveillance Scan complete.")


if __name__ == "__main__":
    run_scan()
