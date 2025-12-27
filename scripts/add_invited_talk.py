#!/usr/bin/env python3
"""
Interactive CLI for adding new invited talk entries to bibtex files.

Prompts user for each field with "?" help text support. Creates or appends
to year-based bibtex files in /data/bibtex/{category}/.

After adding entries via this script, run convert_invited_bibtex.py to
regenerate the JSON files.

Author: Claude
Date: 2025-12-26
"""

import argparse
import re
from datetime import datetime
from pathlib import Path
from typing import Optional, Tuple

from utils import get_repo_root


# Help text for each field
HELP_TEXT = {
    'category': (
        "Choose category:\n"
        "  1. conferences - Invited conference talks\n"
        "  2. presentations - Colloquia and seminars\n"
        "  3. public - Public-facing lectures"
    ),
    'citation_key': (
        "Format: VenueYear (e.g., GSFC2023, UNH2025)\n"
        "Should be unique identifier for this entry."
    ),
    'title': (
        "Can include LaTeX formatting: {}, \\emph{}, \\textbf{}\n"
        "Example: {From Kinetics to the Solar Cycle: Probing \\emph{In Situ} Observations}"
    ),
    'year': "4-digit year (2015-2025). Required.",
    'month': "Text name (January, April) or number (1, 4). Press Enter to skip.",
    'day': "Numeric day (1-31). Press Enter to skip.",
    'author': (
        "LaTeX format recommended for your name.\n"
        "Example: \\textbf{Alterman, B.~L.}\n"
        "For multiple authors, separate with 'and': Author1 and Author2\n"
        "Press Enter for default."
    ),
    'booktitle': (
        "Full venue or institution name.\n"
        "Examples:\n"
        "  - NASA Goddard Space Flight Center\n"
        "  - SHINE Conference\n"
        "  - University of New Hampshire"
    ),
    'location': (
        "Format: 'City, State' or 'City, Country'\n"
        "Examples: 'Greenbelt, MD' or 'Rome, Italy'\n"
        "Press Enter to skip."
    ),
    'bibcode': (
        "NASA ADS bibcode format: YYYYjour..vvv..pppA\n"
        "Example: 2021shin.confE...7A\n"
        "RECOMMENDED for conferences to enable deduplication.\n"
        "Press Enter to skip."
    ),
    'keywords': (
        "Common keywords: 'invited', 'invitedother', 'public'\n"
        "Press Enter for 'invited'."
    ),
    'url': (
        "Link to event/talk page (not DOI).\n"
        "Press Enter to skip."
    ),
}


def prompt_with_help(field_name: str, prompt_text: str, required: bool = False, default: Optional[str] = None) -> str:
    """
    Prompt user for input with "?" help support.

    Args:
        field_name: Field name for help text lookup
        prompt_text: Text to display in prompt
        required: Whether field is required
        default: Default value if user presses Enter

    Returns:
        User input string
    """
    while True:
        # Build prompt
        if default:
            full_prompt = f"{prompt_text} (default: {default}): "
        elif not required:
            full_prompt = f"{prompt_text} (optional, ? for help): "
        else:
            full_prompt = f"{prompt_text} (? for help): "

        # Get input
        value = input(full_prompt).strip()

        # Check for help request
        if value == "?":
            print(f"\n{HELP_TEXT.get(field_name, 'No help available')}\n")
            continue

        # Handle empty input
        if not value:
            if default:
                return default
            elif not required:
                return ""
            else:
                print("  Error: This field is required.\n")
                continue

        return value


def validate_year(year_str: str) -> bool:
    """Validate that year is a 4-digit number."""
    return bool(re.match(r'^\d{4}$', year_str)) and 1900 <= int(year_str) <= 2100


def validate_month(month_str: str) -> bool:
    """Validate month (empty, 1-12, or month name)."""
    if not month_str:
        return True

    if month_str.isdigit():
        return 1 <= int(month_str) <= 12

    month_names = ['january', 'february', 'march', 'april', 'may', 'june',
                   'july', 'august', 'september', 'october', 'november', 'december']
    return month_str.lower() in month_names


def validate_day(day_str: str) -> bool:
    """Validate day (empty or 1-31)."""
    if not day_str:
        return True
    return day_str.isdigit() and 1 <= int(day_str) <= 31


def suggest_citation_key(booktitle: str, year: str) -> str:
    """
    Generate a citation key suggestion from booktitle and year.

    Args:
        booktitle: Venue/institution name
        year: 4-digit year

    Returns:
        Suggested citation key
    """
    # Extract first significant word from booktitle
    words = re.findall(r'\b[A-Z][a-z]*\b|\b[A-Z]{2,}\b', booktitle)
    if words:
        venue = words[0]
    else:
        venue = "Talk"

    return f"{venue}{year}"


