from rest_framework import generics, permissions
from umuganda.models import CellUmugandaSession
from users.serializer.dashbord_serializer import CellUmugandaSessionSerializer

class UmugandaSessionDetailViews(generics.RetrieveAPIView):
    queryset = CellUmugandaSession.objects.all()
    serializer_class = CellUmugandaSessionSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'
