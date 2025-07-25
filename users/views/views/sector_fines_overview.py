from django.views import View
from django.shortcuts import render
from umuganda.models import Fine
from users.models.addresses import Cell
from users.models.userprofile import UserProfile

class SectorFinesOverviewView(View):
    template_name = 'admin/admin_level2_dashboard.html'

    def get(self, request):
        user = request.user
        if user.user_level != 'sector_officer':
            return render(request, 'not_authorized.html')

        sector = user.profile.sector
        cells = Cell.objects.filter(sector=sector)

        context = {
            'cells': cells
        }
        return render(request, self.template_name, context)
