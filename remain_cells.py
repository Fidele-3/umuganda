import os
import django
import csv
import math

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pro_2.settings")
django.setup()

from report.models import Cell, Sector

def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0  # Earth radius in km
    from math import radians, cos, sin, sqrt, atan2

    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    lat1 = radians(lat1)
    lat2 = radians(lat2)

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c

csv_path = "cells_cords.csv"  # CSV file path (same dir as manage.py)

updated_count = 0
not_found = []
duplicates = []

with open(csv_path, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        cell_name = row["shapeName"].strip()
        cell_lat = float(row["Y"])
        cell_lon = float(row["X"])

        # Query all cells matching the name (case-insensitive)
        matching_cells = list(Cell.objects.filter(name__iexact=cell_name).select_related('sector'))

        if not matching_cells:
            not_found.append(cell_name)
            continue

        if len(matching_cells) == 1:
            # Exactly one cell found with this name
            cell = matching_cells[0]
            if cell.latitude is None or cell.longitude is None:
                cell.latitude = cell_lat
                cell.longitude = cell_lon
                cell.save()
                updated_count += 1
                print(f"✅ Updated cell '{cell_name}' (single match)")
            else:
                print(f"ℹ️ Cell '{cell_name}' already has coordinates, skipped.")
        else:
            # Multiple cells with same name - pick closest sector by haversine to CSV coords
            closest_cell = None
            min_distance = float('inf')

            for c in matching_cells:
                sec = c.sector
                if sec.latitude is None or sec.longitude is None:
                    # Cannot compare distances without sector coords, skip this candidate
                    continue
                dist = haversine(cell_lat, cell_lon, float(sec.latitude), float(sec.longitude))
                if dist < min_distance:
                    min_distance = dist
                    closest_cell = c

            if closest_cell:
                if closest_cell.latitude is None or closest_cell.longitude is None:
                    closest_cell.latitude = cell_lat
                    closest_cell.longitude = cell_lon
                    closest_cell.save()
                    updated_count += 1
                    print(f"✅ Updated cell '{cell_name}' (closest match in sector '{closest_cell.sector.name}')")
                else:
                    print(f"ℹ️ Cell '{cell_name}' (closest match) already has coordinates, skipped.")
            else:
                duplicates.append(cell_name)
                print(f"⚠️ Multiple cells named '{cell_name}', but no sectors with coordinates to decide closest match.")

print(f"\nTotal updated cells: {updated_count}")
if not_found:
    print(f"Cells not found in DB: {not_found}")
if duplicates:
    print(f"Cells with ambiguous multiple matches lacking sector coordinates: {duplicates}")
