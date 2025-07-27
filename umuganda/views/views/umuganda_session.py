import logging
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.http import Http404

from umuganda.models import UmugandaSession, CellUmugandaSession
from users.models.addresses import Cell
from umuganda.forms.cell_umuganda_session_form import CellUmugandaSessionForm  # Use your actual form import path
from admn.models.cell_admin_membership import CellAdminMembership

logger = logging.getLogger(__name__)


@method_decorator(login_required, name='dispatch')
class CreateUmugandaSessionView(View):
    def get(self, request):
        if request.user.user_level != 'cell_officer':
            logger.warning(f"Unauthorized access attempt by user {request.user} with level {request.user.user_level}")
            return render(request, '403.html')

        try:
            membership = CellAdminMembership.objects.get(admin=request.user)
            cell = membership.cell
        except CellAdminMembership.DoesNotExist:
            logger.error(f"CellAdminMembership does not exist for user {request.user}")
            return render(request, 'cell_not_assigned.html')

        sector_session = UmugandaSession.objects.filter(sector=cell.sector).order_by('-date').first()
        if not sector_session:
            logger.warning(f"No UmugandaSession found for sector {cell.sector}")
            raise Http404("No sector-level Umuganda session has been created yet.")

        try:
            cell_session = CellUmugandaSession.objects.get(cell=cell, sector_session=sector_session)
        except CellUmugandaSession.DoesNotExist:
            cell_session = None

        form = CellUmugandaSessionForm(instance=cell_session, cell=cell)
        session_date = sector_session.date  # Inherited date

        return render(request, 'admin/create_umuganda_session.html', {
            'form': form,
            'sector_session': sector_session,
            'session_date': session_date,  # Pass it explicitly if needed in template
        })

    def post(self, request):
        if request.user.user_level != 'cell_officer':
            logger.warning(f"Unauthorized POST access attempt by user {request.user}")
            return render(request, '403.html')

        try:
            membership = CellAdminMembership.objects.get(admin=request.user)
            cell = membership.cell
        except CellAdminMembership.DoesNotExist:
            logger.error(f"CellAdminMembership missing for POST request by user {request.user}")
            return render(request, 'cell_not_assigned.html')

        sector_session = UmugandaSession.objects.filter(sector=cell.sector).order_by('-date').first()
        if not sector_session:
            logger.warning(f"POST failed: No UmugandaSession found for sector {cell.sector}")
            raise Http404("No sector-level session found.")

        try:
            cell_session = CellUmugandaSession.objects.get(cell=cell, sector_session=sector_session)
        except CellUmugandaSession.DoesNotExist:
            cell_session = None

        form = CellUmugandaSessionForm(request.POST, instance=cell_session, cell=cell)
        session_date = sector_session.date  # Still needed in case form is invalid

        if form.is_valid():
            new_cell_session = form.save(commit=False)
            new_cell_session.cell = cell
            new_cell_session.sector_session = sector_session
            new_cell_session.updated_by = request.user
            new_cell_session.save()

            logger.info(f"CellUmugandaSession saved by user {request.user} for cell {cell} and sector session {sector_session}")
            messages.success(request, "Umuganda session updated successfully.")
            return redirect('cell_officer_dashboard')
        else:
            logger.warning(f"Invalid form submission by user {request.user}: {form.errors}")

        return render(request, 'admin/create_umuganda_session.html', {
            'form': form,
            'sector_session': sector_session,
            'session_date': session_date,  # Still pass date back to template
        })
