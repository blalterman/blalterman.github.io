#!/usr/bin/env python3
"""
Derive yearly citation counts from the ADS metrics payload.

The citation histogram charted by the site is already present in
public/data/ads_metrics.json, which fetch_ads_metrics_to_data_dir.py
refreshes weekly in a single API call. This script reshapes that histogram
into public/data/citations_by_year.json rather than re-querying NASA ADS
per bibcode.

Consumers of the output are unchanged: generate_citations_timeline.py and
generate_publication_statistics.py.

Usage:
    python scripts/derive_citations_by_year.py
"""

import json

from utils import get_public_data_dir, get_relative_path

# Citations *received by* refereed and non-refereed papers, respectively.
# These are the same four histogram keys the previous per-bibcode fetch summed.
REFEREED_KEYS = ("refereed to refereed", "nonrefereed to refereed")
NONREFEREED_KEYS = ("refereed to nonrefereed", "nonrefereed to nonrefereed")


def derive_counts(metrics):
    """Reshape an ADS metrics payload into per-year citation counts.

    Returns (years, refereed, nonrefereed) with years as ascending strings,
    matching the schema the previous fetch script produced.

    Raises KeyError if ADS renames a histogram key, and ValueError if the
    derived total disagrees with the total ADS reports separately.
    """
    histogram = metrics["histograms"]["citations"]

    # Index the four keys directly. If ADS renames one, this raises KeyError
    # rather than silently zeroing a series, which a .get(key, {}) default
    # would do invisibly.
    series = {key: histogram[key] for key in REFEREED_KEYS + NONREFEREED_KEYS}

    # A given year may legitimately be absent from an individual sub-series
    # (e.g. no non-refereed citations that year), so within the union of years
    # a missing entry is a true zero.
    all_years = sorted({year for counts in series.values() for year in counts})

    refereed = [sum(series[k].get(year, 0) for k in REFEREED_KEYS) for year in all_years]
    nonrefereed = [sum(series[k].get(year, 0) for k in NONREFEREED_KEYS) for year in all_years]

    # ADS computes this total through a different path than the histogram, so
    # agreement is an independent check rather than a restatement.
    derived_total = sum(refereed) + sum(nonrefereed)
    reported_total = metrics["citation stats"]["total number of citations"]
    if derived_total != reported_total:
        raise ValueError(
            f"Derived citation total ({derived_total}) disagrees with the total "
            f"ADS reports ({reported_total}). The histogram schema or its "
            f"semantics have changed; do not publish this data."
        )

    # Drop years with no citations of either kind, as the previous script did.
    kept = [(y, r, n) for y, r, n in zip(all_years, refereed, nonrefereed) if r or n]
    if not kept:
        raise ValueError("No years with nonzero citations; refusing to write an empty series.")

    years, refereed, nonrefereed = (list(column) for column in zip(*kept))
    return years, refereed, nonrefereed


def main():
    data_dir = get_public_data_dir()
    metrics_file = data_dir / "ads_metrics.json"

    if not metrics_file.exists():
        raise FileNotFoundError(
            f"ADS metrics not found at {get_relative_path(metrics_file)}. "
            "Run fetch_ads_metrics_to_data_dir.py first."
        )

    print(f"📖 Reading metrics from {get_relative_path(metrics_file)}")
    with open(metrics_file, "r") as f:
        metrics = json.load(f)

    skipped = metrics["skipped bibcodes"]
    if skipped:
        print(
            f"⚠️  ADS skipped {len(skipped)} bibcode(s) when building these metrics; "
            f"citation counts below are incomplete: {skipped}"
        )

    years, refereed, nonrefereed = derive_counts(metrics)

    print(f"   Time span: {years[0]}-{years[-1]} ({len(years)} years)")
    print(f"   Total citations: {sum(refereed) + sum(nonrefereed)}")
    print(f"   Refereed: {sum(refereed)}  Non-refereed: {sum(nonrefereed)}")

    output_path = data_dir / "citations_by_year.json"
    with open(output_path, "w") as f:
        json.dump({"years": years, "refereed": refereed, "nonrefereed": nonrefereed}, f, indent=2)

    print(f"\n💾 Data saved to {get_relative_path(output_path)}")


if __name__ == "__main__":
    main()
