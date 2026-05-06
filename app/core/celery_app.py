from celery import Celery
from app.core.config import settings

celery_app = Celery(
    "order_management_worker",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=["app.tasks.notifications"],
)