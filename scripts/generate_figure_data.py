import json
from pathlib import Path
from fetch_figure_licenses import fetch_licenses_for_dois
from utils import get_repo_root, get_public_data_dir, get_relative_path

def generate_full_caption(figure_metadata, pub_info):
    """Formats the figure caption with citation."""
    # Skip citation for placeholders or missing pub info
    if figure_metadata.get("placeholder") or not pub_info:
        return figure_metadata.get('caption', '')

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

    return f"{figure_metadata.get('caption', '')} {citation}."

def main():
    """
    Combines figure metadata and page mappings to generate final output.
    Clean and simple: every page maps to a figure (real or placeholder).
    """
    # Define paths
    public_data_dir = get_public_data_dir()
    repo_root = get_repo_root()

    # Input files
    projects_path = public_data_dir / "research-projects.json"
    figure_metadata_path = repo_root / "public" / "paper-figures" / "figure-metadata.json"
    page_mappings_path = public_data_dir / "page-figure-mappings.json"
    pubs_path = public_data_dir / "ads_publications.json"
    output_path = public_data_dir / "research-figures-with-captions.json"

    # Load JSON files
    with open(projects_path, 'r') as f:
        research_projects = json.load(f)
    with open(figure_metadata_path, 'r') as f:
        figure_metadata = json.load(f)
    with open(page_mappings_path, 'r') as f:
        page_mappings = json.load(f)
    with open(pubs_path, 'r') as f:
        pubs_data = json.load(f)

    # Create publication lookup (filter out publications without bibcode, e.g., manually added invited talks)
    pubs_lookup = {pub['bibcode']: pub for pub in pubs_data if 'bibcode' in pub}

    # Collect DOIs for license fetching (only for real figures)
    all_dois = []
    for fig_name, metadata in figure_metadata.items():
        if not metadata.get("placeholder"):
            bibcode = metadata.get('bibcode')
            if bibcode and bibcode != "TODO":
                pub = pubs_lookup.get(bibcode)
                if pub and pub.get('url', '').startswith('https://dx.doi.org/'):
                    doi = pub['url'].replace('https://dx.doi.org/', '')
                    all_dois.append(doi)

    # Fetch licenses
    print(f"Fetching licenses for {len(all_dois)} DOIs...")
    doi_to_license = fetch_licenses_for_dois(all_dois)
    print("...Done fetching licenses.")

    # Process each research project
    processed_data = []
    for project in research_projects:
        slug = project["slug"]
        figure_key = page_mappings.get(slug)

        if not figure_key:
            print(f"Warning: No figure mapping for {slug}")
            continue

        # Get figure metadata
        fig_metadata = figure_metadata.get(figure_key)
        if not fig_metadata:
            print(f"Warning: No metadata for figure {figure_key}")
            continue

        # Determine the source URL
        if fig_metadata.get("placeholder"):
            # Use the src field for placeholder
            src = fig_metadata.get("src")
        else:
            # Build src from filename for SVG files
            src = f"/paper-figures/svg/{figure_key}"

        # Get publication info if bibcode exists and is valid
        bibcode = fig_metadata.get("bibcode")
        pub_info = None
        if bibcode and bibcode != "TODO":
            pub_info = pubs_lookup.get(bibcode)

        # Generate full caption (handles placeholders automatically)
        full_caption = generate_full_caption(fig_metadata, pub_info)

        # Create output structure
        project_data = {
            "slug": slug,
            "title": project["title"],
            "figure": {
                "src": src,
                "alt": fig_metadata.get("alt", ""),
                "caption": full_caption
            }
        }
        processed_data.append(project_data)

    # Write output
    with open(output_path, 'w') as f:
        json.dump(processed_data, f, indent=2)

    print(f"Successfully generated {get_relative_path(output_path)}")

if __name__ == "__main__":
    main()