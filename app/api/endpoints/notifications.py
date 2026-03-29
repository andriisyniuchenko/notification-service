from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.notification import NotificationCreate, NotificationResponse
from app.services.notification_service import create_notification

router = APIRouter(prefix="/notifications", tags=["notifications"])


@router.post("/", response_model=NotificationResponse)
def create(data: NotificationCreate, db: Session = Depends(get_db)):
    return create_notification(db, data)