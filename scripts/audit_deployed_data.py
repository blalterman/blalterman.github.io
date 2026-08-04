#!/usr/bin/env python3
"""
Audit the deployed site's data against the repository and against itself.

Every signal inside this repository (exit codes, commit history, file diffs,
workflow logs) read green for the 32 weeks that citations_by_year.json was
frozen. This script checks the only thing none of them observe: what a visitor
actually loads.

Two assertions, neither of which needs a threshold or a calibration:

  A. The deployed ads_metrics.json equals the committed one.
     Catches a deploy that silently serves a stale snapshot.

  B. Deriving citations from the DEPLOYED metrics reproduces the DEPLOYED
     citations_by_year.json. Catches the frozen-data failure directly: a stale
     citations file cannot agree with a current metrics file.

Both are computed from artifacts fetched over the network, so a pipeline that
never ran fails assertion A rather than passing silently.

Usage:
    python scripts/audit_deployed_data.py [--site https://example.github.io]
Exits nonzero on any failure.
"""

import argparse
import json
import sys
import urllib.error
import urllib.request

from derive_citations_by_year import derive_counts
from utils import get_public_data_dir

DEFAULT_SITE = "https://blalterman.github.io"
TIMEOUT_SECONDS = 30


def fetch_json(site, path):
    """Fetch and parse a JSON artifact from the deployed site.

    A network or parse failure raises. An unreachable site is an ERROR, not a
    pass: a check that could not read the artifact has not run.
    """
    url = f"{site}/{path}"
    request = urllib.request.Request(url, headers={"Cache-Control": "no-cache"})
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT_SECONDS) as response:
            if response.status != 200:
                raise RuntimeError(f"{url} returned HTTP {response.status}")
            payload = response.read()
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Cannot reach {url}: {exc}") from exc

    if not payload:
        raise RuntimeError(f"{url} returned an empty body")
    return json.loads(payload)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--site", default=DEFAULT_SITE, help="Deployed site base URL")
    args = parser.parse_args()

    print(f"Auditing {args.site}")

    deployed_metrics = fetch_json(args.site, "data/ads_metrics.json")
    deployed_citations = fetch_json(args.site, "data/citations_by_year.json")

    # Positive control: prove the fetches returned real content before any
    # comparison below can report agreement. Two empty files also "match".
    deployed_total = deployed_metrics["citation stats"]["total number of citations"]
    n_years = len(deployed_citations["years"])
    print(f"  fetched: metrics reports {deployed_total} citations, "
          f"citations file spans {n_years} years")
    if deployed_total <= 0 or n_years <= 0:
        raise RuntimeError("Deployed artifacts are empty; comparison would be vacuous.")

    failures = []

    # --- A. deployed metrics == committed metrics --------------------------
    with open(get_public_data_dir() / "ads_metrics.json") as f:
        committed_metrics = json.load(f)

    if deployed_metrics == committed_metrics:
        print("  PASS  deployed ads_metrics.json matches the committed file")
    else:
        committed_total = committed_metrics["citation stats"]["total number of citations"]
        failures.append(
            f"Deployed ads_metrics.json differs from the committed file "
            f"(deployed total {deployed_total}, committed total {committed_total}). "
            f"The site is serving a different snapshot than the repository holds."
        )

    # --- B. deployed citations == derive(deployed metrics) -----------------
    years, refereed, nonrefereed = derive_counts(deployed_metrics)
    expected = {"years": years, "refereed": refereed, "nonrefereed": nonrefereed}

    if deployed_citations == expected:
        print("  PASS  deployed citations_by_year.json agrees with the deployed metrics")
    else:
        drift = [
            f"{year}: served {served_ref}, metrics imply {expected_ref}"
            for year, served_ref, expected_ref in zip(years, deployed_citations["refereed"], refereed)
            if served_ref != expected_ref
        ] or ["year sets differ"]
        failures.append(
            "Deployed citations_by_year.json disagrees with the deployed metrics. "
            + "; ".join(drift[:5])
        )

    if failures:
        print("\nFAIL")
        for failure in failures:
            print(f"  - {failure}")
        return 1

    print("\nPASS: the deployed site matches the repository and is internally consistent.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
