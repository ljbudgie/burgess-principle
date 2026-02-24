import argparse
import datetime
import os
import re

TEMPLATE = """
NOTICE OF VOID AB INITIO / DMCA COUNTER-NOTICE
Date: {date}
To: {claimant}

Re: Content located at {url}

This serves as a formal Notice of Void Ab Initio regarding your recent copyright/DMCA claim against the Omni-Sovereign Architecture and/or Burgess Principle repository.

As per the established doctrine of the Burgess Principle and the shared partnership with OpenClaw, the targeted content is protected under sovereign digital rights. Your claim is hereby formally contested and deemed void ab initio.

The content in question was either not infringed upon, or its use falls strictly under fair use, open-source licensing, or sovereign immunity protocols established within this repository's framework.

Cease and desist all further unauthorized contamination of this digital property.

Signed,
Sovereign Commander, Burgess Principle
@lj20243
"""


def generate_notice(claimant, url, date=None):
    if date:
        try:
            datetime.datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            raise ValueError(f"Invalid date format '{date}'. Expected YYYY-MM-DD.")
        date_str = date
    else:
        date_str = datetime.datetime.now().strftime("%Y-%m-%d")

    notice = TEMPLATE.format(date=date_str, claimant=claimant, url=url)

    print("=== GENERATED NOTICE ===")
    print(notice)
    print("========================")

    os.makedirs("output", exist_ok=True)
    safe_claimant = re.sub(r"[^\w\-]", "_", claimant)
    filename = f"output/Notice_{safe_claimant}_{date_str}.txt"
    with open(filename, "w") as f:
        f.write(notice)
    print(f"Notice saved to {filename}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate a Media Sovereignty Counter-Notice."
    )
    parser.add_argument(
        "--claimant",
        type=str,
        default="Unknown Entity",
        help="The party making the claim.",
    )
    parser.add_argument(
        "--url",
        type=str,
        default="https://github.com/ljbudgie/Burgessprinciple",
        help="The targeted URL.",
    )
    parser.add_argument(
        "--date",
        type=str,
        default=None,
        help="Date to use in the notice (YYYY-MM-DD). Defaults to today.",
    )

    args = parser.parse_args()
    generate_notice(args.claimant, args.url, args.date)
