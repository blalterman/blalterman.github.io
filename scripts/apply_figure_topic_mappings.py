#!/usr/bin/env python3
"""
Apply domain expert's figure-to-topic mappings from reviewed Excel.

Reads: review-docs/figure-registry-combined-review.xlsx
Writes: public/data/figure-registry.json, public/data/research-topics/*.json

One-time migration script for Step 2 of the figure registry pipeline.
The domain expert reviewed all 94 figures and assigned each to one or more
of 13 research topics with a role (PRIMARY, RELATED, or NOT SHOWN).

Multi-topic assignments (6 figures with 2+ topics) are encoded in the Excel's
notes column (H) but not expressible in the one-row-per-figure format. These
are applied as overrides from the authoritative dispatch table.

Generated with Claude Code.
"""

import json
import sys
from collections import defaultdict
from copy import deepcopy
from dataclasses import dataclass, field
from pathlib import Path

import openpyxl

from utils import get_repo_root, get_public_data_dir


# =============================================================================
# Constants: Multi-topic overrides and expected counts from dispatch
# =============================================================================

# These encode domain expert decisions from Excel column H notes that the
# one-row-per-figure format cannot represent. Source: dispatch table lines 118-125.
MULTI_TOPIC_OVERRIDES: list[tuple[str, str, str]] = [
    # (figure_key, topic, role)
    ("Alterman_2025_ApJL_982_L40/fig_11", "sources-of-the-solar-wind", "RELATED"),
    ("Alterman_2025_ApJL_982_L40/fig_4", "sources-of-the-solar-wind", "NOT SHOWN"),
    ("Alterman_2026_ApJL_996_L12/fig_1", "helium-abundance", "PRIMARY"),
    ("Alterman_2026_ApJL_996_L12/fig_10", "helium-abundance", "RELATED"),
    ("Alterman_2026_ApJL_996_L12/fig_14", "solar-wind-acceleration", "RELATED"),
    ("Alterman_2026_ApJL_996_L12/fig_2", "turbulence", "RELATED"),
    ("Alterman_2026_ApJL_996_L12/fig_2", "sources-of-the-solar-wind", "RELATED"),
]

# Expected per-topic counts from dispatch table (lines 91-104).
# Format: {topic: (PRIMARY, RELATED, NOT_SHOWN)}
EXPECTED_COUNTS: dict[str, tuple[int, int, int]] = {
    "coulomb-collisions": (1, 3, 0),
    "heavy-ion-composition": (1, 7, 1),
    "helium-abundance": (1, 7, 0),
    "kinetic-processes": (0, 0, 3),
    "proton-beams": (1, 1, 0),
    "solar-activity": (2, 5, 8),
    "solar-wind-acceleration": (1, 2, 2),
    "solar-wind-compressibility": (2, 10, 13),
    "sources-of-the-solar-wind": (1, 3, 4),
    "space-weather": (2, 2, 0),
    "suprathermal-ions": (1, 7, 7),
    "turbulence": (0, 2, 0),
}

# Topics that replace alfven-waves in related_topics cross-references
ALFVEN_WAVES_REPLACEMENT = "solar-wind-acceleration"


@dataclass
class Assignment:
    """A single figure-to-topic mapping from the domain expert."""
    figure_key: str
    topic: str
    role: str  # PRIMARY, RELATED, NOT SHOWN
    relevance: str | None = None


# =============================================================================
# Phase A: Read Excel
# =============================================================================

def read_excel(excel_path: Path) -> list[Assignment]:
    """Read all figure assignments from the review Excel."""
    wb = openpyxl.load_workbook(excel_path, read_only=True, data_only=True)
    ws = wb.active

    assignments = []
    for row in ws.iter_rows(min_row=2, values_only=False):
        key = row[1].value       # Column B: figure key
        topic = row[3].value     # Column D: topic slug
        role = row[4].value      # Column E: role (PRIMARY/RELATED/NOT SHOWN)
        relevance = row[5].value  # Column F: relevance string
        # Column H (notes) is handled via multi-topic overrides

        if key is None:
            continue

        # Clean values
        key = str(key).strip()
        if topic:
            topic = str(topic).strip()
        if role:
            role = str(role).strip().upper()
        if relevance:
            relevance = str(relevance).strip()

        # Skip rows with missing topic/role (e.g., 2026_L12/fig_2 — handled by overrides)
        if not topic or not role:
            continue

        assignments.append(Assignment(
            figure_key=key,
            topic=topic,
            role=role,
            relevance=relevance if relevance else None,
        ))

    wb.close()
    return assignments


