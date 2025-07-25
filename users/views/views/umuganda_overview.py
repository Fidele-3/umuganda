# admn/views/umuganda_overview.py

from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from users.models import CustomUser
from admn.models import AdminHierarchy
from sector.models.sector import AdminSector
from users.models.addresses import Sector
from umuganda.models import UmugandaSession  # adjust import if needed

class SuperAdminUmugandaOverviewView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user

        if user.user_level != 'super_admin':
            return redirect('unauthorized')

        # 1. Get all sector officers added by this superadmin
        sector_admins = AdminHierarchy.objects.filter(
            added_by=user,
            admin__user_level='sector_officer'
        ).select_related('admin')

        data = []

        for hierarchy in sector_admins:
            sector_officer = hierarchy.admin

            # 2. Get all sectors managed by this officer
            sectors = AdminSector.objects.filter(admin=sector_officer).select_related('sector')

            for admin_sector in sectors:
                sector = admin_sector.sector

                # 3. Fetch UmugandaSessions for this sector
                sessions = UmugandaSession.objects.filter(sector=sector).select_related(
                    'created_by', 'updated_by_cell_admin', 'cell', 'village'
                ).order_by('-date')

                sector_data = {
                    'sector_name': sector.name,
                    'sector_officer': sector_officer.full_names,
                    'umuganda_sessions': []
                }

                for session in sessions:
                    sector_data['umuganda_sessions'].append({
                        'date': session.date,
                        'description': session.description,
                        'tools_needed': session.tools_needed,
                        'fines_policy': session.fines_policy,
                        'cell': session.cell.name if session.cell else None,
                        'village': session.village.name if session.village else None,
                        'created_by': session.created_by.full_names if session.created_by else None,
                        'updated_by': session.updated_by_cell_admin.full_names if session.updated_by_cell_admin else None,
                        'updated_at': session.updated_at,
                    })

                data.append(sector_data)

        context = {
            'super_admin': user,
            'sector_data': data
        }

        return render(request, 'admin/umuganda_overview.html', context)
