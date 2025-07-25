# serializers/userprofile.py

from rest_framework import serializers
from users.models import UserProfile
from users.models.addresses import Province, District, Sector, Cell, Village
from users.models import CustomUser
from umuganda.models import UmugandaSession
from umuganda.models import Attendance
from umuganda.models import Fine


class UserProfileSerializer(serializers.ModelSerializer):
    province = serializers.StringRelatedField()
    district = serializers.StringRelatedField()
    sector = serializers.StringRelatedField()
    cell = serializers.StringRelatedField()
    village = serializers.StringRelatedField()

    class Meta:
        model = UserProfile
        fields = [
            "bio", "gender", "date_of_birth", "work", "work_description",
            "province", "district", "sector", "cell", "village", "website",
            "created_at", "updated_at"
        ]

class CustomUserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer()

    class Meta:
        model = CustomUser
        fields = [
            "id", "email", "full_names", "phone_number", "user_level",
            "national_id", "is_active", "is_staff", "date_joined", "profile"
        ]



class UmugandaSessionSerializer(serializers.ModelSerializer):
    created_by = CustomUserSerializer()
    updated_by_cell_admin = CustomUserSerializer()
    sector = serializers.StringRelatedField()
    cell = serializers.StringRelatedField()
    village = serializers.StringRelatedField()

    class Meta:
        model = UmugandaSession
        fields = [
            "id", "date", "sector", "cell", "village", "description",
            "tools_needed", "fines_policy", "created_by", "updated_by_cell_admin",
            "created_at", "updated_at"
        ]

class AttendanceSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()
    session = UmugandaSessionSerializer()

    class Meta:
        model = Attendance
        fields = [
            "id", "user", "session", "status", "remarks", "recorded_at"
        ]

class FineSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()
    session = UmugandaSessionSerializer()

    class Meta:
        model = Fine
        fields = [
            "id", "user", "session", "amount", "status", "moths_overdue",
            "issued_at", "paid_at", "reason"
        ]
