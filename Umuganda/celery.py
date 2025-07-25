import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings
import ssl

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Umuganda.settings")

app = Celery("Umuganda")

# Load config from settings.py
app.config_from_object("django.conf:settings", namespace="CELERY")

# 👇 Override to include required SSL setting explicitly
app.conf.broker_use_ssl = {
    "ssl_cert_reqs": ssl.CERT_NONE,  # CERT_NONE disables SSL cert check
}

app.conf.result_backend_use_ssl = {
    "ssl_cert_reqs": ssl.CERT_NONE,
}

# Autodiscover tasks
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# Optional: Celery Beat schedule
app.conf.beat_schedule = {
    'send-umuganda-notifications-twice-daily': {
        'task': 'users.tasks.send_umuganda_reminder.send_umuganda_notifications',
        'schedule': crontab(minute=0, hour='6,18')
    },
}
