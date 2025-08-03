
import requests
import json
import os

# Define mapping from license URL to short name
LICENSE_INFO = {
    "http://creativecommons.org/licenses/by/4.0/": "CC-BY-4.0",
    "https://creativecommons.org/licenses/by/4.0": "CC-BY-4.0",
    "https://creativecommons.org/licenses/by-nc/4.0/": "CC-BY-NC-4.0",
    "https://creativecommons.org/licenses/by-nc-nd/4.0/": "CC-BY-NC-ND-4.0",
    "http://creativecommons.org/licenses/by/3.0/": "CC-BY-3.0",
    # Springer Nature SharedIt license
    "https://www.springernature.com/gp/open-research/shared-standards#license": "SN-SharedIt-3.0",
    # Add more known license URLs here as needed...
}



def get_license_short(doi):
    """Fetches Crossref metadata for a DOI and returns only the short license name."""
    url = f"https://api.crossref.org/works/{doi}"
    resp = requests.get(url, headers={"Accept": "application/json"})
    if resp.status_code != 200:
        return "N/A"

    msg = resp.json().get("message", {})
    lic_list = msg.get("license", [])
    if not lic_list:
        return "N/A"

    lic_url = lic_list[0].get("URL", "")
    return LICENSE_INFO.get(lic_url, "Unknown")

def parse_doi_list(dois):
    """Processes a list of DOIs and returns a mapping DOI -> short license name."""
    return {doi: get_license_short(doi) for doi in dois}

if __name__ == "__main__":
    doi_list = [
        "10.3847/2041-8213/ab2391",
        "10.1007/s11207-021-01801-9",
        "10.1051/0004-6361/202451550"
    ]

    # Parse the DOIs
    license_data = parse_doi_list(doi_list)

    for k, v in license_data.items():
        print(f"DOI:            {k}")
        print(f"License Name:   {v}")
        print("-" * 40)

    # Ensure output directory exists
    output_path = "public/paper-figures/figure-licenses.json"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Write the JSON file
    with open(output_path, "w") as f:
        json.dump(license_data, f, indent=2)

    print(f"License data for {len(license_data)} DOIs written to {output_path}")
