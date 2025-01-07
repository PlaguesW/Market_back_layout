import os
import sys
from celery import Celery

print("PYTHONPATH:", sys.path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PartsShopSettings.settings')

celery_app = Celery('PartsShop')

celery_app.config_from_object('django.conf:settings', namespace='CELERY')

celery_app.autodiscover_tasks(related_name='tasks')
