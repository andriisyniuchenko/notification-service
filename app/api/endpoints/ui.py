from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.notification import NotificationCreate
from app.services.notification_service import create_notification, get_notifications

router = APIRouter(prefix="/ui", tags=["ui"])
templates = Jinja2Templates(directory="templates")


@router.get("/")
def index(request: Request, db: Session = Depends(get_db)):
    notifications = get_notifications(db)
    return templates.TemplateResponse(request=request, name="index.html", context={"notifications": notifications})


@router.post("/send")
def send(
    channel: str = Form(...),
    recipient: str = Form(...),
    content: str = Form(...),
    db: Session = Depends(get_db),
):
    data = NotificationCreate(channel=channel, recipient=recipient, content=content)
    create_notification(db, data)
    return RedirectResponse(url="/ui/", status_code=303)