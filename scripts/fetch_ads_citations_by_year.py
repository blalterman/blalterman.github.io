"""
Fetches yearly citation counts for all NASA ADS publications associated with a given ORCID.

Reads ADS_ORCID and ADS_DEV_KEY from environment variables, retrieves all bibcodes, then fetches citation histograms per year from the NASA ADS metrics API. Outputs a JSON file and an SVG plot.

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
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path
import os
import json
import sys

import pandas as pd

from zoneinfo import ZoneInfo

# Hard code Eastern Time because changing that is a quick update,
# but it requires a lot of package installs and such to auto-detect.
local_tz = ZoneInfo("America/New_York")

import pdb

# === Read ORCID and API token from environment variables ===
ORCID_ID = os.getenv("ADS_ORCID")
ADS_DEV_KEY = os.getenv("ADS_DEV_KEY")

if not ORCID_ID or not ADS_DEV_KEY:
    raise ValueError("Both ADS_ORCID and ADS_DEV_KEY must be set in the environment.")

ads.config.token = ADS_DEV_KEY

# === Step 1: Get all bibcodes ===
print("Querying NASA ADS for publications...")
# results = ads.SearchQuery(orcid=ORCID_ID, fl=["bibcode"], rows=2000)
# bibcodes = [paper.bibcode for paper in results]

results = ads.SearchQuery(
    orcid=ORCID_ID,
    fl=[
        "bibcode",
        # "property"
    ],
    rows=2000,
)

bibcodes = []
# is_refereed = {}
for paper in results:
    bibcodes.append(paper.bibcode)
#     props = getattr(paper, "property", []) or []
#     is_refereed[paper.bibcode] = "REFEREED" in props

# print(f"Found {len(bibcodes)} papers ({sum([v for k, v in is_refereed.items() if v])} refereed).")
print(f"Found {len(bibcodes)} papers.")

# === Step 2: Query citation histogram by year ===
headers = {"Authorization": f"Bearer {ADS_DEV_KEY}"}
refereed_citations = dict()
nonrefereed_citations = dict()

# keys_to_get_citations = {"refereed":
#                      {"refereed": "refereed to refereed",
#                      "nonrefereed": "refereed to nonrefereed"},
#                      "nonrefereed":
#                      {"refereed": "nonrefereed to refereed",
#                      "nonrefereed": "nonrefereed to nonrefereed"},
#                      }

refereed_keys = ("refereed to refereed", "nonrefereed to refereed")
nonrefereed_keys = ("refereed to nonrefereed", "nonrefereed to nonrefereed")


def print_failure_msg(i, bibcode, response):

    if response.status_code != 429:
        print(f"""Failed to get metrics for ({i}) {bibcode}"""
)
        return

    reset_time = int(response.headers["X-RateLimit-Reset"])
    reset_dt = int(response.headers["Retry-After"])

    reset_time = datetime.fromtimestamp(reset_time, tz=ZoneInfo("UTC"))
    reset_dt = timedelta(seconds=reset_dt)

    print(
        f"""
Failed to get metrics
Bibcode          : {bibcode}
Status Code      : {response.status_code}
Reason           : {response.reason}
Retry After      : {reset_time.astimezone(local_tz)}
Wait Time        : {reset_dt}
Rate Exceeded at : {(reset_time - reset_dt).astimezone(local_tz)}

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

    #     print(i, bibcode)
    #     print(hist)

    #     print(is_refereed[bibcode])
    #     hist_keys = keys_to_get_citations["refereed" if is_refereed[bibcode] else "nonrefereed"]
    #     refereed_keys = [k for k in hist.keys() if k.endswith("to refereed")]
    #     nonrefereed_keys = [k for k in hist.keys() if k.endswith("to nonrefereed")]

    for k in refereed_keys:
        case = hist.get(k, {})
        for kk, vv in case.items():
            refereed_citations[(bibcode, k, kk)] = vv
    for k in nonrefereed_keys:
        case = hist.get(k, {})
        for kk, vv in case.items():
            nonrefereed_citations[(bibcode, k, kk)] = vv

