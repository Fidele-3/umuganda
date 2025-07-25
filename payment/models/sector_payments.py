import uuid
from django.db import models
from users.models.addresses import Sector
from payment.models.payment_provider import PaymentProvider

class SectorPaymentConfig(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sector = models.OneToOneField(Sector, on_delete=models.CASCADE, related_name='payment_config')
    provider = models.ForeignKey(PaymentProvider, on_delete=models.CASCADE)
    account_number = models.CharField(max_length=100)  # E.g., MoMo number
    api_key = models.CharField(max_length=255, blank=True, null=True)  # Reserved for future API use

    def __str__(self):
        return f"{self.sector.name} - {self.provider.name}"
