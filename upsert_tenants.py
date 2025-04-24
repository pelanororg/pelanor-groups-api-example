#!/usr/bin/env python3
"""
Bulk-create or update tenant groups in Pelanor from a CSV file.

Prerequisites
-------------
1. `pip install python-dotenv requests`
2. Create a file named `.env` **next to this script** containing:
   PELANOR_API_TOKEN=<your-token-here>

Usage
-----
$ python bulk_upsert_tenants.py
"""

import csv
import os
from pathlib import Path

import requests
from dotenv import load_dotenv

# ─── Load API token ──────────────────────────────────────────────────────────
ENV_FILE = Path(__file__).with_suffix(".env")
load_dotenv(ENV_FILE)                     # falls back to normal .env lookup
API_TOKEN = os.getenv("PELANOR_API_TOKEN")
if not API_TOKEN:
    raise RuntimeError(
        "PELANOR_API_TOKEN is missing. "
        "Create a .env file with:\n"
        "PELANOR_API_TOKEN=<your-token-here>"
    )

# ─── Configuration ───────────────────────────────────────────────────────────
CSV_FILENAME      = "example_tenants.csv"
BASE_URL          = "https://api.pelanor.io"
GROUPS_ENDPOINT   = f"{BASE_URL}/v1/groups"
HEADERS = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json",
}

# ─── Helper ──────────────────────────────────────────────────────────────────
def upsert_tenant(name: str) -> None:
    """
    Create (or update) a `Tenants` group whose identifying tag /
    namespace / database equals *name* (case-adjusted as needed).
    """
    payload = {
        "dimension": "Tenants",
        "name": name.capitalize(),
        "request": {
            "cost_type": "Amortized",
            "filter_groups": [
                # Tag: tenant=<lowercase name>
                {
                    "filters": [
                        {
                            "operator": "Equals",
                            "property": {"Tag": "tenant"},
                            "values": [name.lower()],
                        }
                    ],
                    "add_used_by_filter": False,
                },
                # Kubernetes namespace equals <lowercase name>
                {
                    "filters": [
                        {
                            "operator": "Equals",
                            "property": {"K8sNamespace": None},
                            "values": [name.lower()],
                        }
                    ],
                    "add_used_by_filter": False,
                },
                # Snowflake database equals <UPPERCASE NAME>
                {
                    "filters": [
                        {
                            "operator": "Equals",
                            "property": {"SnowflakeDatabase": None},
                            "values": [name.upper()],
                        }
                    ],
                    "add_used_by_filter": False,
                },
            ],
            "global_filters": [],
            "group_bys": [
                {"by_network_target": False, "property": {"MainEntity": None}}
            ],
            "time_range": {"Relative": {"days_back": 90}},
            "timeseries_limit": 90,
        },
    }

    r = requests.put(GROUPS_ENDPOINT, json=payload, headers=HEADERS, timeout=30)
    if r.ok:
        print(f"✔  Upserted tenant '{name}'")
    else:
        print(f"✖  Failed for '{name}': {r.status_code} — {r.text}")


# ─── Main ────────────────────────────────────────────────────────────────────
def main() -> None:
    with open(CSV_FILENAME, newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            tenant = row.get("name", "").strip()
            if tenant:
                upsert_tenant(tenant)
            else:
                print("• Skipping row with empty tenant name")


if __name__ == "__main__":
    main()
