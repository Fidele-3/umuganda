from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.utils import timezone
from users.models.notification import Notification
from users.models.customuser import CustomUser
from umuganda.models import UmugandaSession
import logging
from datetime import timedelta

logger = logging.getLogger(__name__)

def send_sms(phone_number: str, message: str) -> bool:
    logger.info(f"[SMS SEND] To: {phone_number}\nMessage: {message}")
    # Replace with real SMS gateway integration here
    return True

@shared_task(bind=True, max_retries=3)
def send_umuganda_notifications(self, session_id=None):
    """
    Send notifications for upcoming Umuganda sessions.

    - If session_id given, notify only that session.
    - Otherwise notify all sessions within next 3 days (including today).
    """

    now = timezone.now()
    today = now.date()

    if session_id:
        try:
            sessions = [UmugandaSession.objects.get(id=session_id)]
            logger.info(f"[UmugandaNotification] Sending notification for session id: {session_id}")
        except UmugandaSession.DoesNotExist:
            logger.error(f"[UmugandaNotification] Session id {session_id} not found.")
            return {"error": "Session not found"}
    else:
        # Filter sessions from today up to 3 days ahead inclusive
        max_date = today + timedelta(days=3)
        sessions = UmugandaSession.objects.filter(
            date__gte=today,
            date__lte=max_date,
            sector__isnull=False,
            cell__isnull=False
        ).order_by('date')

        count = sessions.count()
        logger.info(f"[UmugandaNotification] Found {count} upcoming sessions between {today} and {max_date}")

        if count == 0:
            logger.info("[UmugandaNotification] No upcoming sessions with sector and cell to notify.")
            return {"sessions_notified": 0, "emails_sent": 0, "sms_sent": 0}

    sent_emails = 0
    sent_sms = 0

    for session in sessions:
        # Defensive check: skip if mandatory fields missing (should be covered by queryset)
        if not (session.sector and session.cell):
            logger.warning(f"[UmugandaNotification] Skipping session {session.id} due to missing sector or cell.")
            continue

        # Find active citizen users whose profile cell and sector match the session
        users = CustomUser.objects.filter(
            user_level='citizen',
            is_active=True,
            profile__sector=session.sector,
            profile__cell=session.cell,
        )

        user_count = users.count()
        logger.info(f"[UmugandaNotification] Session {session.id} on {session.date} has {user_count} users to notify.")

        if user_count == 0:
            continue

        # Prepare common notification context for templates
        session_context = {
            'id': str(session.id),
            'date': session.date,
            'sector_name': session.sector.name,
            'cell_name': session.cell.name,
            'village_name': session.village.name if session.village else None,
            'tools_needed': session.tools_needed,
            'fines_policy': session.fines_policy,
            'description': session.description or "No additional details provided.",
        }

        for user in users:
            subject = "Upcoming Umuganda Activity Scheduled"
            message = (
                f"Dear {user.full_names},\n\n"
                f"There is an Umuganda activity scheduled on {session.date.strftime('%Y-%m-%d')} "
                f"in your sector {session.sector.name} and cell {session.cell.name}.\n\n"
                f"Details: {session_context['description']}\n\n"
                "Please participate actively.\n\n"
                "Thank you!"
            )

            # Send Email
            email_notif = None
            try:
                email_notif = Notification.objects.create(
                    recipient=user,
                    triggered_by=None,
                    notification_type='email',
                    subject=subject,
                    message=message,
                    is_sent=False,
                )

                context = {
                    "full_names": user.full_names,
                    "session": session_context,
                    "support_email": getattr(settings, "DEFAULT_SUPPORT_EMAIL", "support@example.com"),
                }

                text_content = render_to_string("emails/umuganda_notification.txt", context)
                html_content = render_to_string("emails/umuganda_notification.html", context)

                from_email = settings.DEFAULT_FROM_EMAIL
                email_msg = EmailMultiAlternatives(subject, text_content, from_email, [user.email])
                email_msg.attach_alternative(html_content, "text/html")

                logger.debug(f"Sending email to {user.email} for session {session.id}")
                email_msg.send()

                email_notif.is_sent = True
                email_notif.sent_at = timezone.now()
                email_notif.save()
                sent_emails += 1

                logger.info(f"[UmugandaNotification] Email sent to {user.email}")

            except Exception as e:
                logger.error(f"[UmugandaNotification] Failed to send email to {user.email}: {e}")
                if email_notif:
                    email_notif.is_sent = False
                    email_notif.save()
                raise self.retry(exc=e, countdown=60)

            # Send SMS
            sms_notif = None
            try:
                if user.phone_number:
                    sms_sent = send_sms(user.phone_number, message)
                    sms_notif = Notification.objects.create(
                        recipient=user,
                        triggered_by=None,
                        notification_type='sms',
                        subject=subject,
                        message=message,
                        is_sent=sms_sent,
                        sent_at=timezone.now() if sms_sent else None,
                    )
                    if sms_sent:
                        sent_sms += 1
                        logger.info(f"[UmugandaNotification] SMS sent to {user.phone_number}")
                    else:
                        logger.warning(f"[UmugandaNotification] Failed to send SMS to {user.phone_number}")
                else:
                    logger.warning(f"[UmugandaNotification] User {user.id} has no phone number; skipping SMS.")
            except Exception as e:
                logger.error(f"[UmugandaNotification] Error sending SMS to user {user.id}: {e}")
                if sms_notif:
                    sms_notif.is_sent = False
                    sms_notif.save()

    return {
        "sessions_notified": len(sessions),
        "emails_sent": sent_emails,
        "sms_sent": sent_sms,
    }
