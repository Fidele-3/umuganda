from rest_framework import serializers
from umuganda.models import Fine
from users.models.userprofile import UserProfile  
class UserProfileMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'full_names', 'national_id', 'phone_number', 'village', 'cell', 'sector']

class FineSerializer(serializers.ModelSerializer):
    user = UserProfileMiniSerializer()

    class Meta:
        model = Fine
        fields = [
            'id',
            'user',
            'session',
            'amount',
            'status',
            'moths_overdue',
            'issued_at',
            'paid_at',
            'reason'
        ]
