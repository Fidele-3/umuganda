from django.db import models
from django.utils import timezone
from users.models.customuser import CustomUser

from sector.models.sector import AdminSector

class Notification(models.Model):
    NOTIFICATION_TYPE_CHOICES = [
        ("in_app", "In-App"),
        ("email", "Email"),
        ("sms", "SMS"),
    ]

    recipient = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE,
        related_name="notifications", null=True, blank=True,
        help_text="User receiving this notification"
    )
    sector = models.ForeignKey(
        AdminSector,
        on_delete=models.CASCADE,
        related_name="notifications",
        null=True, blank=True,
        help_text="If set, this notification is directed to the entire sector"
    )

    triggered_by = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name="triggered_notifications",
        help_text="User or admin who triggered this notification"
    )

    notification_type = models.CharField(
        max_length=10, choices=NOTIFICATION_TYPE_CHOICES
    )

    subject = models.CharField(
        max_length=255, blank=True,
        help_text="Short summary or subject line for email/SMS"
    )

    message = models.TextField(help_text="Full notification message")

    is_read = models.BooleanField(default=False)
    is_sent = models.BooleanField(default=False, help_text="Only relevant for email and SMS")

    created_at = models.DateTimeField(auto_now_add=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"

    def __str__(self):
        return f"{self.notification_type.upper()} notification to {self.recipient.full_names}"
