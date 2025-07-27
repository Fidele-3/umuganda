import uuid
from django.db import models
from users.models.customuser import CustomUser
from .umugandasession import CellUmugandaSession

class Attendance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='attendances')
    session = models.ForeignKey(CellUmugandaSession, on_delete=models.CASCADE, related_name='attendances')
    status = models.CharField(max_length=10, choices=[('present', 'Present'), ('absent', 'Absent')])
    remarks = models.TextField(blank=True, null=True)

    recorded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'session')

    def __str__(self):
        return f"{self.user.full_names} - {self.session.date} - {self.status}"
