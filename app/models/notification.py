from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from app.db.database import Base


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    channel = Column(String, nullable=False)
    recipient = Column(String, nullable=False)
    content = Column(String, nullable=False)
    status = Column(String, default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)