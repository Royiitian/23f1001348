from celery import Celery
from celery.schedules import crontab

app = Celery('HSM',
             broker='redis://127.0.0.1:6379/0',
             backend='redis://127.0.0.1:6379/0',
             include=['tasks'])

app.conf.beat_schedule = {
    'run-test-task-every-minute': {
        'task': 'tasks.notify_pending_service_requests',
        'schedule': crontab('*/1'),  # Execute every minute
    },
}