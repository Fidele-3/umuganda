from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone
from django.conf import settings
from users.models.customuser import CustomUser
from users.models.notification import Notification
from umuganda.models import Fine
import logging

logger = logging.getLogger(__name__)

@shared_task(bind=True, max_retries=3)
def send_fine_created_notification(self, fine_id):
    email_notif = None
    try:
        fine = Fine.objects.select_related("user", "session").get(id=fine_id)
        user = fine.user

        if not user.email:
            logger.warning(f"[FineCreated] User '{user.full_names}' has no email. Skipping email notification.")
            return

        
        subject = "⚠️ New Umuganda Fine Issued"
        message = (
            f"Hello {user.full_names},\n\n"
            f"You have been fined {fine.amount} RWF for missing the Umuganda session on {fine.session.date}.\n"
            f"Reason: {fine.reason}\n\n"
            f"Please pay before the due date or contact your local authority."
        )

       
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

      
        context = {
            "full_names": user.full_names,
            "email": user.email,
            "fine_amount": fine.amount,
            "session_date": fine.session.date,
            "reason": fine.reason,
            "support_email": settings.DEFAULT_FROM_EMAIL,
        }

        try:
            text_content = render_to_string("emails/fine_created.txt", context)
            html_content = render_to_string("emails/fine_created.html", context)
        except Exception as template_error:
            logger.warning(f"[FineCreated] Template rendering failed: {template_error}")
            text_content = message
            html_content = f"<p>{message}</p>"

   
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

        logger.info(f"[FineCreated] Email sent to {user.email} for fine {fine.id}")

    except Fine.DoesNotExist:
        logger.error(f"[FineCreated] Fine with ID {fine_id} does not exist.")

    except Exception as e:
        logger.error(f"[FineCreated] Failed to notify user for fine_id={fine_id}: {e}")
        if email_notif:
            email_notif.is_sent = False
            email_notif.save()
        raise self.retry(exc=e, countdown=60)
