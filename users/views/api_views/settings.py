# user/views/settings.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

class SettingsDashboardView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        """Returns only password change option with full correct paths"""
        return Response({
            "security": {
                "change_password": {
                    "request_otp": {
                        "endpoint": "/api_views/user/reset-password/",
                        "method": "POST",
                        "description": "Request OTP for password reset",
                        "body_params": {
                            "email": "string (your registered email)"
                        }
                    },
                    "confirm_reset": {
                        "endpoint": "/api_views/user/reset-password/reset/",
                        "method": "POST",
                        "description": "Submit OTP and new password",
                        "body_params": {
                            "email": "string",
                            "otp": "string (6-digit code)",
                            "password": "string (new password)"
                        }
                    }
                }
            }
        })