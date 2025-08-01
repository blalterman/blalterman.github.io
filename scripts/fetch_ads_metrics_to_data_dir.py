import ads
import requests
import os
import json
import argparse
from pathlib import Path


def fetch_ads_metrics(orcid: str, data_dir: str = "data"):
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

    # Ensure the output directories exist
    data_path = Path(data_dir)
    public_data_path = Path("public") / data_path
    data_path.mkdir(parents=True, exist_ok=True)
    public_data_path.mkdir(parents=True, exist_ok=True)

    output_filename = "ads_metrics.json"
    data_output_path = data_path / output_filename
    public_data_output_path = public_data_path / output_filename

    with open(data_output_path, "w") as f:
        json.dump(metrics, f, indent=2)
    print(f"Metrics written to {data_output_path}")

    with open(public_data_output_path, "w") as f:
        json.dump(metrics, f, indent=2)
    print(f"Metrics written to {public_data_output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Fetch ADS citation metrics using ORCID."
    )
    parser.add_argument(
        "--orcid", type=str, required=True, help="ORCID ID of the author"
    )
    parser.add_argument(
        "--data_dir",
        type=str,
        default="data",
        help="Output data directory path",
    )

    args = parser.parse_args()
    fetch_ads_metrics(args.orcid, args.data_dir)
