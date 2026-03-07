#!/usr/bin/env python3
"""
Interactive CLI and batch importer for adding non-ADS publications to the website.

Supports two modes:
  1. Interactive CLI: Prompt the user for each field (similar to add_invited_talk.py)
  2. Batch import: Parse a .bib file via --from-bibtex flag

Categories:
  - conference: Non-ADS conference presentations (publication_type: "inproceedings")
  - whitepaper: Zenodo/other white papers (publication_type: "techreport")

Usage:
  # Interactive mode
  python scripts/add_non_ads_publication.py

  # Batch import from BibTeX
  python scripts/add_non_ads_publication.py --from-bibtex path/to/file.bib --category conference

  # Dry run (preview without writing)
  python scripts/add_non_ads_publication.py --from-bibtex path/to/file.bib --category whitepaper --dry-run

Generated with Claude Code
"""

import argparse
import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import bibtexparser
from bibtexparser.bparser import BibTexParser
from bibtexparser.customization import convert_to_unicode

from utils import get_public_data_dir

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

PUBLICATIONS_FILE = "ads_publications.json"

CATEGORY_MAP = {
    "conference": "inproceedings",
    "whitepaper": "techreport",
}

MONTH_NAME_TO_NUM = {
    "january": "01", "jan": "01",
    "february": "02", "feb": "02",
    "march": "03", "mar": "03",
    "april": "04", "apr": "04",
    "may": "05",
    "june": "06", "jun": "06",
    "july": "07", "jul": "07",
    "august": "08", "aug": "08",
    "september": "09", "sep": "09",
    "october": "10", "oct": "10",
    "november": "11", "nov": "11",
    "december": "12", "dec": "12",
}

BIBTEX_TYPE_MAP = {
    "inproceedings": "inproceedings",
    "report": "techreport",
}

HELP_TEXT = {
    "category": (
        "Choose category:\n"
        "  1. conference   - Non-ADS conference presentations\n"
        "  2. whitepaper   - Zenodo / other white papers"
    ),
    "title": "Full title of the publication.",
    "authors": (
        "Comma-separated list of authors in 'Last, First M.' format.\n"
        "Example: Alterman, B. L., Rivera, Y., Murphy, Nicholas A."
    ),
    "year": "4-digit year (e.g. 2023). Required.",
    "month": (
        "Month name or number (e.g. February, feb, 2).\n"
        "Press Enter to skip."
    ),
    "journal": (
        "Journal, venue, or booktitle.\n"
        "Examples:\n"
        "  - Chapman Conference on Advances in Understanding ...\n"
        "  - Zenodo"
    ),
    "doi": (
        "DOI string (e.g. 10.5281/zenodo.4043006).\n"
        "Press Enter to skip."
    ),
    "url": (
        "Direct URL if no DOI is available.\n"
        "Press Enter to skip."
    ),
    "citation_key": (
        "Used to generate the synthetic bibcode (NOADS-<key>).\n"
        "Format: VenueYear (e.g. Chapman2023, SolO82024)\n"
        "Should be unique."
    ),
    "keywords": (
        "Optional keywords (e.g. whitepaper).\n"
        "Press Enter to skip."
    ),
}


# ---------------------------------------------------------------------------
# LaTeX Stripping
# ---------------------------------------------------------------------------

def strip_latex_formatting(text: str) -> str:
    r"""
    Strip LaTeX formatting commands from text while preserving content.

    Removes \textbf{}, \emph{}, \textit{}, \textsuperscript{}, curly braces,
    non-breaking spaces (~), and backslashes before special characters.

    Args:
        text: Text potentially containing LaTeX commands.

    Returns:
        Plain text with LaTeX formatting removed.
    """
    if not text:
        return ""

    # Replace non-breaking spaces with regular spaces
    text = text.replace("~", " ")

    # Remove \textsuperscript{...}
    while r"\textsuperscript{" in text:
        text = re.sub(r"\\textsuperscript\{([^}]*)\}", r"\1", text)

    # Remove common LaTeX commands but keep their content
    while re.search(r"\\(?:textbf|emph|textit|textsc|textrm|text)\{", text):
        text = re.sub(
            r"\\(?:textbf|emph|textit|textsc|textrm|text)\{([^}]*)\}",
            r"\1",
            text,
        )

    # Remove remaining curly braces
    text = text.replace("{", "").replace("}", "")

    # Remove any remaining backslash commands (e.g. \textbf without braces)
    text = re.sub(r"\\(?:textbf|emph|textit|textsc|textrm)", "", text)

    # Remove backslashes before special characters
    text = re.sub(r"\\([&$%#_])", r"\1", text)

    # Remove any remaining stray backslashes
    text = text.replace("\\", "")

    # Clean up multiple spaces
    text = re.sub(r"\s+", " ", text)

    return text.strip()


