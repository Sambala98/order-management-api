import logging
from app.core.celery_app import celery_app

logger = logging.getLogger("app")


@celery_app.task(name="send_order_notification")
def send_order_notification(order_id: int, customer_name: str, item_name: str) -> str:
    message = f"Order notification sent for order_id={order_id}, customer={customer_name}, item={item_name}"
    logger.info(message)
    return message