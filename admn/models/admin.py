
from django.db import models
from users.models.customuser import CustomUser
class AdminHierarchy(models.Model):
    added_by = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='admins_added',
        limit_choices_to={'user_level__in': ['super_admin', 'sector_officer']},
        help_text="The admin who added this admin"
    )
    admin = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='added_by_admin',
        limit_choices_to={'user_level__in': ['sector_officer', 'cell_officer']},
        help_text="The admin who was added"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.added_by.full_names} → {self.admin.full_names}"



class AdminActionLog(models.Model):
    admin = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        limit_choices_to={'user_level__startswith': 'admin_'}
    )

    action = models.CharField(max_length=255)

    action_type = models.CharField(
        max_length=50,
        choices=[
            ("admin_created", "Admin Created"),
            ("user_suspended", "User Suspended"),
            ("profile_updated", "Profile Updated"),
            ("login", "Login"),
            ("logout", "Logout"),
            ("otp_requested", "OTP Requested"),
            ("otp_verified", "OTP Verified"),
            ("password_reset_requested", "Password Reset Requested"),
            ("password_reset_successful", "Password Reset Successful"),
            ("sector_created", "Sector Created"),
            ("umuganda_created", "Umuganda Activity Created"),
            ("umuganda_edited", "Umuganda Activity Edited"),
            ("umuganda_deleted", "Umuganda Activity Deleted"),
            ("assignment_made", "Officer Assigned to Umuganda"),
            ("other", "Other"),
        ],
        default="other",
        help_text="Category of action performed"
    )

    target_user = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='actions_taken_on',
        help_text="If the action was about another user"
    )

    extra_data = models.JSONField(
        null=True,
        blank=True,
        help_text="Optional extra context (e.g. old/new values)"
    )

    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.admin.full_names} - {self.action} - {self.timestamp.strftime('%Y-%m-%d %H:%M')}"
