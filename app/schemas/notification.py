from datetime import datetime

from pydantic import BaseModel


class NotificationCreate(BaseModel):
    channel: str
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