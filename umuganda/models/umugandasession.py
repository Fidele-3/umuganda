import uuid
from django.db import models
from users.models.addresses import Sector, Cell, Village
from users.models.customuser import CustomUser

class UmugandaSession(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    date = models.DateField()
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE, related_name='umuganda_sessions')
    created_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='sector_created_sessions',
        help_text="Sector admin who initiated the Umuganda date"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    cell = models.ForeignKey(
        Cell,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='umuganda_sessions',
        help_text="Cell where Umuganda will be held (added by Cell admin)"
    )
    village = models.ForeignKey(
        Village,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='umuganda_sessions',
        help_text="Optional village where the Umuganda will take place"
    )

    tools_needed = models.TextField(blank=True, null=True, help_text="Tools required for the session")
    fines_policy = models.TextField(blank=True, null=True, help_text="Fines for absence or delays")
    description = models.TextField(blank=True, null=True, help_text="Extra details or description of the activity")

    updated_by_cell_admin = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='cell_updated_sessions',
        limit_choices_to={'user_level': 'cell_officer'},
        help_text="Cell admin who updated details"
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('date', 'sector')  
        ordering = ['-date']

    def __str__(self):
        return f"{self.sector.name} - {self.date}"
