import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils.timezone import now
from users.serializer.dashbord_serializer import (
    CustomUserSerializer,
    UserProfileSerializer,
    UmugandaSessionSerializer,
    AttendanceSerializer,
    FineSerializer
)
from umuganda.models import UmugandaSession, Attendance, Fine

logger = logging.getLogger(__name__)

class CitizenDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        logger.info(f"Received dashboard request for user: {user} (ID: {user.id})")
        print(f"[DEBUG] User: {user} | ID: {user.id}")

        # Profile Info
        user_data = CustomUserSerializer(user).data
        logger.debug(f"User serialized data: {user_data}")
        print(f"[DEBUG] User Data Serialized")

        profile_data = {}
        if hasattr(user, 'profile'):
            profile_data = UserProfileSerializer(user.profile).data
            logger.debug(f"Profile data: {profile_data}")
            print(f"[DEBUG] Profile exists for user: {user.profile}")
        else:
            logger.warning(f"No profile found for user ID {user.id}")
            print(f"[WARNING] No profile found")

        # Check for required location fields
        profile = getattr(user, 'profile', None)
        if not profile:
            logger.error("Profile is missing for the user.")
            return Response({"error": "Profile missing"}, status=400)

        if not all([profile.sector, profile.cell, profile.village]):
            logger.warning(f"Incomplete location in profile: Sector={profile.sector}, Cell={profile.cell}, Village={profile.village}")
            print(f"[WARNING] Missing location info")
        else:
            logger.info(f"Filtering sessions by: Sector={profile.sector}, Cell={profile.cell}, Village={profile.village}")
            print(f"[DEBUG] Filtering by sector={profile.sector.id}, cell={profile.cell.id}, village={profile.village.id}")

        # Available sessions
        today = now().date()
        logger.debug(f"Today’s date: {today}")
        print(f"[DEBUG] Today: {today}")

        sessions = UmugandaSession.objects.filter(
            date__gte=today,
            sector=profile.sector,
            cell=profile.cell,
            village=profile.village,
        ).order_by('date')

        logger.info(f"Found {sessions.count()} Umuganda sessions for user location")
        print(f"[DEBUG] Sessions found: {sessions.count()}")

        for s in sessions:
            logger.debug(f"Session ID: {s.id} | Date: {s.date} | Sector: {s.sector} | Cell: {s.cell} | Village: {s.village}")
            print(f"[DEBUG] Session: {s.id} - {s.date}")

        sessions_data = UmugandaSessionSerializer(sessions, many=True).data

        # Attendance records
        attendances = Attendance.objects.filter(user=user)
        logger.info(f"Found {attendances.count()} attendance records for user ID {user.id}")
        attendances_data = AttendanceSerializer(attendances, many=True).data

        # Fines
        fines = Fine.objects.filter(user=user)
        logger.info(f"Found {fines.count()} fine records for user ID {user.id}")
        fines_data = FineSerializer(fines, many=True).data

        logger.info("Dashboard data successfully generated")
        print(f"[DEBUG] Dashboard data ready")

        return Response({
            "user": user_data,
            "profile": profile_data,
            "available_sessions": sessions_data,
            "attendance_history": attendances_data,
            "fines": fines_data,
        })
