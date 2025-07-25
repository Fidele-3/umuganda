from django.db import models
from users.models.addresses import Province, District, Sector, Cell, Village  

class sectorAssignment(models.Model):
    sector = models.ForeignKey('sector.Sector', on_delete=models.CASCADE, related_name='assignments')

    province = models.ForeignKey(Province, on_delete=models.SET_NULL, null=True, blank=True)
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True, blank=True)
    sector = models.ForeignKey(Sector, on_delete=models.SET_NULL, null=True, blank=True)
    cell = models.ForeignKey(Cell, on_delete=models.SET_NULL, null=True, blank=True)
    village = models.ForeignKey(Village, on_delete=models.SET_NULL, null=True, blank=True)

    assigned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'sector Assignment'
        verbose_name_plural = 'sector Assignments'
        unique_together = ('sector', )

    def __str__(self):
        return f"{self.sector.name} handles ({self.village or self.sector or self.district or self.province or 'All Regions'})"
