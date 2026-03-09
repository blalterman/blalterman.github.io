#!/usr/bin/env python3
"""
Generates a line plot showing publication counts by year and category.

Uses locally available publication data from ads_publications.json.
Outputs JSON data and SVG/PNG plots to public/ directories.

This script reads from existing data and does NOT make API calls.
It should run whenever publications data is updated.

Example
-------
$ python scripts/generate_publications_timeline.py

Saved 135 publications to public/data/publications_timeline.json
Plot saved to public/plots/publications_timeline.svg
Plot saved to public/plots/publications_timeline.png
"""

import json
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
from utils import get_public_data_dir, get_public_plots_dir, get_relative_path
from plot_config import COLORS, FIGURE, FONTS, LINES, GRID, LEGEND, LAYOUT, OUTPUT, THEMES, get_theme_config

# === SECTION 1: Load Publications Data ===
public_data_dir = get_public_data_dir()
ads_file = public_data_dir / "ads_publications.json"
invited_file = public_data_dir / "invited_presentations.json"

if not ads_file.exists():
    raise FileNotFoundError(
        f"Publications data not found at {get_relative_path(ads_file)}. "
        "Run fetch_ads_publications_to_data_dir.py first."
    )

non_ads_file = public_data_dir / "non_ads_publications.json"

print(f"📖 Loading ADS publications from {get_relative_path(ads_file)}")
with open(ads_file, 'r') as f:
    ads_publications = json.load(f)

# Merge non-ADS publications (conferences, white papers not indexed by ADS)
if non_ads_file.exists():
    with open(non_ads_file, 'r') as f:
        non_ads_publications = json.load(f)
    ads_publications = ads_publications + non_ads_publications
    print(f"   Loaded {len(ads_publications)} publications ({len(ads_publications) - len(non_ads_publications)} ADS + {len(non_ads_publications)} non-ADS)")
else:
    print(f"   Loaded {len(ads_publications)} ADS publications")

# Load invited presentations (seminars/colloquia not in ADS)
if invited_file.exists():
    print(f"📖 Loading invited presentations from {get_relative_path(invited_file)}")
    with open(invited_file, 'r') as f:
        invited_presentations = json.load(f)
    print(f"   Loaded {len(invited_presentations)} invited presentations")
    # Merge into publications list
    publications = ads_publications + invited_presentations
    print(f"   Total: {len(publications)} publications (ADS + invited)")
else:
    publications = ads_publications
    print(f"   No invited presentations file found, using ADS only")

# === SECTION 2: Data Processing ===
# Convert to DataFrame
df = pd.DataFrame(publications)

# Extract year from "YYYY-MM-DD" format
df['year'] = df['year'].str.split('-').str[0]
df = df[df['year'] != ''].copy()  # Filter out empty years
df['year'] = df['year'].astype(int)

# Define category mappings
category_map = {
    'article': 'Refereed Articles',
    'abstract': 'Conference Contributions',
    'inproceedings': 'Conference Contributions',
    'techreport': 'Other Publications',
    'eprint': 'Other Publications',
    'dataset': 'Other Publications',
    'phdthesis': 'Other Publications',
    'software': 'Other Publications',
}

df['category'] = df['publication_type'].map(category_map)

# Handle unmapped types
if df['category'].isna().any():
    unmapped = df[df['category'].isna()]['publication_type'].unique()
    print(f"⚠️  Warning: Unmapped publication types found: {unmapped}")
    df = df[df['category'].notna()]  # Drop unmapped for now

# Count publications by year and category
counts = df.groupby(['year', 'category']).size().unstack(fill_value=0)

# Ensure all years are present (fill gaps with zeros)
year_range = range(counts.index.min(), counts.index.max() + 1)
counts = counts.reindex(year_range, fill_value=0)

