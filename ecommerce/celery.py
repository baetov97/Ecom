import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
app = Celery('ecommerce')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'delete_no_active_user': {
        'task': 'account.tasks.delete_no_active_user',
        'schedule': 30
    }
}
