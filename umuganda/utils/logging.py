# admn/utils/logging.py
from admn.models import AdminActionLog

def log_admin_action(admin, action, action_type="other", target_user=None,  extra_data=None):
    AdminActionLog.objects.create(
        admin=admin,
        action=action,
        action_type=action_type,
        target_user=target_user,
        extra_data=extra_data or {}
    )
