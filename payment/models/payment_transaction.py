import uuid
from django.db import models
from users.models.addresses import Sector
from payment.models.payment_provider import PaymentProvider
from users.models.customuser import CustomUser
from umuganda.models.fine import Fine




class PaymentTransaction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='payment_transactions')
    fine = models.OneToOneField(Fine, on_delete=models.CASCADE, related_name='transaction')
    provider = models.ForeignKey(PaymentProvider, on_delete=models.SET_NULL, null=True, blank=True)
    
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(max_length=10, choices=[
        ('pending', 'Pending'),
        ('success', 'Success'),
        ('failed', 'Failed')
    ], default='pending')

    reference_code = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    confirmed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.full_names} - {self.amount} - {self.status}"
