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
from plot_config import COLORS, FIGURE, FONTS, LINES, GRID, AXES, LAYOUT, OUTPUT


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

    current_h = metrics.get("indicators", {}).get("h", h_values[-1] if h_values else 0)

    print(f"   Current h-index: {current_h}")
    print(f"   Time span: {years[0]}-{years[-1]} ({len(years)} years)")

    return years, h_values


def generate_h_index_plot():
    """Generate and save h-index timeline plot."""
    years, h_values = load_h_index_data()

    # Create figure with configured settings
    fig, ax = plt.subplots(figsize=FIGURE['figsize'], dpi=FIGURE['dpi'])
    fig.patch.set_facecolor(FIGURE['facecolor'])

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

    # Apply styling
    ax.set_title('H-Index Timeline', **FONTS['title'])
    ax.set_xlabel('Year', **FONTS['axis_label'])
    ax.set_ylabel('h-index', **FONTS['axis_label'])

    # Configure x-axis: label every 2nd year, minor ticks for all years
    major_ticks = years[::2]  # Every 2nd year for labels
    ax.set_xticks(major_ticks, minor=False)  # Major ticks with labels
    ax.set_xticks(years, minor=True)         # Minor ticks for all years
    ax.tick_params(axis='x', which='minor', length=3)  # Shorter minor ticks
    ax.tick_params(axis='x', which='major', length=6)  # Standard major ticks

    # Integer y-axis (h-index is always integer)
    ax.yaxis.set_major_locator(plt.MaxNLocator(integer=True))

    # Configure grid
    ax.grid(GRID['visible'],
            alpha=GRID['alpha'],
            linestyle=GRID['linestyle'],
            linewidth=GRID['linewidth'],
            color=GRID['color'])
    ax.set_axisbelow(True)  # Grid behind plot elements

    # Hide top and right spines for cleaner look
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # Apply tight layout
    if LAYOUT['tight_layout']:
        plt.tight_layout(pad=LAYOUT['pad'])

    # Save both SVG and PNG
    plots_dir = get_public_plots_dir()

    # Save SVG
    plot_path_svg = plots_dir / "h_index_timeline.svg"
    plt.savefig(plot_path_svg,
                format='svg',
                dpi=OUTPUT['svg_dpi'],
                bbox_inches=OUTPUT['bbox_inches'])
    print(f"📈 Plot saved to {get_relative_path(plot_path_svg)}")

    # Save PNG
    plot_path_png = plots_dir / "h_index_timeline.png"
    plt.savefig(plot_path_png,
                format='png',
                dpi=OUTPUT['png_dpi'],
                bbox_inches=OUTPUT['bbox_inches'])
    print(f"📈 Plot saved to {get_relative_path(plot_path_png)}")

    plt.close()


if __name__ == '__main__':
    generate_h_index_plot()
    print("\n✓ H-index timeline generation complete")
