from fastapi import FastAPI
from app.api.endpoints.notifications import router as notification_router
from app.db.init_db import init_db

app = FastAPI(title="Notification Service")


@app.on_event("startup")
def on_startup():
    init_db()


app.include_router(notification_router)


@app.get("/")
async def root():
    return {"status": "OK"}