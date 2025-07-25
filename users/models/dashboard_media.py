from django.db import models
from django.conf import settings
from users.models.customuser import CustomUser

class DashboardMedia(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='dashboard_media/', blank=True, null=True)
    file = models.FileField(upload_to='dashboard_media/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
