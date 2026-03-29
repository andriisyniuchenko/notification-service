from sqlalchemy.orm import Session
from app.models.notification import Notification


def create_notification(db: Session, data):
    notification = Notification(
        channel=data.channel,
        recipient=data.recipient,
        content=data.content,
    )

    db.add(notification)
    db.commit()
    db.refresh(notification)

    return notification