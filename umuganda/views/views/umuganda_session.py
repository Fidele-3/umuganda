import logging
from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.http import Http404
from umuganda.models import UmugandaSession
from users.models.addresses import Cell
from umuganda.forms.umuganda_seesion_form import UmugandaSessionForm
from admn.models.cell_admin_membership import CellAdminMembership

# Setup logger
logger = logging.getLogger(__name__)

@method_decorator(login_required, name='dispatch')
class CreateUmugandaSessionView(View):
    def get(self, request):
        try:
            if request.user.user_level != 'cell_officer':
                logger.warning(f"Unauthorized access attempt by user {request.user} with level {request.user.user_level}")
                return render(request, 'cell_not_assigned.html')

            try:
                membership = CellAdminMembership.objects.get(admin=request.user)
                cell = membership.cell
            except CellAdminMembership.DoesNotExist:
                logger.error(f"CellAdminMembership does not exist for user {request.user}")
                return render(request, 'cell_not_assigned.html')

            sector = cell.sector
            session = UmugandaSession.objects.filter(sector=sector).order_by('-date').first()

            if not session:
                logger.warning(f"No UmugandaSession found for sector {sector}")
                raise Http404("No session has been created by your sector officer.")

            if session.cell and session.cell != cell:
                logger.warning(f"User {request.user} tried to access session not assigned to their cell {cell}")
                return render(request, 'cell_not_assigned.html')

            form = UmugandaSessionForm(instance=session, cell=cell)
            return render(request, 'admin/create_umuganda_session.html', {
                'form': form,
                'session': session,
            })
        
        except Exception as e:
            logger.exception(f"Unexpected error in GET CreateUmugandaSessionView: {str(e)}")
            return render(request, '500.html', status=500)

    def post(self, request):
        try:
            if request.user.user_level != 'cell_officer':
                logger.warning(f"Unauthorized POST access attempt by user {request.user}")
                return render(request, '403.html')

            try:
                membership = CellAdminMembership.objects.get(admin=request.user)
                cell = membership.cell
            except CellAdminMembership.DoesNotExist:
                logger.error(f"CellAdminMembership missing for POST request by user {request.user}")
                return render(request, 'cell_not_assigned.html')

            sector = cell.sector
            session = UmugandaSession.objects.filter(sector=sector).order_by('-date').first()

            if not session:
                logger.warning(f"POST failed: No UmugandaSession found for sector {sector}")
                raise Http404("No session found to update.")

            if session.cell and session.cell != cell:
                logger.warning(f"POST blocked: User {request.user} tried to update session for wrong cell.")
                return render(request, 'cell_not_assigned.html')

            form = UmugandaSessionForm(request.POST, instance=session, cell=cell)
            if form.is_valid():
                session = form.save(commit=False)
                session.cell = cell
                session.updated_by_cell_admin = request.user
                session.save()
                logger.info(f"Session updated by cell admin {request.user} for cell {cell}")
                messages.success(request, "Umuganda session successfully updated.")
                return redirect('cell_officer_dashboard')
            else:
                logger.warning(f"Invalid form data by user {request.user}: {form.errors}")

            return render(request, 'admin/create_umuganda_session.html', {
                'form': form,
                'session': session,
            })
        
        except Exception as e:
            logger.exception(f"Unexpected error in POST CreateUmugandaSessionView: {str(e)}")
            return render(request, '500.html', status=500)
