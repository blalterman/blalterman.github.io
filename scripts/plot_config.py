"""
Shared plotting configuration for academic productivity visualizations.

Ensures consistent styling across publications timeline and citations plots.
"""

# === COLOR PALETTE ===
COLORS = {
    # Primary categories
    'refereed': '#6495ED',          # cornflowerblue - peer-reviewed work
    'conference': '#F08080',        # lightcoral - conference contributions
    'other': '#90EE90',             # lightgreen - other scholarly outputs
    'nonrefereed': '#90EE90',       # lightgreen - non-refereed citations

    # Accent colors (for future expansion)
    'preprint': '#FFB366',          # light orange
    'dataset': '#9370DB',           # medium purple
    'highlight': '#FF6B6B',         # light red
}

# === FIGURE SETTINGS ===
FIGURE = {
    'figsize': (5, 3.5),            # Width x Height in inches
    'dpi': 300,                     # Resolution for PNG output
    'facecolor': 'white',           # Background color
}

# === FONT SETTINGS ===
FONTS = {
    'title': {
        'size': 14,
        'weight': 'bold',
        'family': 'sans-serif',
    },
    'axis_label': {
        'size': 12,
        'weight': 'normal',
    },
    'tick_label': {
        'size': 10,
    },
    'legend': {
        'size': 10,
    },
}

# === LINE/MARKER STYLES ===
LINES = {
    'refereed': {
        'linewidth': 2.5,
        'marker': 'o',              # circle
        'markersize': 6,
        'linestyle': '-',           # solid
    },
    'conference': {
        'linewidth': 2.0,
        'marker': 's',              # square
        'markersize': 6,
        'linestyle': '-',
    },
    'other': {
        'linewidth': 1.5,
        'marker': 'D',              # diamond
        'markersize': 5,
        'linestyle': '--',          # dashed
    },
}

# === BAR STYLES ===
BARS = {
    'width': 0.8,                   # Bar width (0-1 scale)
    'alpha': 0.9,                   # Transparency (0-1)
    'edgecolor': 'none',            # Bar border color
}

# === GRID SETTINGS ===
GRID = {
    'visible': True,
    'alpha': 0.3,                   # Transparency
    'linestyle': ':',               # dotted
    'linewidth': 0.5,
    'color': 'gray',
}

# === LEGEND SETTINGS ===
LEGEND = {
    'loc': 'upper left',            # Position
    'frameon': True,                # Show box around legend
    'shadow': True,                 # Drop shadow
    'fancybox': True,               # Rounded corners
    'framealpha': 0.9,              # Legend box transparency
}

# === AXIS SETTINGS ===
AXES = {
    'grid': True,
    'axisbelow': True,              # Grid behind plot elements
    'spines': {
        'top': False,               # Hide top spine
        'right': False,             # Hide right spine
    },
}

# === LAYOUT ===
LAYOUT = {
    'tight_layout': True,           # Auto-adjust spacing
    'pad': 0.1,                     # Padding around figure
}

# === OUTPUT SETTINGS ===
OUTPUT = {
    'formats': ['svg', 'png'],      # File formats to generate
    'svg_dpi': 300,
    'png_dpi': 300,
    'bbox_inches': 'tight',         # Crop whitespace
}

# === THEME CONFIGURATIONS ===
THEMES = {
    'light': {
        'facecolor': 'white',
        'text_color': '#1f2937',       # gray-800
        'tick_color': '#1f2937',
        'spine_color': '#1f2937',
        'grid_color': 'gray',
        'grid_alpha': 0.3,
        'legend_facecolor': 'white',
        'legend_edgecolor': '#d1d5db',
        'legend_text_color': '#1f2937',
    },
    'dark': {
        'facecolor': 'none',           # transparent
        'text_color': '#d1d5db',       # gray-300
        'tick_color': '#d1d5db',
        'spine_color': '#4b5563',      # gray-600
        'grid_color': '#4b5563',
        'grid_alpha': 0.4,
        'legend_facecolor': '#1e293b', # slate-800
        'legend_edgecolor': '#4b5563',
        'legend_text_color': '#d1d5db',
    },
}


def get_theme_config(theme_name='light'):
    """Return theme config dict for a given theme name."""
    return THEMES.get(theme_name, THEMES['light'])