def format_bibtex_entry(fields: dict) -> str:
    """
    Format collected fields into a bibtex entry.

    Args:
        fields: Dictionary of field name -> value

    Returns:
        Formatted bibtex string
    """
    lines = [f"@inproceedings{{{fields['citation_key']},}}"]

    # Add fields in standard order
    field_order = ['author', 'title', 'year', 'month', 'day', 'booktitle',
                   'location', 'bibcode', 'keywords', 'url']

    for field in field_order:
        if field in fields and fields[field]:
            value = fields[field]

            # Format based on field type
            if field == 'title':
                # Wrap title in double braces
                lines.append(f" title = {{{{{value}}}}},")
            elif field == 'author':
                lines.append(f" author = {{{value}}},")
            elif field in ['year', 'month', 'day']:
                # Numbers or month names without braces
                lines.append(f" {field} = {{{value}}},")
            else:
                lines.append(f" {field} = {{{value}}},")

    # Close entry
    lines.append("}")

    return "\n".join(lines)


def write_to_bibtex_file(category: str, year: str, entry: str, dry_run: bool = False) -> Tuple[bool, str]:
    """
    Write bibtex entry to appropriate file.

    Args:
        category: Category (conferences/presentations/public)
        year: 4-digit year
        entry: Formatted bibtex entry
        dry_run: If True, don't actually write file

    Returns:
        Tuple of (success: bool, message: str)
    """
    repo_root = get_repo_root()
    bibtex_dir = repo_root / "data" / "bibtex" / category
    bib_file = bibtex_dir / f"{year}.bib"

    if dry_run:
        return True, f"DRY RUN: Would write to {bib_file}"

    # Ensure directory exists
    bibtex_dir.mkdir(parents=True, exist_ok=True)

    # Check if file exists
    if bib_file.exists():
        # Append with double newline separator
        with open(bib_file, 'a', encoding='utf-8') as f:
            f.write("\n\n" + entry + "\n")
        return True, f"Appended to existing file: {bib_file}"
    else:
        # Create new file
        with open(bib_file, 'w', encoding='utf-8') as f:
            f.write(entry + "\n")
        return True, f"Created new file: {bib_file}"


def main():
    """Main interactive CLI function."""
    parser = argparse.ArgumentParser(
        description="Add a new invited talk entry to bibtex files"
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help="Print bibtex entry without writing to file"
    )
    args = parser.parse_args()

    print("=" * 60)
    print("Add Invited Talk Entry")
    print("=" * 60)
    print("\nType '?' at any prompt for help.\n")

    # Collect fields
    fields = {}

    # Category selection
    print(HELP_TEXT['category'])
    category_map = {'1': 'conferences', '2': 'presentations', '3': 'public'}
    while True:
        choice = input("\nSelect category (1-3): ").strip()
        if choice in category_map:
            category = category_map[choice]
            print(f"  → Selected: {category}")
            break
        elif choice == "?":
            print(f"\n{HELP_TEXT['category']}\n")
        else:
            print("  Error: Please enter 1, 2, or 3")

    # Year (needed for file path and citation key suggestion)
    while True:
        year = prompt_with_help('year', "Enter year (YYYY)", required=True)
        if validate_year(year):
            fields['year'] = year
            break
        print("  Error: Year must be a 4-digit number (e.g., 2023)\n")

    # Booktitle (needed for citation key suggestion)
    fields['booktitle'] = prompt_with_help('booktitle', "Enter venue/institution", required=True)

    # Citation key (with auto-suggestion)
    suggested_key = suggest_citation_key(fields['booktitle'], fields['year'])
    fields['citation_key'] = prompt_with_help(
        'citation_key',
        "Enter citation key",
        required=True,
        default=suggested_key
    )

    # Title
    fields['title'] = prompt_with_help('title', "Enter title", required=True)

    # Month
    while True:
        month = prompt_with_help('month', "Enter month", required=False)
        if validate_month(month):
            if month:
                fields['month'] = month
            break
        print("  Error: Month must be 1-12 or a month name (e.g., January)\n")

    # Day
    while True:
        day = prompt_with_help('day', "Enter day", required=False)
        if validate_day(day):
            if day:
                fields['day'] = day
            break
        print("  Error: Day must be 1-31\n")

    # Author
    fields['author'] = prompt_with_help(
        'author',
        "Enter author",
        required=True,
        default=r"\textbf{Alterman, B.~L.}"
    )

    # Location
    location = prompt_with_help('location', "Enter location", required=False)
    if location:
        fields['location'] = location

    # Bibcode
    bibcode = prompt_with_help('bibcode', "Enter ADS bibcode (if available)", required=False)
    if bibcode:
        fields['bibcode'] = bibcode

    # Keywords
    fields['keywords'] = prompt_with_help(
        'keywords',
        "Enter keywords",
        required=False,
        default="invited"
    )

    # URL
    url = prompt_with_help('url', "Enter event URL", required=False)
    if url:
        fields['url'] = url

    # Format bibtex entry
    print("\n" + "=" * 60)
    print("Generated Bibtex Entry:")
    print("=" * 60)
    entry = format_bibtex_entry(fields)
    print(entry)

    # Write to file
    print("\n" + "=" * 60)
    success, message = write_to_bibtex_file(category, fields['year'], entry, dry_run=args.dry_run)

    if success:
        print(f"✓ {message}")
        if not args.dry_run:
            print(f"\nNext steps:")
            print(f"  1. Run: python scripts/convert_invited_bibtex.py")
            print(f"  2. Run: python scripts/merge_invited_conferences.py (if category=conferences)")
    else:
        print(f"✗ Error: {message}")

    print("=" * 60)


if __name__ == "__main__":
    main()
