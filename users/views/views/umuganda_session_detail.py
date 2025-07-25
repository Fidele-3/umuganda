import logging
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from admn.models.cell_admin_membership import CellAdminMembership
from admn.models.sector_membership import sectorAdminMembership
from umuganda.models import UmugandaSession

logger = logging.getLogger(__name__)

@login_required
def umuganda_session_detail(request, session_id):
    user = request.user
    logger.info(f"[SESSION_DETAIL] Request by user: {user} for session ID: {session_id}")

    # Get sector memberships
    sector_memberships = sectorAdminMembership.objects.filter(admin=user)
    # Get AddressSector instances from sectorMemberships
    user_address_sectors = [m.sector.sector for m in sector_memberships]  # <-- Note the extra .sector

    cell_memberships = CellAdminMembership.objects.filter(admin=user)
    user_cells = [m.cell for m in cell_memberships]

    logger.debug(f"[SESSION_DETAIL] User Address Sectors: {user_address_sectors}")
    logger.debug(f"[SESSION_DETAIL] User Cells: {user_cells}")

    try:
        session = UmugandaSession.objects.get(id=session_id)
        logger.info(f"[SESSION_DETAIL] UmugandaSession found: {session}")
    except UmugandaSession.DoesNotExist:
        logger.warning(f"[SESSION_DETAIL] UmugandaSession with ID {session_id} does not exist.")
        return render(request, '404.html', status=404)

    # Now check if user sector or cell matches the session sector or cell
    if session.sector in user_address_sectors:
        logger.info(f"[SESSION_DETAIL] Access granted as sector admin: {user}")
    elif session.cell in user_cells:
        logger.info(f"[SESSION_DETAIL] Access granted as cell admin: {user}")
    else:
        logger.warning(f"[SESSION_DETAIL] Access denied for user {user}. Session sector: {session.sector}, session cell: {session.cell}")
        return render(request, '403.html', status=403)

    context = {
        'session': session
    }
    logger.info(f"[SESSION_DETAIL] Rendering detail page for session {session.id}")
    return render(request, 'admin/session_detail.html', context)