# ---------------------------------------------------------------------------
# Author Parsing
# ---------------------------------------------------------------------------

def parse_bibtex_authors(author_str: str) -> List[str]:
    r"""
    Parse a BibTeX author field into a list of clean author name strings.

    Handles the CV's custom BibTeX author format which includes:
    - LaTeX formatting: \textbf{Alterman, B.~L.}
    - Position annotations: (1\textsuperscript{st} of 5)
    - 'and others' sentinel

    Algorithm:
      1. Split by ' and ' (case-sensitive).
      2. For each token:
         - Skip if it equals 'others' (after stripping).
         - Remove position annotations like (Nth of M).
         - Strip all LaTeX formatting.
         - Clean up whitespace.
      3. Return list of clean author names.

    Examples:
        >>> parse_bibtex_authors(r'\textbf{Alterman, B.~L.} and others')
        ['Alterman, B. L.']
        >>> parse_bibtex_authors(
        ...     r'Rivera, Y. and \textbf{Alterman, B.~L.} '
        ...     r'(7\textsuperscript{th} of 10) and others'
        ... )
        ['Rivera, Y.', 'Alterman, B. L.']

    Args:
        author_str: Raw author string from BibTeX.

    Returns:
        List of author names in 'Last, First M.' format.
    """
    if not author_str:
        return []

    # Normalize 'and' followed by non-space to 'and ' for splitting.
    # bibtexparser's convert_to_unicode can strip braces, turning
    # 'and{\textbf{Name}}' into 'and\textbfName' with no separator.
    author_str = re.sub(r"\band(?=\S)", "and ", author_str)

    # Split by ' and ' (case-sensitive, as BibTeX convention)
    tokens = re.split(r"\s+and\s+", author_str)

    authors: List[str] = []
    for token in tokens:
        token = token.strip()

        # Skip 'others'
        if token.lower() == "others":
            continue

        # Strip LaTeX formatting first, so position annotations become
        # plain text like "(9th of 39)" before we try to remove them.
        name = strip_latex_formatting(token)

        # Remove position annotations like (1st of 5), (9th of 39), etc.
        name = re.sub(r"\(\d+(?:st|nd|rd|th)\s+of\s+\d+\)", "", name)
        # Also handle partially-stripped forms like (9textsuperscriptth of 39)
        name = re.sub(r"\(\d+\w*(?:st|nd|rd|th)\s+of\s+\d+\)", "", name)

        # Clean up whitespace and trailing/leading punctuation artifacts
        name = re.sub(r"\s+", " ", name).strip()
        # Remove any trailing/leading parentheses that may remain
        name = name.strip("() ")

        if name:
            authors.append(name)

    return authors


# ---------------------------------------------------------------------------
# Month / Date Helpers
# ---------------------------------------------------------------------------

def normalize_month(month_raw: str) -> str:
    """
    Normalize a BibTeX month value to a two-digit month number string.

    Handles month macros (jan, feb, ...), full names (January, ...),
    numeric strings ('2', '02'), and braced values ({February}).

    Args:
        month_raw: Raw month value from BibTeX or user input.

    Returns:
        Two-digit month string ('01'..'12') or '00' if unrecognized/empty.
    """
    if not month_raw:
        return "00"

    cleaned = month_raw.strip().strip("{}").strip().lower()

    if cleaned.isdigit():
        num = int(cleaned)
        return str(num).zfill(2) if 1 <= num <= 12 else "00"

    return MONTH_NAME_TO_NUM.get(cleaned, "00")


