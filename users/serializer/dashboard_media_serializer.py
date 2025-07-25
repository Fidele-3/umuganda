from rest_framework import serializers
from users.models import DashboardMedia

class DashboardMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DashboardMedia
        fields = ['id', 'title', 'description', 'image', 'file', 'uploaded_at']
