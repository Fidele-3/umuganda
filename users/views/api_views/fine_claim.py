# views/fine_claim.py
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from umuganda.models import Fine
from users.serializer.fine_claim import FineClaimSerializer

class ClaimFineAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, fine_id):
        user = request.user
        try:
            fine = Fine.objects.get(id=fine_id, user=user)
        except Fine.DoesNotExist:
            return Response({"detail": "Fine not found."}, status=status.HTTP_404_NOT_FOUND)

        if fine.claim:
            return Response({"detail": "You have already claimed this fine."}, status=status.HTTP_400_BAD_REQUEST)

        if fine.claim_has_been_approved:
            return Response({"detail": "Claim has already been approved."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = FineClaimSerializer(fine, data=request.data)
        if serializer.is_valid():
            fine.reason = serializer.validated_data['reason']
            fine.claim = True
            fine.save(update_fields=['reason', 'claim'])
            return Response({
                "detail": "Fine claimed successfully.",
                "fine_id": str(fine.id),
                "claim": fine.claim,
                "reason": fine.reason,
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
