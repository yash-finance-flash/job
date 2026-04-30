#!/usr/bin/env python3
"""Generate LinkedIn job-search links for the last 24 hours.

This script is intended for daily morning use. It builds LinkedIn search URLs
for requested roles and locations, limited to jobs posted in the last 24 hours.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote_plus

DEFAULT_ROLES = [
    "Data Engineer",
    "Full Stack Developer",
    "ML Engineer",
    "AI Engineer",
    "Backend Software Engineer",
]


def build_linkedin_url(role: str, location: str, max_jobs: int) -> str:
    """Return a LinkedIn jobs search URL.

    - f_TPR=r86400: posted in the last 24 hours
    - sortBy=DD: newest first
    - start=0 and position/pageNum are standard LinkedIn params
    """
    role_q = quote_plus(role)
    loc_q = quote_plus(location)
    return (
        "https://www.linkedin.com/jobs/search/"
        f"?keywords={role_q}"
        f"&location={loc_q}"
        "&f_TPR=r86400"
        "&sortBy=DD"
        "&position=1"
        "&pageNum=0"
        f"&count={max_jobs}"
    )


def parse_csv(value: str) -> list[str]:
    if value.strip().lower() == "all":
        return []
    return [item.strip() for item in value.split(",") if item.strip()]


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate daily LinkedIn links for jobs posted in last 24h"
    )
    parser.add_argument(
        "--roles",
        default="all",
        help="Comma-separated roles (or 'all' for default role list)",
    )
    parser.add_argument(
        "--locations",
        default="all",
        help="Comma-separated locations (or 'all' for broad location presets)",
    )
    parser.add_argument(
        "--max-jobs",
        type=int,
        default=50,
        help="Maximum jobs per LinkedIn query (recommended up to 50)",
    )
    parser.add_argument(
        "--output",
        default="job_links_last24h.json",
        help="Output JSON file",
    )

    args = parser.parse_args()

    roles = parse_csv(args.roles) or DEFAULT_ROLES
    locations = parse_csv(args.locations) or ["Remote", "United States"]

    max_jobs = max(1, min(args.max_jobs, 50))

    generated_at = datetime.now(timezone.utc).isoformat()
    links: list[dict[str, str]] = []

    for role in roles:
        for location in locations:
            links.append(
                {
                    "role": role,
                    "location": location,
                    "url": build_linkedin_url(role, location, max_jobs),
                }
            )

    payload = {
        "generated_at_utc": generated_at,
        "time_window": "last_24_hours",
        "max_jobs_per_search": max_jobs,
        "searches": links,
    }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    print(f"Generated {len(links)} LinkedIn search links")
    print(f"Saved to: {output_path.resolve()}")
    for item in links:
        print(f"- {item['role']} | {item['location']}: {item['url']}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
