#!/usr/bin/env python3
"""
Apply standardized conference name mappings to publications data.

This script simplifies and normalizes conference venue names in ads_publications.json
based on specific user-defined mapping rules.

Mapping Rules:
1. All SHINE conferences → "SHINE"
2. "Bulletin of the American Astronomical Society" → "Bulletin of AAS"
3. All COSPAR → "COSPAR"
4. "Triennial Earth-Sun Summit" variants → "Triennial Earth-Sun Summit"
5. "APS Division of Plasma Physics Meeting Abstracts" → "APS Division of Plasma Physics"
"""

import json
import re
from pathlib import Path
from typing import Dict

from utils import get_public_data_dir


def create_venue_mappings() -> Dict[str, str]:
    """Create mapping dictionary for venue name standardization."""
    return {
        # SHINE conferences (all variants to "SHINE")
        "Solar Heliospheric and INterplanetary Environment (SHINE 2015)": "SHINE",
        "Solar Heliospheric and INterplanetary Environment (SHINE 2016)": "SHINE",
        "Solar Heliospheric and INterplanetary Environment (SHINE 2017)": "SHINE",
        "Solar Heliospheric and INterplanetary Environment (SHINE 2018)": "SHINE",
        "Solar Heliospheric and INterplanetary Environment (SHINE 2019)": "SHINE",
        "SHINE 2022 Workshop": "SHINE",
        # Bulletin of AAS
        "Bulletin of the American Astronomical Society": "Bulletin of AAS",
        # COSPAR (both variants to "COSPAR")
        "43rd COSPAR Scientific Assembly. Held 28 January - 4 February": "COSPAR",
        "44th COSPAR Scientific Assembly. Held 16-24 July": "COSPAR",
        # Triennial Earth-Sun Summit
        "Third Triennial Earth-Sun Summit (TESS)": "Triennial Earth-Sun Summit",
        # APS Division of Plasma Physics
        "APS Division of Plasma Physics Meeting Abstracts": "APS Division of Plasma Physics",
    }


def apply_mappings(publications: list, mappings: Dict[str, str]) -> tuple[list, Dict[str, int]]:
    """
    Apply venue name mappings to publications.

    Args:
        publications: List of publication dictionaries
        mappings: Dictionary of venue name mappings

    Returns:
        Tuple of (updated publications list, mapping statistics)
    """
    stats = {venue: 0 for venue in mappings.keys()}

    for pub in publications:
        original_venue = pub.get("journal", "")
        if original_venue in mappings:
            pub["journal"] = mappings[original_venue]
            stats[original_venue] += 1

    return publications, stats


def main():
    """Load publications, apply mappings, and save."""
    data_dir = get_public_data_dir()
    publications_file = data_dir / "ads_publications.json"

    # Load publications
    print(f"📖 Loading publications from {publications_file}")
    with open(publications_file, "r") as f:
        publications = json.load(f)

    print(f"   Loaded {len(publications)} publications")

    # Create and apply mappings
    mappings = create_venue_mappings()
    print(f"\n🔄 Applying {len(mappings)} venue name mappings...")
    publications, stats = apply_mappings(publications, mappings)

    # Display statistics
    print("\n📊 Mapping Results:")
    total_mapped = 0
    for venue, count in stats.items():
        if count > 0:
            mapped_venue = mappings[venue]
            print(f"   {count:2d} publication(s): '{venue}' → '{mapped_venue}'")
            total_mapped += count

    if total_mapped == 0:
        print("   ⚠️  No publications were mapped (possibly already updated?)")
    else:
        print(f"\n✅ Total publications updated: {total_mapped}")

    # Save updated publications
    with open(publications_file, "w") as f:
        json.dump(publications, f, indent=2)

    print(f"\n💾 Saved updated publications to {publications_file}")

    return total_mapped > 0


if __name__ == "__main__":
    main()
