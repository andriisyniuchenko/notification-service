from app.db.database import Base, engine
from app.models import notification


def init_db():
    Base.metadata.create_all(bind=engine)