import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'newspaper.settings')

app = Celery('newspaper')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'action_every_monday_morning': {
        'task': 'news.tasks.notify_subscribers_about_weekly_news',
        'schedule': crontab(hour=9, minute=0, day_of_week=1),
    },
}
