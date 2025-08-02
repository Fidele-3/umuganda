from django.views import View
from django.shortcuts import render, get_object_or_404
from django.utils.timezone import now
from users.models import CustomUser
from users.models.userprofile import UserProfile
from umuganda.models import CellUmugandaSession, Attendance, Fine
from admn.models.cell_admin_membership import CellAdminMembership
from admn.models.sector_membership import sectorAdminMembership
import math


class UmugandaFinesListView(View):
    template_name = 'admin/fines_list.html'

    def get(self, request, session_id):
        cell_session = get_object_or_404(CellUmugandaSession, id=session_id)

        umuganda_date = None
        if cell_session.sector_session:
            umuganda_date = cell_session.sector_session.date

        user = request.user

        is_cell_officer = user.user_level == 'cell_officer'
        is_sector_officer = user.user_level == 'sector_officer'

        if not (is_cell_officer or is_sector_officer):
            return render(request, 'not_authorized.html')

        # 🔒 Cell officer restriction
        if is_cell_officer:
            try:
                membership = CellAdminMembership.objects.get(admin=user, is_active=True)
                if membership.cell != cell_session.cell:
                    return render(request, 'cell_not_assigned.html')
            except CellAdminMembership.DoesNotExist:
                return render(request, 'cell_not_assigned.html')

        # 🔒 Sector officer restriction
        if is_sector_officer:
            try:
                sector_membership = sectorAdminMembership.objects.get(admin=user)
                if cell_session.cell.sector != sector_membership.sector:
                    return render(request, 'not_authorized.html')
            except sectorAdminMembership.DoesNotExist:
                return render(request, 'not_authorized.html')

        # 🧍‍♂️ Citizens in the cell
        citizens = CustomUser.objects.filter(user_level='citizen')
        profiles = UserProfile.objects.filter(user__in=citizens, cell=cell_session.cell)

        # 🚫 Absentees
        attended_user_ids = Attendance.objects.filter(session=cell_session).values_list('user_id', flat=True)
        absentees = profiles.exclude(user_id__in=attended_user_ids)

        fines_to_render = []

        for user_profile in absentees:
            fine, created = Fine.objects.get_or_create(
                user=user_profile.user,
                session=cell_session,
                defaults={
                    'amount': 1000.00,
                    'status': 'unpaid',
                    'reason': 'Missed Umuganda attendance'
                }
            )

            # ⏰ Recalculate overdue fines
            if fine.status == 'unpaid':
                months_passed = (
                    (now().date().year - fine.issued_at.date().year) * 12 +
                    (now().date().month - fine.issued_at.date().month)
                )
                if months_passed > fine.moths_overdue:
                    for _ in range(months_passed - fine.moths_overdue):
                        fine.amount *= 1.3
                    fine.moths_overdue = months_passed
                    fine.amount = round(fine.amount, 2)
                    fine.save()

            fines_to_render.append(fine)

        # 🔢 Summary amounts
        total_fines_amount = sum(f.amount for f in fines_to_render)
        paid_fines_amount = sum(f.amount for f in fines_to_render if f.status == 'PAID')
        pending_fines_amount = sum(f.amount for f in fines_to_render if f.status == 'PENDING')
        overdue_fines_amount = sum(f.amount for f in fines_to_render if f.months_overdue > 0)

        context = {
            'session': cell_session,
            'fines': fines_to_render,
            'total_fines_amount': total_fines_amount,
            'paid_fines_amount': paid_fines_amount,
            'pending_fines_amount': pending_fines_amount,
            'overdue_fines_amount': overdue_fines_amount,
            'umuganda_date': umuganda_date,
        }

        return render(request, self.template_name, context)
