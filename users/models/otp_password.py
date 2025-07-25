
from django.db import models
from django.utils import timezone
from .customuser import CustomUser

class PasswordResetOTP(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(default=timezone.now)
    is_used = models.BooleanField(default=False)
    expires_at = models.DateTimeField(null=True, blank= False)

    def __str__(self):
        return f"OTP for {self.user.email}"
