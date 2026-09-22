#!/usr/bin/env python3
"""
Audit the deployed site's data against the repository and against itself.

Every signal inside this repository (exit codes, commit history, file diffs,
workflow logs) read green for the 32 weeks that citations_by_year.json was
frozen. This script checks the only thing none of them observe: what a visitor
actually loads.

Three assertions, none of which needs a threshold or a calibration:

  A. The deployed ads_metrics.json equals the committed one.
     Catches a deploy that silently serves a stale snapshot.

  B. Deriving citations from the DEPLOYED metrics reproduces the DEPLOYED
     citations_by_year.json. Catches the frozen-data failure directly: a stale
     citations file cannot agree with a current metrics file.

  C. Every publication the deployed Refereed page renders has a self-hosted PDF
     in the deployed publication-pdfs.json, or an explicit exemption below.
     data-loader.ts already warns when a registry key matches no publication;
     nothing warned about the reverse, and the registry is hand-curated while
     ads_publications.json is refreshed weekly, so the automated side outgrows
     the curated one and a paper loses its Download button silently.

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

# Publications on the Refereed page for which no file can be served at all, each
# paired with the reason. Assertion C treats an entry here as covered, so adding
# one is a deliberate, reviewable act; the default for a new paper is to fail.
PDF_EXEMPT = {
    "2022RNAAS...6..135A": "RNAAS is published HTML-only; the AAS issues no PDF.",
}

# The slug of the category whose PDF coverage assertion C checks, as
# publications-categories.json spells it.
AUDITED_CATEGORY = "refereed"


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

    # --- C. every refereed publication has a PDF or an exemption -----------
    #
    # The population is taken from the deployed publications-categories.json
    # rather than hardcoded, because that file is what the page itself filters
    # on (getPublicationsByType -> filterPublicationsByType matches
    # publication_type only). Auditing a population derived any other way --
    # ADS's REFEREED property, say -- would silently exclude papers the page
    # does render, which is the same silent gap this assertion exists to close.
    deployed_pubs = fetch_json(args.site, "data/ads_publications.json")
    deployed_non_ads = fetch_json(args.site, "data/non_ads_publications.json")
    deployed_pdfs = fetch_json(args.site, "data/publication-pdfs.json")
    deployed_categories = fetch_json(args.site, "data/publications-categories.json")

    audited = next(
        c for c in deployed_categories["categories"]
        if c["slug"] == AUDITED_CATEGORY
    )
    wanted = audited["publicationType"]
    wanted = wanted if isinstance(wanted, list) else [wanted]

    # loadAllPublications() merges both sources before joining the registry, so
    # the audit must merge them too or it would miss a non-ADS entry.
    rendered = [
        p for p in deployed_pubs + deployed_non_ads
        if p.get("publication_type") in wanted
    ]

    # Positive control: the category must not be empty, or "all of them have a
    # PDF" is vacuously true.
    print(f"  fetched: {len(rendered)} publications on /publications/"
          f"{AUDITED_CATEGORY}, {len(deployed_pdfs)} PDF registry entries")
    if not rendered:
        raise RuntimeError(
            f"No deployed publication has type {wanted}; assertion C would be vacuous."
        )

    uncovered = [
        p["bibcode"] for p in rendered
        if p["bibcode"] not in deployed_pdfs and p["bibcode"] not in PDF_EXEMPT
    ]
    stale_exemptions = [b for b in PDF_EXEMPT if b in deployed_pdfs]

    if not uncovered and not stale_exemptions:
        print(f"  PASS  every deployed {AUDITED_CATEGORY} publication has a PDF "
              f"or a recorded exemption")
    if uncovered:
        failures.append(
            f"{len(uncovered)} publication(s) on /publications/{AUDITED_CATEGORY} "
            f"have no self-hosted PDF and no exemption: {', '.join(sorted(uncovered))}. "
            f"Add each to public/data/publication-pdfs.json, or to PDF_EXEMPT in "
            f"this script with the reason no file can be served."
        )
    if stale_exemptions:
        failures.append(
            f"PDF_EXEMPT names {', '.join(sorted(stale_exemptions))}, which now "
            f"has a registry entry. Remove the exemption so it cannot mask a "
            f"future gap."
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
