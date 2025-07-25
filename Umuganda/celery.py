
import os
import ssl
from celery import Celery
from celery.schedules import crontab
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Umuganda.settings")

app = Celery("Umuganda")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.conf.timezone = 'Africa/Kigali'
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
app.autodiscover_tasks()

# Add Redis SSL config for Upstash (or any rediss:// broker)
app.conf.broker_use_ssl = {
    'ssl_cert_reqs': ssl.CERT_NONE,  # or ssl.CERT_REQUIRED if you have proper certs
}

app.conf.beat_schedule = {
    'send-umuganda-notifications-twice-daily': {
        'task': 'users.tasks.send_umuganda_reminder.send_umuganda_notifications',
        'schedule': crontab(minute=0, hour='6,18')
    },
}
