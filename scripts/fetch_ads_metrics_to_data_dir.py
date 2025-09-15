import ads
import requests
import os
import json
import argparse
from pathlib import Path
from utils import get_public_data_dir, get_relative_path


def fetch_ads_metrics(orcid: str):
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
            "Content-Type": "application/json",
        },
        json={"bibcodes": bibcodes},
    )

    if response.status_code != 200:
        raise RuntimeError(f"ADS API error: {response.status_code} {response.text}")

    metrics = response.json()

    # Save metrics to public/data directory
    public_data_dir = get_public_data_dir()
    public_data_dir.mkdir(parents=True, exist_ok=True)
    output_file = public_data_dir / "ads_metrics.json"

    with open(output_file, "w") as f:
        json.dump(metrics, f, indent=2)

    print(f"Metrics written to {get_relative_path(output_file)}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Fetch ADS citation metrics using ORCID."
    )
    parser.add_argument(
        "--orcid", type=str, required=True, help="ORCID ID of the author"
    )

    args = parser.parse_args()
    fetch_ads_metrics(args.orcid)
