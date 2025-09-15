
"""
Fetches yearly citation counts for all NASA ADS publications associated with a given ORCID.

Reads ADS_ORCID and ADS_DEV_KEY from environment variables, retrieves all bibcodes, then fetches citation histograms per year from the NASA ADS metrics API. Outputs a JSON file and an SVG plot.

This script includes a caching mechanism. If the output data file has been modified
in the last 7 days, it will skip the download and processing steps.

Raises
------
ValueError
    If required environment variables are not set.

Example
-------
$ python scripts/fetch_ads_citations_by_year.py
"""

import ads
import requests
import matplotlib.pyplot as plt
from datetime import datetime, timedelta, timezone
from pathlib import Path
import os
import json
import sys

import pandas as pd

from zoneinfo import ZoneInfo
from utils import get_public_data_dir, get_public_plots_dir, get_relative_path

# Hard code Eastern Time because changing that is a quick update,
# but it requires a lot of package installs and such to auto-detect.
local_tz = ZoneInfo("America/New_York")

# === Define output paths and check cache ===
public_data_dir = get_public_data_dir()
output_filename = "citations_by_year.json"
cached_json_path = public_data_dir / output_filename

# Caching logic
if cached_json_path.exists():
    last_modified_time = datetime.fromtimestamp(cached_json_path.stat().st_mtime, tz=timezone.utc)
    if datetime.now(timezone.utc) - last_modified_time < timedelta(days=7):
        print(f"Cached data at {get_relative_path(cached_json_path)} is less than 7 days old. Skipping download.")
        # Optionally load the data if needed by subsequent steps
        with open(cached_json_path, "r") as f:
            cached_data = json.load(f)
        print("Loaded data from cache.")
        sys.exit(0) # Exit successfully
    else:
        print("Cached data is older than 7 days. Fetching new data.")
else:
    print("No cached data found. Fetching new data.")


# === Read ORCID and API token from environment variables ===
ORCID_ID = os.getenv("ADS_ORCID")
ADS_DEV_KEY = os.getenv("ADS_DEV_KEY")

if not ORCID_ID or not ADS_DEV_KEY:
    raise ValueError("Both ADS_ORCID and ADS_DEV_KEY must be set in the environment.")

ads.config.token = ADS_DEV_KEY

# === Step 1: Get all bibcodes ===
print("Querying NASA ADS for publications...")
results = ads.SearchQuery(
    orcid=ORCID_ID,
    fl=["bibcode"],
    rows=2000,
)
bibcodes = [paper.bibcode for paper in results]
print(f"Found {len(bibcodes)} papers.")

# === Step 2: Query citation histogram by year ===
headers = {"Authorization": f"Bearer {ADS_DEV_KEY}"}
refereed_citations = dict()
nonrefereed_citations = dict()

refereed_keys = ("refereed to refereed", "nonrefereed to refereed")
nonrefereed_keys = ("refereed to nonrefereed", "nonrefereed to nonrefereed")


def print_failure_msg(i, bibcode, response):
    if response.status_code != 429:
        print(f"""Failed to get metrics for ({i}) {bibcode}""")
        return

    reset_time = int(response.headers["X-RateLimit-Reset"])
    reset_dt = int(response.headers["Retry-After"])
    reset_time_utc = datetime.fromtimestamp(reset_time, tz=ZoneInfo("UTC"))
    reset_dt_td = timedelta(seconds=reset_dt)

    print(
        f"""
Failed to get metrics
Bibcode          : {bibcode}
Status Code      : {response.status_code}
Reason           : {response.reason}
Retry After      : {reset_time_utc.astimezone(local_tz)}
Wait Time        : {reset_dt_td}
Rate Exceeded at : {(reset_time_utc - reset_dt_td).astimezone(local_tz)}

Exiting program
"""
    )
    sys.exit(1)  # Stop making more calls


print("Downloading citation data by year...")
for i, bibcode in enumerate(bibcodes, 1):
    if not (i % 10):
        print(f"Downloading bibcode {i} ({bibcode})")
        
    url = f"https://api.adsabs.harvard.edu/v1/metrics/{bibcode}"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print_failure_msg(i, bibcode, response)
        continue

    data = response.json()
    hist = data.get("histograms", {}).get("citations", {})

    for k in refereed_keys:
        case = hist.get(k, {})
        for kk, vv in case.items():
            refereed_citations[(bibcode, k, kk)] = vv
    for k in nonrefereed_keys:
        case = hist.get(k, {})
        for kk, vv in case.items():
            nonrefereed_citations[(bibcode, k, kk)] = vv


# === Step 3: Align years and prepare data ===
refereed_citations = pd.Series(refereed_citations)
nonrefereed_citations = pd.Series(nonrefereed_citations)

ref_counts = refereed_citations.groupby(level=-1).sum().sort_index()
nonref_counts = nonrefereed_citations.groupby(level=-1).sum().sort_index()
all_counts = pd.concat({"Refereed": ref_counts, "Nonrefereed": nonref_counts}, axis=1).fillna(0).astype(int)

print(all_counts.T, "", sep="\n")
print(
    f"""
Total Citations
Refereed    : {all_counts.Refereed.sum()}
Nonrefereed : {all_counts.Nonrefereed.sum()}
Total       : {all_counts.sum().sum()}
"""
)

all_years = all_counts.index.tolist()
ref_counts = all_counts.Refereed.tolist()
nonref_counts = all_counts.Nonrefereed.tolist()


# === Step 4: Save JSON data ===
public_data_dir.mkdir(parents=True, exist_ok=True)
output_path = public_data_dir / output_filename

data_to_save = {"years": all_years, "refereed": ref_counts, "nonrefereed": nonref_counts}

with open(output_path, "w") as f:
    json.dump(data_to_save, f, indent=2)

print(f"Citation data saved to {get_relative_path(output_path)}")


# === Step 5: Plot and save SVG and PNG to public/plots/ ===
image_output_dir = get_public_plots_dir()
image_output_dir.mkdir(parents=True, exist_ok=True)

plt.figure(figsize=(10, 6))
plt.bar(all_years, ref_counts, label="Refereed", color="cornflowerblue")
plt.bar(all_years, nonref_counts, bottom=ref_counts, label="Non-Refereed", color="lightgreen")

plt.title("Citations per Year by Type (NASA ADS)")
plt.xlabel("Year")
plt.ylabel("Citations")
plt.legend()
plt.tight_layout()

plot_path_svg = image_output_dir / "citations_by_year.svg"
plt.savefig(plot_path_svg, format="svg")
print(f"Plot saved to {get_relative_path(plot_path_svg)}")

plot_path_png = image_output_dir / "citations_by_year.png"
plt.savefig(plot_path_png, format="png")
print(f"Plot saved to {get_relative_path(plot_path_png)}")
