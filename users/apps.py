from django.apps import AppConfig


class UserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self):
        import users.signals.account_notifications
        import users.signals.otp_notification
        from users.signals.pasword_reset_success import notify_password_reset
        from users.signals.notify_umuganda import schedule_umuganda_notifications
        from users.signals.umuganda_fines import assign_fines_to_absentees
        
