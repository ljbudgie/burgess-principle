"""Hunter Scan: monitors repository events via the GitHub API."""

import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone


def run_scan():
    token = os.environ.get("GITHUB_TOKEN")
    url = "https://api.github.com/repos/ljbudgie/Burgessprinciple/events"

    req = urllib.request.Request(url)
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("X-GitHub-Api-Version", "2022-11-28")
    if token:
        req.add_header("Authorization", f"Bearer {token}")

    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode())
    except urllib.error.HTTPError as exc:
        print(
            f"[Hunter Scan] ERROR: HTTP {exc.code} when fetching events — {exc.reason}",
            file=sys.stderr,
        )
        sys.exit(1)
    except urllib.error.URLError as exc:
        print(f"[Hunter Scan] ERROR: network error fetching events — {exc.reason}", file=sys.stderr)
        sys.exit(1)

    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    count = len(data)

    if count > 0:
        latest = data[0]
        latest_type = latest.get("type", "unknown")
        latest_ts = latest.get("created_at", "unknown")
        print(
            f"[Hunter Scan] {now} — scan successful. "
            f"Events fetched: {count}. "
            f"Most recent event: type={latest_type}, timestamp={latest_ts}."
        )
    else:
        print(
            f"[Hunter Scan] {now} — scan successful. "
            f"Events fetched: 0. No recent events found."
        )


if __name__ == "__main__":
    run_scan()
