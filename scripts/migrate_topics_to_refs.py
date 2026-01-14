#!/usr/bin/env python3
"""Migrate topic JSONs to use figure registry references."""

import json
from pathlib import Path

def migrate_topics():
    repo_root = Path(__file__).parent.parent
    topics_dir = repo_root / "public" / "data" / "research-topics"

    for json_path in sorted(topics_dir.glob("*.json")):
        with open(json_path) as f:
            topic = json.load(f)

        slug = topic["slug"]
        print(f"Migrating: {slug}")

        # Migrate primary figure
        pf = topic["primary_figure"]
        fig_ref = f"{pf['paper_id']}/{pf['figure_id']}"

        # Keep only ref and topic-specific keywords (merged at render time)
        topic["primary_figure"] = {
            "ref": fig_ref,
            "topic_keywords": pf.get("keywords", [])  # Topic can add keywords
        }

        # Migrate related figures
        new_related = []
        for rf in topic.get("related_figures", []):
            fig_ref = f"{rf['paper_id']}/{rf['figure_id']}"
            new_related.append({
                "ref": fig_ref,
                "relevance": rf["relevance"]
            })
        topic["related_figures"] = new_related

        # Write updated topic
        with open(json_path, "w") as f:
            json.dump(topic, f, indent=2)

        print(f"  Primary: {topic['primary_figure']['ref']}")
        print(f"  Related: {len(new_related)} figures")

    print("\nMigration complete!")

if __name__ == "__main__":
    migrate_topics()
