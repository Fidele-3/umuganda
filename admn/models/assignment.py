from django.db import models
from users.models.customuser import CustomUser
from users.models.userprofile import UserProfile
from users.models.addresses import Cell  # adjust if your Cell model is in a different path

class UmugandaAssignment(models.Model):
    cell_officer = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        limit_choices_to={'user_level': 'cell_officer'},
        related_name='umuganda_assignments',
        help_text="Cell officer assigned to coordinate Umuganda"
    )

    cell = models.ForeignKey(
        Cell,
        on_delete=models.CASCADE,
        related_name='umuganda_assignments',
        help_text="The cell to which this assignment applies"
    )

    assigned_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'user_level__in': ['sector_officer', 'district_admin', 'project_superadmin']},
        related_name='umuganda_assignments_made',
        help_text="Higher-level admin who made or edited the assignment"
    )

    assigned_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    notes = models.TextField(blank=True, null=True, help_text="Optional notes about the assignment")

    class Meta:
        unique_together = ('cell_officer', 'cell')  # to avoid duplicates
        verbose_name = "Umuganda Assignment"
        verbose_name_plural = "Umuganda Assignments"

    def __str__(self):
        return f"{self.cell_officer.full_names} assigned to Umuganda in {self.cell.name}"
