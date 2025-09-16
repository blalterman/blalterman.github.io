#!/usr/bin/env python3
"""
Test script for create_research_page.py

This script tests the research page creation functionality including:
- Input validation
- JSON file operations
- Edge cases and error handling
- End-to-end functionality

Usage:
    python scripts/test_create_research_page.py
"""

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

# Import the module to test
import sys
sys.path.append(str(Path(__file__).parent))

from create_research_page import ResearchPageCreator


class TestResearchPageCreator(unittest.TestCase):
    def setUp(self):
        """Set up test environment with temporary files."""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_path = Path(self.temp_dir.name)

        # Create test data directories
        self.data_dir = self.temp_path / "data"
        self.figures_dir = self.temp_path / "figures"
        self.data_dir.mkdir()
        self.figures_dir.mkdir()

        # Create test JSON files
        self.test_projects = [
            {
                "title": "Test Research",
                "slug": "test-research",
                "description": "A test research topic",
                "image": "https://placehold.co/600x400.png",
                "imageHint": "test image"
            }
        ]

        self.test_mappings = {
            "test-research": "test-figure.svg"
        }

        self.test_paragraphs = {
            "test-research": "This is a test research paragraph."
        }

        # Write test files
        self.projects_file = self.data_dir / "research-projects.json"
        self.mappings_file = self.data_dir / "page-figure-mappings.json"
        self.paragraphs_file = self.data_dir / "research-paragraphs.json"

        with open(self.projects_file, 'w') as f:
            json.dump(self.test_projects, f)
        with open(self.mappings_file, 'w') as f:
            json.dump(self.test_mappings, f)
        with open(self.paragraphs_file, 'w') as f:
            json.dump(self.test_paragraphs, f)

        # Create test figure files
        (self.figures_dir / "available-figure.svg").touch()
        (self.figures_dir / "another-figure.svg").touch()
        (self.figures_dir / "test-figure.svg").touch()

        # Mock the creator with our test paths
        self.creator = ResearchPageCreator(dry_run=True)
        self.creator.data_dir = self.data_dir
        self.creator.figures_dir = self.figures_dir
        self.creator.projects_file = self.projects_file
        self.creator.mappings_file = self.mappings_file
        self.creator.paragraphs_file = self.paragraphs_file

        # Reload data with test files
        self.creator.existing_projects = self.creator._load_json(self.projects_file)
        self.creator.existing_mappings = self.creator._load_json(self.mappings_file)
        self.creator.existing_paragraphs = self.creator._load_json(self.paragraphs_file)
        self.creator.available_figures = self.creator._get_available_figures()

    def tearDown(self):
        """Clean up temporary files."""
        self.temp_dir.cleanup()

    def test_slug_validation_valid(self):
        """Test valid slug formats."""
        valid_slugs = [
            "valid-slug",
            "another-valid-slug",
            "slug123",
            "valid-slug-with-numbers-123"
        ]

        for slug in valid_slugs:
            with self.subTest(slug=slug):
                valid, error = self.creator._validate_slug(slug)
                self.assertTrue(valid, f"Slug '{slug}' should be valid: {error}")

    def test_slug_validation_invalid(self):
        """Test invalid slug formats."""
        invalid_slugs = [
            "",  # Empty
            "-invalid",  # Starts with hyphen
            "invalid-",  # Ends with hyphen
            "invalid--slug",  # Double hyphen
            "Invalid-Slug",  # Uppercase
            "invalid slug",  # Spaces
            "invalid_slug",  # Underscore
            "invalid@slug",  # Special characters
        ]

        for slug in invalid_slugs:
            with self.subTest(slug=slug):
                valid, error = self.creator._validate_slug(slug)
                self.assertFalse(valid, f"Slug '{slug}' should be invalid")
                self.assertNotEqual(error, "", f"Error message should be provided for '{slug}'")

    def test_slug_validation_duplicate(self):
        """Test duplicate slug detection."""
        valid, error = self.creator._validate_slug("test-research")
        self.assertFalse(valid)
        self.assertIn("already exists", error)

    def test_slug_suggestion(self):
        """Test slug generation from titles."""
        test_cases = [
            ("Solar Energetic Particles", "solar-energetic-particles"),
            ("Test Research Topic!", "test-research-topic"),
            ("Multiple   Spaces", "multiple-spaces"),
            ("Title with Numbers 123", "title-with-numbers-123"),
            ("Special@Characters#Removed", "specialcharactersremoved"),
        ]

        for title, expected in test_cases:
            with self.subTest(title=title):
                result = self.creator._suggest_slug(title)
                self.assertEqual(result, expected)

    def test_figure_validation(self):
        """Test figure validation."""
        # Valid cases
        valid, error = self.creator._validate_figure("placeholder.png")
        self.assertTrue(valid)

        valid, error = self.creator._validate_figure("available-figure.svg")
        self.assertTrue(valid)

        # Invalid case
        valid, error = self.creator._validate_figure("nonexistent-figure.svg")
        self.assertFalse(valid)
        self.assertIn("not found", error)

    def test_get_unused_figures(self):
        """Test unused figures detection."""
        unused = self.creator._get_unused_figures()
        expected = ["another-figure.svg", "available-figure.svg"]  # test-figure.svg is used
        self.assertEqual(sorted(unused), sorted(expected))

    def test_json_file_operations(self):
        """Test JSON loading and saving."""
        # Test loading
        projects = self.creator._load_json(self.projects_file)
        self.assertEqual(len(projects), 1)
        self.assertEqual(projects[0]['slug'], 'test-research')

        # Test saving (dry run mode)
        new_data = projects + [{"title": "New", "slug": "new", "description": "New desc"}]
        # Should not raise exception in dry run mode
        self.creator._save_json(self.projects_file, new_data)

    def test_update_files_dry_run(self):
        """Test file updates in dry run mode."""
        test_data = {
            'title': 'New Research Topic',
            'slug': 'new-research-topic',
            'description': 'A new research topic for testing',
            'paragraph': 'This is a detailed paragraph about the new research topic.',
            'figure': 'available-figure.svg',
            'image_hint': 'test hint'
        }

        # Should succeed in dry run mode
        result = self.creator.update_files(test_data)
        self.assertTrue(result)

        # Original files should remain unchanged
        projects = self.creator._load_json(self.projects_file)
        self.assertEqual(len(projects), 1)  # Still only original project

    def test_edge_cases(self):
        """Test edge cases and error conditions."""
        # Test with very long strings
        long_title = "A" * 1000
        slug = self.creator._suggest_slug(long_title)
        self.assertLessEqual(len(slug), 1000)

        # Test empty figure list scenario
        self.creator.available_figures = []
        unused = self.creator._get_unused_figures()
        self.assertEqual(unused, [])

    def test_data_consistency(self):
        """Test that operations maintain data consistency."""
        # Check that all existing slugs have mappings and paragraphs
        slugs = self.creator._get_existing_slugs()
        for slug in slugs:
            self.assertIn(slug, self.creator.existing_mappings, f"Slug {slug} missing from mappings")
            self.assertIn(slug, self.creator.existing_paragraphs, f"Slug {slug} missing from paragraphs")


