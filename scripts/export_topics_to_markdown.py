#!/usr/bin/env python3
"""Export research topic JSON files to markdown for review."""

import json
from pathlib import Path

def export_topic_to_markdown(json_path: Path, output_dir: Path) -> Path:
    """Convert a research topic JSON to a markdown file for review."""
    with open(json_path) as f:
        data = json.load(f)

    slug = data['slug']
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
    lines.append(data['subtitle'])
    lines.append("")

    # Description
    lines.append("## Description")
    lines.append("")
    lines.append(data['description'])
    lines.append("")

    # Primary Figure
    pf = data['primary_figure']
    lines.append("---")
    lines.append("")
    lines.append("## Primary Figure")
    lines.append("")
    lines.append(f"**Figure:** `{pf['paper_id']}/{pf['figure_id']}`")
    lines.append("")
    lines.append("### Short Title")
    lines.append("")
    lines.append(pf['short_title'])
    lines.append("")
    lines.append("### Alt Text")
    lines.append("")
    lines.append(pf['alt'])
    lines.append("")
    lines.append("### What We See")
    lines.append("")
    lines.append(pf['summary']['what_we_see'])
    lines.append("")
    lines.append("### The Finding")
    lines.append("")
    lines.append(pf['summary']['the_finding'])
    lines.append("")
    lines.append("### Why It Matters")
    lines.append("")
    lines.append(pf['summary']['why_it_matters'])
    lines.append("")
    lines.append("### Keywords")
    lines.append("")
    lines.append(", ".join(pf['keywords']))
    lines.append("")

    # Related Figures
    if data.get('related_figures'):
        lines.append("---")
        lines.append("")
        lines.append("## Related Figures")
        lines.append("")

        for i, rf in enumerate(data['related_figures'], 1):
            lines.append(f"### Related Figure {i}: `{rf['paper_id']}/{rf['figure_id']}`")
            lines.append("")
            lines.append(f"**Short Title:** {rf['short_title']}")
            lines.append("")
            lines.append(f"**Alt Text:** {rf['alt']}")
            lines.append("")
            lines.append(f"**Relevance:** {rf['relevance']}")
            lines.append("")
            lines.append(f"**Summary:** {rf['summary_short']}")
            lines.append("")

    # Related Topics
    if data.get('related_topics'):
        lines.append("---")
        lines.append("")
        lines.append("## Related Topics")
        lines.append("")
        for rt in data['related_topics']:
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

    with open(output_path, 'w') as f:
        f.write('\n'.join(lines))

    return output_path


def main():
    repo_root = Path(__file__).parent.parent
    topics_dir = repo_root / "public" / "data" / "research-topics"
    output_dir = repo_root / "review-docs"
    output_dir.mkdir(exist_ok=True)

    json_files = sorted(topics_dir.glob("*.json"))

    print(f"Exporting {len(json_files)} topics to markdown...")

    for json_path in json_files:
        output_path = export_topic_to_markdown(json_path, output_dir)
        print(f"  {json_path.name} -> {output_path.name}")

    print(f"\nMarkdown files created in: {output_dir}")


if __name__ == "__main__":
    main()
