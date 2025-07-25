import os
import django
import csv
import math

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pro_2.settings")
django.setup()

from report.models import Village, Cell

# Haversine distance formula
def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    d_phi = math.radians(lat2 - lat1)
    d_lambda = math.radians(lon2 - lon1)
    a = math.sin(d_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(d_lambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

# Load all cells with coordinates for Haversine conflict resolution
cells_with_coords = list(Cell.objects.exclude(latitude__isnull=True).exclude(longitude__isnull=True))

if not cells_with_coords:
    print("❌ No cells have coordinates. Cannot compute Haversine.")
    exit()

csv_path = "villages_cords.csv"  # Make sure this file is in your project dir

updated = 0
not_found = []

with open(csv_path, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        village_name = row["shapeName"].strip()
        village_lat = float(row["Y"])
        village_lon = float(row["X"])

        # First, try to find exact match among villages
        matching_villages = Village.objects.filter(name__iexact=village_name)

        if matching_villages.count() == 1:
            village = matching_villages.first()
            village.latitude = village_lat
            village.longitude = village_lon
            village.save()
            updated += 1
            print(f"✅ Updated village '{village_name}' directly")
        elif matching_villages.count() > 1:
            # Use Haversine to resolve among multiple matches
            best_match = None
            min_distance = float("inf")
            for v in matching_villages:
                cell = v.cell
                if cell.latitude is not None and cell.longitude is not None:
                    dist = haversine(village_lat, village_lon, float(cell.latitude), float(cell.longitude))
                    if dist < min_distance:
                        min_distance = dist
                        best_match = v

            if best_match:
                best_match.latitude = village_lat
                best_match.longitude = village_lon
                best_match.save()
                updated += 1
                print(f"✅ Updated '{village_name}' using Haversine (cell: {best_match.cell.name}, distance: {min_distance:.2f} km)")
            else:
                not_found.append(village_name)
                print(f"⚠️ Multiple villages named '{village_name}', but none with usable cell coordinates.")
        else:
            not_found.append(village_name)
            print(f"❌ Village '{village_name}' not found in DB.")

print(f"\n✅ Total villages updated: {updated}")
if not_found:
    print(f"❗ Villages not found or unresolved conflicts: {not_found}")
