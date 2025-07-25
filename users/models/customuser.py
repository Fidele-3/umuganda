
from celery import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from ..managers import CustomUserManager

import uuid
class CustomUser(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    USER_LEVEL_CHOICES = [
        ("super_admin", "Super Admin"),
        ("sector_officer", "SECTOR EXECUTIVE OFFICER"),
        ("cell_officer", "Cell Executive Officer"),
        ("citizen", "citizen"),
    ]

    email = models.EmailField(unique=True)
    full_names = models.CharField(max_length=150, unique=False)
    phone_number = models.CharField(max_length=20, blank=True)
    user_level = models.CharField(max_length=20, choices=USER_LEVEL_CHOICES, default="citizen")
    national_id = models.CharField(max_length=16, unique=True, blank=False, null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    full_names_FIELD = "email"
    REQUIRED_FIELDS = ["full_names"]

    def __str__(self):
        return self.email
    def get_full_name(self):
        return self.full_names    