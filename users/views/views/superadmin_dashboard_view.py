from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.timezone import now

from users.models import CustomUser
from umuganda.models import UmugandaSession
from admn.models import AdminActionLog, AdminHierarchy
from admn.models.sector_membership import sectorAdminMembership  # ✅ Import membership

class SuperAdminDashboardView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user

        if user.user_level != 'super_admin':
            return redirect('unauthorized')

        # Counts of relevant user roles
        total_citizens = CustomUser.objects.filter(user_level='citizen').count()
        total_sector_officers = CustomUser.objects.filter(user_level='sector_officer').count()
        total_cell_officers = CustomUser.objects.filter(user_level='cell_officer').count()

        total_sessions = UmugandaSession.objects.count()
        today = now().date()
        monthly_sessions = UmugandaSession.objects.filter(
            date__year=today.year,
            date__month=today.month
        ).count()

        recent_action_logs = AdminActionLog.objects.select_related('admin') \
            .order_by('-timestamp')[:20]

        added_sector_admins = AdminHierarchy.objects.select_related('admin') \
            .filter(added_by=user, admin__user_level='sector_officer')

        # ✅ Attach sector_name to each sector officer
        for admin_hierarchy in added_sector_admins:
            membership = sectorAdminMembership.objects.filter(admin=admin_hierarchy.admin).select_related('sector__sector').first()
            if membership:
                admin_hierarchy.admin.sector_name = membership.sector.sector.name
            else:
                admin_hierarchy.admin.sector_name = "No Sector Assigned"

        context = {
            'total_citizens': total_citizens,
            'total_sector_officers': total_sector_officers,
            'total_cell_officers': total_cell_officers,
            'total_sessions': total_sessions,
            'monthly_sessions': monthly_sessions,
            'recent_action_logs': recent_action_logs,
            'added_sector_admins': added_sector_admins,
            'super_admin': user,
        }

        return render(request, 'admin/superadmin_dashboard.html', context)
