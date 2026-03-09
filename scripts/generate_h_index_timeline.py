#!/usr/bin/env python3
"""
Generate h-index timeline plot from ADS metrics data.

Reads h-index time series from ads_metrics.json and generates
styled plot matching other timeline visualizations.

Usage:
    python scripts/generate_h_index_timeline.py
"""

import json
import matplotlib.pyplot as plt
from pathlib import Path
from utils import get_repo_root, get_public_data_dir, get_public_plots_dir, get_relative_path
from plot_config import COLORS, FIGURE, FONTS, LINES, GRID, AXES, LAYOUT, OUTPUT, THEMES, get_theme_config


def load_h_index_data():
    """Load h-index time series from ads_metrics.json."""
    data_file = get_public_data_dir() / "ads_metrics.json"

    if not data_file.exists():
        raise FileNotFoundError(
            f"Metrics file not found at {get_relative_path(data_file)}. "
            "Run update-ads-metrics workflow or fetch_ads_metrics_to_data_dir.py first."
        )

    print(f"📖 Loading h-index data from {get_relative_path(data_file)}")

    with open(data_file, 'r') as f:
        metrics = json.load(f)

    h_index_series = metrics.get("time series", {}).get("h", {})

    if not h_index_series:
        raise ValueError("No h-index time series data found in metrics file")

    # Sort by year
    years = sorted([int(year) for year in h_index_series.keys()])
    h_values = [h_index_series[str(year)] for year in years]

    # Filter out leading zeros - start at LAST zero year (shows baseline before growth)
    first_nonzero_idx = next((i for i, h in enumerate(h_values) if h > 0), 0)
    if first_nonzero_idx > 0:
        # Start one year before first non-zero (the last zero year)
        start_idx = first_nonzero_idx - 1
    else:
        # No leading zeros, start at beginning
        start_idx = 0

    years = years[start_idx:]
    h_values = h_values[start_idx:]

    current_h = metrics.get("indicators", {}).get("h", h_values[-1] if h_values else 0)

    print(f"   Current h-index: {current_h}")
    print(f"   Time span: {years[0]}-{years[-1]} ({len(years)} years)")
    print(f"   Starting at last zero year: {years[0]} (h={h_values[0]})")

    return years, h_values


def generate_h_index_plot(theme_name='light'):
    """Generate and save h-index timeline plot."""
    theme = get_theme_config(theme_name)
    suffix = '' if theme_name == 'light' else f'_{theme_name}'

    years, h_values = load_h_index_data()

    # Create figure with configured settings
    fig, ax = plt.subplots(figsize=FIGURE['figsize'], dpi=FIGURE['dpi'])
    fig.patch.set_facecolor(theme['facecolor'])
    ax.set_facecolor('none')

    # Plot h-index timeline with configured line style
    ax.plot(
        years,
        h_values,
        color=COLORS['refereed'],
        **LINES['refereed']
    )

    # Add semi-transparent fill under the line
    ax.fill_between(
        years,
        h_values,
        alpha=0.2,
        color=COLORS['refereed']
    )

    # Apply styling with theme colors
    ax.set_title('H-Index Timeline', color=theme['text_color'], **FONTS['title'])
    ax.set_xlabel('Year', color=theme['text_color'], **FONTS['axis_label'])
    ax.set_ylabel('h-index', color=theme['text_color'], **FONTS['axis_label'])

    # Configure x-axis: label every 2nd year, minor ticks for all years
    major_ticks = years[::2]  # Every 2nd year for labels
    ax.set_xticks(major_ticks, minor=False)  # Major ticks with labels
    ax.set_xticks(years, minor=True)         # Minor ticks for all years
    ax.tick_params(axis='x', which='minor', length=3, colors=theme['tick_color'])
    ax.tick_params(axis='x', which='major', length=6, colors=theme['tick_color'])
    ax.tick_params(axis='y', colors=theme['tick_color'])

    # Integer y-axis (h-index is always integer)
    ax.yaxis.set_major_locator(plt.MaxNLocator(integer=True))

    # Configure grid with theme colors
    ax.grid(GRID['visible'],
            alpha=theme['grid_alpha'],
            linestyle=GRID['linestyle'],
            linewidth=GRID['linewidth'],
            color=theme['grid_color'])
    ax.set_axisbelow(True)  # Grid behind plot elements

    # Style spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    for spine in ['bottom', 'left']:
        ax.spines[spine].set_color(theme['spine_color'])

    # Apply tight layout
    if LAYOUT['tight_layout']:
        plt.tight_layout(pad=LAYOUT['pad'])

    # Save both SVG and PNG
    plots_dir = get_public_plots_dir()

    plot_path_svg = plots_dir / f"h_index_timeline{suffix}.svg"
    plt.savefig(plot_path_svg,
                format='svg',
                dpi=OUTPUT['svg_dpi'],
                bbox_inches=OUTPUT['bbox_inches'],
                transparent=(theme_name == 'dark'))
    print(f"📈 Plot saved to {get_relative_path(plot_path_svg)}")

    plot_path_png = plots_dir / f"h_index_timeline{suffix}.png"
    plt.savefig(plot_path_png,
                format='png',
                dpi=OUTPUT['png_dpi'],
                bbox_inches=OUTPUT['bbox_inches'],
                transparent=(theme_name == 'dark'))
    print(f"📈 Plot saved to {get_relative_path(plot_path_png)}")

    plt.close()


if __name__ == '__main__':
    for theme_name in THEMES:
        generate_h_index_plot(theme_name)
    print("\n✓ H-index timeline generation complete")
