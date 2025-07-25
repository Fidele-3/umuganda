import os
import django
import csv
from math import radians, cos, sin, sqrt, atan2

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pro_2.settings")
django.setup()

from report.models import Sector

def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in km
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

csv_path = "sector.csv"  # Adjust if needed

with open(csv_path, newline="", encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)
    updated = 0
    not_found = []
    no_district_coords = []

    for row in reader:
        sector_name = row["shapeName"].strip()
        lat = float(row["Y"])
        lon = float(row["X"])

        sectors = Sector.objects.filter(name__iexact=sector_name)

        if not sectors.exists():
            not_found.append(sector_name)
            continue

        # Find closest sector by district's coordinates
        min_dist = None
        closest_sector = None
        for sector in sectors:
            district = sector.district
            if district.latitude is None or district.longitude is None:
                no_district_coords.append(sector_name)
                continue
            dist = haversine(lat, lon, float(district.latitude), float(district.longitude))
            if min_dist is None or dist < min_dist:
                min_dist = dist
                closest_sector = sector

        if closest_sector:
            closest_sector.latitude = lat
            closest_sector.longitude = lon
            closest_sector.save()
            updated += 1
        else:
            no_district_coords.append(sector_name)

print(f"✅ Updated {updated} sectors with latitude and longitude.")
if not_found:
    print(f"⚠️ These sectors were not found in DB: {not_found}")
if no_district_coords:
    print(f"⚠️ These sectors have no district coordinates: {set(no_district_coords)}")
