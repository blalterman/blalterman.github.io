#!/usr/bin/env python3
"""
Interactive script for creating new research subpages.

This script helps create new research pages by:
1. Displaying existing pages and available figures
2. Prompting for user input with validation
3. Updating the three required JSON files
4. Providing preview and confirmation options

Usage:
    python scripts/create_research_page.py
    python scripts/create_research_page.py --dry-run
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Import utilities for path management
try:
    from utils import get_repo_root, get_public_data_dir
except ImportError:
    print("Error: Could not import utils.py. Make sure you're running from the repository root.")
    sys.exit(1)


class ResearchPageCreator:
    def __init__(self, dry_run: bool = False):
        self.dry_run = dry_run
        self.repo_root = get_repo_root()
        self.data_dir = get_public_data_dir()
        self.figures_dir = self.repo_root / "public" / "paper-figures" / "svg"

        # File paths
        self.projects_file = self.data_dir / "research-projects.json"
        self.mappings_file = self.data_dir / "page-figure-mappings.json"
        self.paragraphs_file = self.data_dir / "research-paragraphs.json"

        # Load existing data
        self.existing_projects = self._load_json(self.projects_file)
        self.existing_mappings = self._load_json(self.mappings_file)
        self.existing_paragraphs = self._load_json(self.paragraphs_file)
        self.available_figures = self._get_available_figures()

    def _load_json(self, file_path: Path) -> Dict:
        """Load JSON file with error handling."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Error: Could not find {file_path}")
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON in {file_path}: {e}")
            sys.exit(1)

    def _save_json(self, file_path: Path, data: Dict, backup: bool = True) -> None:
        """Save JSON file with pretty formatting and optional backup."""
        if backup and file_path.exists():
            backup_path = file_path.with_suffix(f"{file_path.suffix}.backup")
            backup_path.write_text(file_path.read_text())

        if self.dry_run:
            print(f"[DRY RUN] Would write to {file_path}")
            print(json.dumps(data, indent=2, ensure_ascii=False))
            return

        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            f.write('\n')  # Add trailing newline

    def _get_available_figures(self) -> List[str]:
        """Get list of available SVG figures."""
        if not self.figures_dir.exists():
            return []
        return sorted([f.name for f in self.figures_dir.glob("*.svg")])

    def _get_used_figures(self) -> List[str]:
        """Get list of currently assigned figures."""
        return [fig for fig in self.existing_mappings.values() if fig != "placeholder.png"]

    def _get_unused_figures(self) -> List[str]:
        """Get list of available but unassigned figures."""
        used = set(self._get_used_figures())
        return [fig for fig in self.available_figures if fig not in used]

    def _get_existing_slugs(self) -> List[str]:
        """Get list of existing slugs."""
        return [project['slug'] for project in self.existing_projects]

    def display_summary(self) -> None:
        """Display current research pages and available figures."""
        print("=" * 80)
        print("CURRENT RESEARCH PAGES")
        print("=" * 80)

        for project in self.existing_projects:
            slug = project['slug']
            figure = self.existing_mappings.get(slug, "NOT MAPPED")
            print(f"• {project['title']}")
            print(f"  Slug: {slug}")
            print(f"  Figure: {figure}")
            print(f"  Description: {project['description']}")
            print()

        print("=" * 80)
        print("AVAILABLE FIGURES")
        print("=" * 80)

        unused_figures = self._get_unused_figures()
        if unused_figures:
            print("Unused figures:")
            for figure in unused_figures:
                print(f"  • {figure}")
        else:
            print("All figures are currently assigned.")

        print(f"\nTotal available figures: {len(self.available_figures)}")
        print(f"Currently used figures: {len(self._get_used_figures())}")
        print()

    def _validate_slug(self, slug: str) -> Tuple[bool, str]:
        """Validate slug format and uniqueness."""
        if not slug:
            return False, "Slug cannot be empty"

        # Check format
        if not re.match(r'^[a-z0-9-]+$', slug):
            return False, "Slug must contain only lowercase letters, numbers, and hyphens"

        if slug.startswith('-') or slug.endswith('-'):
            return False, "Slug cannot start or end with a hyphen"

        if '--' in slug:
            return False, "Slug cannot contain consecutive hyphens"

        # Check uniqueness
        if slug in self._get_existing_slugs():
            return False, f"Slug '{slug}' already exists"

        return True, ""

    def _suggest_slug(self, title: str) -> str:
        """Generate a URL-friendly slug from title."""
        # Convert to lowercase, replace spaces with hyphens
        slug = re.sub(r'[^a-z0-9\s-]', '', title.lower())
        slug = re.sub(r'\s+', '-', slug.strip())
        slug = re.sub(r'-+', '-', slug)
        return slug.strip('-')

    def _validate_figure(self, figure: str) -> Tuple[bool, str]:
        """Validate figure exists and format."""
        if figure == "placeholder.png":
            return True, ""

        if figure not in self.available_figures:
            return False, f"Figure '{figure}' not found in {self.figures_dir}"

        return True, ""

    def prompt_for_input(self) -> Optional[Dict]:
        """Interactive prompts for new research page data."""
        print("=" * 80)
        print("CREATE NEW RESEARCH PAGE")
        print("=" * 80)

        try:
            # Title
            while True:
                title = input("Enter page title: ").strip()
                if title:
                    break
                print("Title cannot be empty.")

            # Slug
            suggested_slug = self._suggest_slug(title)
            while True:
                slug = input(f"Enter URL slug [{suggested_slug}]: ").strip() or suggested_slug
                valid, error = self._validate_slug(slug)
                if valid:
                    break
                print(f"Invalid slug: {error}")

            # Description
            while True:
                description = input("Enter brief description (1-2 sentences): ").strip()
                if description:
                    break
                print("Description cannot be empty.")

            # Detailed paragraph
            print("\nEnter detailed paragraph (press Enter twice to finish):")
            paragraph_lines = []
            while True:
                line = input()
                if line == "" and paragraph_lines:
                    break
                paragraph_lines.append(line)
            paragraph = " ".join(paragraph_lines).strip()

            if not paragraph:
                print("Warning: No detailed paragraph provided.")
                paragraph = description  # Fallback to description

            # Figure selection
            print("\nFigure options:")
            print("1. Use placeholder.png")
            unused_figures = self._get_unused_figures()
            if unused_figures:
                print("2. Choose from available figures:")
                for i, figure in enumerate(unused_figures, 3):
                    print(f"   {i}. {figure}")

            while True:
                choice = input("\nEnter choice number or figure filename: ").strip()

                if choice == "1":
                    figure = "placeholder.png"
                    break
                elif choice.isdigit():
                    idx = int(choice) - 3
                    if 0 <= idx < len(unused_figures):
                        figure = unused_figures[idx]
                        break
                elif choice in self.available_figures:
                    figure = choice
                    break
                else:
                    print("Invalid choice. Try again.")

            # Image hint (only for placeholder)
            image_hint = ""
            if figure == "placeholder.png":
                image_hint = input("Enter image hint for placeholder: ").strip()
                if not image_hint:
                    image_hint = "research visualization"

            return {
                'title': title,
                'slug': slug,
                'description': description,
                'paragraph': paragraph,
                'figure': figure,
                'image_hint': image_hint
            }

        except KeyboardInterrupt:
            print("\n\nOperation cancelled.")
            return None

    def preview_changes(self, data: Dict) -> None:
        """Show what will be added to each file."""
        print("=" * 80)
        print("PREVIEW OF CHANGES")
        print("=" * 80)

        print("research-projects.json - New entry:")
        new_project = {
            "title": data['title'],
            "slug": data['slug'],
            "description": data['description'],
            "image": "https://placehold.co/600x400.png",
            "imageHint": data['image_hint'] or "research visualization"
        }
        print(json.dumps(new_project, indent=2))

        print(f"\npage-figure-mappings.json - New mapping:")
        print(f'"{data["slug"]}": "{data["figure"]}"')

        print(f"\nresearch-paragraphs.json - New paragraph:")
        print(f'"{data["slug"]}": "{data["paragraph"]}"')

        print(f"\nNew page will be available at: /research/{data['slug']}")

    def update_files(self, data: Dict) -> bool:
        """Update all three JSON files with new data."""
        try:
            # Update research-projects.json
            new_project = {
                "title": data['title'],
                "slug": data['slug'],
                "description": data['description'],
                "image": "https://placehold.co/600x400.png",
                "imageHint": data['image_hint'] or "research visualization"
            }
            updated_projects = self.existing_projects + [new_project]

            # Update page-figure-mappings.json
            updated_mappings = self.existing_mappings.copy()
            updated_mappings[data['slug']] = data['figure']

            # Update research-paragraphs.json
            updated_paragraphs = self.existing_paragraphs.copy()
            updated_paragraphs[data['slug']] = data['paragraph']

            # Save all files
            self._save_json(self.projects_file, updated_projects)
            self._save_json(self.mappings_file, updated_mappings)
            self._save_json(self.paragraphs_file, updated_paragraphs)

            if not self.dry_run:
                print("✅ Successfully updated all files!")
                print(f"New research page created: /research/{data['slug']}")
                print("\nNext steps:")
                print("1. Run 'npm run build' to generate the static page")
                print("2. Commit and push the changes")

            return True

        except Exception as e:
            print(f"❌ Error updating files: {e}")
            return False

    def run(self) -> None:
        """Main script execution."""
        print("Research Page Creator")
        if self.dry_run:
            print("🧪 DRY RUN MODE - No files will be modified")
        print()

        self.display_summary()

        data = self.prompt_for_input()
        if not data:
            return

        self.preview_changes(data)

        if self.dry_run:
            print("\n🧪 DRY RUN COMPLETE - No changes made")
            return

        confirm = input("\nProceed with creating this research page? [y/N]: ").strip().lower()
        if confirm == 'y':
            self.update_files(data)
        else:
            print("Operation cancelled.")


def main():
    parser = argparse.ArgumentParser(description="Create new research subpages interactively")
    parser.add_argument("--dry-run", action="store_true",
                      help="Preview changes without modifying files")

    args = parser.parse_args()

    creator = ResearchPageCreator(dry_run=args.dry_run)
    creator.run()


if __name__ == "__main__":
    main()