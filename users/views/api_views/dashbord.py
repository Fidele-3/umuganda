import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils.timezone import now

from users.serializer.dashbord_serializer import (
    CustomUserSerializer,
    UserProfileSerializer,
    CellUmugandaSessionSerializer,
    AttendanceSerializer,
    FineSerializer
)

from umuganda.models import CellUmugandaSession, Attendance, Fine

logger = logging.getLogger(__name__)

class CitizenDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        logger.info(f"Dashboard request started for user ID: {user.id}")
        print(f"[LOG] Starting dashboard request for user ID: {user.id}")

        # Check for profile existence
        if not hasattr(user, 'profile') or user.profile is None:
            logger.warning(f"User {user.id} missing profile.")
            print(f"[WARN] User {user.id} missing profile.")
            return Response({"error": "User profile is missing."}, status=400)

        profile = user.profile
        logger.debug(f"User profile loaded: {profile}")
        print(f"[LOG] User profile found: Sector={getattr(profile.sector, 'id', None)}, Cell={getattr(profile.cell, 'id', None)}, Village={getattr(profile.village, 'id', None)}")

        # Serialize user and profile info
        user_data = CustomUserSerializer(user).data or {}
        logger.debug(f"User serialized data keys: {list(user_data.keys())}")
        profile_data = UserProfileSerializer(profile).data or {}
        logger.debug(f"Profile serialized data keys: {list(profile_data.keys())}")
        print(f"[LOG] Serialized user and profile data.")

        # Fetch upcoming sessions
        today = now().date()
        sessions_qs = CellUmugandaSession.objects.filter(
            cell_id=profile.cell_id,
            sector_session__date__gte=today
        ).order_by('sector_session__date')
        logger.info(f"Found {sessions_qs.count()} upcoming sessions for cell {profile.cell_id}")
        print(f"[LOG] Upcoming sessions count: {sessions_qs.count()}")

        sessions = CellUmugandaSessionSerializer(sessions_qs, many=True).data or []
        logger.debug(f"Serialized {len(sessions)} sessions")

        # Fetch past attendance
        attendances_qs = Attendance.objects.filter(user=user).order_by('-recorded_at')
        logger.info(f"Found {attendances_qs.count()} attendance records for user {user.id}")
        print(f"[LOG] Attendance records count: {attendances_qs.count()}")

        attendances = AttendanceSerializer(attendances_qs, many=True).data or []
        logger.debug(f"Serialized {len(attendances)} attendance records")

        # Fetch fines
        fines_qs = Fine.objects.filter(user=user).order_by('-issued_at')
        logger.info(f"Found {fines_qs.count()} fines for user {user.id}")
        print(f"[LOG] Fines count: {fines_qs.count()}")

        fines = FineSerializer(fines_qs, many=True).data or []
        logger.debug(f"Serialized {len(fines)} fines")

        # Prepare response
        response = {
            "user": {
                **user_data,
                "profile": profile_data,
            },
            "available_sessions": sessions,        # renamed from upcoming_sessions
            "attendance_history": attendances,
            "fines": fines,
        }


        logger.info(f"Dashboard data prepared and sent for user ID: {user.id}")
        print(f"[LOG] Dashboard response ready for user ID: {user.id}")

        return Response(response)
