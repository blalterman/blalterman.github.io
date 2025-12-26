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
from plot_config import COLORS, FIGURE, FONTS, LINES, GRID, LEGEND, LAYOUT, OUTPUT

# === SECTION 1: Load Publications Data ===
public_data_dir = get_public_data_dir()
input_file = public_data_dir / "ads_publications.json"

if not input_file.exists():
    raise FileNotFoundError(
        f"Publications data not found at {get_relative_path(input_file)}. "
        "Run fetch_ads_publications_to_data_dir.py first."
    )

print(f"📖 Loading publications from {get_relative_path(input_file)}")
with open(input_file, 'r') as f:
    publications = json.load(f)

print(f"   Loaded {len(publications)} publications")

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

# Extract data for plotting
all_years = counts.index.tolist()
refereed = counts.get('Refereed Articles', pd.Series(0, index=counts.index)).tolist()
conferences = counts.get('Conference Contributions', pd.Series(0, index=counts.index)).tolist()
other = counts.get('Other Publications', pd.Series(0, index=counts.index)).tolist()

print("\n📊 Publication counts by year:")
print(counts)
print(f"\n✓ Total publications: {len(df)}")
print(f"  • Refereed Articles: {sum(refereed)}")
print(f"  • Conference Contributions: {sum(conferences)}")
print(f"  • Other Publications: {sum(other)}")

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

# === SECTION 4: Generate Line Plot ===
image_output_dir = get_public_plots_dir()
image_output_dir.mkdir(parents=True, exist_ok=True)

# Create figure with configured settings
fig, ax = plt.subplots(figsize=FIGURE['figsize'], dpi=FIGURE['dpi'])
fig.patch.set_facecolor(FIGURE['facecolor'])

# Plot lines with configured styles
ax.plot(all_years, refereed,
        label='Refereed Articles',
        color=COLORS['refereed'],
        **LINES['refereed'])

ax.plot(all_years, conferences,
        label='Conference Contributions',
        color=COLORS['conference'],
        **LINES['conference'])

ax.plot(all_years, other,
        label='Other Publications',
        color=COLORS['other'],
        **LINES['other'])

# Apply styling
ax.set_title('Publications Timeline', **FONTS['title'])
ax.set_xlabel('Year', **FONTS['axis_label'])
ax.set_ylabel('Number of Publications', **FONTS['axis_label'])

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

# === SECTION 5: Save Plots ===
# Save SVG
plot_path_svg = image_output_dir / "publications_timeline.svg"
plt.savefig(plot_path_svg,
            format='svg',
            dpi=OUTPUT['svg_dpi'],
            bbox_inches=OUTPUT['bbox_inches'])
print(f"📈 Plot saved to {get_relative_path(plot_path_svg)}")

# Save PNG
plot_path_png = image_output_dir / "publications_timeline.png"
plt.savefig(plot_path_png,
            format='png',
            dpi=OUTPUT['png_dpi'],
            bbox_inches=OUTPUT['bbox_inches'])
print(f"📈 Plot saved to {get_relative_path(plot_path_png)}")

print("\n✓ Publications timeline generation complete")