# =============================================================================
# Phase B: Apply multi-topic overrides
# =============================================================================

def apply_overrides(assignments: list[Assignment]) -> list[Assignment]:
    """Add multi-topic assignments from the dispatch table."""
    for fig_key, topic, role in MULTI_TOPIC_OVERRIDES:
        # Check this assignment doesn't already exist in Excel data
        exists = any(
            a.figure_key == fig_key and a.topic == topic
            for a in assignments
        )
        if not exists:
            assignments.append(Assignment(
                figure_key=fig_key,
                topic=topic,
                role=role,
                relevance=None,
            ))

    return assignments


# =============================================================================
# Phase C: Validate counts
# =============================================================================

def validate_counts(assignments: list[Assignment]) -> bool:
    """Compare computed counts against dispatch expectations. Returns True if valid."""
    # Group by topic
    counts: dict[str, dict[str, int]] = defaultdict(lambda: {"PRIMARY": 0, "RELATED": 0, "NOT SHOWN": 0})
    for a in assignments:
        counts[a.topic][a.role] += 1

    all_ok = True
    for topic, (exp_p, exp_r, exp_n) in sorted(EXPECTED_COUNTS.items()):
        got_p = counts[topic]["PRIMARY"]
        got_r = counts[topic]["RELATED"]
        got_n = counts[topic]["NOT SHOWN"]

        if (got_p, got_r, got_n) != (exp_p, exp_r, exp_n):
            print(f"  MISMATCH {topic}: expected {exp_p}P {exp_r}R {exp_n}N, "
                  f"got {got_p}P {got_r}R {got_n}N", file=sys.stderr)
            all_ok = False
        else:
            total = got_p + got_r + got_n
            print(f"  OK {topic}: {got_p}P {got_r}R {got_n}N = {total}")

    # Check for unexpected topics
    for topic in counts:
        if topic not in EXPECTED_COUNTS:
            print(f"  UNEXPECTED topic: {topic}", file=sys.stderr)
            all_ok = False

    return all_ok


# =============================================================================
# Phase D: Update figure-registry.json
# =============================================================================

def update_registry(registry_path: Path, assignments: list[Assignment]) -> dict:
    """Populate used_as_*_in fields for all 94 figures."""
    with open(registry_path) as f:
        registry = json.load(f)

    # Build reverse mapping: figure_key -> {primary_in: [topics], related_in: [...], not_shown_in: [...]}
    reverse_map: dict[str, dict[str, list[str]]] = defaultdict(
        lambda: {"primary_in": [], "related_in": [], "not_shown_in": []}
    )
    for a in assignments:
        if a.role == "PRIMARY":
            reverse_map[a.figure_key]["primary_in"].append(a.topic)
        elif a.role == "RELATED":
            reverse_map[a.figure_key]["related_in"].append(a.topic)
        elif a.role == "NOT SHOWN":
            reverse_map[a.figure_key]["not_shown_in"].append(a.topic)

    # Update each registry entry
    for key, entry in registry.items():
        mapping = reverse_map.get(key, {"primary_in": [], "related_in": [], "not_shown_in": []})
        entry["used_as_primary_in"] = sorted(mapping["primary_in"])
        entry["used_as_related_in"] = sorted(mapping["related_in"])
        entry["used_as_not_shown_in"] = sorted(mapping["not_shown_in"])

    # Write back
    with open(registry_path, "w") as f:
        json.dump(registry, f, indent=2, ensure_ascii=False)
        f.write("\n")

    # Verify all figures have at least one assignment
    empty = [k for k, v in registry.items()
             if not v["used_as_primary_in"]
             and not v["used_as_related_in"]
             and not v["used_as_not_shown_in"]]
    if empty:
        print(f"  WARNING: {len(empty)} figures without any topic: {empty}", file=sys.stderr)

    return registry


# =============================================================================
# Phase E: Update existing topic files
# =============================================================================

def build_topic_assignments(
    assignments: list[Assignment],
) -> dict[str, dict[str, list[Assignment]]]:
    """Group assignments by topic and role."""
    result: dict[str, dict[str, list[Assignment]]] = defaultdict(
        lambda: {"PRIMARY": [], "RELATED": [], "NOT SHOWN": []}
    )
    for a in assignments:
        result[a.topic][a.role].append(a)
    return result


def get_existing_relevance(topic_data: dict) -> dict[str, str]:
    """Extract existing relevance strings from a topic file, keyed by ref."""
    relevance_map = {}
    for rf in topic_data.get("related_figures", []):
        relevance_map[rf["ref"]] = rf["relevance"]
    return relevance_map


