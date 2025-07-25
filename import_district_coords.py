import csv
import os
import django
from pathlib import Path

# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pro_2.settings")
django.setup()

from report.models import District

# Path to the CSV file (same directory as manage.py)
BASE_DIR = Path(__file__).resolve().parent
csv_path = BASE_DIR / "district.csv"

with open(csv_path, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    updated = 0
    not_found = []

    for row in reader:
        name = row["shapeName"].strip()
        try:
            district = District.objects.get(name__iexact=name)
            district.latitude = float(row["Y"])
            district.longitude = float(row["X"])
            district.save()
            updated += 1
        except District.DoesNotExist:
            not_found.append(name)

print(f"✅ {updated} districts updated successfully.")
if not_found:
    print("⚠️ Not found in DB:", not_found)
