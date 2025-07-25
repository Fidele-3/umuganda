from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from users.serializer.register import RegisterUserSerializer
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema

class RegisterUserAPIView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []  

    @extend_schema(
        request=RegisterUserSerializer,
        responses={201: RegisterUserSerializer},
        summary="Register a new user (citizen)"
    )
    def post(self, request):
        serializer = RegisterUserSerializer(data=request.data, context={"request": request})

        if serializer.is_valid():
            try:
                user = serializer.save()
                return Response({
                    "message": "Account created successfully",
                    "user_id": str(user.id),
                    "full_names": user.full_names,
                    "email": user.email,
                    "user_level": user.user_level
                }, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({
                    "error": "Account creation failed.",
                    "details": str(e)
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
