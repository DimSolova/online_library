from celery import Celery
from celery.schedules import crontab

from src.config import setting

celery_instance = Celery(
    "tasks",
    broker=setting.REDIS_URL,
    include=[
        "src.tasks.tasks",
    ],
)

# Не работает crontab
celery_instance.conf.beat_schedule = {
    "Clear cache": {"task": "clear_all_cache", "schedule": crontab(hour=19, minute=45)}
}
