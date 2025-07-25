import os
import django
import csv
import math

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pro_2.settings")
django.setup()

from report.models import Cell, Sector

# Haversine formula to calculate distance between two points on Earth
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in km
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    d_phi = math.radians(lat2 - lat1)
    d_lambda = math.radians(lon2 - lon1)
    a = math.sin(d_phi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(d_lambda/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

# Load sectors and their lat/lon in memory
sectors = list(Sector.objects.filter(latitude__isnull=False, longitude__isnull=False))
print(f"Loaded {len(sectors)} sectors with coordinates.")

csv_path = "cells_cords.csv"  # Your CSV file in the same dir as manage.py

updated_count = 0
not_found = []

with open(csv_path, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        cell_name = row["shapeName"].strip()
        cell_lat = float(row["Y"])
        cell_lon = float(row["X"])

        # Find closest sector by Haversine distance
        closest_sector = None
        min_distance = float('inf')
        for sector in sectors:
            distance = haversine(cell_lat, cell_lon, float(sector.latitude), float(sector.longitude))
            if distance < min_distance:
                min_distance = distance
                closest_sector = sector

        if not closest_sector:
            print(f"⚠️ No sector with coordinates found for cell '{cell_name}', skipping.")
            continue

        try:
            # Find cell by name and closest sector
            cell = Cell.objects.get(name__iexact=cell_name, sector=closest_sector)
            cell.latitude = cell_lat
            cell.longitude = cell_lon
            cell.save()
            updated_count += 1
            print(f"✅ Updated cell '{cell_name}' assigned to sector '{closest_sector.name}' (distance {min_distance:.2f} km)")
        except Cell.DoesNotExist:
            not_found.append(f"{cell_name} (closest sector: {closest_sector.name})")
        except Cell.MultipleObjectsReturned:
            print(f"⚠️ Multiple cells named '{cell_name}' found in sector '{closest_sector.name}', manual check needed.")

print(f"\nTotal updated cells: {updated_count}")
if not_found:
    print("Cells not found in DB (or need manual addition):", not_found)
