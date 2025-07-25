from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import timedelta
from django.utils import timezone
from umuganda.models import UmugandaSession
from users.tasks.send_umuganda_reminder import send_umuganda_notifications


@receiver(post_save, sender=UmugandaSession)
def schedule_umuganda_notifications(sender, instance, created, **kwargs):
   
    if created:
        
        send_umuganda_notifications.delay(session_id=str(instance.id))
