from celery import Celery

from src.config import setting

celery_instance = Celery(
    "tasks",
    broker=setting.REDIS_URL,
    include=[
        "src.tasks.tasks",
    ]
)