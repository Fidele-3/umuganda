from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from users.models import DashboardMedia
from users.serializer.dashboard_media_serializer import DashboardMediaSerializer

class DashboardMediaListView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        media_items = DashboardMedia.objects.all().order_by('-uploaded_at')
        serializer = DashboardMediaSerializer(media_items, many=True)
        return Response(serializer.data)
