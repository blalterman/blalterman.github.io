import json
from pathlib import Path
from fetch_figure_licenses import fetch_licenses_for_dois

def generate_full_caption(caption_info, pub_info, license_info):
    """Formats the full figure caption with citation and license."""
    authors = pub_info.get("authors", [])
    year = pub_info.get("year", "")
    journal = pub_info.get("journal", "")
    
    # Use the license info passed in, default to "N/A"
    license_text = license_info or "N/A"

    # Create a simplified author list (e.g., Alterman et al.)
    first_author_lastname = ""
    if authors:
        first_author_lastname = authors[0].split(',')[0]

    author_str = f"{first_author_lastname} et al." if len(authors) > 1 else first_author_lastname

    citation = f"From {author_str} ({year}), {journal}."
    
    # Combine all parts
    full_caption = f"{caption_info.get('Caption', '')} {citation} © AAS. Reproduced with permission under a {license_text}."
    
    return full_caption.strip()


def main():
    """
    Generates a new JSON file with combined figure and publication data.
    """
    # Define paths
    data_dir = Path("data")
    public_dir = Path("public")
    
    projects_path = data_dir / "research-projects.json"
    figures_path = data_dir / "research-figures.json"
    captions_path = public_dir / "paper-figures" / "captions-bibcodes.json"
    pubs_path = public_dir / "data" / "ads_publications.json"
    paragraphs_path = data_dir / "research-paragraphs.json"
    output_path = data_dir / "research-figures-with-captions.json"

    # Load all necessary JSON files
    with open(projects_path, 'r') as f:
        research_projects = json.load(f)
    with open(figures_path, 'r') as f:
        research_figures_data = json.load(f)
    with open(captions_path, 'r') as f:
        captions_data = json.load(f)
    with open(pubs_path, 'r') as f:
        pubs_data = json.load(f)
    with open(paragraphs_path, 'r') as f:
        paragraphs_data = json.load(f)

    # Create a lookup for publications by bibcode for efficiency
    pubs_lookup = {pub['bibcode']: pub for pub in pubs_data}

    # Extract all unique bibcodes from the captions data
    required_bibcodes = set(data['bibcode'] for data in captions_data.values() if 'bibcode' in data)

    # Collect DOIs only for the required publications
    all_dois = []
    for bibcode in required_bibcodes:
        pub = pubs_lookup.get(bibcode)
        # The DOI is part of the URL, formatted as "https://dx.doi.org/{doi}"
        if pub and pub.get('url', '').startswith('https://dx.doi.org/'):
            doi = pub['url'].replace('https://dx.doi.org/', '')
            all_dois.append(doi)
    
    # Fetch all licenses for the collected DOIs
    print(f"Fetching licenses for {len(all_dois)} DOIs...")
    doi_to_license = fetch_licenses_for_dois(all_dois)
    print("...Done fetching licenses.")


    # Process the data
    processed_data = []
    for project in research_projects:
        slug = project["slug"]
        
        # Find the corresponding figure data using the slug
        figure_info = research_figures_data.get(slug)
        if not figure_info:
            continue
            
        # Get the paragraph for the project
        paragraph = paragraphs_data.get(slug, "")
            
        # Extract the SVG filename from the path
        svg_filename = Path(figure_info.get("src", "")).name
        
        # Find the corresponding caption info using the SVG filename
        caption_info = captions_data.get(svg_filename)
        if not caption_info:
            # Handle placeholders or figures without detailed captions
            project_data = {
                "slug": slug,
                "title": project["title"],
                "paragraph": paragraph,
                "figure": figure_info
            }
            processed_data.append(project_data)
            continue

        # Find the publication using the bibcode
        bibcode = caption_info.get("bibcode")
        pub_info = pubs_lookup.get(bibcode, {})
        
        # Get the license for the current DOI
        current_doi = None
        if pub_info.get('url', '').startswith('https://dx.doi.org/'):
            current_doi = pub_info['url'].replace('https://dx.doi.org/', '')

        license_info = doi_to_license.get(current_doi)

        # Generate the full caption
        full_caption = generate_full_caption(caption_info, pub_info, license_info)

        # Update the figure info with the new caption
        updated_figure_info = figure_info.copy()
        updated_figure_info["caption"] = full_caption
        
        # Combine into a single record for the new file
        project_data = {
            "slug": slug,
            "title": project["title"],
            "paragraph": paragraph,
            "figure": updated_figure_info
        }
        processed_data.append(project_data)

    # Write the processed data to the new file
    with open(output_path, 'w') as f:
        json.dump(processed_data, f, indent=2)

    print(f"Successfully generated {output_path}")

if __name__ == "__main__":
    main()
