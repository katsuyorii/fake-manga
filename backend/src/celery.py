import sys

from pathlib import Path

from celery import Celery

from .settings import rabbit_mq_settings


sys.path.append(str(Path(__file__).resolve().parent.parent))

celery_app = Celery('worker', broker=rabbit_mq_settings.RABBIT_MQ_URL)

celery_app.autodiscover_tasks(['auth'])