from django.views import View
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from umuganda.models import UmugandaSession
from admn.models.cell_admin_membership import CellAdminMembership
from admn.models.sector_membership import sectorAdminMembership  

@method_decorator(login_required, name='dispatch')
class UmugandaSessionListView(View):
    template_name = 'admin/session_list.html'

    def get(self, request):
        user = request.user

        sessions = None
        working_cell = None
        working_sector = None

        # ✅ If user is sector officer
        if user.user_level == 'sector_officer':
            sector_membership_qs = sectorAdminMembership.objects.filter(admin=user, is_active=True)
            if not sector_membership_qs.exists():
                return render(request, 'cell_not_assigned.html', status=403)

            working_sector = sector_membership_qs.first().sector

            # ✅ Fetch all sessions under the sector (by matching cell.sector)
            sessions = UmugandaSession.objects.filter(cell__sector=working_sector).order_by('-date')

        # ✅ If user is cell officer
        elif user.user_level == 'cell_officer':
            cell_membership_qs = CellAdminMembership.objects.filter(admin=user, is_active=True)
            if not cell_membership_qs.exists():
                return render(request, 'cell_not_assigned.html', status=403)

            working_cell = cell_membership_qs.first().cell

            # ✅ Fetch sessions by cell
            sessions = UmugandaSession.objects.filter(cell=working_cell).order_by('-date')

        # ❌ If user level is not recognized
        else:
            return render(request, 'cell_not_assigned.html', status=403)

        # ✅ Render template with context
        return render(request, self.template_name, {
            'sessions': sessions,
            'working_cell': working_cell,
            'working_sector': working_sector,
            'user': user
        })