class TestIntegrationScenarios(unittest.TestCase):
    """Integration tests for common usage scenarios."""

    def setUp(self):
        """Set up for integration tests."""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_path = Path(self.temp_dir.name)

        # Create realistic test environment
        self.data_dir = self.temp_path / "data"
        self.figures_dir = self.temp_path / "figures"
        self.data_dir.mkdir()
        self.figures_dir.mkdir()

        # Create realistic test data
        self.projects = [
            {
                "title": "Proton Beams",
                "slug": "proton-beams",
                "description": "Testing proton beam research",
                "image": "https://placehold.co/600x400.png",
                "imageHint": "proton beams"
            }
        ]

        self.mappings = {"proton-beams": "placeholder.png"}
        self.paragraphs = {"proton-beams": "Proton beam research details."}

        # Create files
        files_data = [
            (self.data_dir / "research-projects.json", self.projects),
            (self.data_dir / "page-figure-mappings.json", self.mappings),
            (self.data_dir / "research-paragraphs.json", self.paragraphs)
        ]

        for file_path, data in files_data:
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=2)

        # Create figure files
        for figure in ["solar-particles.svg", "wind-analysis.svg", "plasma-data.svg"]:
            (self.figures_dir / figure).touch()

    def tearDown(self):
        """Clean up integration test environment."""
        self.temp_dir.cleanup()

    def test_complete_workflow(self):
        """Test complete workflow from input to file updates."""
        creator = ResearchPageCreator(dry_run=True)
        creator.data_dir = self.data_dir
        creator.figures_dir = self.figures_dir
        creator.projects_file = self.data_dir / "research-projects.json"
        creator.mappings_file = self.data_dir / "page-figure-mappings.json"
        creator.paragraphs_file = self.data_dir / "research-paragraphs.json"

        # Reload with test data
        creator.existing_projects = creator._load_json(creator.projects_file)
        creator.existing_mappings = creator._load_json(creator.mappings_file)
        creator.existing_paragraphs = creator._load_json(creator.paragraphs_file)
        creator.available_figures = creator._get_available_figures()

        # Test data for new page
        test_data = {
            'title': 'Solar Energetic Particles',
            'slug': 'solar-energetic-particles',
            'description': 'Study of high-energy particles from solar events',
            'paragraph': 'Solar energetic particles are accelerated during solar flares and coronal mass ejections.',
            'figure': 'solar-particles.svg',
            'image_hint': 'particle acceleration'
        }

        # Test the complete update process
        result = creator.update_files(test_data)
        self.assertTrue(result)

        # Verify validation would work for this data
        valid_slug, _ = creator._validate_slug(test_data['slug'])
        self.assertTrue(valid_slug)

        valid_figure, _ = creator._validate_figure(test_data['figure'])
        self.assertTrue(valid_figure)


def run_manual_tests():
    """Run manual tests that require user interaction."""
    print("Running manual integration tests...")
    print("These tests check the interactive functionality.")

    # Test dry run mode
    print("\n1. Testing dry run mode:")
    print("   Run: python scripts/create_research_page.py --dry-run")
    print("   Expected: Should show current pages and allow input without making changes")

    print("\n2. Testing input validation:")
    print("   Try entering invalid slugs (with spaces, uppercase, etc.)")
    print("   Expected: Should reject invalid input with helpful error messages")

    print("\n3. Testing figure selection:")
    print("   Try selecting different figures from the list")
    print("   Expected: Should validate figure existence")

    print("\n4. Testing cancellation:")
    print("   Start the script and press Ctrl+C")
    print("   Expected: Should exit gracefully with 'Operation cancelled' message")


if __name__ == "__main__":
    print("Research Page Creator - Test Suite")
    print("=" * 50)

    # Run unit tests
    print("Running unit tests...")
    unittest.main(argv=[''], exit=False, verbosity=2)

    print("\n" + "=" * 50)
    run_manual_tests()