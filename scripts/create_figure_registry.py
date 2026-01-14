#!/usr/bin/env python3
"""Extract all figures from topic JSONs into a centralized registry."""

import json
from pathlib import Path
from collections import OrderedDict

def create_figure_registry():
    repo_root = Path(__file__).parent.parent
    topics_dir = repo_root / "public" / "data" / "research-topics"
    output_path = repo_root / "public" / "data" / "figure-registry.json"

    registry = OrderedDict()

    # Track which topics use each figure
    figure_usage = {}

    for json_path in sorted(topics_dir.glob("*.json")):
        with open(json_path) as f:
            topic = json.load(f)

        slug = topic["slug"]

        # Process primary figure
        pf = topic["primary_figure"]
        fig_key = f"{pf['paper_id']}/{pf['figure_id']}"

        if fig_key not in registry:
            registry[fig_key] = {
                "paper_id": pf["paper_id"],
                "figure_id": pf["figure_id"],
                "src": pf["src"],
                "short_title": pf["short_title"],
                "alt": pf["alt"],
                "summary": pf["summary"],  # Extended summary for primary figures
                "summary_short": None,  # Will be filled if also used as related
                "keywords": pf.get("keywords", [])
            }
            figure_usage[fig_key] = {"primary_in": [], "related_in": []}

        figure_usage[fig_key]["primary_in"].append(slug)

        # Process related figures
        for rf in topic.get("related_figures", []):
            fig_key = f"{rf['paper_id']}/{rf['figure_id']}"

            if fig_key not in registry:
                registry[fig_key] = {
                    "paper_id": rf["paper_id"],
                    "figure_id": rf["figure_id"],
                    "src": rf["src"],
                    "short_title": rf["short_title"],
                    "alt": rf["alt"],
                    "summary": None,  # No extended summary for related-only figures
                    "summary_short": rf["summary_short"],
                    "keywords": []
                }
                figure_usage[fig_key] = {"primary_in": [], "related_in": []}
            else:
                # Figure exists, maybe add summary_short if we don't have it
                if registry[fig_key]["summary_short"] is None:
                    registry[fig_key]["summary_short"] = rf["summary_short"]

            figure_usage[fig_key]["related_in"].append(slug)

    # Add usage metadata to each figure
    for fig_key, usage in figure_usage.items():
        registry[fig_key]["used_as_primary_in"] = usage["primary_in"]
        registry[fig_key]["used_as_related_in"] = usage["related_in"]

    # Write registry
    with open(output_path, "w") as f:
        json.dump(registry, f, indent=2)

    print(f"Created figure registry with {len(registry)} figures")
    print(f"Output: {output_path}")

    # Print summary
    print("\nFigure inventory:")
    for fig_key, fig_data in registry.items():
        primary = fig_data["used_as_primary_in"]
        related = fig_data["used_as_related_in"]
        print(f"  {fig_key}")
        if primary:
            print(f"    Primary in: {', '.join(primary)}")
        if related:
            print(f"    Related in: {', '.join(related)}")

if __name__ == "__main__":
    create_figure_registry()
