import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Umuganda.settings")

app = Celery("Umuganda")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.conf.timezone = 'Africa/Kigali'
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.beat_schedule = {
    'send-umuganda-notifications-twice-daily': {
        'task': 'users.tasks.send_umuganda_reminder.send_umuganda_notifications',
        'schedule': crontab(minute=0, hour='6,18')
    },
}
