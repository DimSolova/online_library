from celery import Celery

from src.config import setting

celery_instance = Celery(
    "tasks",
    broker=setting.REDIS_URL,
    include=[
        "src.tasks.tasks",
    ],
)

celery_instance.conf.beat_schedule = {
    "Clear cache": {
        "task": "clear_all_cache",
        "schedule": 5
    }
}
