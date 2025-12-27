#!/usr/bin/env python3
"""
Merge invited conferences with ADS publication data.

This script deduplicates invited conference presentations with ADS data via bibcode
matching. Invited conferences found in ADS are enriched with additional metadata
(location, booktitle, invited_url). Invited conferences not in ADS are appended
as new entries.

This script can be run repeatedly - it's safe to re-run after ADS data updates.

Author: Claude
Date: 2025-12-26
"""

import json
from pathlib import Path
from typing import Dict, List, Any

from utils import get_public_data_dir


def find_publication_by_bibcode(publications: List[Dict[str, Any]], bibcode: str) -> int:
    """
    Find the index of a publication in the list by bibcode.

    Args:
        publications: List of publication dictionaries
        bibcode: Bibcode to search for

    Returns:
        Index of matching publication, or -1 if not found
    """
    for idx, pub in enumerate(publications):
        if pub.get('bibcode') == bibcode:
            return idx
    return -1


def enrich_ads_entry(ads_entry: Dict[str, Any], invited_entry: Dict[str, Any]) -> Dict[str, Any]:
    """
    Enrich an ADS publication entry with invited-specific metadata.

    Args:
        ads_entry: Original ADS publication dictionary
        invited_entry: Invited conference dictionary with enrichment data

    Returns:
        Enriched publication dictionary
    """
    # Start with ADS entry (preserves all ADS fields like citations, url, etc.)
    enriched = ads_entry.copy()

    # Update invited flag
    enriched['invited'] = True

    # Add optional enrichment fields from invited entry if present
    enrichment_fields = ['location', 'day', 'booktitle', 'invited_url', 'keywords']

    for field in enrichment_fields:
        if field in invited_entry:
            enriched[field] = invited_entry[field]

    return enriched


def merge_conferences(ads_pubs: List[Dict[str, Any]], invited_confs: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Merge invited conferences with ADS publications.

    Args:
        ads_pubs: List of ADS publications (all with invited: false)
        invited_confs: List of invited conference entries (all with invited: true)

    Returns:
        Dictionary with:
        - 'publications': merged publication list
        - 'stats': deduplication statistics
    """
    # Statistics
    stats = {
        'matched_via_bibcode': 0,
        'added_as_new': 0,
        'missing_bibcode': 0,
        'warnings': []
    }

    # Work with a copy to avoid modifying original
    merged_pubs = [pub.copy() for pub in ads_pubs]

    print("\nProcessing invited conferences:")
    print("-" * 60)

    for invited in invited_confs:
        title = invited.get('title', 'Unknown')
        year = invited.get('year', '')
        bibcode = invited.get('bibcode')

        if not bibcode:
            # No bibcode - can't verify if duplicate, add as new
            stats['missing_bibcode'] += 1
            warning = f"No bibcode for: {title} ({year})"
            stats['warnings'].append(warning)
            print(f"  ⚠ {warning}")
            print(f"    → Adding as new entry (potential duplicate)")
            merged_pubs.append(invited)
            stats['added_as_new'] += 1
            continue

        # Search for bibcode in ADS data
        idx = find_publication_by_bibcode(merged_pubs, bibcode)

        if idx != -1:
            # Found match - enrich ADS entry
            stats['matched_via_bibcode'] += 1
            merged_pubs[idx] = enrich_ads_entry(merged_pubs[idx], invited)
            print(f"  ✓ Matched: {title}")
            print(f"    Bibcode: {bibcode}")
            print(f"    → Updated invited: true + added enrichment data")
        else:
            # Not in ADS - add as new entry
            stats['added_as_new'] += 1
            print(f"  + New entry: {title}")
            print(f"    Bibcode: {bibcode} (not found in ADS data)")
            print(f"    → Added to publications")
            merged_pubs.append(invited)

    return {
        'publications': merged_pubs,
        'stats': stats
    }


def main():
    """Main merge function."""
    print("=" * 60)
    print("Invited Conferences + ADS Publications Merge")
    print("=" * 60)

    # Get data directory
    data_dir = get_public_data_dir()

    # Load ADS publications
    ads_file = data_dir / "ads_publications.json"
    if not ads_file.exists():
        print(f"\nError: ADS publications file not found: {ads_file}")
        print("Run fetch_ads_publications_to_data_dir.py first to generate ADS data.")
        return

    print(f"\nLoading ADS publications from {ads_file.name}...")
    with open(ads_file, 'r', encoding='utf-8') as f:
        ads_pubs = json.load(f)
    print(f"  Loaded {len(ads_pubs)} ADS publications")

    # Load invited conferences
    invited_file = data_dir / "invited_conferences.json"
    if not invited_file.exists():
        print(f"\nError: Invited conferences file not found: {invited_file}")
        print("Run convert_invited_bibtex.py first to generate invited data.")
        return

    print(f"\nLoading invited conferences from {invited_file.name}...")
    with open(invited_file, 'r', encoding='utf-8') as f:
        invited_confs = json.load(f)
    print(f"  Loaded {len(invited_confs)} invited conferences")

    # Perform merge
    result = merge_conferences(ads_pubs, invited_confs)
    merged_pubs = result['publications']
    stats = result['stats']

    # Save merged data back to ads_publications.json
    print(f"\nSaving merged data to {ads_file.name}...")
    with open(ads_file, 'w', encoding='utf-8') as f:
        json.dump(merged_pubs, f, indent=2, ensure_ascii=False)
    print(f"  ✓ Saved {len(merged_pubs)} publications")

    # Print statistics
    print("\n" + "=" * 60)
    print("Merge Complete!")
    print("=" * 60)
    print(f"\nStatistics:")
    print(f"  Total ADS publications (before merge): {len(ads_pubs)}")
    print(f"  Total invited conferences:              {len(invited_confs)}")
    print(f"  Total publications (after merge):       {len(merged_pubs)}")
    print(f"\nDeduplication:")
    print(f"  Matched via bibcode (enriched):         {stats['matched_via_bibcode']}")
    print(f"  Added as new entries:                   {stats['added_as_new']}")
    print(f"  Missing bibcode (warnings):             {stats['missing_bibcode']}")

    if stats['warnings']:
        print(f"\nWarnings ({len(stats['warnings'])}):")
        for warning in stats['warnings']:
            print(f"  - {warning}")

    # Verify invited field distribution
    invited_count = sum(1 for pub in merged_pubs if pub.get('invited', False))
    print(f"\nVerification:")
    print(f"  Publications with invited=true:         {invited_count}")
    print(f"  Publications with invited=false:        {len(merged_pubs) - invited_count}")


if __name__ == "__main__":
    main()
