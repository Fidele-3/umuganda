from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction
from django.utils import timezone
from users.models.customuser import CustomUser
from users.models.notification import Notification
from users.tasks.account_created import send_account_created_email

@receiver(post_save, sender=CustomUser)
def send_in_app_and_email_account_created(sender, instance, created, **kwargs):
    if created:
       
        Notification.objects.create(
            recipient=instance,
            triggered_by=None, 
            notification_type='in_app',
            subject="Account Created Successfully",
            message="Your account has been created and is now active.",
            is_sent=True,
            sent_at=timezone.now()
        )

        if instance.email:
            transaction.on_commit(lambda: send_account_created_email.delay(instance.id))