def update_existing_topics(
    topics_dir: Path,
    topic_assignments: dict[str, dict[str, list[Assignment]]],
    alfven_waves_data: dict,
) -> None:
    """Update 8 existing topic files (all except alfven-waves)."""
    existing_topics = [
        "coulomb-collisions",
        "heavy-ion-composition",
        "helium-abundance",
        "solar-activity",
        "solar-wind-compressibility",
        "sources-of-the-solar-wind",
        "space-weather",
        "suprathermal-ions",
    ]

    for slug in existing_topics:
        topic_path = topics_dir / f"{slug}.json"
        with open(topic_path) as f:
            topic_data = json.load(f)

        # Preserve existing relevance strings for reuse
        existing_relevance = get_existing_relevance(topic_data)

        # Also preserve topic_keywords from old primaries for transfer
        old_primary_keywords = {}
        old_primary = topic_data.get("primary_figure")
        if old_primary:
            old_primary_keywords[old_primary["ref"]] = old_primary.get("topic_keywords", [])

        ta = topic_assignments[slug]

        # Build primary_figures array
        primary_figures = []
        for a in ta["PRIMARY"]:
            pf_entry: dict[str, str | list[str]] = {"ref": a.figure_key}

            # Transfer topic_keywords: if this is a "new version" of an old primary,
            # carry over the keywords (they describe the topic, not the specific figure)
            if slug == "helium-abundance" and a.figure_key == "Alterman_2026_ApJL_996_L12/fig_1":
                # New version of Alterman_2025_ApJL_982_L40/fig_3
                old_kw = old_primary_keywords.get("Alterman_2025_ApJL_982_L40/fig_3", [])
                if old_kw:
                    pf_entry["topic_keywords"] = old_kw
            elif old_primary and a.figure_key == old_primary["ref"]:
                # Same primary as before — preserve its keywords
                kw = old_primary.get("topic_keywords", [])
                if kw:
                    pf_entry["topic_keywords"] = kw

            primary_figures.append(pf_entry)

        # Build related_figures array
        related_figures = []
        for a in ta["RELATED"]:
            # Prefer existing relevance, then Excel relevance, then placeholder
            relevance = (
                existing_relevance.get(a.figure_key)
                or a.relevance
                or "TODO: Add relevance description"
            )
            related_figures.append({
                "ref": a.figure_key,
                "relevance": relevance,
            })

        # Update topic data — preserve all non-figure fields
        topic_data["primary_figures"] = primary_figures
        # Remove old singular key if present
        topic_data.pop("primary_figure", None)
        topic_data["related_figures"] = related_figures

        # Update alfven-waves → solar-wind-acceleration in related_topics
        if topic_data.get("related_topics"):
            for rt in topic_data["related_topics"]:
                if rt["slug"] == "alfven-waves":
                    rt["slug"] = ALFVEN_WAVES_REPLACEMENT

        # Write back
        with open(topic_path, "w") as f:
            json.dump(topic_data, f, indent=2, ensure_ascii=False)
            f.write("\n")

        n_primary = len(primary_figures)
        n_related = len(related_figures)
        print(f"  Updated {slug}: {n_primary}P {n_related}R")


# =============================================================================
# Phase F: Create new topic files
# =============================================================================

