from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from users.models.addresses import Cell, Sector, District, Province
from admn.models.sector_membership import sectorAdminMembership

@login_required
def get_cells_by_logged_in_sector(request):
    try:
        membership = sectorAdminMembership.objects.get(admin=request.user)
        sector_string = str(membership.sector)  # e.g., "Kimisagara (Nyarugenge, Umujyi wa Kigali)"

        # Split sector string into parts
        if "(" in sector_string and ")" in sector_string:
            sector_name, rest = sector_string.split("(", 1)
            sector_name = sector_name.strip()  # "Kimisagara"
            district_name, province_name = rest.strip(")").split(",")
            district_name = district_name.strip()  # "Nyarugenge"
            province_name = province_name.strip()  # "Umujyi wa Kigali"

            # Try to find the correct province
            province = Province.objects.get(name=province_name)

            # Then find the district within that province
            district = District.objects.get(name=district_name, province=province)

            # Then find the sector within that district
            sector = Sector.objects.get(name=sector_name, district=district)

            # Now fetch the cells in that exact sector
            cells = Cell.objects.filter(sector=sector)
            cell_list = [{'id': cell.id, 'name': cell.name} for cell in cells]
            return JsonResponse({'cells': cell_list})

        return JsonResponse({'cells': []})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
