from django.views import View
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from umuganda.models import UmugandaSession, CellUmugandaSession
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

        # ✅ Sector Officer
        if user.user_level == 'sector_officer':
            sector_membership_qs = sectorAdminMembership.objects.filter(admin=user, is_active=True)
            if not sector_membership_qs.exists():
                return render(request, 'cell_not_assigned.html', status=403)

            working_sector = sector_membership_qs.first().sector

            # ✅ All sessions for this sector
            sessions = UmugandaSession.objects.filter(sector=working_sector).order_by('-date')

        # ✅ Cell Officer
        elif user.user_level == 'cell_officer':
            cell_membership_qs = CellAdminMembership.objects.filter(admin=user, is_active=True)
            if not cell_membership_qs.exists():
                return render(request, 'cell_not_assigned.html', status=403)

            working_cell = cell_membership_qs.first().cell

            # ✅ Filter UmugandaSession where this cell has a CellUmugandaSession entry
            cell_sessions = CellUmugandaSession.objects.filter(cell=working_cell).select_related('sector_session')
            sessions = [cs.sector_session for cs in cell_sessions]
            sessions = sorted(sessions, key=lambda s: s.date, reverse=True)

        # ❌ Unknown user level
        else:
            return render(request, 'cell_not_assigned.html', status=403)

        return render(request, self.template_name, {
            'sessions': sessions,
            'working_cell': working_cell,
            'working_sector': working_sector,
            'user': user
        })
