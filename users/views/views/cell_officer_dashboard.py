from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now, timedelta

from umuganda.models import UmugandaSession, CellUmugandaSession
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

        # ✅ Get nearest cell-level session
        cell_sessions_qs = CellUmugandaSession.objects.filter(
            cell=cell,
            sector_session__date__gte=today
        ).select_related('sector_session').order_by('sector_session__date')

        current_cell_session = cell_sessions_qs.first()

        # ✅ Sessions filtering for dashboard
        queryset = CellUmugandaSession.objects.filter(cell=cell)

        if scope == 'today':
            queryset = queryset.filter(updated_at__date=today)
        elif scope == 'week':
            start_of_week = today - timedelta(days=today.weekday())
            queryset = queryset.filter(updated_at__date__gte=start_of_week)

        queryset = queryset.order_by('-updated_at')

        # ✅ Find sector-level sessions for this cell's sector
        sector_sessions = UmugandaSession.objects.filter(
            sector=cell.sector,
            date__gte=today
        ).order_by('date')

        pending_sector_sessions = sector_sessions.exclude(
            id__in=CellUmugandaSession.objects.filter(cell=cell).values_list('sector_session_id', flat=True)
        )
        needs_attention = pending_sector_sessions.exists()

        # ✅ Extract the date directly from the pending UmugandaSession
        pending_session_date = None
        if needs_attention:
            first_pending = pending_sector_sessions.first()
            if first_pending is not None:
                pending_session_date = first_pending.date

        # ✅ Always return a response
        context = {
            'admin': admin,
            'cell': cell,
            'scope': scope,
            'sessions': queryset,
            'umuganda_session': current_cell_session,
            'today': today,
            'needs_attention': needs_attention,
            'pending_session_date': pending_session_date,
            'create_deadline': today + timedelta(days=3),
        }

        return render(request, self.template_name, context)
