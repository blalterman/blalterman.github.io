#!/usr/bin/env python3
"""
Compute invited talk metrics from ads_publications.json.

This script analyzes publications with invited=true to generate statistics
for display on the publications page. NASA ADS API doesn't track invited
status, so we compute these metrics manually.

Author: Claude
Date: 2025-12-26
"""

import json
from collections import Counter
from pathlib import Path

from utils import get_public_data_dir


def compute_invited_metrics(publications):
    """
    Compute metrics for invited talks.

    Args:
        publications: List of publication dictionaries

    Returns:
        Dictionary containing invited talk metrics
    """
    # Filter for invited publications only
    invited = [pub for pub in publications if pub.get('invited', False)]

    # Count by year
    year_counts = Counter()
    for pub in invited:
        year = pub.get('year', '').split('-')[0]  # Extract YYYY from YYYY-MM-DD
        if year:
            year_counts[year] += 1

    # Count by conference/venue
    conferences = Counter()
    for pub in invited:
        # Try booktitle first (for inproceedings), fall back to journal
        venue = pub.get('booktitle') or pub.get('journal', 'Unknown')
        conferences[venue] += 1

    return {
        'total_invited_talks': len(invited),
        'invited_by_year': dict(sorted(year_counts.items())),
        'invited_conferences': dict(sorted(
            conferences.items(),
            key=lambda x: x[1],
            reverse=True
        ))
    }


def main():
    """Main execution function."""
    data_dir = get_public_data_dir()
    ads_file = data_dir / "ads_publications.json"
    metrics_file = data_dir / "invited_metrics.json"

    # Load publications
    try:
        with open(ads_file, 'r', encoding='utf-8') as f:
            publications = json.load(f)
    except FileNotFoundError:
        print(f"\nError: Publications file not found: {ads_file}")
        print("Run fetch_ads_publications_to_data_dir.py first.")
        return 1
    except json.JSONDecodeError as e:
        print(f"\nError: Invalid JSON in {ads_file}")
        print(f"Details: {e}")
        return 1

    # Compute metrics
    metrics = compute_invited_metrics(publications)

    # Save metrics
    try:
        with open(metrics_file, 'w', encoding='utf-8') as f:
            json.dump(metrics, f, indent=2)
    except IOError as e:
        print(f"\nError: Could not write to {metrics_file}")
        print(f"Details: {e}")
        return 1

    # Print summary
    print(f"\n{'=' * 60}")
    print("Invited Talks Metrics Computed")
    print(f"{'=' * 60}")
    print(f"Total invited talks: {metrics['total_invited_talks']}")
    print(f"\nBreakdown by year:")
    for year, count in metrics['invited_by_year'].items():
        print(f"  {year}: {count}")
    print(f"\nBreakdown by venue:")
    for venue, count in list(metrics['invited_conferences'].items())[:5]:
        print(f"  {venue}: {count}")
    if len(metrics['invited_conferences']) > 5:
        print(f"  ... and {len(metrics['invited_conferences']) - 5} more")
    print(f"\n✓ Metrics saved to: {metrics_file}")
    print(f"{'=' * 60}\n")

    return 0


if __name__ == "__main__":
    exit(main())
