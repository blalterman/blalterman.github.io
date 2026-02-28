#!/usr/bin/env python3
"""Export research topic JSON files to markdown for review.

Joins topic JSONs with the centralized figure registry to produce
complete markdown documents for track-changes review in Word.
"""

import json
from pathlib import Path


def load_figure_registry(repo_root: Path) -> dict:
    """Load the centralized figure registry."""
    registry_path = repo_root / "public" / "data" / "figure-registry.json"
    with open(registry_path) as f:
        return json.load(f)


def export_topic_to_markdown(
    json_path: Path, output_dir: Path, registry: dict
) -> Path:
    """Convert a research topic JSON to a markdown file for review.

    Resolves figure refs against the registry to include all metadata.
    """
    with open(json_path) as f:
        data = json.load(f)

    slug = data["slug"]
    output_path = output_dir / f"{slug}.md"

    lines = []

    # Header
    lines.append(f"# {data['title']}")
    lines.append("")
    lines.append(f"**Slug:** `{slug}`")
    lines.append("")

    # Subtitle
    lines.append("## Subtitle")
    lines.append("")
    lines.append(data["subtitle"])
    lines.append("")

    # Description
    lines.append("## Description")
    lines.append("")
    lines.append(data["description"])
    lines.append("")

    # Primary Figure
    pf_ref = data["primary_figure"]["ref"]
    pf_entry = registry.get(pf_ref, {})
    topic_keywords = data["primary_figure"].get("topic_keywords", [])

    lines.append("---")
    lines.append("")
    lines.append("## Primary Figure")
    lines.append("")
    lines.append(f"**Figure:** `{pf_ref}`")
    lines.append("")

    if pf_entry.get("short_title"):
        lines.append("### Short Title")
        lines.append("")
        lines.append(pf_entry["short_title"])
        lines.append("")

    if pf_entry.get("alt"):
        lines.append("### Alt Text")
        lines.append("")
        lines.append(pf_entry["alt"])
        lines.append("")

    if pf_entry.get("summary"):
        summary = pf_entry["summary"]
        lines.append("### What We See")
        lines.append("")
        lines.append(summary["what_we_see"])
        lines.append("")
        lines.append("### The Finding")
        lines.append("")
        lines.append(summary["the_finding"])
        lines.append("")
        lines.append("### Why It Matters")
        lines.append("")
        lines.append(summary["why_it_matters"])
        lines.append("")

    # Merge keywords: registry + topic-specific
    registry_keywords = pf_entry.get("keywords", [])
    all_keywords = list(dict.fromkeys(registry_keywords + topic_keywords))
    if all_keywords:
        lines.append("### Keywords")
        lines.append("")
        lines.append(", ".join(all_keywords))
        lines.append("")

    # Related Figures
    if data.get("related_figures"):
        lines.append("---")
        lines.append("")
        lines.append("## Related Figures")
        lines.append("")

        for i, rf in enumerate(data["related_figures"], 1):
            rf_ref = rf["ref"]
            rf_entry = registry.get(rf_ref, {})

            lines.append(f"### Related Figure {i}: `{rf_ref}`")
            lines.append("")

            if rf_entry.get("short_title"):
                lines.append(f"**Short Title:** {rf_entry['short_title']}")
                lines.append("")

            if rf_entry.get("alt"):
                lines.append(f"**Alt Text:** {rf_entry['alt']}")
                lines.append("")

            lines.append(f"**Relevance:** {rf.get('relevance', 'N/A')}")
            lines.append("")

            if rf_entry.get("summary_short"):
                lines.append(f"**Summary:** {rf_entry['summary_short']}")
                lines.append("")

    # Related Topics
    if data.get("related_topics"):
        lines.append("---")
        lines.append("")
        lines.append("## Related Topics")
        lines.append("")
        for rt in data["related_topics"]:
            lines.append(f"- **{rt['slug']}**: {rt['connection']}")
        lines.append("")

    # Paper metadata (for reference, not editing)
    lines.append("---")
    lines.append("")
    lines.append("## Source Paper (reference only)")
    lines.append("")
    lines.append(f"- **Title:** {data['paper']['title']}")
    lines.append(f"- **DOI:** {data['paper']['doi']}")
    lines.append(f"- **Bibcode:** {data['paper']['bibcode']}")
    lines.append(f"- **Year:** {data['paper']['year']}")
    lines.append("")

    with open(output_path, "w") as f:
        f.write("\n".join(lines))

    return output_path


def main():
    repo_root = Path(__file__).parent.parent
    topics_dir = repo_root / "public" / "data" / "research-topics"
    output_dir = repo_root / "review-docs"
    output_dir.mkdir(exist_ok=True)

    registry = load_figure_registry(repo_root)
    print(f"Loaded figure registry: {len(registry)} figures")

    json_files = sorted(topics_dir.glob("*.json"))
    print(f"Exporting {len(json_files)} topics to markdown...\n")

    for json_path in json_files:
        output_path = export_topic_to_markdown(json_path, output_dir, registry)
        print(f"  {json_path.name} -> {output_path.name}")

    print(f"\nMarkdown files created in: {output_dir}")


if __name__ == "__main__":
    main()
