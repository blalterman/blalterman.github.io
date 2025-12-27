#!/usr/bin/env python3
"""
Generate integrated publication statistics file.

Merges ads_metrics.json, invited_presentations.json, and invited_conferences.json
into a single comprehensive statistics file.

Output: /public/data/publication_statistics.json

Author: Claude
Date: 2025-12-26
"""

import json
from pathlib import Path
from collections import defaultdict
from utils import get_public_data_dir


def load_json(filepath):
    """Load JSON file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def compute_invited_breakdown(invited_pres, invited_conf):
    """Compute invited talks breakdown by year and venue."""
    by_year = defaultdict(lambda: {'presentations': 0, 'conferences': 0, 'total': 0})
    by_venue = defaultdict(int)

    # Process presentations
    for pres in invited_pres:
        year = pres['year'][:4]
        venue = pres.get('journal', 'Unknown')

        by_year[year]['presentations'] += 1
        by_year[year]['total'] += 1
        by_venue[venue] += 1

    # Process conferences
    for conf in invited_conf:
        year = conf['year'][:4]
        venue = conf.get('journal', 'Unknown')

        by_year[year]['conferences'] += 1
        by_year[year]['total'] += 1
        by_venue[venue] += 1

    return {
        'by_year': dict(by_year),
        'by_venue': dict(sorted(by_venue.items(), key=lambda x: x[1], reverse=True))
    }


def compute_total_citations_by_year(ads_metrics):
    """Sum all citation types by year."""
    citations = ads_metrics['histograms']['citations']
    years = set()
    for cat in ['refereed to refereed', 'refereed to nonrefereed',
                'nonrefereed to refereed', 'nonrefereed to nonrefereed']:
        years.update(citations[cat].keys())

    total_by_year = {}
    for year in sorted(years):
        total = sum(citations[cat].get(year, 0) for cat in [
            'refereed to refereed', 'refereed to nonrefereed',
            'nonrefereed to refereed', 'nonrefereed to nonrefereed'
        ])
        total_by_year[year] = total

    return total_by_year


def compute_category_counts(ads_pubs, invited_pres):
    """Compute publication counts by category."""
    from collections import Counter

    # Count by publication type
    type_counts = Counter(pub['publication_type'] for pub in ads_pubs)

    return {
        'refereed': sum(1 for pub in ads_pubs if pub.get('publication_type') == 'article'),
        'conferences': type_counts.get('inproceedings', 0) + type_counts.get('abstract', 0),
        'datasets': type_counts.get('dataset', 0),
        'software': type_counts.get('software', 0),
        'invited-talks': len(invited_pres),  # Seminars only
        'phd-thesis': type_counts.get('phdthesis', 0),
        'white-papers': type_counts.get('techreport', 0),
        'preprints': type_counts.get('eprint', 0)
    }


def merge_publications_by_year(ads_pubs_by_year, invited_by_year):
    """Merge ADS publications and invited presentations by year."""
    all_years = set(ads_pubs_by_year.keys()) | set(invited_by_year.keys())

    merged = {}
    for year in all_years:
        ads_count = ads_pubs_by_year.get(year, 0)
        invited_count = invited_by_year.get(year, {}).get('total', 0)
        merged[year] = ads_count + invited_count

    return merged


def main():
    """Generate integrated publication statistics file."""
    data_dir = get_public_data_dir()

    print("Loading source files...")

    # Load source files
    ads_metrics = load_json(data_dir / 'ads_metrics.json')
    ads_pubs = load_json(data_dir / 'ads_publications.json')
    invited_pres = load_json(data_dir / 'invited_presentations.json')
    invited_conf = load_json(data_dir / 'invited_conferences.json')

    print(f"  ADS metrics: h-index={ads_metrics['indicators']['h']}")
    print(f"  ADS publications: {len(ads_pubs)}")
    print(f"  Invited presentations: {len(invited_pres)}")
    print(f"  Invited conferences: {len(invited_conf)}")

    # Compute invited breakdown
    invited_breakdown = compute_invited_breakdown(invited_pres, invited_conf)

    # Build integrated statistics
    stats = {
        'summary': {
            'h_index': ads_metrics['indicators']['h'],
            'g_index': ads_metrics['indicators']['g'],
            'i10': ads_metrics['indicators']['i10'],
            'i100': ads_metrics['indicators']['i100'],
            'm_index': ads_metrics['indicators']['m'],
            'total_citations': ads_metrics['citation stats']['total number of citations'],
            'refereed_citations': ads_metrics['citation stats']['total number of refereed citations'],
            'ads_papers': ads_metrics['basic stats']['number of papers'],
            'refereed_papers': ads_metrics['basic stats refereed']['number of papers'],
            'invited_conferences': len(invited_conf),
            'invited_presentations': len(invited_pres),
            'invited_total': len(invited_conf) + len(invited_pres),
            'total_papers': ads_metrics['basic stats']['number of papers'] + len(invited_pres),
            'total_reads': ads_metrics['basic stats']['total number of reads'],
            'total_downloads': ads_metrics['basic stats']['total number of downloads'],
        },

        'time_series': ads_metrics['time series'],

        'publications_by_year': {
            'all': ads_metrics['histograms']['publications']['all publications'],
            'refereed': ads_metrics['histograms']['publications']['refereed publications'],
            'normalized_all': ads_metrics['histograms']['publications']['all publications normalized'],
            'normalized_refereed': ads_metrics['histograms']['publications']['refereed publications normalized'],
            'all_including_invited': merge_publications_by_year(
                ads_metrics['histograms']['publications']['all publications'],
                invited_breakdown['by_year']
            ),
        },

        'invited_by_year': invited_breakdown['by_year'],
        'invited_by_venue': invited_breakdown['by_venue'],

        'citations_by_year': {
            **ads_metrics['histograms']['citations'],
            'total_by_year': compute_total_citations_by_year(ads_metrics)
        },

        'reads_by_year': {
            'all_reads': ads_metrics['histograms']['reads']['all reads'],
            'refereed_reads': ads_metrics['histograms']['reads']['refereed reads'],
            'normalized_all': ads_metrics['histograms']['reads']['all reads normalized'],
            'normalized_refereed': ads_metrics['histograms']['reads']['refereed reads normalized'],
        },

        'downloads_by_year': {
            'all_downloads': ads_metrics['histograms']['downloads']['all downloads'],
            'refereed_downloads': ads_metrics['histograms']['downloads']['refereed downloads'],
            'normalized_all': ads_metrics['histograms']['downloads']['all downloads normalized'],
            'normalized_refereed': ads_metrics['histograms']['downloads']['refereed downloads normalized'],
        },

        'category_counts': compute_category_counts(ads_pubs, invited_pres)
    }

    # Write output
    output_file = data_dir / 'publication_statistics.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(stats, f, indent=2, ensure_ascii=False)

    print(f"\n✓ Generated {output_file.name}")
    print(f"  Total papers: {stats['summary']['total_papers']}")
    print(f"  h-index: {stats['summary']['h_index']} (from ADS only - correct!)")
    print(f"  Total citations: {stats['summary']['total_citations']}")
    print(f"  Invited talks: {stats['summary']['invited_total']} ({stats['summary']['invited_conferences']} conferences + {stats['summary']['invited_presentations']} presentations)")


if __name__ == "__main__":
    main()
