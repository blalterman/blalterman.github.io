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

import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional

from utils import get_public_data_dir


def make_synthetic_citation_key(title: str, year: str) -> str:
    """Generate a deterministic citation key for a bibcodeless invited entry.

    Format: {FirstSignificantWord}{Year4}{Hash4}, e.g.,
    ('An Experimentalists Introduction...', '2017-07') -> 'Experimentalists2017a3f7'
    """
    skip = {'a', 'an', 'the', 'on', 'in', 'of', 'for', 'to', 'and', 'with', 'at'}
    words = re.findall(r'\b[A-Za-z]+\b', title)
    significant = next((w for w in words if w.lower() not in skip), 'Untitled')
    year_4 = (year or '0000')[:4]
    hash_suffix = hashlib.md5(f"{title}{year}".encode()).hexdigest()[:4]
    return f"{significant}{year_4}{hash_suffix}"


def get_dedup_key(entry: Dict[str, Any]) -> tuple:
    """Build a (lowered-title, year-prefix-4) dedup key for one entry.

    Mirrors the convention in scripts/add_non_ads_publication.py:305-323.
    """
    title = (entry.get('title') or '').lower().strip()
    year = (entry.get('year') or '')[:4]
    return (title, year)


def build_dedup_keys(entries: List[Dict[str, Any]]) -> set:
    """Build a set of dedup keys from a list of entries (skips empty titles/years)."""
    return {get_dedup_key(e) for e in entries if e.get('title') and e.get('year')}


def extract_bibcode_from_entry(entry: Dict[str, Any]) -> Optional[str]:
    """
    Extract bibcode from invited entry, checking multiple fields.

    Checks (in priority order):
    1. entry['bibcode']
    2. Bibcode pattern in entry['invited_url']
    3. Bibcode pattern in entry['url']

    Args:
        entry: Invited conference entry dictionary

    Returns:
        Bibcode string or None if not found
    """
    # Check bibcode field first
    if entry.get('bibcode'):
        return entry['bibcode']

    # Pattern to match ADS bibcodes (e.g., 2019AGUFM.U21B..14A)
    bibcode_pattern = r'(?:ui\.adsabs\.harvard\.edu/abs/)?([12][0-9]{3}[A-Za-z0-9&.]+)'

    # Check invited_url field
    if 'invited_url' in entry and entry['invited_url']:
        match = re.search(bibcode_pattern, entry['invited_url'])
        if match:
            bibcode = match.group(1)
            print(f"  ⚠ Found bibcode in invited_url instead of bibcode field: {bibcode}")
            return bibcode

    # Check url field
    if 'url' in entry and entry['url']:
        match = re.search(bibcode_pattern, entry['url'])
        if match:
            bibcode = match.group(1)
            print(f"  ⚠ Found bibcode in url instead of bibcode field: {bibcode}")
            return bibcode

    return None


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


