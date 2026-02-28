#!/usr/bin/env python3
"""
Generate figure-registry.json from the research-corpus submodule.

This script reads paper_metadata.json from each paper in the corpus,
extracts figure descriptions (summaries, keywords, technical captions),
and produces a centralized registry keyed by "paper_id/figure_id".

Key complexity: The corpus uses paper-level figure numbering (with panel
suffixes like fig_10a), but the website SVGs use the original sequential
numbering from the first extraction. This script maps between them using
technical_caption matching against the old corpus metadata stored in git.

The registry keys use WEBSITE figure IDs (matching topic JSON refs and
SVG filenames), while descriptions come from the UPDATED corpus.

Usage:
    python scripts/generate_figure_registry_from_corpus.py [--dry-run]
"""

import json
import subprocess
import re
import sys
from collections import OrderedDict
from pathlib import Path

from utils import get_repo_root, get_public_data_dir


# The submodule commit that matches the website SVGs.
# Before this commit, figure numbering matched the website.
# After this commit, some papers had figures renumbered.
OLD_CORPUS_COMMIT = "f75299a"


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


def load_old_corpus_metadata(corpus_dir: Path, commit: str) -> dict[str, dict]:
    """Load paper_metadata.json from a previous corpus commit via git."""
    papers = {}
    # List paper directories at the old commit
    try:
        result = subprocess.run(
            ["git", "ls-tree", "--name-only", commit, "papers/"],
            capture_output=True, text=True, cwd=corpus_dir, check=True
        )
    except subprocess.CalledProcessError:
        print(f"WARNING: Could not read old corpus at commit {commit}")
        return papers

    for paper_path in result.stdout.strip().split("\n"):
        if not paper_path:
            continue
        # Ensure trailing slash for directory path
        if not paper_path.endswith("/"):
            paper_path += "/"
        meta_ref = f"{commit}:{paper_path}paper_metadata.json"
        try:
            raw = subprocess.run(
                ["git", "show", meta_ref],
                capture_output=True, text=True, cwd=corpus_dir, check=True
            )
            data = json.loads(raw.stdout)
            paper_id = data["paper"]["id"]
            papers[paper_id] = data
        except (subprocess.CalledProcessError, json.JSONDecodeError):
            continue

    return papers


def build_corpus_to_website_mapping(
    new_papers: dict[str, dict],
    old_papers: dict[str, dict],
) -> dict[str, dict[str, str | None]]:
    """
    Build mapping from new corpus figure_id to website figure_id.

    For figures that weren't renamed, the mapping is identity.
    For renamed/reordered figures, we match by technical_caption.
    For panel figures from combined originals, we use the old multi-file info.

    Returns:
        {paper_id: {corpus_figure_id: website_figure_id_or_None}}
        None means this panel figure has no individual website SVG.
    """
    mapping = {}

    for paper_id, new_data in new_papers.items():
        old_data = old_papers.get(paper_id)
        if not old_data:
            # No old data — assume identity mapping
            mapping[paper_id] = {
                f["figure_id"]: f["figure_id"]
                for f in new_data["figures"]
            }
            continue

        paper_map = {}

        # Build old caption → figure_id lookup using multiple prefix lengths
        # for robustness against caption rewrites
        old_by_caption = {}
        for fig in old_data["figures"]:
            cap_key = fig["technical_caption"][:150]
            old_by_caption[cap_key] = fig

        # Build old figure_id set for fallback identity matching
        old_ids = {fig["figure_id"] for fig in old_data["figures"]}

        # Track old figures with multi-file filenames (like 982_L40 fig_10)
        old_multifile = {}
        for fig in old_data["figures"]:
            if isinstance(fig.get("filename"), list):
                old_multifile[fig["figure_id"]] = fig["filename"]

        # Track which old captions have been claimed by a caption match,
        # to detect when multiple new panels each match different old figures.
        caption_claim_count = {}

        # Match new figures to old
        for fig in new_data["figures"]:
            new_id = fig["figure_id"]
            cap_key = fig["technical_caption"][:150]
            panel_id = fig.get("panel_id")

            old_fig = old_by_caption.get(cap_key)

            if old_fig:
                old_id = old_fig["figure_id"]
                caption_claim_count[cap_key] = caption_claim_count.get(cap_key, 0) + 1

                if not panel_id:
                    # Non-panel figure: direct mapping
                    paper_map[new_id] = old_id
                elif old_id in old_multifile:
                    # Panel figure from a multi-file old figure (e.g., 982_L40).
                    # Map panels to individual old filenames by position.
                    filenames = old_multifile[old_id]
                    panel_idx = ord(panel_id) - ord("a")
                    if panel_idx < len(filenames):
                        old_fname = filenames[panel_idx]
                        website_id = Path(old_fname).stem
                        paper_map[new_id] = website_id
                    else:
                        paper_map[new_id] = None
                elif caption_claim_count[cap_key] == 1:
                    # First panel to claim this caption — this panel uniquely
                    # matched a specific old figure (e.g., 879_L6 where each
                    # panel had its own caption in both old and new corpus).
                    paper_map[new_id] = old_id
                else:
                    # Multiple panels matched the SAME old caption, meaning
                    # this was a combined figure in the old corpus with only
                    # one caption. Only the first claimant maps; others skip.
                    paper_map[new_id] = None
            else:
                # No caption match. Two possible reasons:
                # 1. Captions were rewritten (but figure IDs stayed the same)
                # 2. New figure extraction (panel split, etc.)
                if not panel_id and new_id in old_ids:
                    # Same figure_id exists in old corpus — identity mapping.
                    # Captions may have been rewritten but it's the same figure.
                    paper_map[new_id] = new_id
                else:
                    # Try panel-based fallback
                    paper_map[new_id] = _find_unmatched_figure(
                        new_id, panel_id, old_data, paper_id
                    )

        mapping[paper_id] = paper_map

    return mapping


