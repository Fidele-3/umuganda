import logging
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from admn.models.sector_membership import sectorAdminMembership
from umuganda.models import UmugandaSession, CellUmugandaSession

logger = logging.getLogger(__name__)

@login_required
def umuganda_session_detail(request, session_id):
    user = request.user
    logger.info(f"[SESSION_DETAIL] Request by user: {user} for session ID: {session_id}")

    try:
        session = UmugandaSession.objects.get(id=session_id)
        logger.info(f"[SESSION_DETAIL] UmugandaSession found: {session}")
    except UmugandaSession.DoesNotExist:
        logger.warning(f"[SESSION_DETAIL] UmugandaSession with ID {session_id} does not exist.")
        return render(request, '404.html', status=404)

    # Validate user is a sector officer assigned to this session's sector
    if user.user_level != 'sector_officer':
        logger.warning(f"[SESSION_DETAIL] Access denied: User {user} is not a sector officer.")
        return render(request, '403.html', status=403)

    is_assigned = sectorAdminMembership.objects.filter(admin=user, sector=session.sector).exists()
    if not is_assigned:
        logger.warning(f"[SESSION_DETAIL] Access denied: User {user} is not assigned to sector {session.sector}.")
        return render(request, '403.html', status=403)

    # Fetch Cell-level sessions for this UmugandaSession
    cell_sessions = CellUmugandaSession.objects.filter(umuganda_session=session).select_related('cell')

    context = {
        'session': session,
        'cell_sessions': cell_sessions,
    }
    logger.info(f"[SESSION_DETAIL] Rendering detail page for session {session.id}")
    return render(request, 'admin/session_detail.html', context)
