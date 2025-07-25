import csv
import os
import django
from pathlib import Path

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pro_2.settings")
django.setup()

from report.models import Province

# Path to the CSV file (same directory as manage.py)
BASE_DIR = Path(__file__).resolve().parent
csv_path = BASE_DIR / "province.csv"

with open(csv_path, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    updated = 0
    not_found = []

    for row in reader:
        name = row["shapeName"].strip()
        try:
            province = Province.objects.get(name__iexact=name)
            province.latitude = float(row["Y"])
            province.longitude = float(row["X"])
            province.save()
            updated += 1
        except Province.DoesNotExist:
            not_found.append(name)

print(f"✅ {updated} provinces updated successfully.")
if not_found:
    print("⚠️ Not found in DB:", not_found)
