from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from users.models import UserProfile, CustomUser
from umuganda.models import UmugandaSession, Attendance
from admn.models.cell_admin_membership import CellAdminMembership

@method_decorator(login_required, name='dispatch')
class SessionAttendanceSubmitView(View):
    def post(self, request, session_id):
        user = request.user

        # Check if the user is a cell officer
        if user.user_level != 'cell_officer':
            return render(request, 'cell_not_assigned.html')

        # Try to get cell admin membership
        try:
            membership = CellAdminMembership.objects.get(admin=user, is_active=True)
            user_cell = membership.cell
        except CellAdminMembership.DoesNotExist:
            return render(request, 'cell_not_assigned.html')

        # Get the session
        session = get_object_or_404(UmugandaSession, id=session_id)

        # Check if the session belongs to the officer's cell
        if session.cell != user_cell:
            return render(request, 'cell_not_assigned.html')

        # Process attendance
        user_ids = request.POST.getlist('attended_user_ids')
        created_count = 0

        for user_id in user_ids:
            try:
                user = CustomUser.objects.get(id=user_id)

                if not Attendance.objects.filter(user=user, session=session).exists():
                    Attendance.objects.create(
                        user=user,
                        session=session,
                        status='present'
                    )
                    created_count += 1
            except CustomUser.DoesNotExist:
                continue

        messages.success(request, f"Attendance recorded for {created_count} participants.")
        return redirect('umuganda_participants_list', session_id=session.id)
