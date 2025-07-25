import os
import django
import csv
import math

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pro_2.settings")
django.setup()

from report.models import Village, Cell

def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in km
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    d_phi = math.radians(lat2 - lat1)
    d_lambda = math.radians(lon2 - lon1)
    a = math.sin(d_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(d_lambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

# Load all villages with lat/lon already set, to skip them
villages_with_coords = Village.objects.exclude(latitude__isnull=True).exclude(longitude__isnull=True)
village_ids_with_coords = set(villages_with_coords.values_list("id", flat=True))

csv_path = "villages_cords.csv"  # Make sure this is your original file path
updated_count = 0
skipped_existing = []
not_found = []

with open(csv_path, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        name = row["shapeName"].strip()
        lat = float(row["Y"])
        lon = float(row["X"])

        # Find all villages with that name (case-insensitive)
        matching = Village.objects.filter(name__iexact=name)

        if not matching.exists():
            not_found.append(name)
            continue

        # Filter out those that already have coordinates
        matching = matching.filter(latitude__isnull=True, longitude__isnull=True)
        if not matching.exists():
            skipped_existing.append(name)
            continue

        if matching.count() == 1:
            village = matching.first()
        else:
            # Use Haversine to pick the closest one based on its cell
            closest = None
            min_dist = float("inf")
            for v in matching:
                cell_lat = v.cell.latitude
                cell_lon = v.cell.longitude
                if cell_lat and cell_lon:
                    dist = haversine(float(cell_lat), float(cell_lon), lat, lon)
                    if dist < min_dist:
                        min_dist = dist
                        closest = v
            village = closest

        if village:
            village.latitude = lat
            village.longitude = lon
            village.save()
            updated_count += 1
            print(f"✅ Updated village '{village.name}' (cell: {village.cell.name})")
        else:
            not_found.append(name)

print(f"\n✅ Total villages updated: {updated_count}")
if skipped_existing:
    print(f"⏭️ Skipped (already had lat/lon): {len(skipped_existing)}")
if not_found:
    print(f"❗ Villages not found or unresolved: {not_found}")
