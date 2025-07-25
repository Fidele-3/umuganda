from django.db.models.signals import post_save
from django.dispatch import receiver
from umuganda.models import Fine
from users.tasks .send_fine_created_notification import send_fine_created_notification

@receiver(post_save, sender=Fine)
def notify_user_on_fine_created(sender, instance, created, **kwargs):
    if created:
        send_fine_created_notification.delay(str(instance.id))
