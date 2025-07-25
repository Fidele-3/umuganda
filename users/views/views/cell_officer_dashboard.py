from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now, timedelta

from umuganda.models import UmugandaSession
from users.models import CustomUser, UserProfile
from users.models.addresses import Cell
from admn.models.cell_admin_membership import CellAdminMembership


@method_decorator(login_required, name='dispatch')
class AdminLevel3DashboardView(View):
    template_name = 'admin/admin_level3_dashboard.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.user_level != 'cell_officer':
            messages.error(request, "Unauthorized access.")
            return redirect('admin_login')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        admin = request.user

        try:
            membership = CellAdminMembership.objects.get(admin=admin)
            cell = membership.cell
        except CellAdminMembership.DoesNotExist:
            messages.error(request, "You are not assigned to any cell.")
            return render(request, 'admin/cell_not_assigned.html')

        today = now().date()
        scope = request.GET.get('scope', 'all')

        # Get the most relevant Umuganda session for this cell
        umuganda_session = UmugandaSession.objects.filter(
            sector=cell.sector,
            date__gte=today
        ).order_by('date').first()  # Get the nearest upcoming session

        # Existing sessions list
        queryset = UmugandaSession.objects.filter(cell=cell)
        if scope == 'today':
            queryset = queryset.filter(created_at__date=today)
        elif scope == 'week':
            start_of_week = today - timedelta(days=today.weekday())
            queryset = queryset.filter(created_at__date__gte=start_of_week)

        queryset = queryset.order_by('-created_at')

        # Check if a sector session is pending for this cell's sector
        pending_sector_sessions = UmugandaSession.objects.filter(
            sector=cell.sector,
            cell__isnull=True,
            date__gte=today
        )
        needs_attention = pending_sector_sessions.exists()

        context = {
            'admin': admin,
            'cell': cell,
            'scope': scope,
            'sessions': queryset,
            'umuganda_session': umuganda_session,  # Add this
            'today': today,  # Add this
            'needs_attention': needs_attention,
            'create_deadline': today + timedelta(days=3),
        }

        return render(request, self.template_name, context)