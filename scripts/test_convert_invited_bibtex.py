#!/usr/bin/env python3
"""
Test script for convert_invited_bibtex.py

Tests merge behavior (preserving existing JSON entries when converting BibTeX),
malformed BibTeX detection, and regression tests for existing conversion logic.

Usage:
    python scripts/test_convert_invited_bibtex.py
"""

import json
import tempfile
import unittest
import warnings
from pathlib import Path
from unittest.mock import patch
from io import StringIO

# Import the module to test
import sys
sys.path.append(str(Path(__file__).parent))

from convert_invited_bibtex import (
    strip_latex_formatting,
    format_date_field,
    convert_bibtex_entry_to_json,
    parse_bibtex_file,
    process_category,
    main,
)


class TestMergeBehavior(unittest.TestCase):
    """Tests that BibTeX conversion merges with existing JSON entries."""

    def setUp(self):
        """Set up temp directories mimicking the repo structure."""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_path = Path(self.temp_dir.name)

        # Create directory structure expected by the script
        self.bibtex_dir = self.temp_path / "data" / "bibtex"
        self.output_dir = self.temp_path / "public" / "data"
        self.bibtex_dir.mkdir(parents=True)
        self.output_dir.mkdir(parents=True)

        # Also create markers so get_repo_root-like validation could work
        # (we'll mock get_repo_root and get_public_data_dir instead)

        # Sample existing JSON entries (manually curated, no BibTeX source)
        self.existing_entries = [
            {
                "title": "The Multi-scale Solar Wind",
                "authors": ["Alterman, B. L."],
                "year": "2019-03-04",
                "month": "March",
                "publication_type": "inproceedings",
                "citations": 0,
                "invited": True,
                "booktitle": "Southwest Research Institute",
                "journal": "Southwest Research Institute",
                "location": "San Antonio, TX",
                "day": "4",
                "keywords": "invitedother",
                "url": "",
            },
            {
                "title": "Solar Wind Helium Abundance Predicts Solar Cycle Onset",
                "authors": ["Alterman, B. L."],
                "year": "2021-02-22",
                "month": "February",
                "publication_type": "inproceedings",
                "citations": 0,
                "invited": True,
                "booktitle": "University of Arizona",
                "journal": "University of Arizona",
                "location": "Virtual",
                "day": "22",
                "keywords": "invitedother",
                "url": "",
            },
        ]

        # A valid BibTeX entry that is NEW (not in existing JSON)
        self.new_bib_content = """\
@inproceedings{NewTalk2026,
 author = {Alterman, B.~L.},
 title = {{Brand New Talk Title}},
 year = {2026},
 month = {01},
 day = {15},
 booktitle = {Some Conference},
 location = {Somewhere, USA},
 keywords = {invited},
}
"""

        # A BibTeX entry that DUPLICATES an existing JSON entry (same title + year)
        self.dup_bib_content = """\
@inproceedings{DupTalk,
 author = {Alterman, B.~L.},
 title = {{The Multi-scale Solar Wind}},
 year = {2019},
 month = {03},
 day = {4},
 booktitle = {Southwest Research Institute},
 location = {San Antonio, TX},
 keywords = {invitedother},
}
"""

    def tearDown(self):
        self.temp_dir.cleanup()

    def _write_existing_json(self, filename, entries):
        """Write entries to a JSON file in the output dir."""
        output_file = self.output_dir / filename
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(entries, f, indent=2, ensure_ascii=False)

    def _write_bib_file(self, category, filename, content):
        """Write a .bib file to the appropriate category dir."""
        category_dir = self.bibtex_dir / category
        category_dir.mkdir(parents=True, exist_ok=True)
        bib_file = category_dir / filename
        bib_file.write_text(content, encoding="utf-8")

    def _read_output_json(self, filename):
        """Read and parse a JSON file from the output dir."""
        output_file = self.output_dir / filename
        with open(output_file, "r", encoding="utf-8") as f:
            return json.load(f)

    def _run_main(self):
        """Run main() with mocked paths pointing to our temp dirs."""
        with patch("convert_invited_bibtex.get_repo_root", return_value=self.temp_path), \
             patch("convert_invited_bibtex.get_public_data_dir", return_value=self.output_dir):
            main()

    def test_merge_preserves_existing_entries(self):
        """Existing JSON entries survive when BibTeX dir has new entries."""
        self._write_existing_json("invited_presentations.json", self.existing_entries)
        self._write_bib_file("presentations", "2026.bib", self.new_bib_content)

        self._run_main()

        result = self._read_output_json("invited_presentations.json")
        existing_titles = {e["title"] for e in self.existing_entries}
        result_titles = {e["title"] for e in result}

        for title in existing_titles:
            self.assertIn(title, result_titles, f"Existing entry '{title}' was lost during merge")

    def test_merge_appends_new_entries(self):
        """New BibTeX entries are appended after existing JSON entries."""
        self._write_existing_json("invited_presentations.json", self.existing_entries)
        self._write_bib_file("presentations", "2026.bib", self.new_bib_content)

        self._run_main()

        result = self._read_output_json("invited_presentations.json")
        self.assertEqual(len(result), len(self.existing_entries) + 1)

        # The new entry should be present
        new_titles = {e["title"] for e in result}
        self.assertIn("Brand New Talk Title", new_titles)

    def test_merge_deduplicates_by_title_and_year(self):
        """BibTeX entry matching existing JSON entry (same title + year) is not duplicated."""
        self._write_existing_json("invited_presentations.json", self.existing_entries)
        self._write_bib_file("presentations", "dup.bib", self.dup_bib_content)

        self._run_main()

        result = self._read_output_json("invited_presentations.json")
        # Count entries with the duplicate title
        matching = [e for e in result if e["title"] == "The Multi-scale Solar Wind"]
        self.assertEqual(len(matching), 1, "Duplicate entry was not deduplicated")

        # Total should remain the same
        self.assertEqual(len(result), len(self.existing_entries))

    def test_merge_empty_bibtex_preserves_json(self):
        """If no BibTeX files exist for a category, existing JSON is untouched."""
        self._write_existing_json("invited_presentations.json", self.existing_entries)
        # Create the category dir but with no .bib files
        (self.bibtex_dir / "presentations").mkdir(parents=True, exist_ok=True)

        self._run_main()

        result = self._read_output_json("invited_presentations.json")
        self.assertEqual(len(result), len(self.existing_entries))

    def test_merge_no_existing_json(self):
        """If JSON file doesn't exist yet, BibTeX entries create it fresh."""
        # Don't write any existing JSON
        self._write_bib_file("presentations", "2026.bib", self.new_bib_content)

        self._run_main()

        result = self._read_output_json("invited_presentations.json")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["title"], "Brand New Talk Title")


