import requests
import json
import os

# 1) Define a mapping from license URL → (License Name, License Holder)
LICENSE_INFO = {
    "http://creativecommons.org/licenses/by/4.0/": (
        "Creative Commons Attribution 4.0 International",
        "Creative Commons"
    ),
    "https://creativecommons.org/licenses/by-nc/4.0/": (
        "Creative Commons Attribution-NonCommercial 4.0 International",
        "Creative Commons"
    ),
    "https://creativecommons.org/licenses/by-nc-nd/4.0/": (
        "Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International",
        "Creative Commons"
    ),
    "http://creativecommons.org/licenses/by/3.0/": (
        "Creative Commons Attribution 3.0 Licence",
        "Creative Commons"
    ),
    # Add more known license URLs here as needed...
}

def get_license_record(doi):
    """Fetches Crossref metadata for a DOI and returns license info dict."""
    url = f"https://api.crossref.org/works/{doi}"
    resp = requests.get(url, headers={"Accept": "application/json"})
    if resp.status_code != 200:
        return {
            "doi": doi,
            "name": "N/A",
            "url": "N/A",
            "holder": "N/A"
        }

    msg = resp.json().get("message", {})
    lic_list = msg.get("license", [])
    if not lic_list:
        return {
            "doi": doi,
            "name": "N/A",
            "url": "N/A",
            "holder": "N/A"
        }

    lic = lic_list[0]  # take the first license block
    lic_url = lic.get("URL", "")
    name, holder = LICENSE_INFO.get(
        lic_url,
        # Fallback if URL not in our map:
        ("Unknown license", "N/A")
    )
    return {
        "doi": doi,
        "name": name,
        "url": lic_url,
        "holder": holder
    }

def parse_doi_list(dois):
    """Processes a list of DOIs and returns a list of license info objects."""
    results = []
    for doi in dois:
        results.append(get_license_record(doi))
    return results

if __name__ == "__main__":
    # Example DOIs (replace or extend with your own list)
    doi_list = [
        "10.1038/s41586-020-2649-2",
        "10.1103/PhysRevLett.116.061102",
        "10.1000/xyz123"   # non-existent or closed-access example
    ]

    # Parse the DOIs
    license_data = parse_doi_list(doi_list)

    for row in license_data:
        print(f"DOI:            {row['doi']}")
        print(f"License Name:   {row['name']}")
        print(f"License URL:    {row['url']}")
        print(f"License Holder: {row['holder']}")
        print("-" * 40)

    # Ensure output directory exists
    output_path = "public/paper-figures/figure-licenses.json"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Write the JSON file
    with open(output_path, "w") as f:
        json.dump(license_data, f, indent=2)

    print(f"License data for {len(license_data)} DOIs written to {output_path}")
