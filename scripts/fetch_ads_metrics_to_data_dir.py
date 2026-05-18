import ads
import requests
import os
import json
import argparse
import time
from pathlib import Path
from utils import get_public_data_dir, get_relative_path


def fetch_ads_metrics(orcid: str):
    token = os.getenv("ADS_DEV_KEY")
    if not token:
        raise EnvironmentError("ADS_DEV_KEY environment variable not set.")

    ads.config.token = token

    print(f"Fetching publications for ORCID: {orcid}")
    MAX_ATTEMPTS = 3
    BACKOFF_SECONDS = [60, 180]
    bibcodes = None
    for attempt in range(MAX_ATTEMPTS):
        try:
            results = ads.SearchQuery(orcid=orcid, fl=["bibcode"], rows=2000)
            # ADS load-sheds the ads-api-client User-Agent during high load;
            # override with a generic UA so requests aren't categorized as bot traffic.
            results.session.headers["User-Agent"] = "python-requests/2.32.3"
            bibcodes = [article.bibcode for article in results]
            break
        except ads.exceptions.APIResponseError as e:
            if attempt < MAX_ATTEMPTS - 1:
                wait = BACKOFF_SECONDS[attempt]
                print(f"⚠️  ADS API error on attempt {attempt + 1}/{MAX_ATTEMPTS}: {e}")
                print(f"   Retrying in {wait}s...")
                time.sleep(wait)
            else:
                print(f"✗ ADS API failed after {MAX_ATTEMPTS} attempts: {e}")
                raise

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
