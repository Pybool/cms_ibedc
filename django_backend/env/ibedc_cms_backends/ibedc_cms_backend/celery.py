import os
from celery import Celery
#set the default django settings to celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ibedc_cms_backend.settings')
app = Celery('ibedc_cms_backend')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# celery -A ibedc_cms_backend worker --loglevel=info -P eventlet
