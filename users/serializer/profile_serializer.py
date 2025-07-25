from rest_framework import serializers
from users.models.userprofile import UserProfile
from users.models.addresses import Province, District, Sector, Cell, Village
from sector.models.sector import AdminSector


class UserProfileSerializer(serializers.ModelSerializer):
    # CustomUser fields (from linked `user` field)
    email = serializers.EmailField(source='user.email', read_only=True)
    full_names = serializers.CharField(source='user.full_names', read_only=True)
    phone_number = serializers.CharField(source='user.phone_number', read_only=True)
    user_level = serializers.CharField(source='user.user_level', read_only=True)

    # Foreign key fields
    province = serializers.PrimaryKeyRelatedField(queryset=Province.objects.all())
    district = serializers.PrimaryKeyRelatedField(queryset=District.objects.all())
    sector = serializers.PrimaryKeyRelatedField(queryset=Sector.objects.all())
    cell = serializers.PrimaryKeyRelatedField(queryset=Cell.objects.all())
    village = serializers.PrimaryKeyRelatedField(queryset=Village.objects.all())
    assigned_sector = serializers.PrimaryKeyRelatedField(queryset=AdminSector.objects.all(), allow_null=True, required=False)

    class Meta:
        model = UserProfile
        fields = [
            # From CustomUser
            'email', 'full_names', 'phone_number', 'user_level',
            # From UserProfile
            'bio', 'gender', 'date_of_birth',
            'work', 'work_description', 'website', 'sector',
            'province', 'district', 'assigned_sector', 'cell', 'village',
        ]

    def validate_gender(self, value):
        if value and value not in dict(UserProfile.GENDER_CHOICES):
            raise serializers.ValidationError("Invalid gender value.")
        return value

    def update(self, instance, validated_data):
        # Handle nested `user` fields safely
        user_data = validated_data.pop('user', {})
        user = instance.user
        for attr, value in user_data.items():
            setattr(user, attr, value)
        user.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
