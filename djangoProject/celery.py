import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoProject.settings')

app = Celery('djangoProject')

app.conf.update(timezone='Europe/Moscow')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'update_table_every_5_min': {
        'task': 'mainapp.tasks.update_table_in_interval',
        'schedule': crontab(minute='*/100'),
    },
    'update_currency_rate_every_day': {
        'task': 'mainapp.tasks.update_currency_rate',
        'schedule': crontab(hour=2, minute=10),  # ЦБРФ выпускает релиз курса на день в 11 30 по мск
        'args': ('usd',),
    },
}

app.autodiscover_tasks()