def format_year_field(year: str, month_raw: str = "") -> str:
    """
    Format year and month into the ads_publications.json date format.

    Args:
        year: 4-digit year string.
        month_raw: Raw month value (optional).

    Returns:
        Date string in 'YYYY-MM-00' format.
    """
    month_num = normalize_month(month_raw)
    return f"{year}-{month_num}-00"


# ---------------------------------------------------------------------------
# Synthetic Bibcode
# ---------------------------------------------------------------------------

def make_synthetic_bibcode(citation_key: str) -> str:
    """
    Generate a synthetic bibcode for a non-ADS publication.

    Args:
        citation_key: BibTeX citation key or user-provided key.

    Returns:
        Synthetic bibcode string like 'NOADS-Chapman2023'.
    """
    return f"NOADS-{citation_key}"


# ---------------------------------------------------------------------------
# Deduplication
# ---------------------------------------------------------------------------

def build_dedup_keys(entries: List[Dict]) -> set:
    """
    Build a set of deduplication keys from existing publication entries.

    Key is (lowercased title, 4-char year prefix).

    Args:
        entries: List of existing publication dictionaries.

    Returns:
        Set of (title, year) tuples for deduplication.
    """
    keys = set()
    for entry in entries:
        title = entry.get("title", "").lower().strip()
        year = entry.get("year", "")[:4]
        if title and year:
            keys.add((title, year))
    return keys


def is_duplicate(entry: Dict, dedup_keys: set) -> bool:
    """
    Check whether a publication entry is a duplicate.

    Args:
        entry: Publication dictionary to check.
        dedup_keys: Set of existing (title, year) tuples.

    Returns:
        True if entry is a duplicate.
    """
    title = entry.get("title", "").lower().strip()
    year = entry.get("year", "")[:4]
    return (title, year) in dedup_keys


# ---------------------------------------------------------------------------
# BibTeX File Parsing
# ---------------------------------------------------------------------------

def parse_bibtex_file(file_path: Path) -> List[Dict]:
    """
    Parse a BibTeX file and return the list of raw entry dictionaries.

    Args:
        file_path: Path to a .bib file.

    Returns:
        List of parsed BibTeX entry dictionaries.
    """
    parser = BibTexParser(common_strings=True)
    parser.customization = convert_to_unicode
    # Accept biblatex entry types like @report, @dataset, @eprint
    # (bibtexparser defaults to ignoring non-standard BibTeX types)
    parser.ignore_nonstandard_types = False

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Strip %-prefixed comment lines: bibtexparser doesn't handle LaTeX-style
    # comments inside entries and silently drops entries that contain them.
    content = re.sub(r"^\s*%.*$", "", content, flags=re.MULTILINE)

    bib_db = bibtexparser.loads(content, parser)

    return bib_db.entries


def convert_bibtex_entry(entry: Dict, category: str) -> Dict:
    """
    Convert a parsed BibTeX entry dict to the ads_publications.json schema.

    Args:
        entry: Raw BibTeX entry dictionary (from bibtexparser).
        category: One of 'conference' or 'whitepaper'.

    Returns:
        Dictionary matching the ads_publications.json schema.
    """
    # Determine publication_type from BibTeX entry type or category
    bib_type = entry.get("ENTRYTYPE", "").lower()
    publication_type = BIBTEX_TYPE_MAP.get(bib_type, CATEGORY_MAP.get(category, "inproceedings"))

    # Title
    title = strip_latex_formatting(entry.get("title", ""))

    # Authors
    authors = parse_bibtex_authors(entry.get("author", ""))

    # Year and month
    year_raw = entry.get("year", "")
    month_raw = entry.get("month", "")
    year_field = format_year_field(year_raw, month_raw)

    # Journal / booktitle (fall back to publisher for Zenodo white papers)
    journal = strip_latex_formatting(
        entry.get("booktitle", "") or entry.get("journal", "") or entry.get("publisher", "")
    )

    # URL: prefer DOI-based URL, fall back to url field
    doi = entry.get("doi", "")
    url_field = entry.get("url", "")
    if doi:
        url = f"https://dx.doi.org/{doi}"
    elif url_field:
        url = url_field
    else:
        url = ""

    # Synthetic bibcode from citation key
    citation_key = entry.get("ID", "unknown")
    bibcode = make_synthetic_bibcode(citation_key)

    result: Dict = {
        "bibcode": bibcode,
        "title": title,
        "authors": authors,
        "month": "",
        "year": year_field,
        "journal": journal,
        "publication_type": publication_type,
        "citations": 0,
        "url": url,
        "invited": False,
    }

    # Preserve keywords if present
    keywords = entry.get("keywords", "")
    if keywords:
        result["keywords"] = strip_latex_formatting(keywords)

    return result


