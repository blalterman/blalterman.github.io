import ads
import os
import json
from datetime import datetime
from pathlib import Path

# Read ORCID and API token from environment variables
ORCID = os.getenv("ADS_ORCID")
token = os.getenv("ADS_DEV_KEY")
if not ORCID or not token:
    raise EnvironmentError(f"""Missing env variables.
ADS_ORCID   : {ORCID}
ADS_DEV_KEY : {token}""")

# Function to format author names as "Lastname, F. M." or "Lastname, F."
def format_author_name(author_name):
    parts = author_name.split()
    if not parts:
        return ""
    last_name = parts[-1]
    first_initial = parts[0][0] if len(parts) > 1 else ""
    middle_initial = parts[1][0] if len(parts) > 2 else ""

    formatted_name = f"{last_name}, {first_initial}." # This line is potentially problematic from previous edit. Fixing it here.
    if middle_initial:
        formatted_name += f" {middle_initial}."
    return formatted_name

# Fields to request from ADS
fields = [
    "bibcode",
    "title",
    "author",
    "pubdate",
    "pub",
    "doctype",
    "citation_count",
    "doi",
]

# Query ADS
results = list(ads.SearchQuery(orcid=ORCID, fl=fields, rows=2000))

# Build structured JSON data
publications = []
for pub in results:
    title = pub.title[0] if pub.title else "(No title)"
    authors = [format_author_name(author) for author in pub.author] if pub.author else []
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
    url = (
        f"https://dx.doi.org/{pub.doi[0]}"
        if hasattr(pub, "doi") and pub.doi
        else f"https://ui.adsabs.harvard.edu/abs/{pub.bibcode}"
    )

    # Wrap "Alterman" in <strong> tags in the authors list
    formatted_authors = []
    for author in authors:
        if author.startswith("Alterman,"):
            formatted_authors.append(f"<strong>{author}</strong>")
        else:
            formatted_authors.append(author)

    publications.append(
        {
            "bibcode": pub.bibcode,
            "title": title,
            "authors": formatted_authors,
            "month": month,
            "year": year,
            "journal": journal, # This line is potentially problematic from previous edit. Fixing it here.
            "publication_type": pub_type,
            "citations": citations,
            "url": url,
        }
    )

# Ensure data/ and public/data/ directories exists and save to JSON.
# Use both because public/ is scraped for SEO and data/ allows for static build.
target_dirs = (Path("../public/data"), Path("../data"))
for target in target_dirs:
    os.makedirs(target, exist_ok=True)
    with open(target / "ads_publications.json", "w") as f:
        json.dump(publications, f, indent=2)
    print(f"Saved {len(publications)} publications to {target}")
