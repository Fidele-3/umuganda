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


class CitizenDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        # Profile Info
        user_data = CustomUserSerializer(user).data
        profile_data = UserProfileSerializer(user.profile).data if hasattr(user, 'profile') else {}

        # Available sessions (Today or future) for citizen’s sector/cell/village
        sessions = UmugandaSession.objects.filter(
            date__gte=now().date(),
            sector=user.profile.sector,
            cell=user.profile.cell,
            village=user.profile.village,
        ).order_by('date')

        sessions_data = UmugandaSessionSerializer(sessions, many=True).data

        # Attendance records (if any)
        attendances = Attendance.objects.filter(user=user)
        attendances_data = AttendanceSerializer(attendances, many=True).data

        # Fines (if any)
        fines = Fine.objects.filter(user=user)
        fines_data = FineSerializer(fines, many=True).data

        return Response({
            "user": user_data,
            "profile": profile_data,
            "available_sessions": sessions_data,
            "attendance_history": attendances_data,
            "fines": fines_data,
        })
