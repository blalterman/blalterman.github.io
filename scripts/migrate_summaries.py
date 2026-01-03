#!/usr/bin/env python3
"""
Migrate figure summaries from for-integration to public/papers/{paper_id}/figures/.

This is a one-time migration script as part of the figure integration project.
Source: for-integration/public/data/figure_summaries/{paper_id}/figure_summaries.json
Target: public/papers/{paper_id}/figures/figure_summaries.json
"""

import json
import shutil
from pathlib import Path

from utils import get_repo_root


def get_source_dir() -> Path:
    """Get the for-integration figure summaries directory."""
    return get_repo_root() / "for-integration" / "public" / "data" / "figure_summaries"


def get_target_dir() -> Path:
    """Get the public/papers directory."""
    return get_repo_root() / "public" / "papers"


def migrate_summaries(dry_run: bool = False) -> None:
    """
    Migrate figure_summaries.json files from for-integration to public/papers/.

    Args:
        dry_run: If True, print what would be done without copying files.
    """
    source_dir = get_source_dir()
    target_dir = get_target_dir()

    if not source_dir.exists():
        raise FileNotFoundError(f"Source directory not found: {source_dir}")

    if not target_dir.exists():
        raise FileNotFoundError(
            f"Target directory not found: {target_dir}\n"
            "Run: mkdir -p public/papers/{{paper_id}}/figures/ first"
        )

    # Find all paper directories in source
    paper_dirs = [d for d in source_dir.iterdir() if d.is_dir()]

    print(f"Found {len(paper_dirs)} paper directories to migrate")
    print(f"Source: {source_dir}")
    print(f"Target: {target_dir}")
    print()

    migrated = 0
    skipped = 0
    errors = 0

    for paper_dir in sorted(paper_dirs):
        paper_id = paper_dir.name
        source_file = paper_dir / "figure_summaries.json"
        target_paper_dir = target_dir / paper_id / "figures"
        target_file = target_paper_dir / "figure_summaries.json"

        if not source_file.exists():
            print(f"  SKIP: {paper_id} - no figure_summaries.json")
            skipped += 1
            continue

        if not target_paper_dir.exists():
            print(f"  ERROR: {paper_id} - target directory missing: {target_paper_dir}")
            errors += 1
            continue

        if dry_run:
            print(f"  WOULD COPY: {paper_id}")
            print(f"    From: {source_file}")
            print(f"    To:   {target_file}")
        else:
            # Validate JSON before copying
            try:
                with open(source_file, 'r') as f:
                    data = json.load(f)
                figures_count = len(data.get('figures', []))
            except json.JSONDecodeError as e:
                print(f"  ERROR: {paper_id} - invalid JSON: {e}")
                errors += 1
                continue

            # Copy the file
            shutil.copy2(source_file, target_file)
            print(f"  COPIED: {paper_id} ({figures_count} figures)")
            migrated += 1

    print()
    print(f"Summary: {migrated} migrated, {skipped} skipped, {errors} errors")

    if dry_run:
        print("\nThis was a dry run. Run without --dry-run to perform migration.")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Migrate figure summaries from for-integration to public/papers/"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print what would be done without copying files"
    )

    args = parser.parse_args()
    migrate_summaries(dry_run=args.dry_run)
