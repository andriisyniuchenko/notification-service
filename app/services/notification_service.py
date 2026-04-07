from sqlalchemy.orm import Session
from app.models.notification import Notification
from app.tasks.notification_tasks import send_notification_task


def get_notifications(db: Session):
    return db.query(Notification).order_by(Notification.created_at.desc()).all()


def create_notification(db, data):
    notification = Notification(
        channel=data.channel,
        recipient=data.recipient,
        content=data.content,
    )

    db.add(notification)
    db.commit()
    db.refresh(notification)

    send_notification_task.delay(notification.id)

    return notification