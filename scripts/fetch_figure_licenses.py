
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

def fetch_licenses_for_dois(dois):
    """
    Main function to fetch licenses for a given list of DOIs.
    
    Args:
        dois (list): A list of DOI strings.
        
    Returns:
        dict: A dictionary mapping each DOI to its license short name.
    """
        
    return {doi: get_license_short(doi) for doi in dois}

