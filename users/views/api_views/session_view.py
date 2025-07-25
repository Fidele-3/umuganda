from rest_framework import generics, permissions
from umuganda.models import UmugandaSession
from users.serializer.dashbord_serializer import UmugandaSessionSerializer

class UmugandaSessionDetailView(generics.RetrieveAPIView):
    queryset = UmugandaSession.objects.all()
    serializer_class = UmugandaSessionSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'
