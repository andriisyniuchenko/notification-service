from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from app.api.endpoints.notifications import router as notification_router
from app.api.endpoints.ui import router as ui_router
from app.db.init_db import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="Notification Service", lifespan=lifespan)

app.include_router(notification_router)
app.include_router(ui_router)


@app.get("/")
async def root():
    return RedirectResponse(url="/ui/")