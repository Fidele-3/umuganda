from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.utils import timezone
from users.models.notification import Notification
from users.models.customuser import CustomUser
import logging

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3)
def send_email_password_reset_success(self, user_id: str, full_names: str, email: str):
    """
    Sends an email to notify the user that their password was successfully reset.
    Also logs the email as a Notification in the database.
    """
    notification = None

    try:
        # Convert user_id to integer if model uses IntegerField for ID
        user = CustomUser.objects.get(id=user_id)

        subject = "Password Reset Successful"
        message = (
            f"Hi {full_names}, your password has been successfully reset. "
            "If you didn’t request this change, please contact our support team immediately."
        )

        # Create notification record (marked as not yet sent)
        notification = Notification.objects.create(
            recipient=user,
            triggered_by=None,
            notification_type='email',
            subject=subject,
            message=message,
            is_sent=False,
        )

        context = {
            "full_names": full_names,
            "support_email": getattr(settings, "DEFAULT_SUPPORT_EMAIL", "support@example.com")
        }

        # Render text and HTML email templates
        text_content = render_to_string("emails/password_reset_success.txt", context)
        html_content = render_to_string("emails/password_reset_success.html", context)

        # Compose and send the email
        from_email = settings.DEFAULT_FROM_EMAIL
        email_msg = EmailMultiAlternatives(subject, text_content, from_email, [email])
        email_msg.attach_alternative(html_content, "text/html")
        email_msg.send()

        # Update notification status after successful send
        notification.is_sent = True
        notification.sent_at = timezone.now()
        notification.save()

        logger.info(f"[PasswordResetSuccess] Success email sent to {email}")

    except CustomUser.DoesNotExist:
        logger.error(f"[PasswordResetSuccess] User with ID {user_id} not found.")

    except Exception as e:
        if notification:
            notification.is_sent = False
            notification.save()
        logger.error(f"[PasswordResetSuccess] Failed to send success email to {email}: {e}")
        raise self.retry(exc=e, countdown=60)
