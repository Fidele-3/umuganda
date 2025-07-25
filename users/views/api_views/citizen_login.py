import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from users.models.customuser import CustomUser
from users.models.userprofile import UserProfile

logger = logging.getLogger(__name__)

class citizenLoginView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []  # Allow login without requiring a token

    def post(self, request):
        logger.info("Login request received.")
        email = request.data.get('email')
        password = request.data.get('password')

        logger.debug(f"Received email: {email}")
        if not email or not password:
            logger.warning("Missing email or password in request.")
            return Response({'detail': 'Email and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = CustomUser.objects.get(email=email)
            logger.info(f"User found with email: {email}, ID: {user.id}")
        except CustomUser.DoesNotExist:
            logger.warning(f"User with email {email} not found.")
            return Response({'detail': 'Invalid email or password.'}, status=status.HTTP_401_UNAUTHORIZED)

        if user.user_level != 'citizen':
            logger.warning(f"User {user.id} attempted login but is not a citizen. User level: {user.user_level}")
            return Response({'detail': 'Access denied. Not a citizen account.'}, status=status.HTTP_403_FORBIDDEN)

        user = authenticate(request, email=email, password=password)

        if user is None:
            logger.warning(f"Authentication failed for email: {email}")
            return Response({'detail': 'Invalid email or password.'}, status=status.HTTP_401_UNAUTHORIZED)

        if not user.is_active:
            logger.warning(f"Inactive user attempted login: {user.id}")
            return Response({'detail': 'Account is inactive.'}, status=status.HTTP_403_FORBIDDEN)

        try:
            refresh = RefreshToken.for_user(user)
            logger.info(f"JWT tokens generated for user {user.id}")
        except Exception as e:
            logger.error(f"Error generating tokens for user {user.id}: {str(e)}")
            return Response({'detail': 'Token generation failed.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
            user_profile = UserProfile.objects.get(user=user)
            logger.info(f"UserProfile loaded for user {user.id}")
        except UserProfile.DoesNotExist:
            logger.error(f"UserProfile not found for user {user.id}")
            return Response({'detail': 'User profile not found.'}, status=status.HTTP_404_NOT_FOUND)

        logger.info(f"Login successful for user {user.id}")

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': {
                'id': str(user.id),
                'full_names': user.full_names,
                'email': user.email,
                'national_id': user.national_id,
                'user_level': user.user_level,
                'profile': {
                    'bio': user_profile.bio,
                    'gender': user_profile.gender,
                    'date_of_birth': user_profile.date_of_birth,
                    'work': user_profile.work,
                    'work_description': user_profile.work_description,
                    'province': user_profile.province.name,
                    'district': user_profile.district.name,
                    'sector': user_profile.sector.name,
                    'cell': user_profile.cell.name,
                    'village': user_profile.village.name,
                    'website': user_profile.website,
                }
            }
        }, status=status.HTTP_200_OK)
