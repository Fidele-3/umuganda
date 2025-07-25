import os
import django

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pro_2.settings")
django.setup()

from report.models import Cell, Sector, District

# Ordered list of cells with their correct coordinates
cells_data = [
    {
        "name": "Rwampara",
        "sector": "Kigarama",
        "district": "Kicukiro",
        "longitude": 30.0730474659655,
        "latitude": -1.96683535665393,
    },
    {
        "name": "Ryakibogo",
        "sector": "Gishamvu",
        "district": "Huye",
        "longitude": 29.707814878244,
        "latitude": -2.66071111821726,
    },
    {
        "name": "Terimbere",
        "sector": "Nyabirasi",
        "district": "Rutsiro",
        "longitude": 29.3139084359945,
        "latitude": -1.70478221392383,
    },
    {
        "name": "Gasizi",
        "sector": "Mukamira",
        "district": "Nyabihu",
        "longitude": 29.4842988757597,
        "latitude": -1.57348082382976,
    },
    {
        "name": "Murambi",
        "sector": "Cyato",
        "district": "Nyamasheke",
        "longitude": 29.2016983280098,
        "latitude": -2.38618088435112,
    },
    {
        "name": "Kabuga",
        "sector": "Kageyo",
        "district": "Gicumbi",
        "longitude": 30.0925060907527,
        "latitude": -1.65867722998348,
    },
    {
        "name": "Nyamiyaga",
        "sector": "Kageyo",
        "district": "Gicumbi",
        "longitude": 30.0807635878114,
        "latitude": -1.62053744276731,
    },
    {
        "name": "Gituza",
        "sector": "Kageyo",
        "district": "Gatsibo",
        "longitude": 30.2665842381777,
        "latitude": -1.69665290315583,
    },
    {
        "name": "Nyagisozi",
        "sector": "Kageyo",
        "district": "Gatsibo",
        "longitude": 30.2753714942435,
        "latitude": -1.67780751190928,
    },
]

updated = 0
not_found = []

for data in cells_data:
    try:
        cell = Cell.objects.get(
            name__iexact=data["name"],
            sector__name__iexact=data["sector"],
            sector__district__name__iexact=data["district"],
        )
        cell.latitude = data["latitude"]
        cell.longitude = data["longitude"]
        cell.save()
        updated += 1
        print(f"✅ Updated cell '{data['name']}' in sector '{data['sector']}' of district '{data['district']}'")
    except Cell.DoesNotExist:
        not_found.append(f"{data['name']} ({data['sector']} / {data['district']})")
    except Cell.MultipleObjectsReturned:
        print(f"⚠️ Multiple matches found for '{data['name']}' in '{data['sector']}' / '{data['district']}' – manual check needed")

print(f"\n✅ Total cells updated: {updated}")
if not_found:
    print("❌ Not found in DB:", not_found)
