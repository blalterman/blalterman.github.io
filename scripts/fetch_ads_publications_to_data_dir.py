import ads
import os
import json
import re
from datetime import datetime
from pathlib import Path
from utils import get_public_data_dir, get_relative_path
from html_to_unicode import convert_html_to_unicode

import pdb

def load_author_standardization_config():
    """Load author name standardization rules from config file."""
    config_path = Path(__file__).parent / "author_name_config.json"

    if not config_path.exists():
        print(f"⚠️  Warning: {config_path.name} not found, using no standardization rules")
        return {}

    with open(config_path, 'r') as f:
        data = json.load(f)

    # Convert to dictionary keyed by last name for fast lookup
    rules = {}
    for rule in data.get('standardization_rules', []):
        if rule.get('enabled', True):
            rules[rule['last_name']] = rule

    print(f"✓ Loaded {len(rules)} author standardization rule(s)")
    return rules

# Load configuration at module level
AUTHOR_STANDARDIZATION_CONFIG = load_author_standardization_config()

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

def standardize_author_name(author_name: str) -> str:
    """
    Standardize author names using configuration-based rules.

    Handles multiple format variants for configured authors:
    - Reverse format: "Lastname, Firstname..." (most common from ADS)
    - Forward format: "Firstname Lastname" (some publishers)
    - Initials vs full names: "Benjamin" vs "Ben" vs "B."
    - Spacing variations: "B.L." vs "B. L."

    Falls through to original name if no standardization rule matches.

    Args:
        author_name: Raw author name from ADS API

    Returns:
        Standardized author name (or original if no rule matches)
    """
    name = author_name.strip()

    # Check each configured author
    for last_name, config in AUTHOR_STANDARDIZATION_CONFIG.items():
        canonical = config['canonical']

        # Already canonical - return immediately
        if name == canonical:
            return name

        # Extract configuration
        last = config['last_name']
        first_initial = config['first_initial']
        middle_initial = config.get('middle_initial', '')
        first_names = config.get('first_names', [])

        # PATTERN GROUP 1: REVERSE FORMAT (Lastname, Firstname...)
        # Most common format from ADS API

        # Match: "Alterman, Benjamin L." or "Alterman, Benjamin"
        for first_name in first_names:
            # With optional middle initial (with/without period)
            pattern = rf'^{last},\s*{first_name}(\s+{middle_initial}\.?)?$'
            if re.match(pattern, name, re.IGNORECASE):
                return canonical

        # Match: "Alterman, B." (first initial only, missing middle)
        if re.match(rf'^{last},\s*{first_initial}\.$', name, re.IGNORECASE):
            return canonical

        # Match: "Alterman, B.L." (no space between initials)
        if middle_initial:
            if re.match(rf'^{last},\s*{first_initial}\.{middle_initial}\.$', name, re.IGNORECASE):
                return canonical

        # Match: "Alterman, B. L. L." (triple initial - data error)
        if middle_initial:
            if re.match(rf'^{last},\s*{first_initial}\.\s*{middle_initial}\.\s*{middle_initial}\.$', name, re.IGNORECASE):
                return canonical

        # PATTERN GROUP 2: FORWARD FORMAT (Firstname Lastname)
        # Less common but appears in some datasets (user-reported)

        # Match: "Benjamin L. Alterman" or "Benjamin Alterman"
        for first_name in first_names:
            # With optional middle initial
            pattern = rf'^{first_name}(\s+{middle_initial}\.?)?\s+{last}$'
            if re.match(pattern, name, re.IGNORECASE):
                return canonical

        # Match: "B. L. Alterman" or "B. Alterman"
        if middle_initial:
            # With optional middle initial
            pattern = rf'^{first_initial}\.(\s*{middle_initial}\.?)?\s+{last}$'
            if re.match(pattern, name, re.IGNORECASE):
                return canonical
        else:
            # Just first initial
            if re.match(rf'^{first_initial}\.\s+{last}$', name, re.IGNORECASE):
                return canonical

    # No standardization rule matched - return original name unchanged
    return name

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
    authors = [standardize_author_name(author) for author in pub.author] if pub.author else []
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