# 	refereed_citations[(bibcode, k)] = hist.get(hist_keys["refereed"], {})
#     nonrefereed_citations[bibcode] = hist.get(hist_keys["nonrefereed"], {})

#     for year, count in hist.get(hist_keys["refereed"], {}).items():
#         refereed_citations[int(year)] += count
#     for year, count in hist.get(hist_keys["nonrefereed"], {}).items():
#         nonrefereed_citations[int(year)] += count

# pdb.set_trace()
# 
# refereed_citations = [
#     {"year": k, "citations": v} for k, v in refereed_citations.items()
# ]
# nonrefereed_citations = [
#     {"year": k, "citations": v} for k, v in nonrefereed_citations.items()
# ]

# === Step 3: Align years and prepare data
refereed_citations = pd.Series(refereed_citations)
nonrefereed_citations = pd.Series(nonrefereed_citations)

# print(refereed_citations)
# print(nonrefereed_citations)
# 
# all_years = sorted(set(refereed_citations) | set(nonrefereed_citations))
# ref_counts = [refereed_citations.get(y, 0) for y in all_years]
# nonref_counts = [nonrefereed_citations.get(y, 0) for y in all_years]

# ref_counts = refereed_citations.sum(axis=1)
# nonref_counts = nonrefereed_citations.sum(axis=1)
# all_counts = pd.concat({"refereed": ref_counts, "nonrefereed": nonref_counts}, axis=1)

ref_counts = refereed_citations.groupby(level=-1).sum()
nonref_counts = nonrefereed_citations.groupby(level=-1).sum()
all_counts = pd.concat({"Refereed": ref_counts, "Nonrefereed": nonref_counts}, axis=1)

print(all_counts.T, "", sep="\n")
# print(ref_counts)
# print(nonref_counts)
print(
    f"""
Total Citations
Refereed    : {ref_counts.sum()}
Nonrefereed : {nonref_counts.sum()}
Total       : {all_counts.sum().sum()}
"""
)

all_years = all_counts.index.tolist()
ref_counts = all_counts.Refereed.tolist()
nonref_counts = all_counts.Nonrefereed.tolist()


# === Step 4: Save citation data to data/ and public/data/
data_dir = Path("data")
public_data_dir = Path("public") / data_dir
data_dir.mkdir(parents=True, exist_ok=True)
public_data_dir.mkdir(parents=True, exist_ok=True)

output_filename = "citations_by_year.json"
data_output_path = data_dir / output_filename
public_data_output_path = public_data_dir / output_filename

data_to_save = {"years": all_years, "refereed": ref_counts, "nonrefereed": nonref_counts}

with open(data_output_path, "w") as f:
    json.dump(data_to_save, f, indent=2)
print(f"Citation data saved to {data_output_path}")

with open(public_data_output_path, "w") as f:
    json.dump(data_to_save, f, indent=2)
print(f"Citation data saved to {public_data_output_path}")


# === Step 5: Plot and save SVG and PNG to public/plots/
image_output_dir = Path("public") / "plots"
image_output_dir.mkdir(parents=True, exist_ok=True)

plt.figure(figsize=(10, 6))
plt.plot(
    all_years,
    ref_counts,
    label="Refereed",
    color="cornflowerblue",
    linestyle="-",
    linewidth=2,
)
plt.plot(
    all_years,
    nonref_counts,
    label="Non-Refereed",
    color="lightgreen",
    linestyle="--",
    linewidth=2,
)
plt.title("Citations per Year by Type (NASA ADS)")
plt.xlabel("Year")
plt.ylabel("Citations")
plt.legend()
plt.tight_layout()

plot_path_svg = image_output_dir / "citations_by_year.svg"
plt.savefig(plot_path_svg, format="svg")
print(f"Plot saved to {plot_path_svg}")

plot_path_png = image_output_dir / "citations_by_year.png"
plt.savefig(plot_path_png, format="png")
print(f"Plot saved to {plot_path_png}")
