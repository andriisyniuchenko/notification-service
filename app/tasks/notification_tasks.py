import logging
import time
import random

from app.tasks.celery_app import celery
from app.db.database import SessionLocal
from app.models.notification import Notification

logger = logging.getLogger(__name__)

SIMULATED_FAILURE_RATE = 0.1  # 10% chance of failure to demonstrate retry logic


def _simulate_send(channel: str, recipient: str, content: str) -> None:
    """
    Simulates sending a notification via the given channel.
    Replace this block with a real provider (SendGrid, Twilio, FCM, etc.)
    """
    time.sleep(0.5)  # imitate network latency

    if random.random() < SIMULATED_FAILURE_RATE:
        raise ConnectionError(f"Simulated transient failure for channel '{channel}'")

    logger.info(
        "Notification sent | channel=%s recipient=%s content_length=%d",
        channel,
        recipient,
        len(content),
    )


def _update_status(notification_id: int, status: str) -> None:
    db = SessionLocal()
    try:
        notification = db.get(Notification, notification_id)
        if notification:
            notification.status = status
            db.commit()
    finally:
        db.close()


@celery.task(
    name="app.tasks.notification_tasks.send_notification_task",
    bind=True,
    max_retries=3,
    default_retry_delay=5,
)
def send_notification_task(self, notification_id: int) -> None:
    logger.info("Processing notification id=%d (attempt %d)", notification_id, self.request.retries + 1)

    db = SessionLocal()
    try:
        notification = db.get(Notification, notification_id)
        if not notification:
            logger.error("Notification id=%d not found, skipping", notification_id)
            return

        channel = notification.channel
        recipient = notification.recipient
        content = notification.content
    finally:
        db.close()

    try:
        _simulate_send(channel, recipient, content)
        _update_status(notification_id, "sent")
        logger.info("Notification id=%d marked as sent", notification_id)

    except Exception as exc:
        logger.warning(
            "Failed to send notification id=%d: %s. Retries left: %d",
            notification_id,
            exc,
            self.max_retries - self.request.retries,
        )
        _update_status(notification_id, "failed")
        raise self.retry(exc=exc)