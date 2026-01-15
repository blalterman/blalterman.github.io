#!/usr/bin/env python3
"""Export figure registry to markdown for Word review."""

import json
from pathlib import Path

def export_registry_to_markdown():
    repo_root = Path(__file__).parent.parent
    registry_path = repo_root / "public" / "data" / "figure-registry.json"
    output_path = repo_root / "review-docs" / "figure-registry.md"

    with open(registry_path) as f:
        registry = json.load(f)

    lines = []
    lines.append("# Figure Registry")
    lines.append("")
    lines.append(f"**Total figures:** {len(registry)}")
    lines.append("")
    lines.append("---")
    lines.append("")

    for fig_key, fig in registry.items():
        lines.append(f"## {fig_key}")
        lines.append("")
        lines.append(f"**Short Title:** {fig['short_title']}")
        lines.append("")
        # Embed the figure image
        # Convert src path to absolute path for pandoc
        fig_path = str(repo_root / "public" / fig['src'].lstrip('/'))
        lines.append(f"![{fig['alt']}]({fig_path})")
        lines.append("")
        lines.append(f"**File:** `{fig['src']}`")
        lines.append("")

        # Usage info
        primary_in = fig.get("used_as_primary_in", [])
        related_in = fig.get("used_as_related_in", [])
        if primary_in:
            lines.append(f"**Primary in:** {', '.join(primary_in)}")
        if related_in:
            lines.append(f"**Related in:** {', '.join(related_in)}")
        lines.append("")

        # Alt text
        lines.append("### Alt Text")
        lines.append("")
        lines.append(fig["alt"])
        lines.append("")

        # Extended summary (if exists)
        if fig.get("summary"):
            lines.append("### What We See")
            lines.append("")
            lines.append(fig["summary"]["what_we_see"])
            lines.append("")
            lines.append("### The Finding")
            lines.append("")
            lines.append(fig["summary"]["the_finding"])
            lines.append("")
            lines.append("### Why It Matters")
            lines.append("")
            lines.append(fig["summary"]["why_it_matters"])
            lines.append("")

        # Short summary (for related figures)
        if fig.get("summary_short"):
            lines.append("### Summary (Short)")
            lines.append("")
            lines.append(fig["summary_short"])
            lines.append("")

        # Keywords
        if fig.get("keywords"):
            lines.append("### Keywords")
            lines.append("")
            lines.append(", ".join(fig["keywords"]))
            lines.append("")

        lines.append("---")
        lines.append("")

    output_path.parent.mkdir(exist_ok=True)
    with open(output_path, "w") as f:
        f.write("\n".join(lines))

    print(f"Exported to: {output_path}")
    return output_path

if __name__ == "__main__":
    export_registry_to_markdown()
