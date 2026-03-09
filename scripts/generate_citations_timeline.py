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
from plot_config import COLORS, FIGURE, FONTS, LINES, GRID, LEGEND, LAYOUT, OUTPUT, THEMES, get_theme_config, get_data_colors


def generate_citations_timeline(theme_name='light'):
    """Load existing citations data and generate timeline plot."""
    theme = get_theme_config(theme_name)
    data_colors = get_data_colors(theme_name)
    suffix = '' if theme_name == 'light' else f'_{theme_name}'

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
    fig.patch.set_facecolor(theme['facecolor'])
    ax.set_facecolor('none')

    # Plot lines with configured styles (cumulative data)
    ax.plot(all_years, cum_ref,
            label='Refereed',
            color=data_colors['refereed'],
            **LINES['refereed'])

    ax.plot(all_years, cum_nonref,
            label='Non-Refereed',
            color=data_colors['nonrefereed'],
            **LINES['other'])

    # Add semi-transparent fill under lines for visual interest
    ax.fill_between(all_years, cum_ref, alpha=0.15, color=data_colors['refereed'])
    ax.fill_between(all_years, cum_nonref, alpha=0.15, color=data_colors['nonrefereed'])

    # Apply styling with theme colors
    ax.set_title('Cumulative Citations', color=theme['title_color'], **FONTS['title'])
    ax.set_xlabel('Year', color=theme['label_color'], **FONTS['axis_label'])
    ax.set_ylabel('Total Citations', color=theme['label_color'], **FONTS['axis_label'])

    # Configure x-axis: label every 2nd year, minor ticks for all years
    major_ticks = all_years[::2]  # Every 2nd year for labels
    ax.set_xticks(major_ticks, minor=False)  # Major ticks with labels
    ax.set_xticks(all_years, minor=True)     # Minor ticks for all years
    ax.tick_params(axis='x', which='minor', length=3, colors=theme['tick_color'])
    ax.tick_params(axis='x', which='major', length=6, colors=theme['tick_color'])
    ax.tick_params(axis='y', colors=theme['tick_color'])

    # Configure grid with theme colors
    ax.grid(GRID['visible'],
            alpha=theme['grid_alpha'],
            linestyle=GRID['linestyle'],
            linewidth=GRID['linewidth'],
            color=theme['grid_color'])
    ax.set_axisbelow(True)  # Grid behind plot elements

    # Configure legend with theme colors
    legend = ax.legend(**LEGEND)
    legend.get_frame().set_facecolor(theme['legend_facecolor'])
    legend.get_frame().set_edgecolor(theme['legend_edgecolor'])
    for text in legend.get_texts():
        text.set_color(theme['legend_text_color'])

    # Style spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    for spine in ['bottom', 'left']:
        ax.spines[spine].set_color(theme['spine_color'])

    # Apply tight layout
    if LAYOUT['tight_layout']:
        plt.tight_layout(pad=LAYOUT['pad'])

    # Save plots
    plots_dir = get_public_plots_dir()

    plot_path_svg = plots_dir / f"citations_by_year{suffix}.svg"
    plt.savefig(plot_path_svg,
                format='svg',
                dpi=OUTPUT['svg_dpi'],
                bbox_inches=OUTPUT['bbox_inches'],
                transparent=(theme_name == 'dark'))
    print(f"📈 Plot saved to {get_relative_path(plot_path_svg)}")

    plot_path_png = plots_dir / f"citations_by_year{suffix}.png"
    plt.savefig(plot_path_png,
                format='png',
                dpi=OUTPUT['png_dpi'],
                bbox_inches=OUTPUT['bbox_inches'],
                transparent=(theme_name == 'dark'))
    print(f"📈 Plot saved to {get_relative_path(plot_path_png)}")

    plt.close()


if __name__ == '__main__':
    for theme_name in THEMES:
        generate_citations_timeline(theme_name)
    print("\n✓ Citations timeline plot generation complete")
