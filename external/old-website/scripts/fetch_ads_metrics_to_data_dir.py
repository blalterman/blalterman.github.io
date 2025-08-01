import ads
import requests
import os
import json
import argparse

def fetch_ads_metrics(orcid: str, output_file: str = "_data/ads_metrics.json"):
    token = os.getenv("ADS_DEV_KEY")
    if not token:
        raise EnvironmentError("ADS_DEV_KEY environment variable not set.")

    print(f"Fetching publications for ORCID: {orcid}")
    results = ads.SearchQuery(orcid=orcid, fl=["bibcode"], rows=2000)
    bibcodes = [article.bibcode for article in results]

    if not bibcodes:
        raise ValueError("No bibcodes found for this ORCID.")

    print(f"Found {len(bibcodes)} bibcodes. Requesting metrics...")
    response = requests.post(
        "https://api.adsabs.harvard.edu/v1/metrics",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        },
        json={"bibcodes": bibcodes}
    )

    if response.status_code != 200:
        raise RuntimeError(f"ADS API error: {response.status_code} {response.text}")

    metrics = response.json()

    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    with open(output_file, "w") as f:
        json.dump(metrics, f, indent=2)

    print(f"Metrics written to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch ADS citation metrics using ORCID.")
    parser.add_argument("--orcid", type=str, required=True, help="ORCID ID of the author")
    parser.add_argument("--output", type=str, default="_data/ads_metrics.json", help="Output JSON file path")

    args = parser.parse_args()
    fetch_ads_metrics(args.orcid, args.output)
