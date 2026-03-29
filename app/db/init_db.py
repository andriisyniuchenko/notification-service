import time

from app.db.database import Base, engine
from app.models import notification


def init_db():
    for i in range(10):
        try:
            Base.metadata.create_all(bind=engine)
            print("DB connected successfully")
            return
        except Exception as e:
            print(f"DB not ready, retrying... ({i})")
            time.sleep(2)

    raise Exception("Could not connect to DB")