import os
import django

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pro_2.settings")
django.setup()

from report.models import Sector, District

# Sectors to update with their exact names and district names
sectors_to_update = [
    {
        "name": "Rugendabari",
        "district_name": "Burera",
        "latitude": -1.54461354082771,
        "longitude": 29.7978283173,
    },
    {
        "name": "Ririma",
        "district_name": "Bugesera",
        "latitude": -2.17103416689021,
        "longitude": 30.200119792854,
    },
]

updated_count = 0
not_found = []

for sector_info in sectors_to_update:
    try:
        district = District.objects.get(name__iexact=sector_info["district_name"])
    except District.DoesNotExist:
        print(f"⚠️ District '{sector_info['district_name']}' not found in DB")
        continue

    try:
        sector = Sector.objects.get(name__iexact=sector_info["name"], district=district)
        # Update latitude and longitude only
        sector.latitude = sector_info["latitude"]
        sector.longitude = sector_info["longitude"]
        sector.save()
        updated_count += 1
        print(f"✅ Updated sector '{sector_info['name']}' in district '{sector_info['district_name']}'")
    except Sector.DoesNotExist:
        not_found.append(f"{sector_info['name']} ({sector_info['district_name']})")
    except Sector.MultipleObjectsReturned:
        print(f"⚠️ Multiple sectors found named '{sector_info['name']}' in district '{sector_info['district_name']}' - manual check needed")

print(f"\nTotal updated sectors: {updated_count}")
if not_found:
    print("Sectors not found in DB:", not_found)