def create_new_topics(
    topics_dir: Path,
    topic_assignments: dict[str, dict[str, list[Assignment]]],
    alfven_waves_data: dict,
    existing_topics_data: dict[str, dict],
) -> None:
    """Create 4 new topic files with placeholder metadata."""

    new_topics_config = {
        "solar-wind-acceleration": {
            "title": "Solar Wind Acceleration",
            "subtitle": alfven_waves_data.get("subtitle", "Placeholder — awaiting domain expert review"),
            "description": alfven_waves_data.get("description", "Placeholder — awaiting domain expert review"),
            "paper": alfven_waves_data["paper"],
            "related_topics": alfven_waves_data.get("related_topics", []),
            # Transfer topic_keywords from alfven-waves primary
            "primary_keywords_source": alfven_waves_data.get("primary_figure", {}),
        },
        "proton-beams": {
            "title": "Proton Beams",
            "subtitle": "Placeholder — awaiting domain expert review",
            "description": "Placeholder — awaiting domain expert review",
            "paper": existing_topics_data["coulomb-collisions"]["paper"],
            "related_topics": [],
            "primary_keywords_source": None,
        },
        "kinetic-processes": {
            "title": "Kinetic Processes",
            "subtitle": "Placeholder — awaiting domain expert review",
            "description": "Placeholder — awaiting domain expert review",
            "paper": existing_topics_data["coulomb-collisions"]["paper"],
            "related_topics": [],
            "primary_keywords_source": None,
        },
        "turbulence": {
            "title": "Turbulence",
            "subtitle": "Placeholder — awaiting domain expert review",
            "description": "Placeholder — awaiting domain expert review",
            # Use the L40 paper (first related figure's paper)
            "paper": existing_topics_data["sources-of-the-solar-wind"]["paper"],
            "related_topics": [],
            "primary_keywords_source": None,
        },
    }

    for slug, config in new_topics_config.items():
        ta = topic_assignments[slug]

        # Build primary_figures
        primary_figures = []
        for a in ta["PRIMARY"]:
            pf_entry: dict[str, str | list[str]] = {"ref": a.figure_key}
            # For solar-wind-acceleration, carry over alfven-waves keywords
            if slug == "solar-wind-acceleration" and config["primary_keywords_source"]:
                kw = config["primary_keywords_source"].get("topic_keywords", [])
                if kw:
                    pf_entry["topic_keywords"] = kw
            primary_figures.append(pf_entry)

        # Build related_figures
        related_figures = []
        for a in ta["RELATED"]:
            relevance = a.relevance or "TODO: Add relevance description"
            related_figures.append({
                "ref": a.figure_key,
                "relevance": relevance,
            })

        topic_data = {
            "slug": slug,
            "title": config["title"],
            "subtitle": config["subtitle"],
            "description": config["description"],
            "primary_figures": primary_figures,
            "related_figures": related_figures,
            "related_topics": config["related_topics"],
            "published": False,
            "paper": config["paper"],
        }

        topic_path = topics_dir / f"{slug}.json"
        with open(topic_path, "w") as f:
            json.dump(topic_data, f, indent=2, ensure_ascii=False)
            f.write("\n")

        n_primary = len(primary_figures)
        n_related = len(related_figures)
        print(f"  Created {slug}: {n_primary}P {n_related}R")


# =============================================================================
# Main
# =============================================================================

def main():
    repo_root = get_repo_root()
    data_dir = get_public_data_dir()
    topics_dir = data_dir / "research-topics"
    registry_path = data_dir / "figure-registry.json"
    excel_path = repo_root / "review-docs" / "figure-registry-combined-review.xlsx"

    if not excel_path.exists():
        print(f"ERROR: Excel not found: {excel_path}", file=sys.stderr)
        sys.exit(1)

    # Phase A: Read Excel
    print("Phase A: Reading Excel...")
    assignments = read_excel(excel_path)
    print(f"  Read {len(assignments)} assignments from Excel")

    # Phase B: Apply multi-topic overrides
    print("Phase B: Applying multi-topic overrides...")
    assignments = apply_overrides(assignments)
    print(f"  Total assignments after overrides: {len(assignments)}")

    # Phase C: Validate counts
    print("Phase C: Validating counts against dispatch...")
    if not validate_counts(assignments):
        print("ERROR: Count validation failed. Aborting.", file=sys.stderr)
        sys.exit(1)
    print("  All counts match dispatch expectations.")

    # Load alfven-waves data before deleting
    alfven_path = topics_dir / "alfven-waves.json"
    with open(alfven_path) as f:
        alfven_waves_data = json.load(f)

    # Load existing topic data for paper info reuse
    existing_topics_data = {}
    for json_path in sorted(topics_dir.glob("*.json")):
        with open(json_path) as f:
            td = json.load(f)
        existing_topics_data[td["slug"]] = td

    # Build per-topic assignment groups
    topic_assignments = build_topic_assignments(assignments)

    # Phase D: Update registry
    print("Phase D: Updating figure-registry.json...")
    registry = update_registry(registry_path, assignments)
    print(f"  Updated {len(registry)} entries")

    # Phase E: Update existing topic files
    print("Phase E: Updating existing topic files...")
    update_existing_topics(topics_dir, topic_assignments, alfven_waves_data)

    # Phase F: Create new topic files
    print("Phase F: Creating new topic files...")
    create_new_topics(topics_dir, topic_assignments, alfven_waves_data, existing_topics_data)

    # Phase G: Delete alfven-waves.json
    print("Phase G: Retiring alfven-waves.json...")
    alfven_path.unlink()
    print(f"  Deleted {alfven_path.name}")

    # Summary
    print("\n=== Summary ===")
    topic_files = list(topics_dir.glob("*.json"))
    print(f"  Registry entries: {len(registry)}")
    print(f"  Topic files: {len(topic_files)}")
    print(f"  Total assignments: {len(assignments)}")
    print("Done.")


if __name__ == "__main__":
    main()