def merge_conferences(
    ads_pubs: List[Dict[str, Any]],
    invited_confs: List[Dict[str, Any]],
    non_ads_pubs: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """
    Merge invited conferences with ADS publications.

    Bibcoded invited entries either enrich an existing ADS record (matched
    by bibcode) or are appended to the merged ADS list. Bibcodeless invited
    entries are routed to non_ads_publications.json with synthetic
    NOADS-{citation_key} bibcodes per the convention in
    scripts/add_non_ads_publication.py:288. Per-run idempotence is preserved
    by deduping against existing non_ads entries by (title, year). When an
    invited entry that previously had no bibcode gains a real ADS bibcode,
    the synthetic-bibcoded version is removed from non_ads to prevent
    double-counting.

    Args:
        ads_pubs: List of ADS publications (all with invited: false)
        invited_confs: List of invited conference entries (all with invited: true)
        non_ads_pubs: Current non-ADS publications (manually curated + prior
            synthetic-bibcoded invited entries)

    Returns:
        Dictionary with:
        - 'publications': merged ADS publication list (no bibcodeless entries)
        - 'non_ads': updated non-ADS list (synthetic-bibcoded entries reconciled)
        - 'stats': deduplication statistics
    """
    stats = {
        'matched_via_bibcode': 0,
        'added_as_new': 0,
        'missing_bibcode': 0,
        'added_to_non_ads': 0,
        'skipped_non_ads_duplicate': 0,
        'reconciled_to_bibcode': 0,
        'warnings': []
    }

    merged_pubs = [pub.copy() for pub in ads_pubs]
    updated_non_ads = [pub.copy() for pub in non_ads_pubs]

    # Mitigation 2: reverse-dedup. If an invited entry now has a real bibcode,
    # any prior synthetic-bibcoded NOADS-* version of the same talk should be
    # removed from non_ads_publications.json to avoid double-counting.
    bibcoded_invited_keys = {
        get_dedup_key(e) for e in invited_confs
        if extract_bibcode_from_entry(e)
    }
    if bibcoded_invited_keys:
        before = len(updated_non_ads)
        updated_non_ads = [
            e for e in updated_non_ads
            if not (
                str(e.get('bibcode', '')).startswith('NOADS-')
                and get_dedup_key(e) in bibcoded_invited_keys
            )
        ]
        removed = before - len(updated_non_ads)
        if removed:
            stats['reconciled_to_bibcode'] = removed
            print(f"  Reconciled {removed} synthetic-bibcoded entry(ies) "
                  f"that now have real ADS bibcodes")

    # Mitigation 1: idempotence. Build dedup keys from current non_ads so
    # repeat runs on the same input produce zero diff.
    non_ads_dedup_keys = build_dedup_keys(updated_non_ads)

    print("\nProcessing invited conferences:")
    print("-" * 60)

    for invited in invited_confs:
        title = invited.get('title', 'Unknown')
        year = invited.get('year', '')

        bibcode = extract_bibcode_from_entry(invited)

        if not bibcode:
            # Route to non_ads_publications.json with synthetic bibcode.
            stats['missing_bibcode'] += 1
            warning = f"No bibcode for: {title} ({year})"
            stats['warnings'].append(warning)
            print(f"  ⚠ {warning}")

            dedup_key = get_dedup_key(invited)
            if dedup_key in non_ads_dedup_keys:
                stats['skipped_non_ads_duplicate'] += 1
                print(f"    → already in non_ads_publications.json, skipping")
                continue

            citation_key = make_synthetic_citation_key(title, year)
            synthetic_bibcode = f"NOADS-{citation_key}"
            invited_with_bibcode = {**invited, 'bibcode': synthetic_bibcode}
            updated_non_ads.append(invited_with_bibcode)
            non_ads_dedup_keys.add(dedup_key)
            stats['added_to_non_ads'] += 1
            print(f"    → added to non_ads_publications.json as {synthetic_bibcode}")
            continue

        # Bibcoded path (unchanged behavior for ads_publications.json)
        idx = find_publication_by_bibcode(merged_pubs, bibcode)

        if idx != -1:
            stats['matched_via_bibcode'] += 1
            merged_pubs[idx] = enrich_ads_entry(merged_pubs[idx], invited)
            print(f"  ✓ Matched: {title}")
            print(f"    Bibcode: {bibcode}")
            print(f"    → Updated invited: true + added enrichment data")
        else:
            stats['added_as_new'] += 1
            print(f"  + New entry: {title}")
            print(f"    Bibcode: {bibcode} (not found in ADS data)")
            print(f"    → Added to publications")
            merged_pubs.append(invited)

    return {
        'publications': merged_pubs,
        'non_ads': updated_non_ads,
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
        sys.exit(1)

    print(f"\nLoading ADS publications from {ads_file.name}...")
    with open(ads_file, 'r', encoding='utf-8') as f:
        ads_pubs = json.load(f)
    print(f"  Loaded {len(ads_pubs)} ADS publications")

    # Load invited conferences
    invited_file = data_dir / "invited_conferences.json"
    if not invited_file.exists():
        print(f"\nError: Invited conferences file not found: {invited_file}")
        print("Invited conferences JSON file is missing.")
        sys.exit(1)

    print(f"\nLoading invited conferences from {invited_file.name}...")
    with open(invited_file, 'r', encoding='utf-8') as f:
        invited_confs = json.load(f)
    print(f"  Loaded {len(invited_confs)} invited conferences")

    # Load non_ads publications (destination for bibcodeless invited entries)
    non_ads_file = data_dir / "non_ads_publications.json"
    if non_ads_file.exists():
        with open(non_ads_file, 'r', encoding='utf-8') as f:
            non_ads_pubs = json.load(f)
        print(f"  Loaded {len(non_ads_pubs)} non-ADS publications")
    else:
        non_ads_pubs = []
        print(f"  non_ads_publications.json not found — will be created if needed")

    # Perform merge
    result = merge_conferences(ads_pubs, invited_confs, non_ads_pubs)
    merged_pubs = result['publications']
    updated_non_ads = result['non_ads']
    stats = result['stats']

    # Save merged data back to ads_publications.json
    print(f"\nSaving merged data to {ads_file.name}...")
    with open(ads_file, 'w', encoding='utf-8') as f:
        json.dump(merged_pubs, f, indent=2, ensure_ascii=False)
    print(f"  ✓ Saved {len(merged_pubs)} publications")

    # Save updated non_ads_publications.json only if it changed
    non_ads_changed = (
        len(updated_non_ads) != len(non_ads_pubs)
        or stats['reconciled_to_bibcode'] > 0
    )
    if non_ads_changed:
        print(f"\nSaving updated non-ADS data to {non_ads_file.name}...")
        with open(non_ads_file, 'w', encoding='utf-8') as f:
            json.dump(updated_non_ads, f, indent=2, ensure_ascii=False)
        print(f"  ✓ Saved {len(updated_non_ads)} non-ADS publications")

    # Print statistics
    print("\n" + "=" * 60)
    print("Merge Complete!")
    print("=" * 60)
    print(f"\nStatistics:")
    print(f"  Total ADS publications (before merge): {len(ads_pubs)}")
    print(f"  Total invited conferences:              {len(invited_confs)}")
    print(f"  Total publications (after merge):       {len(merged_pubs)}")
    print(f"  Total non-ADS publications:             {len(updated_non_ads)}")
    print(f"\nDeduplication:")
    print(f"  Matched via bibcode (enriched):         {stats['matched_via_bibcode']}")
    print(f"  Added as new entries (ADS):             {stats['added_as_new']}")
    print(f"  Missing bibcode (warnings):             {stats['missing_bibcode']}")
    print(f"  Routed to non_ads (synthetic bibcode):  {stats['added_to_non_ads']}")
    print(f"  Skipped (already in non_ads):           {stats['skipped_non_ads_duplicate']}")
    print(f"  Reconciled (synthetic → real bibcode):  {stats['reconciled_to_bibcode']}")

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
