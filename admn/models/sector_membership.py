# sector/models/sector_admin_membership.py

from django.db import models
from django.conf import settings

class sectorAdminMembership(models.Model):
    admin = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sector_membership',
        unique=True  # technically redundant, but clear
    )
    sector = models.OneToOneField(
        'sector.AdminSector',
        on_delete=models.CASCADE,
        related_name='admin_membership',
        unique=True  # ensures one sector can have only one admin
    )

    assigned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Sector Admin Membership"
        verbose_name_plural = "Sector Admin Memberships"
        constraints = [
            models.UniqueConstraint(fields=['admin'], name='unique_admin_per_sector'),
            models.UniqueConstraint(fields=['sector'], name='unique_sector_per_admin'),
        ]

    def __str__(self):
        return f"{self.admin.email} belongs to {self.sector}"
