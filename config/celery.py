from __future__ import absolute_import

import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

from django.conf import settings  # noqa

from celery.schedules import crontab


app = Celery('config')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


## celery app configuration
app.conf.CELERYBEAT_SCHEDULE = {
    # Executes at midnight
    'update-matches': {
        'task': 'apps.overseer.tasks.UpdateMatches',
        'schedule': crontab(hour=12, minute=7),
    },
}
app.conf.CELERY_TIMEZONE = 'Asia/Kolkata'