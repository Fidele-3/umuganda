from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.utils import timezone
from users.models.notification import Notification
from users.models.customuser import CustomUser
import logging
from uuid import UUID

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3)
def send_email_password_reset_otp(self, user_id: str, full_names: str, email: str, otp_code: str, reset_link: str):
    notif = None
    try:
        user = CustomUser.objects.get(id=UUID(user_id))  # ✅ Fixed UUID parsing

        subject = "Your Password Reset OTP and Reset Link"
        message = f"Hi {full_names}, your OTP for password reset is: {otp_code}. You can also reset your password directly using the link provided."

        notif = Notification.objects.create(
            recipient=user,
            triggered_by=None,
            notification_type='email',
            subject=subject,
            message=message,
            is_sent=False
        )

        context = {
            "full_names": full_names,
            "otp_code": otp_code,
            "reset_link": reset_link
        }

        text_content = render_to_string("emails/password_reset_otp.txt", context)
        html_content = render_to_string("emails/password_reset_otp.html", context)
        from_email = settings.DEFAULT_FROM_EMAIL

        msg = EmailMultiAlternatives(subject, text_content, from_email, [email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        notif.is_sent = True
        notif.sent_at = timezone.now()
        notif.save()

        logger.info(f"Password reset OTP email sent to {email}")

    except CustomUser.DoesNotExist:
        logger.error(f"User with ID {user_id} does not exist.")
    except Exception as e:
        if notif:
            notif.is_sent = False
            notif.save()
        logger.error(f"Error sending password reset OTP email to {email}: {e}")
        raise self.retry(exc=e, countdown=60)


@shared_task(bind=True, max_retries=3)
def send_email_password_reset_success(self, user_id: str, full_names: str, email: str):
    notif = None
    try:
        user = CustomUser.objects.get(id=UUID(user_id))  # ✅ Fixed UUID parsing

        subject = "Password Reset Successful"
        message = f"Hi {full_names}, your password has been successfully reset. If you didn't request this, please contact support immediately."

        notif = Notification.objects.create(
            recipient=user,
            triggered_by=None,
            notification_type='email',
            subject=subject,
            message=message,
            is_sent=False
        )

        context = {
            "full_names": full_names
        }

        text_content = render_to_string("emails/password_reset_success.txt", context)
        html_content = render_to_string("emails/password_reset_success.html", context)
        from_email = settings.DEFAULT_FROM_EMAIL

        msg = EmailMultiAlternatives(subject, text_content, from_email, [email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        notif.is_sent = True
        notif.sent_at = timezone.now()
        notif.save()

        logger.info(f"Password reset success email sent to {email}")

    except CustomUser.DoesNotExist:
        logger.error(f"User with ID {user_id} not found.")
    except Exception as e:
        if notif:
            notif.is_sent = False
            notif.save()
        logger.error(f"Error sending password reset success email to {email}: {e}")
        raise self.retry(exc=e, countdown=60)
