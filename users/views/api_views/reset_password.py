# views/user/reset_password.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from users.models import CustomUser, PasswordResetOTP
from django.utils import timezone
from datetime import timedelta
from umuganda.utils.generate_otp import generate_otp
from users.tasks.otp_notification import send_email_password_reset_otp 
from django.urls import reverse
from django.conf import settings
import uuid
from rest_framework.permissions import AllowAny
from rest_framework.authentication import BasicAuthentication

class RequestPasswordResetOTPView(APIView):
    authentication_classes = []  # No authentication required
    permission_classes = [AllowAny]
    def post(self, request):
        email = request.data.get("email")
        try:
            user = CustomUser.objects.get(email=email)

            otp_code = generate_otp()
            expiration = timezone.now() + timedelta(minutes=15)

            PasswordResetOTP.objects.create(
                user=user,
                otp_code=otp_code,
                expires_at=expiration
            )

            reset_link = request.build_absolute_uri(
                reverse("reset-password-link")
            )

            send_email_password_reset_otp.delay(
                user_id=str(user.id),
                full_names=user.full_names,
                email=user.email,
                otp_code=otp_code,
                reset_link=reset_link
            )

            return Response({"detail": "OTP sent to your email."}, status=status.HTTP_200_OK)

        except CustomUser.DoesNotExist:
            return Response({"error": "User with this email does not exist."}, status=status.HTTP_400_BAD_REQUEST)



from users.models import PasswordResetOTP
from rest_framework import serializers

class VerifyResetOTPView(APIView):
    authentication_classes = []  # No authentication required
    permission_classes = [AllowAny]
    def post(self, request):
        email = request.data.get("email")
        otp = request.data.get("otp")

        try:
            user = CustomUser.objects.get(email=email)
            latest_otp = PasswordResetOTP.objects.filter(user=user).latest("created_at")

            if latest_otp.otp_code != otp:
                return Response({"error": "Invalid OTP."}, status=status.HTTP_400_BAD_REQUEST)

            if latest_otp.expires_at < timezone.now():
                return Response({"error": "OTP has expired."}, status=status.HTTP_400_BAD_REQUEST)

            # Optional: mark OTP as used if you want one-time-use
            latest_otp.is_used = True
            latest_otp.save()

            return Response({"detail": "OTP verified."}, status=status.HTTP_200_OK)

        except CustomUser.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        except PasswordResetOTP.DoesNotExist:
            return Response({"error": "No OTP found. Please request a new one."}, status=status.HTTP_404_NOT_FOUND)


from django.contrib.auth.hashers import make_password
from users.tasks.send_email_password_reset_success import send_email_password_reset_success  # Celery task for success email

class ResetPasswordView(APIView):
    authentication_classes = []  # No authentication required
    permission_classes = [AllowAny]
    def post(self, request):
        email = request.data.get("email")
        otp = request.data.get("otp")
        password = request.data.get("password")

        try:
            user = CustomUser.objects.get(email=email)
            otp_obj = PasswordResetOTP.objects.filter(user=user).latest("created_at")

            if otp_obj.otp_code != otp:
                return Response({"error": "Invalid OTP."}, status=status.HTTP_400_BAD_REQUEST)

            if otp_obj.expires_at < timezone.now():
                return Response({"error": "OTP has expired."}, status=status.HTTP_400_BAD_REQUEST)

          
            user.set_password(password)
            user.save()


            send_email_password_reset_success.delay(
                user_id=str(user.id),
                full_names=user.full_names,
                email=user.email
            )

            return Response({"detail": "Password reset successfully."}, status=status.HTTP_200_OK)

        except CustomUser.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        except PasswordResetOTP.DoesNotExist:
            return Response({"error": "No OTP found. Please request a new one."}, status=status.HTTP_404_NOT_FOUND)
