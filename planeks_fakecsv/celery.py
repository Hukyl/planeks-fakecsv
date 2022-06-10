"""
This module provides with `celery` app.

Variables:
    - app: `celery` app
"""

import os

from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'planeks_fakecsv.settings')

app = Celery('planeks_fakecsv')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.broker_url = os.environ.get('REDIS_URL')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()