def import_from_bibtex(
    bib_path: Path,
    category: str,
    existing: List[Dict],
    dedup_keys: set,
) -> Tuple[List[Dict], List[Dict]]:
    """
    Parse a .bib file and convert entries to website JSON format.

    Args:
        bib_path: Path to the .bib file.
        category: One of 'conference' or 'whitepaper'.
        existing: Current list of publications (for context).
        dedup_keys: Set of (title, year) dedup keys.

    Returns:
        Tuple of (new_entries, skipped_duplicates).
    """
    raw_entries = parse_bibtex_file(bib_path)
    new_entries: List[Dict] = []
    skipped: List[Dict] = []

    for raw in raw_entries:
        converted = convert_bibtex_entry(raw, category)

        if is_duplicate(converted, dedup_keys):
            skipped.append(converted)
        else:
            new_entries.append(converted)
            # Add to dedup keys so later entries in same file are checked
            title = converted.get("title", "").lower().strip()
            year = converted.get("year", "")[:4]
            dedup_keys.add((title, year))

    return new_entries, skipped


# ---------------------------------------------------------------------------
# Interactive CLI
# ---------------------------------------------------------------------------

def prompt_with_help(
    field_name: str,
    prompt_text: str,
    required: bool = False,
    default: Optional[str] = None,
) -> str:
    """
    Prompt user for input with '?' help support.

    Args:
        field_name: Field name for help text lookup.
        prompt_text: Text to display in prompt.
        required: Whether field is required.
        default: Default value if user presses Enter.

    Returns:
        User input string.
    """
    while True:
        if default:
            full_prompt = f"{prompt_text} (default: {default}): "
        elif not required:
            full_prompt = f"{prompt_text} (optional, ? for help): "
        else:
            full_prompt = f"{prompt_text} (? for help): "

        value = input(full_prompt).strip()

        if value == "?":
            print(f"\n{HELP_TEXT.get(field_name, 'No help available.')}\n")
            continue

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
    """Validate that year is a 4-digit number in a reasonable range."""
    return bool(re.match(r"^\d{4}$", year_str)) and 1900 <= int(year_str) <= 2100


def validate_month_input(month_str: str) -> bool:
    """Validate month input (empty, 1-12, or month name)."""
    if not month_str:
        return True
    if month_str.isdigit():
        return 1 <= int(month_str) <= 12
    return month_str.strip().lower() in MONTH_NAME_TO_NUM


def parse_interactive_authors(authors_str: str) -> List[str]:
    """
    Parse comma-separated author string from interactive input.

    Handles the case where author names themselves contain commas
    (Last, First M.) by splitting on the pattern ', <Uppercase>' that
    starts a new last name — but only after the first comma which is
    part of the 'Last, First' format.

    Simple approach: split by pattern where we see ", " followed by an
    uppercase letter that starts a new surname after a prior first-name
    token. In practice, the user is told to delimit authors with semicolons
    or we use a simpler heuristic.

    Actually, the task says "comma-separated 'Last, First M.' format".
    Since author names themselves have commas, we need a delimiter.
    We'll use semicolons if present, otherwise try to parse intelligently.

    Args:
        authors_str: Raw author string from user input.

    Returns:
        List of author name strings.
    """
    # If semicolons are present, use them as the delimiter
    if ";" in authors_str:
        authors = [a.strip() for a in authors_str.split(";")]
        return [a for a in authors if a]

    # Otherwise, try splitting by "., " which appears between authors
    # e.g. "Alterman, B. L., Rivera, Y., Murphy, Nicholas A."
    # Pattern: after "X." or "X. X." there's a comma+space before next surname
    # Heuristic: split on ", " that is followed by a capitalized word and
    # then a comma (i.e., the start of a new "Last, First" pair).
    # This works for "Last1, First1 M., Last2, First2"
    parts = re.split(r",\s+(?=[A-Z][a-z]*,\s)", authors_str)
    if len(parts) > 1:
        return [p.strip().rstrip(",") for p in parts if p.strip()]

    # Fallback: treat the whole string as a single author
    return [authors_str.strip()] if authors_str.strip() else []


