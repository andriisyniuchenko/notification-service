from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class Channel(str, Enum):
    email = "email"
    sms = "sms"
    push = "push"


class NotificationCreate(BaseModel):
    channel: Channel
    recipient: str
    content: str


class NotificationResponse(BaseModel):
    id: int
    channel: str
    recipient: str
    content: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True