from rest_framework import serializers
from users.models.customuser import CustomUser
from users.models.userprofile import UserProfile
from admn.models.admin import AdminHierarchy
from sector.models.sector import AdminSector
from users.models.addresses import Province, District, Sector, Cell, Village
from django.db import transaction
from django.core.exceptions import ValidationError

class RegisterUserSerializer(serializers.ModelSerializer):
    added_by_id = serializers.UUIDField(required=False, write_only=True)
    sector_id = serializers.UUIDField(required=False, write_only=True)

    bio = serializers.CharField(required=False, allow_blank=True)
    gender = serializers.ChoiceField(choices=UserProfile.GENDER_CHOICES, required=False)
    national_id = serializers.CharField(required=False)
    date_of_birth = serializers.DateField(required=False)
    work = serializers.CharField(required=False, allow_blank=True)
    work_description = serializers.CharField(required=False, allow_blank=True)
    province = serializers.PrimaryKeyRelatedField(queryset=Province.objects.all(), required=True)
    district = serializers.PrimaryKeyRelatedField(queryset=District.objects.all(), required=True)
    sector = serializers.PrimaryKeyRelatedField(queryset=Sector.objects.all(), required=True)
    cell = serializers.PrimaryKeyRelatedField(queryset=Cell.objects.all(), required=True)
    village = serializers.PrimaryKeyRelatedField(queryset=Village.objects.all(), required=True)
    website = serializers.URLField(required=False, allow_blank=True)

    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = CustomUser
        fields = [
            'full_names', 'email', 'password', 'user_level',
            'added_by_id', 'sector_id','national_id', 
            # Profile info
            'bio', 'gender', 'date_of_birth',
            'work', 'work_description', 'province', 'district',
            'sector', 'cell', 'village', 'website'
        ]
        extra_kwargs = {
            'user_level': {'required': False}  # Make user_level optional
        }

    def validate(self, attrs):
        request_data = self.context['request'].data
        user_level = attrs.get('user_level')
        added_by_id = request_data.get('added_by_id')
        sector_id = request_data.get('sector_id')

        # Default to citizen
        if user_level is None:
            attrs['user_level'] = 'citizen'
            user_level = 'citizen'

        # ----- Address Hierarchy Validation -----
        province = attrs.get('province')
        district = attrs.get('district')
        sector = attrs.get('sector')
        cell = attrs.get('cell')
        village = attrs.get('village')

        if district.province_id != province.id:
            raise serializers.ValidationError("District does not belong to the selected Province.")

        if sector.district_id != district.id:
            raise serializers.ValidationError("Sector does not belong to the selected District.")

        if cell.sector_id != sector.id:
            raise serializers.ValidationError("Cell does not belong to the selected Sector.")

        if village.cell_id != cell.id:
            raise serializers.ValidationError("Village does not belong to the selected Cell.")

        # ----- Role Logic -----
        if user_level == 'citizen':
            if added_by_id or sector_id:
                raise serializers.ValidationError("Citizen cannot have added_by or sector.")
            return attrs

        if user_level not in ['super_admin', 'sector_officer', 'cell_officer']:
            raise serializers.ValidationError("Invalid user level for admin.")

        if user_level == 'super_admin':
            if CustomUser.objects.filter(user_level='super_admin').exists():
                raise serializers.ValidationError("Only one super admin can exist.")
            if added_by_id or sector_id:
                raise serializers.ValidationError("Super Admin should not have added_by or sector.")
            return attrs

        if not added_by_id or not sector_id:
            raise serializers.ValidationError("Admins must have both added_by_id and sector_id.")

        try:
            added_by = CustomUser.objects.get(id=added_by_id)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("Adding user does not exist.")

        if user_level == 'sector_officer' and added_by.user_level != 'super_admin':
            raise serializers.ValidationError("Only super admin can add sector_officer.")
        if user_level == 'cell_officer' and added_by.user_level != 'sector_officer':
            raise serializers.ValidationError("Only sector_officer can add cell_officer.")

        if not AdminSector.objects.filter(sector_id=sector_id).exists():
            raise serializers.ValidationError("Sector assignment not found in AdminSector.")

        return attrs

    def create(self, validated_data):
        with transaction.atomic():
            request_data = self.context['request'].data
            added_by_id = request_data.get('added_by_id')
            sector_id = request_data.get('sector_id')
            password = validated_data.pop('password')
            user_level = validated_data.get('user_level', 'citizen')  # Default to citizen
    
            profile_fields = {
                'bio': validated_data.get('bio', ''),
                'gender': validated_data.get('gender'),
                
                'date_of_birth': validated_data.get('date_of_birth'),
                'work': validated_data.get('work', ''),
                'work_description': validated_data.get('work_description', ''),
                'province': validated_data.get('province'),
                'district': validated_data.get('district'),
                'sector': validated_data.get('sector'),
                'cell': validated_data.get('cell'),
                'village': validated_data.get('village'),
                'website': validated_data.get('website', '')
            }

            for field in profile_fields.keys():
                validated_data.pop(field, None)

            # Ensure user_level is set (defaults to citizen)
            validated_data['user_level'] = user_level

            user = CustomUser.objects.create(**validated_data)
            user.set_password(password)
            user.save()

            # Only set sector for admin users
            sector_obj = AdminSector.objects.get(sector_id=sector_id) if sector_id and user_level != 'citizen' else None

            UserProfile.objects.create(
                user=user,
                assigned_sector=sector_obj,
                **profile_fields
                
            )

            if added_by_id and user_level != 'citizen':
                AdminHierarchy.objects.create(
                    added_by_id=added_by_id,
                    admin=user
                )

            return user