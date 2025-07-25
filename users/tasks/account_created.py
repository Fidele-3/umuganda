from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone
from django.conf import settings
from users.models.customuser import CustomUser
from users.models.notification import Notification
import logging

logger = logging.getLogger(__name__)

@shared_task(bind=True, max_retries=3)
def send_account_created_email(self, user_id):
    email_notif = None
    try:
        user = CustomUser.objects.only("id", "full_names", "email").get(id=user_id)

        if not user.email:
            logger.warning(f"[AccountCreated] User '{user.full_names}' has no email. Skipping email notification.")
            return

        # Message content
        subject = "🎉 Welcome to Umuganda!"
        message = f"Hello {user.full_names}, your account has been successfully created."

        # === In-App Notification ===
        Notification.objects.create(
            recipient=user,
            sector=None,
            triggered_by=None,
            notification_type="in_app",
            subject=subject,
            message=message,
            is_sent=True,
            sent_at=timezone.now()
        )

        # === Email Notification Context ===
        context = {
            "full_names": user.full_names,
            "email": user.email,
            "support_email": settings.DEFAULT_FROM_EMAIL,
        }

        try:
            text_content = render_to_string("emails/account_created.txt", context)
            html_content = render_to_string("emails/account_created.html", context)
        except Exception as template_error:
            logger.warning(f"[AccountCreated] Template rendering failed: {template_error}")
            text_content = message
            html_content = f"<p>{message}</p>"

        # Save email notification record
        email_notif = Notification.objects.create(
            recipient=user,
            sector=None,
            triggered_by=None,
            notification_type="email",
            subject=subject,
            message=message,
            is_sent=False
        )

        # Send email
        msg = EmailMultiAlternatives(subject, text_content, settings.DEFAULT_FROM_EMAIL, [user.email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        # Mark as sent
        email_notif.is_sent = True
        email_notif.sent_at = timezone.now()
        email_notif.save()

        logger.info(f"[AccountCreated] Email sent to {user.email}")

    except CustomUser.DoesNotExist:
        logger.error(f"[AccountCreated] User with ID {user_id} does not exist.")

    except Exception as e:
        logger.error(f"[AccountCreated] Failed to send email to user_id={user_id}: {e}")
        if email_notif:
            email_notif.is_sent = False
            email_notif.save()
        raise self.retry(exc=e, countdown=60)