def interactive_add() -> Optional[Dict]:
    """
    Run the interactive CLI to collect publication fields from the user.

    Returns:
        A publication dictionary matching the JSON schema, or None if cancelled.
    """
    print("=" * 60)
    print("Add Non-ADS Publication")
    print("=" * 60)
    print("\nType '?' at any prompt for help.\n")

    # --- Category ---
    print(HELP_TEXT["category"])
    category_choices = {"1": "conference", "2": "whitepaper"}
    while True:
        choice = input("\nSelect category (1-2): ").strip()
        if choice in category_choices:
            category = category_choices[choice]
            pub_type = CATEGORY_MAP[category]
            print(f"  -> Selected: {category} (publication_type: {pub_type})")
            break
        elif choice == "?":
            print(f"\n{HELP_TEXT['category']}\n")
        else:
            print("  Error: Please enter 1 or 2.")

    # --- Title ---
    title = prompt_with_help("title", "Enter title", required=True)

    # --- Authors ---
    print("\n  Tip: Separate multiple authors with semicolons:")
    print("       Alterman, B. L.; Rivera, Y.; Murphy, Nicholas A.")
    authors_raw = prompt_with_help("authors", "Enter authors", required=True)
    authors = parse_interactive_authors(authors_raw)
    print(f"  Parsed {len(authors)} author(s): {authors}")

    # --- Year ---
    while True:
        year = prompt_with_help("year", "Enter year (YYYY)", required=True)
        if validate_year(year):
            break
        print("  Error: Year must be a 4-digit number (e.g. 2023).\n")

    # --- Month ---
    while True:
        month = prompt_with_help("month", "Enter month")
        if validate_month_input(month):
            break
        print("  Error: Month must be 1-12 or a month name.\n")

    # --- Journal / Venue ---
    journal = prompt_with_help("journal", "Enter journal/venue", required=True)

    # --- DOI ---
    doi = prompt_with_help("doi", "Enter DOI")
    if doi:
        url = f"https://dx.doi.org/{doi}"
    else:
        url = prompt_with_help("url", "Enter URL")

    # --- Citation Key (for synthetic bibcode) ---
    suggested_key = re.sub(r"[^A-Za-z0-9]", "", journal.split()[0] if journal else "Pub") + year
    citation_key = prompt_with_help(
        "citation_key",
        "Enter citation key for synthetic bibcode",
        required=True,
        default=suggested_key,
    )
    bibcode = make_synthetic_bibcode(citation_key)

    # --- Keywords ---
    default_kw = "whitepaper" if category == "whitepaper" else ""
    keywords = prompt_with_help("keywords", "Enter keywords", default=default_kw if default_kw else None)

    # --- Build entry ---
    entry: Dict = {
        "bibcode": bibcode,
        "title": title,
        "authors": authors,
        "month": "",
        "year": format_year_field(year, month),
        "journal": journal,
        "publication_type": pub_type,
        "citations": 0,
        "url": url,
        "invited": False,
    }

    if keywords:
        entry["keywords"] = keywords

    return entry


# ---------------------------------------------------------------------------
# File I/O
# ---------------------------------------------------------------------------

