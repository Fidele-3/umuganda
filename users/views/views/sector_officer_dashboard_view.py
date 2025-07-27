from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.timezone import now

from users.models import CustomUser
from users.models.addresses import Cell
from admn.models.cell_admin_membership import CellAdminMembership
from umuganda.models import UmugandaSession, CellUmugandaSession
from admn.models import sectorAdminMembership
from sector.models.sector import AdminSector
from users.models.addresses import Province, District, Sector as AddressSector


class AdminLevel2DashboardView(LoginRequiredMixin, View):
    def get(self, request):
        admin = request.user

        if admin.user_level != 'sector_officer':
            return redirect('unauthorized')

        try:
            # Get sector membership (1-to-1)
            membership = admin.sector_membership  # sectorAdminMembership instance

            # Assigned AdminSector object
            admin_sector = membership.sector

            # Get real address foreign keys
            province = admin_sector.province
            district = admin_sector.district
            address_sector = admin_sector.sector  # AddressSector instance

        except (sectorAdminMembership.DoesNotExist, AdminSector.DoesNotExist):
            return render(request, 'admin/sector_not_assigned.html')

        today = now().date()

        upcoming_session = (
            UmugandaSession.objects
            .filter(sector=address_sector)
            .order_by('-date')
            .first()
        )

        display_umuganda_notice = upcoming_session and upcoming_session.date >= today

        # Filter all cell officers under this sector
        cell_officer_users_qs = CustomUser.objects.filter(
            user_level='cell_officer',
            cell_memberships__cell__sector=address_sector
        ).distinct()

        cell_officers = cell_officer_users_qs

        # Get latest sessions updated by those officers
        cell_updated_sessions = (
            CellUmugandaSession.objects
            .filter(updated_by__in=cell_officer_users_qs)
            .select_related('updated_by', 'cell', 'village', 'sector_session')
            .order_by('-updated_at')[:20]
        )

        # ✅ This is the fixed part
        # Map: officer.id => CellAdminMembership
        cell_memberships = {
            m.admin_id: m
            for m in CellAdminMembership.objects.select_related('cell')
            .filter(admin__in=cell_officers)
        }

        context = {
            'admin': admin,
            'sector': address_sector,
            'district': district,
            'province': province,
            'upcoming_session': upcoming_session,
            'display_umuganda_notice': display_umuganda_notice,
            'cell_officer_count': cell_officers.count(),
            'cell_officers': cell_officers,
            'cell_updated_sessions': cell_updated_sessions,
            'cell_memberships': cell_memberships,  # now a dict
        }

        return render(request, 'admin/admin_level_2_dashboard.html', context)
