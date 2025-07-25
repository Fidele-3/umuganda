from django.db import models
from django.conf import settings
from umuganda.models import UmugandaSession, Fine

class Feedback(models.Model):
    FEEDBACK_TYPE_CHOICES = [
        ('fine', 'Fine Issue'),
        ('lateness', 'Lateness Concern'),
        ('system', 'System Bug/Problem'),
        ('other', 'Other'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='feedbacks')
    session = models.ForeignKey(UmugandaSession, null=True, blank=True, on_delete=models.SET_NULL, related_name='feedbacks')
    fine = models.ForeignKey(Fine, null=True, blank=True, on_delete=models.SET_NULL, related_name='feedbacks')
    feedback_type = models.CharField(max_length=20, choices=FEEDBACK_TYPE_CHOICES)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user} - {self.feedback_type} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"