def load_publications() -> List[Dict]:
    """
    Load the existing ads_publications.json file.

    Returns:
        List of publication dictionaries.
    """
    pub_file = get_public_data_dir() / PUBLICATIONS_FILE
    if pub_file.exists():
        with open(pub_file, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_publications(entries: List[Dict], dry_run: bool = False) -> str:
    """
    Save publications to ads_publications.json, sorted by year descending.

    Args:
        entries: Full list of publication dictionaries.
        dry_run: If True, do not write to disk.

    Returns:
        Status message string.
    """
    # Sort by year descending (year field is 'YYYY-MM-DD')
    entries.sort(key=lambda e: e.get("year", ""), reverse=True)

    pub_file = get_public_data_dir() / PUBLICATIONS_FILE

    if dry_run:
        return f"DRY RUN: Would write {len(entries)} entries to {pub_file}"

    with open(pub_file, "w", encoding="utf-8") as f:
        json.dump(entries, f, indent=2, ensure_ascii=False)
    # Ensure trailing newline
    with open(pub_file, "a", encoding="utf-8") as f:
        f.write("\n")

    return f"Wrote {len(entries)} entries to {pub_file}"


# ---------------------------------------------------------------------------
# Display Helpers
# ---------------------------------------------------------------------------

def print_entry(entry: Dict, index: Optional[int] = None) -> None:
    """Pretty-print a publication entry for review."""
    prefix = f"  [{index}] " if index is not None else "  "
    print(f"{prefix}bibcode:  {entry.get('bibcode', '')}")
    print(f"{prefix}title:    {entry.get('title', '')}")
    authors = entry.get("authors", [])
    if len(authors) <= 3:
        print(f"{prefix}authors:  {', '.join(authors)}")
    else:
        print(f"{prefix}authors:  {authors[0]} ... +{len(authors) - 1} others")
    print(f"{prefix}year:     {entry.get('year', '')}")
    print(f"{prefix}journal:  {entry.get('journal', '')}")
    print(f"{prefix}type:     {entry.get('publication_type', '')}")
    print(f"{prefix}url:      {entry.get('url', '')}")
    if entry.get("keywords"):
        print(f"{prefix}keywords: {entry.get('keywords', '')}")
    print()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Add non-ADS publications (conferences, white papers) to the website."
    )
    parser.add_argument(
        "--from-bibtex",
        type=Path,
        metavar="FILE",
        help="Path to a .bib file for batch import.",
    )
    parser.add_argument(
        "--category",
        choices=list(CATEGORY_MAP.keys()),
        help="Publication category (required with --from-bibtex).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview entries without writing to files.",
    )
    args = parser.parse_args()

    # Load existing publications
    existing = load_publications()
    dedup_keys = build_dedup_keys(existing)
    original_count = len(existing)

    print(f"Loaded {original_count} existing publications from {PUBLICATIONS_FILE}.\n")

    if args.from_bibtex:
        # ----- Batch import mode -----
        bib_path = args.from_bibtex.resolve()
        if not bib_path.exists():
            print(f"Error: File not found: {bib_path}")
            return

        if not args.category:
            print("Error: --category is required when using --from-bibtex.")
            print("       Use --category conference or --category whitepaper.")
            return

        print(f"Importing from: {bib_path}")
        print(f"Category:       {args.category} -> publication_type: {CATEGORY_MAP[args.category]}")
        print()

        new_entries, skipped = import_from_bibtex(
            bib_path, args.category, existing, dedup_keys
        )

        if skipped:
            print(f"Skipped {len(skipped)} duplicate(s):")
            for entry in skipped:
                print(f"  - {entry.get('title', '?')} ({entry.get('year', '?')[:4]})")
            print()

        if not new_entries:
            print("No new entries to add.")
            return

        print(f"Found {len(new_entries)} new entry/entries:\n")
        for i, entry in enumerate(new_entries, 1):
            print_entry(entry, index=i)

        existing.extend(new_entries)

    else:
        # ----- Interactive mode -----
        entry = interactive_add()
        if entry is None:
            print("Cancelled.")
            return

        print("\n" + "=" * 60)
        print("Generated Entry:")
        print("=" * 60)
        print_entry(entry)

        if is_duplicate(entry, dedup_keys):
            print("WARNING: This entry appears to be a duplicate (matching title + year).")
            confirm = input("Add anyway? (y/N): ").strip().lower()
            if confirm != "y":
                print("Cancelled.")
                return

        existing.append(entry)
        new_entries = [entry]

    # Save
    print("=" * 60)
    message = save_publications(existing, dry_run=args.dry_run)
    print(message)

    added_count = len(existing) - original_count
    if not args.dry_run and added_count > 0:
        print(f"\nAdded {added_count} new publication(s).")
        print("Total publications: ", len(existing))
    elif args.dry_run:
        print(f"\nWould add {len(new_entries)} new publication(s) (dry run).")

    print("=" * 60)


if __name__ == "__main__":
    main()
