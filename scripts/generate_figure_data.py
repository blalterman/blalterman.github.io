"""
Generate figure data by combining:
- Technical metadata from research-corpus (paper_metadata.json)
- Rich summaries from public/papers/{paper_id}/figures/figure_summaries.json
- Licenses from research-corpus (paper.license)
- Topic mappings from page-figure-mappings.json (transitional)

This replaces the old approach that called fetch_figure_licenses.py.
"""

import json
from pathlib import Path
from utils import get_repo_root, get_public_data_dir, get_relative_path


def load_corpus_metadata(corpus_dir: Path) -> dict:
    """Load all paper metadata from research-corpus."""
    papers = {}
    papers_dir = corpus_dir / "papers"

    if not papers_dir.exists():
        print(f"Warning: Corpus papers directory not found: {papers_dir}")
        return papers

    for paper_dir in papers_dir.iterdir():
        if not paper_dir.is_dir():
            continue

        metadata_file = paper_dir / "paper_metadata.json"
        if metadata_file.exists():
            with open(metadata_file, 'r') as f:
                data = json.load(f)
                paper_id = data.get("paper", {}).get("id", paper_dir.name)
                papers[paper_id] = data

    return papers


def load_figure_summaries(papers_dir: Path) -> dict:
    """Load all figure summaries from public/papers/."""
    summaries = {}

    if not papers_dir.exists():
        print(f"Warning: Papers directory not found: {papers_dir}")
        return summaries

    for paper_dir in papers_dir.iterdir():
        if not paper_dir.is_dir():
            continue

        summary_file = paper_dir / "figures" / "figure_summaries.json"
        if summary_file.exists():
            with open(summary_file, 'r') as f:
                data = json.load(f)
                paper_id = data.get("paper_id", paper_dir.name)
                # Index by figure_id for quick lookup
                figures_by_id = {fig["figure_id"]: fig for fig in data.get("figures", [])}
                summaries[paper_id] = {
                    "paper_title": data.get("paper_title"),
                    "paper_doi": data.get("paper_doi"),
                    "figures": figures_by_id
                }

    return summaries


def get_license_text(license_info: dict) -> str:
    """Format license information for display."""
    if not license_info:
        return ""

    holder = license_info.get("holder", "")
    year = license_info.get("year", "")
    license_type = license_info.get("type", "")

    if holder and year and license_type:
        return f"© {year} {holder}. {license_type}"
    elif license_info.get("full_text"):
        return license_info["full_text"]
    return ""


def generate_full_caption(fig_metadata: dict, pub_info: dict, license_info: dict = None) -> str:
    """Formats the figure caption with citation and license."""
    # Skip citation for placeholders or missing pub info
    if fig_metadata.get("placeholder") or not pub_info:
        return fig_metadata.get('caption', '')

    authors = pub_info.get("authors", [])
    year = pub_info.get("year", "")
    journal = pub_info.get("journal", "")
    url = pub_info.get("url")

    # Build author string
    if len(authors) == 1:
        author_str = authors[0].split(',')[0]
    elif len(authors) == 2:
        author_str = f"{authors[0].split(',')[0]} & {authors[1].split(',')[0]}"
    elif len(authors) > 2:
        author_str = f"{authors[0].split(',')[0]} et al."
    else:
        author_str = ""

    year_only = year.split('-')[0] if year else ""
    citation_text = f"From {author_str} ({year_only}), {journal}"

    if url:
        citation = f'<a href="{url}" target="_blank" rel="noopener noreferrer" class="text-primary hover:underline">{citation_text}</a>'
    else:
        citation = citation_text

    caption = f"{fig_metadata.get('caption', '')} {citation}."

    # Add license if available
    if license_info:
        license_text = get_license_text(license_info)
        if license_text:
            caption += f" {license_text}"

    return caption


