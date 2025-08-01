import ads
import os
import json
from datetime import datetime

# Read ORCID and API token from environment variables
ORCID = os.getenv("ADS_ORCID")
token = os.getenv("ADS_DEV_KEY")
if not ORCID or not token:
    raise EnvironmentError("ADS_ORCID and ADS_DEV_KEY must be set in the environment.")

# Fields to request from ADS
fields = [
    "bibcode", "title", "author", "pubdate", "pub", "doctype",
    "citation_count", "doi"
]

# Query ADS
results = list(ads.SearchQuery(orcid=ORCID, fl=fields, rows=2000))

# Build structured JSON data
publications = []
for pub in results:
    title = pub.title[0] if pub.title else "(No title)"
    authors = pub.author if pub.author else []
    pubdate = pub.pubdate or ""
    month, year = "", ""
    if pubdate:
        try:
            dt = datetime.strptime(pubdate, "%Y-%m")
            month = dt.strftime("%B")
            year = str(dt.year)
        except ValueError:
            year = pubdate
    journal = pub.pub or ""
    pub_type = pub.doctype or ""
    citations = pub.citation_count if hasattr(pub, "citation_count") else 0
    url = f"https://dx.doi.org/{pub.doi[0]}" if hasattr(pub, "doi") and pub.doi else f"https://ui.adsabs.harvard.edu/abs/{pub.bibcode}"

    publications.append({
        "bibcode": pub.bibcode,
        "title": title,
        "authors": authors,
        "month": month,
        "year": year,
        "journal": journal,
        "publication_type": pub_type,
        "citations": citations,
        "url": url
    })

# Ensure _data/ directory exists and save to JSON
os.makedirs("_data", exist_ok=True)
with open("_data/ads_publications.json", "w") as f:
    json.dump(publications, f, indent=2)

print(f"Saved {len(publications)} publications to _data/ads_publications.json")
