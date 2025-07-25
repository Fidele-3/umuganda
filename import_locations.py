import os
import django
import json

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pro_2.settings')  # use your correct settings module here
django.setup()

from report.models import Province, District, Sector, Cell, Village

with open("report/fixtures/locations.json", "r", encoding="utf-8") as f:
    data = json.load(f)

for province_data in data["provinces"]:
    province = Province.objects.create(name=province_data["name"])
    for district_data in province_data.get("districts", []):
        district = District.objects.create(name=district_data["name"], province=province)
        for sector_data in district_data.get("sectors", []):
            sector = Sector.objects.create(name=sector_data["name"], district=district)
            for cell_data in sector_data.get("cells", []):
                cell = Cell.objects.create(name=cell_data["name"], sector=sector)
                for village_data in cell_data.get("villages", []):
                    Village.objects.create(name=village_data["name"], cell=cell)

print("✅ Location data imported successfully.")
