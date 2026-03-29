from fastapi import FastAPI
from app.db.init_db import init_db

app = FastAPI(title="Notification Service")


@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/")
async def root():
    return {"status": "OK"}