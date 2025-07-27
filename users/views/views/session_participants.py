from django.views import View
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseForbidden
from users.models import UserProfile
from umuganda.models import CellUmugandaSession
from admn.models.cell_admin_membership import CellAdminMembership
from admn.models.sector_membership import sectorAdminMembership
from users.models.addresses import Cell
import logging

logger = logging.getLogger(__name__)

class SessionParticipantListView(View):
    template_name = 'admin/session_participants_list.html'

    def get(self, request, session_id):
        user = request.user
        session = get_object_or_404(CellUmugandaSession, id=session_id)  # ⬅️ Switched to CellUmugandaSession

        # ➤ If Cell Admin
        if user.user_level == 'cell_officer':
            try:
                membership = CellAdminMembership.objects.get(admin=user)
                user_cell = membership.cell
            except CellAdminMembership.DoesNotExist:
                logger.warning(f"Cell officer {user} has no CellAdminMembership")
                return render(request, 'admin/cell_not_assigned.html')

            # Ensure they are only accessing their cell's session
            if session.cell != user_cell:
                logger.warning(f"Cell officer's cell ({user_cell}) does not match session's cell ({session.cell})")
                return render(request, 'admin/cell_not_assigned.html')

            participants = UserProfile.objects.select_related('user').filter(cell=user_cell)

            context = {
                'session': session,
                'participants': participants
            }
            return render(request, self.template_name, context)

        # ➤ If Sector Admin
        elif user.user_level == 'sector_officer':
            try:
                membership = sectorAdminMembership.objects.get(admin=user)
                user_sector = membership.sector
            except sectorAdminMembership.DoesNotExist:
                logger.warning(f"Sector officer {user} has no sector membership")
                return render(request, 'admin/sector_not_assigned.html')

            # Validate session belongs to sector
            if session.cell.sector != user_sector:
                return HttpResponseForbidden("Not allowed to access sessions outside your sector")

            selected_cell_id = request.GET.get('cell')
            selected_cell = None
            if selected_cell_id:
                try:
                    selected_cell = Cell.objects.get(id=selected_cell_id, sector=user_sector)
                except Cell.DoesNotExist:
                    return HttpResponseForbidden("Invalid cell selected")

            if selected_cell:
                participants = UserProfile.objects.select_related('user').filter(
                    sector=user_sector,
                    cell=selected_cell
                )
            else:
                participants = []

            all_cells = Cell.objects.filter(sector=user_sector)

            context = {
                'session': session,
                'participants': participants,
                'all_cells': all_cells,
                'selected_cell': selected_cell
            }

            return render(request, self.template_name, context)

        else:
            logger.warning(f"Unauthorized user tried to access participants: {user}")
            return HttpResponseForbidden("You are not authorized to view this page.")
