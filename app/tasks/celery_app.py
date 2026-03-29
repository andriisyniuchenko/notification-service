import os
from celery import Celery
from dotenv import load_dotenv

load_dotenv()

REDIS_URL = os.getenv("REDIS_URL")

celery = Celery(
    "notification_service",
    broker=REDIS_URL,
    backend=REDIS_URL,
)

celery.conf.task_routes = {
    "app.tasks.notification_tasks.*": {"queue": "default"}
}

import app.tasks.notification_tasks