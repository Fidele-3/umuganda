# serializers/userprofile.py

from rest_framework import serializers
from users.models import UserProfile
from users.models.addresses import Province, District, Sector, Cell, Village
from users.models import CustomUser
from umuganda.models import CellUmugandaSession
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








class CellUmugandaSessionSerializer(serializers.ModelSerializer):
    date = serializers.DateField(source='sector_session.date', read_only=True)
    sector = serializers.CharField(source='sector_session.sector.name', read_only=True)
    cell = serializers.CharField(source='cell.name', read_only=True)
    village = serializers.CharField(source='village.name', read_only=True)
    created_at = serializers.DateTimeField(source='sector_session.created_at', read_only=True)

    created_by = serializers.SerializerMethodField()
    updated_by_cell_admin = serializers.SerializerMethodField()

    def split_full_names(self, full_name):
        if not full_name:
            return {"first_name": "", "last_name": ""}
        parts = full_name.strip().split(" ", 1)
        if len(parts) == 1:
            return {"first_name": parts[0], "last_name": ""}
        return {"first_name": parts[0], "last_name": parts[1]}

    def get_created_by(self, obj):
        if obj.sector_session.created_by:
            return self.split_full_names(obj.sector_session.created_by.full_names)
        return {"first_name": "", "last_name": ""}

    def get_updated_by_cell_admin(self, obj):
        if obj.updated_by:
            return self.split_full_names(obj.updated_by.full_names)
        return None

    class Meta:
        model = CellUmugandaSession
        fields = [
            'id',
            'date',
            'sector',
            'cell',
            'village',
            'description',
            'tools_needed',
            'fines_policy',
            'created_by',
            'updated_by_cell_admin',
            'created_at',
            'updated_at',
        ]



class AttendanceSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()
    session = CellUmugandaSessionSerializer()

    class Meta:
        model = Attendance
        fields = [
            "id", "user", "session", "status", "remarks", "recorded_at"
        ]

class FineSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()
    session = CellUmugandaSessionSerializer()

    class Meta:
        model = Fine
        fields = [
            "id", "user", "session", "amount", "status", "moths_overdue",
            "issued_at", "paid_at", "reason"
        ]