def _find_unmatched_figure(
    new_id: str,
    panel_id: str | None,
    old_data: dict,
    paper_id: str,
) -> str | None:
    """
    Handle figures that don't match any old caption.

    Known cases:
    - 952_42 fig_1c: a panel cropped from figure 1, was old fig_11
      (existed as file but not in metadata, had figure_number > last metadata entry)
    - 996_L12 fig_15a-d, fig_16a-b, fig_17a-b: panels split from combined figures
      (old had single combined figures with different captions per-panel)
    """
    if panel_id:
        # For panels from combined figures, map first panel to base figure
        base_num = re.match(r"fig_(\d+)", new_id)
        if base_num:
            base_id = f"fig_{base_num.group(1)}"
            # Check if old data had this base figure
            old_ids = {f["figure_id"] for f in old_data["figures"]}
            if base_id in old_ids:
                if panel_id == "a":
                    return base_id  # First panel → combined SVG
                else:
                    return None  # Other panels → no individual SVG
            else:
                # Base figure not in old metadata at all
                return None

    # Non-panel unmatched figure. Check if it exists as a website SVG
    # by looking at old metadata entry count (files were numbered sequentially).
    old_count = len(old_data["figures"])
    fig_num = re.match(r"fig_(\d+)", new_id)
    if fig_num:
        num = int(fig_num.group(1))
        # Check for figures beyond the old metadata count
        # (e.g., 952_42 fig_1c → old fig_11, which was file #11)
        # This is detected as being beyond old_count
        # We assign it to old_count + 1 if the SVG exists
        # For now, mark as needing manual check
        pass

    return None


def build_website_figure_id(
    paper_id: str,
    corpus_figure_id: str,
    mapping: dict[str, dict[str, str | None]],
) -> str | None:
    """Get the website figure ID for a corpus figure."""
    paper_map = mapping.get(paper_id, {})
    return paper_map.get(corpus_figure_id, corpus_figure_id)


def determine_svg_extension(paper_id: str, website_fig_id: str, repo_root: Path) -> str:
    """Check if the figure is SVG or PNG on the website."""
    figures_dir = repo_root / "public" / "papers" / paper_id / "figures"
    if (figures_dir / f"{website_fig_id}.png").exists():
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
    new_papers: dict[str, dict],
    mapping: dict[str, dict[str, str | None]],
    topic_usage: dict[str, dict],
    repo_root: Path,
) -> OrderedDict:
    """Generate the figure registry from corpus data."""
    registry = OrderedDict()

    for paper_id in sorted(new_papers.keys()):
        paper_data = new_papers[paper_id]

        for fig in paper_data["figures"]:
            corpus_id = fig["figure_id"]

            # Get website figure ID
            website_id = build_website_figure_id(paper_id, corpus_id, mapping)
            if website_id is None:
                # This panel has no individual website SVG — skip
                continue

            registry_key = f"{paper_id}/{website_id}"

            # Skip if we already have this entry (e.g., from a previous panel)
            if registry_key in registry:
                # Aggregate keywords from additional panels
                new_keywords = fig.get("metadata", {}).get("keywords", [])
                existing = registry[registry_key]["keywords"]
                for kw in new_keywords:
                    if kw not in existing:
                        existing.append(kw)
                continue

            # Determine SVG path
            ext = determine_svg_extension(paper_id, website_id, repo_root)
            src = f"/papers/{paper_id}/figures/{website_id}.{ext}"

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
                ("figure_id", website_id),
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


def main():
    dry_run = "--dry-run" in sys.argv

    repo_root = get_repo_root()
    corpus_dir = repo_root / "research-corpus"
    data_dir = get_public_data_dir()
    output_path = data_dir / "figure-registry.json"

    print("Loading current corpus metadata...")
    new_papers = load_corpus_metadata(corpus_dir)
    print(f"  Found {len(new_papers)} papers")

    print(f"Loading old corpus metadata (commit {OLD_CORPUS_COMMIT})...")
    old_papers = load_old_corpus_metadata(corpus_dir, OLD_CORPUS_COMMIT)
    print(f"  Found {len(old_papers)} papers")

    print("Building corpus → website figure ID mapping...")
    mapping = build_corpus_to_website_mapping(new_papers, old_papers)

    # Report mapping changes
    for paper_id in sorted(mapping.keys()):
        paper_map = mapping[paper_id]
        remaps = {k: v for k, v in paper_map.items() if v != k and v is not None}
        skipped = {k for k, v in paper_map.items() if v is None}
        if remaps or skipped:
            print(f"  {paper_id}:")
            for corpus_id, website_id in sorted(remaps.items()):
                print(f"    {corpus_id} → {website_id}")
            for corpus_id in sorted(skipped):
                print(f"    {corpus_id} → (no website SVG, skipped)")

    print("Loading topic JSON refs...")
    topic_usage = load_topic_refs(data_dir)
    print(f"  Found {len(topic_usage)} unique figure refs across topics")

    print("Generating registry...")
    registry = generate_registry(new_papers, mapping, topic_usage, repo_root)
    print(f"  Generated {len(registry)} registry entries")

    # Verify all topic refs resolve
    errors = verify_topic_refs(registry, topic_usage)
    if errors:
        print("\nERRORS - unresolved topic refs:")
        for err in errors:
            print(f"  ✗ {err}")
        print("\nRegistry NOT written due to errors.")
        return 1

    print("\nAll topic refs resolve successfully ✓")

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
