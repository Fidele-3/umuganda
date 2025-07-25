from django.db.models.signals import post_save
from django.dispatch import Signal, receiver
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse
from django.conf import settings
from users.models.customuser import CustomUser

from users.models.otp_password import PasswordResetOTP
from users.tasks.otp_notification import send_email_password_reset_otp, send_email_password_reset_success


@receiver(post_save, sender=PasswordResetOTP)
def trigger_password_reset_email(sender, instance, created, **kwargs):
    if not created:
        return

    user = instance.user
    otp_code = instance.otp_code

    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    reset_link = f"{settings.FRONTEND_URL}/reset-password/{uidb64}/{otp_code}/"


    send_email_password_reset_otp.delay(
        user_id=str(user.id),
        full_names=user.full_names,
        email=user.email,
        otp_code=otp_code,
        reset_link=reset_link
    )



"""
password_reset_successful = Signal()


@receiver(password_reset_successful)
def trigger_password_reset_success_notification(sender, user: CustomUser, **kwargs):
    send_email_password_reset_success.delay(
        str(user.id),
        user.full_names,
        user.email
    )
"""
