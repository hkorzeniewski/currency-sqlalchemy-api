from celery import Celery
from celery.schedules import crontab

celery_app = Celery(
    "tasks",
    broker="redis://redis:6379/0",  # Update this with your actual broker URL
    backend="redis://redis:6379/0",  # Update this with your actual backend URL
)


celery_app.conf.beat_schedule = {
    "save_today_currencies_to_db": {
        "task": "app.currency.worker.save_today_currencies_to_db",
        "schedule": crontab("*/2"),
    },
}

celery_app.conf.timezone = "UTC"
