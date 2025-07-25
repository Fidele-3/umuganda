from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from users.models import DashboardMedia
from users.serializer.dashboard_media_serializer import DashboardMediaSerializer
from users.models import CustomUser

class DashboardMediaUploadView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        user = request.user

        if user.role not in ['super_admin', 'sector_officer']:
            return Response({"error": "You do not have permission to upload dashboard media."}, status=status.HTTP_403_FORBIDDEN)

        serializer = DashboardMediaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({"message": "Media uploaded successfully", "media": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
