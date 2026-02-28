#!/usr/bin/env python3
"""
Generate figure-registry.json from the research-corpus submodule.

This script reads paper_metadata.json from each paper in the corpus,
extracts figure descriptions (summaries, keywords, technical captions),
and produces a centralized registry keyed by "paper_id/figure_id".

The corpus figure_id is used directly as the registry key, matching
the SVG filenames produced by convert-pdfs.yml. No ID translation needed.

Usage:
    python scripts/generate_figure_registry_from_corpus.py [--dry-run]
"""

import json
import sys
from collections import OrderedDict
from pathlib import Path

from utils import get_repo_root, get_public_data_dir


def load_corpus_metadata(corpus_dir: Path) -> dict[str, dict]:
    """Load paper_metadata.json from all papers in the corpus."""
    papers = {}
    for paper_dir in sorted(corpus_dir.glob("papers/*")):
        meta_path = paper_dir / "paper_metadata.json"
        if meta_path.exists():
            with open(meta_path) as f:
                data = json.load(f)
            paper_id = data["paper"]["id"]
            papers[paper_id] = data
    return papers


def determine_extension(paper_id: str, figure_id: str, repo_root: Path) -> str:
    """Check if the figure is SVG or PNG on the website."""
    figures_dir = repo_root / "public" / "papers" / paper_id / "figures"
    if (figures_dir / f"{figure_id}.png").exists():
        return "png"
    return "svg"


def load_topic_refs(data_dir: Path) -> dict[str, dict]:
    """
    Load topic JSONs and extract figure usage information.

    Returns:
        {ref_key: {"primary_in": [slugs], "related_in": [slugs]}}
    """
    topics_dir = data_dir / "research-topics"
    usage = {}

    for json_path in sorted(topics_dir.glob("*.json")):
        with open(json_path) as f:
            topic = json.load(f)

        slug = topic["slug"]

        # Primary figure
        ref = topic["primary_figure"]["ref"]
        if ref not in usage:
            usage[ref] = {"primary_in": [], "related_in": []}
        usage[ref]["primary_in"].append(slug)

        # Related figures
        for rf in topic.get("related_figures", []):
            ref = rf["ref"]
            if ref not in usage:
                usage[ref] = {"primary_in": [], "related_in": []}
            usage[ref]["related_in"].append(slug)

    return usage


def generate_registry(
    papers: dict[str, dict],
    topic_usage: dict[str, dict],
    repo_root: Path,
) -> OrderedDict:
    """Generate the figure registry from corpus data."""
    registry = OrderedDict()

    for paper_id in sorted(papers.keys()):
        paper_data = papers[paper_id]

        for fig in paper_data["figures"]:
            figure_id = fig["figure_id"]
            registry_key = f"{paper_id}/{figure_id}"

            # Determine file extension (SVG or PNG fallback)
            ext = determine_extension(paper_id, figure_id, repo_root)
            src = f"/papers/{paper_id}/figures/{figure_id}.{ext}"

            # Extract summary fields
            summary_data = fig.get("summary")
            if summary_data and isinstance(summary_data, dict):
                summary = {
                    "what_we_see": summary_data.get("what_we_see", ""),
                    "the_finding": summary_data.get("the_finding", ""),
                    "why_it_matters": summary_data.get("why_it_matters", ""),
                }
            else:
                summary = None

            # Extract keywords from metadata
            keywords = fig.get("metadata", {}).get("keywords", [])

            # Build short_title
            short_title = fig.get("short_title", "")

            # Build alt text (use first sentence of what_we_see, or short_title)
            if summary and summary["what_we_see"]:
                first_sentence = summary["what_we_see"].split(". ")[0] + "."
                alt = first_sentence
            else:
                alt = short_title

            # Build summary_short (first sentence of the_finding)
            if summary and summary["the_finding"]:
                summary_short = summary["the_finding"].split(". ")[0] + "."
            else:
                summary_short = None

            # Get usage from topic refs
            usage = topic_usage.get(registry_key, {"primary_in": [], "related_in": []})

            entry = OrderedDict([
                ("paper_id", paper_id),
                ("figure_id", figure_id),
                ("src", src),
                ("short_title", short_title),
                ("alt", alt),
                ("summary", summary),
                ("summary_short", summary_short),
                ("keywords", keywords),
                ("technical_caption", fig.get("technical_caption", "")),
                ("used_as_primary_in", usage["primary_in"]),
                ("used_as_related_in", usage["related_in"]),
            ])

            registry[registry_key] = entry

    return registry


def verify_topic_refs(registry: OrderedDict, topic_usage: dict[str, dict]) -> list[str]:
    """Verify that all topic JSON refs resolve against the registry."""
    errors = []
    for ref_key in topic_usage:
        if ref_key not in registry:
            errors.append(f"Topic ref '{ref_key}' not found in registry")
    return errors


def verify_src_paths(registry: OrderedDict, repo_root: Path) -> list[str]:
    """Verify that all src paths point to existing files."""
    errors = []
    for key, entry in registry.items():
        src = entry["src"]
        file_path = repo_root / "public" / src.lstrip("/")
        if not file_path.exists():
            errors.append(f"Missing file for '{key}': {src}")
    return errors


def main():
    dry_run = "--dry-run" in sys.argv

    repo_root = get_repo_root()
    corpus_dir = repo_root / "research-corpus"
    data_dir = get_public_data_dir()
    output_path = data_dir / "figure-registry.json"

    print("Loading corpus metadata...")
    papers = load_corpus_metadata(corpus_dir)
    print(f"  Found {len(papers)} papers")

    print("Loading topic JSON refs...")
    topic_usage = load_topic_refs(data_dir)
    print(f"  Found {len(topic_usage)} unique figure refs across topics")

    print("Generating registry...")
    registry = generate_registry(papers, topic_usage, repo_root)
    print(f"  Generated {len(registry)} registry entries")

    # Verify all topic refs resolve
    ref_errors = verify_topic_refs(registry, topic_usage)
    if ref_errors:
        print("\nERRORS - unresolved topic refs:")
        for err in ref_errors:
            print(f"  ✗ {err}")
        print("\nRegistry NOT written due to errors.")
        return 1

    print("\nAll topic refs resolve successfully ✓")

    # Verify all src paths exist
    src_errors = verify_src_paths(registry, repo_root)
    if src_errors:
        print("\nWARNINGS - missing figure files:")
        for err in src_errors:
            print(f"  ⚠ {err}")

    # Print summary
    primary_count = sum(1 for e in registry.values() if e["used_as_primary_in"])
    related_count = sum(1 for e in registry.values() if e["used_as_related_in"])
    print(f"\nRegistry summary:")
    print(f"  Total entries: {len(registry)}")
    print(f"  Used as primary: {primary_count}")
    print(f"  Used as related: {related_count}")
    print(f"  Papers covered: {len(set(e['paper_id'] for e in registry.values()))}")

    if dry_run:
        print(f"\nDry run — would write to {output_path}")
        # Print first entry as sample
        first_key = next(iter(registry))
        print(f"\nSample entry ({first_key}):")
        print(json.dumps(registry[first_key], indent=2)[:500])
    else:
        with open(output_path, "w") as f:
            json.dump(registry, f, indent=2, ensure_ascii=False)
        print(f"\nWrote registry to {output_path}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
