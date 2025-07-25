# users/signals.py
from django.db.models.signals import pre_save
from django.dispatch import receiver
from users.models.customuser import CustomUser
from users.tasks.send_email_password_reset_success import send_email_password_reset_success


@receiver(pre_save, sender=CustomUser)
def notify_password_reset(sender, instance, **kwargs):
    if not instance.pk:
        # New user, ignore
        return
    
    try:
        old_user = CustomUser.objects.get(pk=instance.pk)
    except CustomUser.DoesNotExist:
        return
    
    # Check if password has changed
    if old_user.password != instance.password:
        # Password was changed, trigger email task
        send_email_password_reset_success.delay(
            str(instance.pk),
            instance.full_names,
            instance.email,
        )