class TestMalformedBibtexWarnings(unittest.TestCase):
    """Tests that malformed BibTeX files trigger warnings."""

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_path = Path(self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_malformed_bibtex_premature_close_warns(self):
        """A .bib file with premature closing brace yields 0 entries and triggers a warning."""
        category_dir = self.temp_path / "presentations"
        category_dir.mkdir()

        # Malformed: entry closes immediately, fields are outside the entry
        malformed = """\
@inproceedings{Key,}
 author = {Alterman, B.~L.},
 title = {{Some Talk}},
 year = {2025},
"""
        bib_file = category_dir / "malformed.bib"
        bib_file.write_text(malformed, encoding="utf-8")

        # Capture stdout to check for warning
        captured = StringIO()
        with patch("sys.stdout", captured):
            entries = process_category(category_dir, "presentations")

        output = captured.getvalue()
        self.assertEqual(len(entries), 0, "Malformed BibTeX should yield 0 usable entries")
        self.assertIn("Warning", output, "Should print a warning about 0 entries from non-empty file")
        self.assertIn("malformed.bib", output)

    def test_nonempty_file_zero_entries_warns(self):
        """Any non-empty .bib file yielding 0 parsed entries triggers a warning."""
        category_dir = self.temp_path / "presentations"
        category_dir.mkdir()

        # Non-empty but no valid entries (just comments)
        content = "% This is a comment\n% Another comment\n"
        bib_file = category_dir / "comments_only.bib"
        bib_file.write_text(content, encoding="utf-8")

        captured = StringIO()
        with patch("sys.stdout", captured):
            entries = process_category(category_dir, "presentations")

        output = captured.getvalue()
        self.assertEqual(len(entries), 0)
        self.assertIn("Warning", output)
        self.assertIn("comments_only.bib", output)


class TestConversionRegression(unittest.TestCase):
    """Regression tests for existing BibTeX → JSON conversion logic."""

    def test_valid_bibtex_converts_correctly(self):
        """Well-formed BibTeX entry produces expected JSON fields."""
        entry = {
            "ID": "TestKey",
            "ENTRYTYPE": "inproceedings",
            "author": "Alterman, B. L.",
            "title": "Some Important Talk",
            "year": "2025",
            "month": "March",
            "day": "15",
            "booktitle": "Big Conference",
            "location": "New York, NY",
            "keywords": "invited",
        }

        result = convert_bibtex_entry_to_json(entry, "presentations")

        self.assertEqual(result["title"], "Some Important Talk")
        self.assertEqual(result["authors"], ["Alterman, B. L."])
        self.assertEqual(result["year"], "2025-03-15")
        self.assertEqual(result["publication_type"], "inproceedings")
        self.assertEqual(result["citations"], 0)
        self.assertTrue(result["invited"])
        self.assertEqual(result["booktitle"], "Big Conference")
        self.assertEqual(result["journal"], "Big Conference")
        self.assertEqual(result["location"], "New York, NY")
        self.assertEqual(result["keywords"], "invited")
        self.assertEqual(result["url"], "")

    def test_latex_formatting_stripped(self):
        r"""LaTeX commands like \textbf{Alterman, B.~L.} are stripped to plain text."""
        self.assertEqual(
            strip_latex_formatting(r"\textbf{Alterman, B.~L.}"),
            "Alterman, B. L.",
        )
        self.assertEqual(
            strip_latex_formatting(r"\emph{emphasized text}"),
            "emphasized text",
        )
        self.assertEqual(
            strip_latex_formatting(r"Plain text with~tilde"),
            "Plain text with tilde",
        )

    def test_date_formatting(self):
        """Year/month/day are formatted to YYYY-MM-DD."""
        self.assertEqual(format_date_field("2025", "March", "15"), "2025-03-15")
        self.assertEqual(format_date_field("2025", "01", "5"), "2025-01-05")
        self.assertEqual(format_date_field("2025", "", ""), "2025-00-00")
        self.assertEqual(format_date_field("2025", "June", ""), "2025-06-00")

    def test_keywords_preserved(self):
        """The keywords field passes through to JSON output."""
        entry = {
            "ID": "Key",
            "ENTRYTYPE": "inproceedings",
            "author": "Author",
            "title": "Title",
            "year": "2025",
            "keywords": "invited, solar-wind",
        }
        result = convert_bibtex_entry_to_json(entry, "presentations")
        self.assertEqual(result["keywords"], "invited, solar-wind")

    def test_entry_without_optional_fields(self):
        """Entries missing optional fields still convert without error."""
        entry = {
            "ID": "MinimalKey",
            "ENTRYTYPE": "inproceedings",
            "title": "Minimal Talk",
            "year": "2025",
        }
        result = convert_bibtex_entry_to_json(entry, "presentations")
        self.assertEqual(result["title"], "Minimal Talk")
        self.assertEqual(result["authors"], [])
        self.assertEqual(result["url"], "")
        self.assertNotIn("location", result)
        self.assertNotIn("keywords", result)

    def test_doi_creates_url(self):
        """DOI field produces a proper URL."""
        entry = {
            "ID": "DoiKey",
            "ENTRYTYPE": "inproceedings",
            "title": "Talk with DOI",
            "year": "2025",
            "doi": "10.1234/example",
        }
        result = convert_bibtex_entry_to_json(entry, "presentations")
        self.assertEqual(result["url"], "https://dx.doi.org/10.1234/example")

    def test_invited_url_field(self):
        """URL in BibTeX maps to invited_url in JSON (not url)."""
        entry = {
            "ID": "UrlKey",
            "ENTRYTYPE": "inproceedings",
            "title": "Talk with URL",
            "year": "2025",
            "url": "https://example.com/talk",
        }
        result = convert_bibtex_entry_to_json(entry, "presentations")
        self.assertEqual(result["invited_url"], "https://example.com/talk")
        self.assertEqual(result["url"], "")


class TestParsingRealFile(unittest.TestCase):
    """Tests that parse_bibtex_file works with real BibTeX syntax."""

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_path = Path(self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_parses_valid_bibtex(self):
        """A valid .bib file with two entries returns 2 parsed entries."""
        content = """\
@inproceedings{Talk1,
 author = {Alterman, B.~L.},
 title = {{First Talk}},
 year = {2025},
 month = {01},
 day = {10},
}

@inproceedings{Talk2,
 author = {Alterman, B.~L.},
 title = {{Second Talk}},
 year = {2025},
 month = {06},
 day = {20},
}
"""
        bib_file = self.temp_path / "valid.bib"
        bib_file.write_text(content, encoding="utf-8")

        entries = parse_bibtex_file(bib_file)
        self.assertEqual(len(entries), 2)

    def test_empty_file_returns_no_entries(self):
        """An empty .bib file returns an empty list."""
        bib_file = self.temp_path / "empty.bib"
        bib_file.write_text("", encoding="utf-8")

        entries = parse_bibtex_file(bib_file)
        self.assertEqual(len(entries), 0)


if __name__ == "__main__":
    print("Convert Invited BibTeX - Test Suite")
    print("=" * 50)
    unittest.main(argv=[""], exit=False, verbosity=2)
