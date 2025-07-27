import uuid
from django.db import models
from users.models.customuser import CustomUser
from .umugandasession import CellUmugandaSession


class Fine(models.Model):
    PAYMENT_METHODS = (
        ('MoMo', 'Mobile Money'),
        ('Airtel', 'Airtel Money'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='fines')
    session = models.ForeignKey(CellUmugandaSession, on_delete=models.CASCADE, related_name='fines')
    amount = models.DecimalField(max_digits=8, decimal_places=2, default=1000.00)
    status = models.CharField(max_length=10, choices=[('unpaid', 'Unpaid'), ('paid', 'Paid')], default='unpaid')
    moths_overdue = models.PositiveIntegerField(default=0)
    issued_at = models.DateTimeField(auto_now_add=True)
    paid_at = models.DateTimeField(null=True, blank=True)
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHODS, blank=True, null=True)
    payment_id = models.CharField(max_length=100, blank=True, null=True) 
    reason = models.TextField(blank=True, null=True)
    claim = models.BooleanField(default=False)
    claim_has_been_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.full_names} - {self.amount} RWF - {self.status} - {self.moths_overdue} months overdue - {self.reason}"