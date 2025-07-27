from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from users.models import UserProfile, CustomUser
from umuganda.models import CellUmugandaSession, Attendance
from admn.models.cell_admin_membership import CellAdminMembership

@method_decorator(login_required, name='dispatch')
class SessionAttendanceSubmitView(View):
    def post(self, request, session_id):
        user = request.user

        # ✅ Must be a cell officer
        if user.user_level != 'cell_officer':
            return render(request, 'cell_not_assigned.html')

        # ✅ Get cell membership
        try:
            membership = CellAdminMembership.objects.get(admin=user, is_active=True)
            user_cell = membership.cell
        except CellAdminMembership.DoesNotExist:
            return render(request, 'cell_not_assigned.html')

        # ✅ Get cell-specific session
        session = get_object_or_404(CellUmugandaSession, id=session_id)

        # ✅ Ensure session belongs to their cell
        if session.cell != user_cell:
            return render(request, 'cell_not_assigned.html')

        # ✅ Get attended user IDs from form
        user_ids = request.POST.getlist('attended_user_ids')
        created_count = 0

        for user_id in user_ids:
            try:
                target_user = CustomUser.objects.get(id=user_id)

                if not Attendance.objects.filter(user=target_user, session=session).exists():
                    Attendance.objects.create(
                        user=target_user,
                        session=session,
                        status='present'
                    )
                    created_count += 1
            except CustomUser.DoesNotExist:
                continue

        messages.success(request, f"Attendance recorded for {created_count} participants.")
        return redirect('umuganda_participants_list', session_id=session.id)
