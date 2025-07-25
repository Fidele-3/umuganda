
from django.db import models
from django.conf import settings
from users.models.addresses import Cell  

class CellAdminMembership(models.Model):
    admin = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='cell_memberships',
        unique=True,
        help_text="User assigned as the cell officer"
    )
    cell = models.OneToOneField(
        Cell,
        on_delete=models.CASCADE,
        related_name='admin_membership',
        unique=True,
        help_text="Cell this admin is responsible for"
    )

    assigned_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Cell Admin Membership"
        verbose_name_plural = "Cell Admin Memberships"
        constraints = [
            models.UniqueConstraint(fields=['admin'], name='unique_admin_per_cell'),
            models.UniqueConstraint(fields=['cell'], name='unique_cell_per_admin'),
        ]
        ordering = ['cell__sector__district__name', 'cell__sector__name', 'cell__name']

    def __str__(self):
        return f"{self.admin.full_names} is assigned to {self.cell.name}"
