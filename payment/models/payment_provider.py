import uuid
from django.db import models

class PaymentProvider(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, unique=True)  # e.g., "MTN MoMo"
    provider_code = models.CharField(max_length=30, unique=True)  # e.g., "mtn", "airtel"
    api_url = models.URLField(null=True, blank=True)  # Reserve for integration
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
