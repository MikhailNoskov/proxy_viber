import os

from celery import Celery
from celery.schedules import crontab, schedule

from viber_filter.tasks import resend_to_main, flush_celery_tasks

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('core')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
app.conf.beat_schedule = {
    'send_request_to_main': {
            'task': 'viber_filter.tasks.resend_to_main',
            # 'schedule': crontab(second='*/1'),
            'schedule': schedule(run_every=1),
        },
    'clear_redis_from_tasks': {
            'task': 'viber_filter.tasks.flush_celery_tasks',
            'schedule': crontab(minute='*/1'),
        },
}