def main():
    """
    Combines figure metadata from multiple sources to generate final output.

    Data sources:
    - research-corpus/papers/*/paper_metadata.json (technical metadata + licenses)
    - public/papers/*/figures/figure_summaries.json (rich summaries)
    - public/data/page-figure-mappings.json (topic → figure mappings)
    - public/data/ads_publications.json (publication info for citations)
    - public/paper-figures/figure-metadata.json (legacy metadata, transitional)
    """
    repo_root = get_repo_root()
    public_data_dir = get_public_data_dir()

    # Input paths
    projects_path = public_data_dir / "research-projects.json"
    page_mappings_path = public_data_dir / "page-figure-mappings.json"
    pubs_path = public_data_dir / "ads_publications.json"
    legacy_metadata_path = repo_root / "public" / "paper-figures" / "figure-metadata.json"
    output_path = public_data_dir / "research-figures-with-captions.json"

    # New data sources
    corpus_dir = repo_root / "research-corpus"
    papers_dir = repo_root / "public" / "papers"

    # Load all data sources
    with open(projects_path, 'r') as f:
        research_projects = json.load(f)
    with open(page_mappings_path, 'r') as f:
        page_mappings = json.load(f)
    with open(pubs_path, 'r') as f:
        pubs_data = json.load(f)

    # Load legacy metadata (for transitional compatibility)
    legacy_metadata = {}
    if legacy_metadata_path.exists():
        with open(legacy_metadata_path, 'r') as f:
            legacy_metadata = json.load(f)

    # Load new data sources
    corpus_metadata = load_corpus_metadata(corpus_dir)
    figure_summaries = load_figure_summaries(papers_dir)

    print(f"Loaded {len(corpus_metadata)} papers from corpus")
    print(f"Loaded {len(figure_summaries)} papers with summaries")

    # Create publication lookup
    pubs_lookup = {pub['bibcode']: pub for pub in pubs_data if 'bibcode' in pub}

    # Process each research project
    processed_data = []
    for project in research_projects:
        slug = project["slug"]
        figure_key = page_mappings.get(slug)

        if not figure_key:
            print(f"Warning: No figure mapping for {slug}")
            continue

        # Try legacy metadata first (transitional)
        fig_metadata = legacy_metadata.get(figure_key, {})

        if not fig_metadata:
            print(f"Warning: No metadata for figure {figure_key}")
            continue

        # Determine the source URL
        if fig_metadata.get("placeholder"):
            src = fig_metadata.get("src")
        else:
            # Use legacy path for now (will update to new paths later)
            src = f"/paper-figures/svg/{figure_key}"

        # Get publication info
        bibcode = fig_metadata.get("bibcode")
        pub_info = None
        license_info = None

        if bibcode and bibcode != "TODO":
            pub_info = pubs_lookup.get(bibcode)

            # Try to get license from corpus
            # Match bibcode to paper_id (this is a simplification - may need mapping table)
            for paper_id, corpus_data in corpus_metadata.items():
                paper = corpus_data.get("paper", {})
                if paper.get("doi") and pub_info and pub_info.get("url"):
                    # Check if DOIs match
                    corpus_doi = paper.get("doi", "").replace("https://doi.org/", "")
                    pub_doi = pub_info.get("url", "").replace("https://dx.doi.org/", "")
                    if corpus_doi == pub_doi:
                        license_info = paper.get("license")
                        break

        # Generate full caption
        full_caption = generate_full_caption(fig_metadata, pub_info, license_info)

        # Build output structure
        project_data = {
            "slug": slug,
            "title": project["title"],
            "figure": {
                "src": src,
                "alt": fig_metadata.get("alt", ""),
                "caption": full_caption
            }
        }

        # Add summary if available (for future use)
        # This requires mapping old filenames to paper_id/figure_id
        # Will be implemented when figure-topic-mappings.json is created

        processed_data.append(project_data)

    # Write output
    with open(output_path, 'w') as f:
        json.dump(processed_data, f, indent=2)

    print(f"Successfully generated {get_relative_path(output_path)}")


if __name__ == "__main__":
    main()
