#!/usr/bin/env python3
"""
Check derive_citations_by_year.py against the previous method's own output.

Until 2026-08, citations_by_year.json was produced by fetching
/v1/metrics/{bibcode} once per paper and summing the result. This script
replays that method's committed output as a fixture and asserts the
derivation reproduces it.

The fixture is the git tree at FIXTURE_COMMIT, chosen because
ads_metrics.json and citations_by_year.json were both written on the same
day there (2025-09-15). A tree where the two files were written days apart
would differ in the actively-accruing year for reasons unrelated to the
derivation.

Usage:
    python scripts/verify_citations_derivation.py
Exits nonzero on mismatch.
"""

import json
import subprocess
import sys

from derive_citations_by_year import derive_counts

FIXTURE_COMMIT = "f81adbd6da45e73c102b7b0b8ffbdd80ebf5ded7"
EXPECTED_NONZERO_YEARS = 8  # 2018-2025 at the fixture commit


def read_at_commit(commit, path):
    """Read a repo file as it existed at a commit."""
    result = subprocess.run(
        ["git", "show", f"{commit}:{path}"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"Cannot read {path} at {commit[:7]}: {result.stderr.strip()}. "
            f"The fixture commit must be present locally; run 'git fetch'."
        )
    return json.loads(result.stdout)


def main():
    metrics = read_at_commit(FIXTURE_COMMIT, "public/data/ads_metrics.json")
    previous = read_at_commit(FIXTURE_COMMIT, "public/data/citations_by_year.json")

    # Positive control: a fixture that failed to load, or loaded empty, would
    # make any "match" below vacuous.
    if not metrics.get("histograms") or not previous.get("years"):
        raise RuntimeError("Fixture loaded but is empty; the comparison would be vacuous.")

    # The previous method did not filter zero years at this commit, so compare
    # on its nonzero subset.
    expected = {
        year: (ref, nonref)
        for year, ref, nonref in zip(previous["years"], previous["refereed"], previous["nonrefereed"])
        if ref or nonref
    }
    if len(expected) != EXPECTED_NONZERO_YEARS:
        raise RuntimeError(
            f"Fixture has {len(expected)} nonzero years, expected {EXPECTED_NONZERO_YEARS}. "
            f"The fixture changed; re-derive the expectation before trusting this check."
        )

    years, refereed, nonrefereed = derive_counts(metrics)
    derived = {y: (r, n) for y, r, n in zip(years, refereed, nonrefereed)}

    print(f"Fixture: {FIXTURE_COMMIT[:7]} ({len(expected)} nonzero years)")
    print(f"{'year':<6} {'derived':>18} {'previous method':>18}")
    mismatches = []
    for year in sorted(set(expected) | set(derived)):
        d = derived.get(year)
        e = expected.get(year)
        flag = "" if d == e else "   <-- MISMATCH"
        if d != e:
            mismatches.append(year)
        print(f"{year:<6} {str(d):>18} {str(e):>18}{flag}")

    if mismatches:
        print(f"\nFAIL: {len(mismatches)} year(s) disagree: {mismatches}")
        return 1

    print(f"\nPASS: derivation reproduces the previous method on all {len(expected)} years.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
