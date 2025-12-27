"""Quick validation of author name standardization."""

import json
from utils import get_public_data_dir

data_dir = get_public_data_dir()
with open(data_dir / "ads_publications.json", 'r') as f:
    pubs = json.load(f)

# Find all Alterman name variants
variants = {}
for pub in pubs:
    for author in pub.get('authors', []):
        if 'alterman' in author.lower():
            variants[author] = variants.get(author, 0) + 1

print("\nAlterman Name Variants:")
for name, count in sorted(variants.items(), key=lambda x: x[1], reverse=True):
    status = "✅" if name == "Alterman, B. L." else "❌"
    print(f"  {status} {count:3d} - {name}")

correct = variants.get("Alterman, B. L.", 0)
total = sum(variants.values())
print(f"\nStandardization: {correct}/{total} ({correct/total*100:.1f}%) correct")

if len(variants) == 1 and "Alterman, B. L." in variants:
    print("✅ ALL NAMES STANDARDIZED!")
else:
    print(f"❌ {len(variants)-1} variant(s) still need fixing")
