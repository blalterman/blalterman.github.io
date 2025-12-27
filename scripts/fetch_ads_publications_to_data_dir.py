import ads
import os
import json
from datetime import datetime
from pathlib import Path
from utils import get_public_data_dir, get_relative_path
from html_to_unicode import convert_html_to_unicode

import pdb

# Venue name standardization mappings for conference publications
# Groups mappings by conference series for easy maintenance and extension
CONFERENCE_VENUE_MAPPINGS = {
    # SHINE conferences - consolidate all annual meetings to single name
    "Solar Heliospheric and INterplanetary Environment (SHINE 2015)": "SHINE",
    "Solar Heliospheric and INterplanetary Environment (SHINE 2016)": "SHINE",
    "Solar Heliospheric and INterplanetary Environment (SHINE 2017)": "SHINE",
    "Solar Heliospheric and INterplanetary Environment (SHINE 2018)": "SHINE",
    "Solar Heliospheric and INterplanetary Environment (SHINE 2019)": "SHINE",
    "SHINE 2022 Workshop": "SHINE",
    # COSPAR - standardize across different assembly numbers
    "43rd COSPAR Scientific Assembly. Held 28 January - 4 February": "COSPAR",
    "44th COSPAR Scientific Assembly. Held 16-24 July": "COSPAR",
    # Bulletin of the American Astronomical Society
    "Bulletin of the American Astronomical Society": "Bulletin of AAS",
    # Triennial Earth-Sun Summit - standardize naming
    "Third Triennial Earth-Sun Summit (TESS)": "Triennial Earth-Sun Summit",
    # APS Division of Plasma Physics
    "APS Division of Plasma Physics Meeting Abstracts": "APS Division of Plasma Physics",
    # EGU General Assembly - consolidate variants
    "EGU General Assembly Conference Abstracts": "EGU General Assembly",
    "European Geosciences Union General Assembly 2024 (EGU24)": "EGU General Assembly",
    # AGU Fall Meeting
    "AGU Fall Meeting Abstracts": "AGU Fall Meeting",
}

# Read ORCID and API token from environment variables
ORCID = os.getenv("ADS_ORCID")
token = os.getenv("ADS_DEV_KEY")
if not ORCID or not token:
    raise EnvironmentError(f"""Missing env variables.
ADS_ORCID   : {ORCID}
ADS_DEV_KEY : {token}""")

# Function to format author names as "Lastname, F. M." or "Lastname, F."
def format_author_name(author_name):
    """
    Format author name from ADS format.

    ADS returns: 'Lastname, F.' or 'Lastname, F. M.'
    Special handling: Ensures 'Alterman, B. L.' (not just 'Alterman, B.')
    """
    # ADS already provides formatted names, just apply Alterman fix
    formatted_name = author_name.strip()

    # Special handling for Alterman - enforce middle initial
    if formatted_name in ['Alterman, B.', 'Alterman, B.L.']:
        formatted_name = 'Alterman, B. L.'

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
    title = convert_html_to_unicode(title)  # Convert HTML tags to Unicode
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

    # Fix: ADS API returns "The Astrophysical Journal" for both ApJ and ApJL
    # Detect ApJL by bibcode pattern (...L..) or DOI prefix (2041-8213)
    is_apjl = False
    if "...L.." in pub.bibcode:  # Primary: bibcode pattern check
        is_apjl = True
    elif hasattr(pub, "doi") and pub.doi and "2041-8213" in pub.doi[0]:  # Fallback: DOI check
        is_apjl = True

    if is_apjl and journal == "The Astrophysical Journal":
        journal = "The Astrophysical Journal Letters"

    # Apply conference venue name standardization
    journal = CONFERENCE_VENUE_MAPPINGS.get(journal, journal)

    pub_type = pub.doctype or ""
    citations = pub.citation_count if hasattr(pub, "citation_count") else 0
    url = (
        f"https://dx.doi.org/{pub.doi[0]}"
        if hasattr(pub, "doi") and pub.doi
        else f"https://ui.adsabs.harvard.edu/abs/{pub.bibcode}"
    )

    publications.append(
        {
            "bibcode": pub.bibcode,
            "title": title,
            "authors": authors,
            "month": month,
            "year": year,
            "journal": journal, # This line is potentially problematic from previous edit. Fixing it here.
            "publication_type": pub_type,
            "citations": citations,
            "url": url,
            "invited": False,  # Default all publications to non-invited
        }
    )

# Save to public/data directory
public_data_dir = get_public_data_dir()
public_data_dir.mkdir(parents=True, exist_ok=True)
output_file = public_data_dir / "ads_publications.json"

with open(output_file, "w") as f:
    json.dump(publications, f, indent=2)

print(f"Saved {len(publications)} publications to {get_relative_path(output_file)}")
