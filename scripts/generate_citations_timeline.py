#!/usr/bin/env python3
"""
Generate citations timeline plot from citations data.

Reads yearly citation counts from public/data/citations_by_year.json
and creates styled line plots matching other timeline visualizations.

This script does NOT fetch data from NASA ADS - run
fetch_ads_citations_to_data_dir.py first to ensure data is current.

Usage:
    python scripts/generate_citations_timeline.py
"""

import itertools
import json
import matplotlib.pyplot as plt
from utils import get_public_data_dir, get_public_plots_dir, get_relative_path
from plot_config import COLORS, FIGURE, FONTS, LINES, GRID, LEGEND, LAYOUT, OUTPUT


def generate_citations_timeline():
    """Load existing citations data and generate timeline plot."""

    # Load existing data
    data_file = get_public_data_dir() / "citations_by_year.json"

    if not data_file.exists():
        raise FileNotFoundError(
            f"Citations data not found at {get_relative_path(data_file)}. "
            "Run fetch_ads_citations_to_data_dir.py first."
        )

    print(f"📖 Loading citations data from {get_relative_path(data_file)}")

    with open(data_file, 'r') as f:
        data = json.load(f)

    all_years = data['years']
    ref_counts = data['refereed']
    nonref_counts = data['nonrefereed']

    total_citations = sum(ref_counts) + sum(nonref_counts)
    print(f"   Total citations: {total_citations}")
    print(f"   Time span: {all_years[0]}-{all_years[-1]} ({len(all_years)} years)")

    # Compute cumulative sums for plotting
    cum_ref = list(itertools.accumulate(ref_counts))
    cum_nonref = list(itertools.accumulate(nonref_counts))

    print(f"   Cumulative refereed: {cum_ref[-1]}")
    print(f"   Cumulative non-refereed: {cum_nonref[-1]}")

    # Create figure with configured settings
    fig, ax = plt.subplots(figsize=FIGURE['figsize'], dpi=FIGURE['dpi'])
    fig.patch.set_facecolor(FIGURE['facecolor'])

    # Plot lines with configured styles (cumulative data)
    ax.plot(all_years, cum_ref,
            label='Refereed',
            color=COLORS['refereed'],
            **LINES['refereed'])

    ax.plot(all_years, cum_nonref,
            label='Non-Refereed',
            color=COLORS['nonrefereed'],
            **LINES['other'])

    # Add semi-transparent fill under lines for visual interest
    ax.fill_between(all_years, cum_ref, alpha=0.15, color=COLORS['refereed'])
    ax.fill_between(all_years, cum_nonref, alpha=0.15, color=COLORS['nonrefereed'])

    # Apply styling
    ax.set_title('Cumulative Citations', **FONTS['title'])
    ax.set_xlabel('Year', **FONTS['axis_label'])
    ax.set_ylabel('Total Citations', **FONTS['axis_label'])

    # Configure x-axis: label every 2nd year, minor ticks for all years
    major_ticks = all_years[::2]  # Every 2nd year for labels
    ax.set_xticks(major_ticks, minor=False)  # Major ticks with labels
    ax.set_xticks(all_years, minor=True)     # Minor ticks for all years
    ax.tick_params(axis='x', which='minor', length=3)  # Shorter minor ticks
    ax.tick_params(axis='x', which='major', length=6)  # Standard major ticks

    # Configure grid
    ax.grid(GRID['visible'],
            alpha=GRID['alpha'],
            linestyle=GRID['linestyle'],
            linewidth=GRID['linewidth'],
            color=GRID['color'])
    ax.set_axisbelow(True)  # Grid behind plot elements

    # Configure legend
    ax.legend(**LEGEND)

    # Hide top and right spines for cleaner look
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # Apply tight layout
    if LAYOUT['tight_layout']:
        plt.tight_layout(pad=LAYOUT['pad'])

    # Save plots
    plots_dir = get_public_plots_dir()

    # Save SVG
    plot_path_svg = plots_dir / "citations_by_year.svg"
    plt.savefig(plot_path_svg,
                format='svg',
                dpi=OUTPUT['svg_dpi'],
                bbox_inches=OUTPUT['bbox_inches'])
    print(f"📈 Plot saved to {get_relative_path(plot_path_svg)}")

    # Save PNG
    plot_path_png = plots_dir / "citations_by_year.png"
    plt.savefig(plot_path_png,
                format='png',
                dpi=OUTPUT['png_dpi'],
                bbox_inches=OUTPUT['bbox_inches'])
    print(f"📈 Plot saved to {get_relative_path(plot_path_png)}")

    plt.close()


if __name__ == '__main__':
    generate_citations_timeline()
    print("\n✓ Citations timeline plot generation complete")
