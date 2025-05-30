import os

from celery import Celery
from time import sleep

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_project.settings.base')

app = Celery('my_project')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

