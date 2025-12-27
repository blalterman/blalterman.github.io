#!/usr/bin/env python3
"""
# One-time migration artifact - converts bibtex to JSON

Converts invited talk bibtex files to JSON format matching the ADS publications schema.

This script parses bibtex files from /data/bibtex/{conferences,presentations,public}/
and converts them to JSON files suitable for website display.

Author: Claude
Date: 2025-12-26
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Any
import bibtexparser
from bibtexparser.bparser import BibTexParser
from bibtexparser.customization import convert_to_unicode

from utils import get_repo_root, get_public_data_dir


def strip_latex_formatting(text: str) -> str:
    r"""
    Strip LaTeX formatting commands from text while preserving content.

    Removes:
    - \textbf{}, \emph{}, \textit{} and similar commands
    - Curly braces {}
    - Non-breaking spaces ~
    - Backslashes before special characters

    Args:
        text: Text potentially containing LaTeX commands

    Returns:
        Plain text with LaTeX formatting removed
    """
    if not text:
        return ""

    # First, replace non-breaking spaces with regular spaces
    text = text.replace('~', ' ')

    # Remove common LaTeX commands but keep their content
    # \command{content} → content (handles nested braces)
    while re.search(r'\\(?:textbf|emph|textit|textsc|textrm|text)\{', text):
        text = re.sub(r'\\(?:textbf|emph|textit|textsc|textrm|text)\{([^}]*)\}', r'\1', text)

    # Remove remaining curly braces
    text = text.replace('{', '').replace('}', '')

    # Remove any remaining backslash commands (e.g., \textbf without braces)
    text = re.sub(r'\\textbf|\\emph|\\textit|\\textsc|\\textrm', '', text)

    # Remove backslashes before special characters
    text = re.sub(r'\\([&$%#_])', r'\1', text)

    # Remove any remaining stray backslashes
    text = text.replace('\\', '')

    # Clean up multiple spaces
    text = re.sub(r'\s+', ' ', text)

    return text.strip()


def parse_author_field(author_str: str) -> List[str]:
    """
    Parse bibtex author field into list of plain text author names.

    Handles LaTeX formatting and splits multiple authors by "and".

    Args:
        author_str: Raw author string from bibtex (may contain LaTeX)

    Returns:
        List of author names in plain text
    """
    if not author_str:
        return []

    # Split by "and" (but not LaTeX commands)
    authors = re.split(r'\s+and\s+', author_str, flags=re.IGNORECASE)

    # Strip LaTeX formatting from each author
    cleaned_authors = [strip_latex_formatting(author.strip()) for author in authors]

    # Filter out empty strings
    return [author for author in cleaned_authors if author]


def format_date_field(year: str, month: str = "", day: str = "") -> str:
    """
    Format year, month, day into consistent date string.

    Args:
        year: 4-digit year string
        month: Month name or number (optional)
        day: Day number (optional)

    Returns:
        Formatted date string (YYYY-MM-DD format, with 00 for unknown month/day)
    """
    # Month name to number mapping
    month_map = {
        'january': '01', 'february': '02', 'march': '03', 'april': '04',
        'may': '05', 'june': '06', 'july': '07', 'august': '08',
        'september': '09', 'october': '10', 'november': '11', 'december': '12'
    }

    # Convert month to number if it's a name
    month_num = "00"
    if month:
        if month.isdigit():
            month_num = month.zfill(2)
        else:
            month_num = month_map.get(month.lower(), "00")

    # Format day
    day_num = day.zfill(2) if day and day.isdigit() else "00"

    return f"{year}-{month_num}-{day_num}"


def convert_bibtex_entry_to_json(entry: Dict[str, Any], category: str) -> Dict[str, Any]:
    """
    Convert a single bibtex entry to JSON format matching ADS schema.

    Args:
        entry: Parsed bibtex entry dictionary
        category: Category (conferences/presentations/public)

    Returns:
        Dictionary with JSON fields ready for output
    """
    # Extract and clean fields
    title = strip_latex_formatting(entry.get('title', ''))
    authors = parse_author_field(entry.get('author', ''))
    year = entry.get('year', '')
    month = entry.get('month', '')
    day = entry.get('day', '')

    # Format date
    year_formatted = format_date_field(year, month, day)

    # Build JSON object
    json_entry = {
        "title": title,
        "authors": authors,
        "year": year_formatted,
        "month": month,
        "publication_type": "inproceedings",  # All invited talks use this type
        "citations": 0,  # Invited talks typically don't have citation counts
        "invited": True,  # Mark as invited
    }

    # Add optional fields if present
    if 'bibcode' in entry:
        json_entry['bibcode'] = entry['bibcode']

    if 'booktitle' in entry:
        booktitle_clean = strip_latex_formatting(entry['booktitle'])
        json_entry['booktitle'] = booktitle_clean
        # Also use booktitle as journal field for consistency with ADS schema
        json_entry['journal'] = booktitle_clean
    else:
        json_entry['journal'] = ""

    if 'location' in entry:
        # Strip LaTeX formatting from location too
        json_entry['location'] = strip_latex_formatting(entry['location'])

    if 'day' in entry:
        json_entry['day'] = entry['day']

    if 'keywords' in entry:
        json_entry['keywords'] = entry['keywords']

    # Handle URL field - rename to invited_url to distinguish from DOI
    if 'url' in entry:
        json_entry['invited_url'] = entry['url']

    # Set url field (required by schema) - use empty string if no DOI
    if 'doi' in entry:
        json_entry['url'] = f"https://dx.doi.org/{entry['doi']}"
    else:
        json_entry['url'] = ""

    return json_entry


def parse_bibtex_file(file_path: Path) -> List[Dict[str, Any]]:
    """
    Parse a single bibtex file and return list of entries.

    Args:
        file_path: Path to .bib file

    Returns:
        List of parsed bibtex entry dictionaries
    """
    parser = BibTexParser(common_strings=True)
    parser.customization = convert_to_unicode

    try:
        with open(file_path, 'r', encoding='utf-8') as bibfile:
            bib_database = bibtexparser.load(bibfile, parser)
            return bib_database.entries
    except Exception as e:
        print(f"Warning: Error parsing {file_path}: {e}")
        return []


def process_category(category_dir: Path, category_name: str) -> List[Dict[str, Any]]:
    """
    Process all bibtex files in a category directory.

    Args:
        category_dir: Path to category directory (e.g., /data/bibtex/conferences/)
        category_name: Category name (conferences/presentations/public)

    Returns:
        List of JSON entry dictionaries for this category
    """
    json_entries = []

    # Get all .bib files
    bib_files = sorted(category_dir.glob('*.bib'))

    if not bib_files:
        print(f"Warning: No .bib files found in {category_dir}")
        return []

    print(f"\nProcessing {category_name}:")
    for bib_file in bib_files:
        if bib_file.stat().st_size == 0:
            print(f"  Skipping empty file: {bib_file.name}")
            continue

        print(f"  Parsing {bib_file.name}...")
        entries = parse_bibtex_file(bib_file)

        for entry in entries:
            json_entry = convert_bibtex_entry_to_json(entry, category_name)
            json_entries.append(json_entry)

        print(f"    Found {len(entries)} entries")

    return json_entries


def main():
    """Main conversion function."""
    print("=" * 60)
    print("Invited Talks Bibtex → JSON Conversion")
    print("=" * 60)

    # Get paths
    repo_root = get_repo_root()
    bibtex_dir = repo_root / "data" / "bibtex"
    output_dir = get_public_data_dir()

    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)

    # Process each category
    categories = {
        'conferences': 'invited_conferences.json',
        'presentations': 'invited_presentations.json',
        'public': 'invited_public.json'
    }

    for category, output_filename in categories.items():
        category_dir = bibtex_dir / category

        if not category_dir.exists():
            print(f"\nWarning: Category directory not found: {category_dir}")
            continue

        # Process category
        json_entries = process_category(category_dir, category)

        # Save to file
        output_file = output_dir / output_filename
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(json_entries, f, indent=2, ensure_ascii=False)

        print(f"  ✓ Saved {len(json_entries)} entries to {output_filename}")

    print("\n" + "=" * 60)
    print("Conversion complete!")
    print("=" * 60)

    # Print summary
    print("\nOutput files created:")
    for category, output_filename in categories.items():
        output_file = output_dir / output_filename
        if output_file.exists():
            with open(output_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                print(f"  {output_filename}: {len(data)} entries")


if __name__ == "__main__":
    main()