# Extract per-year data (kept for JSON output and summary)
all_years = counts.index.tolist()
refereed = counts.get('Refereed Articles', pd.Series(0, index=counts.index)).tolist()
conferences = counts.get('Conference Contributions', pd.Series(0, index=counts.index)).tolist()
other = counts.get('Other Publications', pd.Series(0, index=counts.index)).tolist()

# Compute cumulative sums for plotting (pandas native)
cum_refereed = counts.get('Refereed Articles', pd.Series(0, index=counts.index)).cumsum().tolist()
cum_conferences = counts.get('Conference Contributions', pd.Series(0, index=counts.index)).cumsum().tolist()
cum_other = counts.get('Other Publications', pd.Series(0, index=counts.index)).cumsum().tolist()

print("\n📊 Publication counts by year:")
print(counts)
print(f"\n✓ Total publications: {len(df)}")
print(f"  • Refereed Articles: {sum(refereed)}")
print(f"  • Conference Contributions: {sum(conferences)}")
print(f"  • Other Publications: {sum(other)}")
print(f"\n📈 Cumulative totals (final year):")
print(f"  • Refereed Articles: {cum_refereed[-1]}")
print(f"  • Conference Contributions: {cum_conferences[-1]}")
print(f"  • Other Publications: {cum_other[-1]}")

# === SECTION 3: Save JSON Data ===
output_filename = "publications_timeline.json"
output_path = public_data_dir / output_filename

data_to_save = {
    "years": all_years,
    "refereed_articles": refereed,
    "conference_contributions": conferences,
    "other_publications": other
}

with open(output_path, 'w') as f:
    json.dump(data_to_save, f, indent=2)

print(f"\n💾 Data saved to {get_relative_path(output_path)}")

# === SECTION 4: Generate Line Plots (light + dark) ===
image_output_dir = get_public_plots_dir()
image_output_dir.mkdir(parents=True, exist_ok=True)


def generate_plot(theme_name='light'):
    """Generate publications timeline plot for a given theme."""
    theme = get_theme_config(theme_name)
    suffix = '' if theme_name == 'light' else f'_{theme_name}'

    # Create figure with configured settings
    fig, ax = plt.subplots(figsize=FIGURE['figsize'], dpi=FIGURE['dpi'])
    fig.patch.set_facecolor(theme['facecolor'])
    ax.set_facecolor('none')

    # Plot lines with configured styles (cumulative data)
    ax.plot(all_years, cum_refereed,
            label='Refereed Articles',
            color=COLORS['refereed'],
            **LINES['refereed'])

    ax.plot(all_years, cum_conferences,
            label='Conference Contributions',
            color=COLORS['conference'],
            **LINES['conference'])

    ax.plot(all_years, cum_other,
            label='Other Publications',
            color=COLORS['other'],
            **LINES['other'])

    # Apply styling with theme colors
    ax.set_title('Cumulative Publications', color=theme['text_color'], **FONTS['title'])
    ax.set_xlabel('Year', color=theme['text_color'], **FONTS['axis_label'])
    ax.set_ylabel('Total Publications', color=theme['text_color'], **FONTS['axis_label'])

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
    plot_path_svg = image_output_dir / f"publications_timeline{suffix}.svg"
    plt.savefig(plot_path_svg,
                format='svg',
                dpi=OUTPUT['svg_dpi'],
                bbox_inches=OUTPUT['bbox_inches'],
                transparent=(theme_name == 'dark'))
    print(f"📈 Plot saved to {get_relative_path(plot_path_svg)}")

    plot_path_png = image_output_dir / f"publications_timeline{suffix}.png"
    plt.savefig(plot_path_png,
                format='png',
                dpi=OUTPUT['png_dpi'],
                bbox_inches=OUTPUT['bbox_inches'],
                transparent=(theme_name == 'dark'))
    print(f"📈 Plot saved to {get_relative_path(plot_path_png)}")

    plt.close()


for theme_name in THEMES:
    generate_plot(theme_name)

print("\n✓ Publications timeline generation complete")
