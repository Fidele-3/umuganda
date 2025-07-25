from django.views import View
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages

from umuganda.models import UmugandaSession
from umuganda.forms.umuganda_seesion_form import UmugandaSessionForm
from admn.models.cell_admin_membership import CellAdminMembership


@method_decorator(login_required, name='dispatch')
class UmugandaSessionDetailView(View):
    def get(self, request, session_id):
        session = get_object_or_404(UmugandaSession, pk=session_id)
        user = request.user

        # 🛡️ Authorization
        if user.user_level not in ['cell_officer', 'sector_officer']:
            return render(request, 'admin/cell_not_assigned.html')

        if user.user_level == 'cell_officer':
            try:
                membership = CellAdminMembership.objects.get(admin=user)
                user_cell = membership.cell
            except CellAdminMembership.DoesNotExist:
                return render(request, 'admin/cell_not_assigned.html')

            if session.cell != user_cell:
                return render(request, 'admin/cell_not_assigned.html')

            form = UmugandaSessionForm(instance=session, cell=user_cell)
        else:
            # Sector officer - maybe allowed to view but not edit
            form = UmugandaSessionForm(instance=session, cell=session.cell)

        return render(request, 'admin/session_detail.html', {
            'session': session,
            'form': form,
            'can_edit': user.user_level == 'cell_officer',
        })

    def post(self, request, session_id):
        session = get_object_or_404(UmugandaSession, pk=session_id)
        user = request.user

        if user.user_level != 'cell_officer':
            return render(request, 'admin/cell_not_assigned.html')

        try:
            membership = CellAdminMembership.objects.get(admin=user)
            user_cell = membership.cell
        except CellAdminMembership.DoesNotExist:
            return render(request, 'admin/cell_not_assigned.html')

        if session.cell != user_cell:
            return render(request, 'admin/cell_not_assigned.html')

        form = UmugandaSessionForm(request.POST, instance=session, cell=user_cell)
        if form.is_valid():
            updated_session = form.save(commit=False)
            updated_session.updated_by_cell_admin = user
            updated_session.save()
            messages.success(request, "Session updated successfully.")
            return redirect('umuganda_session_detail', session_id=session_id)

        return render(request, 'admin/session_detail.html', {
            'session': session,
            'form': form,
            'can_edit': True,
        })
