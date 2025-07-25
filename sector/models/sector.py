from django.db import models
import uuid
from users.models.addresses import Province, District, Sector as AddressSector  # clarify Sector import

class AdminSector(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    province = models.ForeignKey(
        Province,
        on_delete=models.PROTECT,
        related_name="admin_sectors",
        help_text="Province to which this sector belongs"
    )
    district = models.ForeignKey(
        District,
        on_delete=models.PROTECT,
        related_name="admin_sectors",
        help_text="District to which this sector belongs"
    )
    sector = models.ForeignKey(
        AddressSector,
        on_delete=models.PROTECT,
        related_name="admin_sectors",
        help_text="Unique sector reference (must match national hierarchy)"
    )

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Administrative Sector'
        verbose_name_plural = 'Administrative Sectors'
        ordering = ['province__name', 'district__name', 'sector__name']
        constraints = [
            models.UniqueConstraint(
                fields=['province', 'district', 'sector'],
                name='unique_admin_sector_combination'
            )
        ]

    def __str__(self):
        sector_name = getattr(self.sector, 'name', 'Unknown Sector')
        district_name = getattr(self.district, 'name', 'Unknown District')
        province_name = getattr(self.province, 'name', 'Unknown Province')
        return f"{sector_name} ({district_name}, {province_name})"
