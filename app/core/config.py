import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL: str = os.getenv("DATABASE_URL", "")
REDIS_URL: str = os.getenv("REDIS_URL", "")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set")

if not REDIS_URL:
    raise RuntimeError("REDIS_URL is not set")