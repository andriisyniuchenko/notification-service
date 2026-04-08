# Notification Service

A backend service that demonstrates asynchronous notification delivery using **Celery** and **Redis** as a message broker. Supports email, SMS, and push channels. Includes a minimal live UI to observe task processing in real time.

---

## How it works

1. Client sends `POST /notifications/` with channel, recipient, and content
2. The API saves the record to PostgreSQL with status `pending` and immediately returns a response
3. A Celery worker picks up the task from the Redis queue and processes it in the background
4. Status is updated to `retrying`, `sent`, or `failed` depending on the result
5. The UI polls `GET /notifications/` every 3 seconds and reflects current statuses without page reload

```
Client → FastAPI → PostgreSQL
                ↓
              Redis (broker)
                ↓
           Celery Worker → updates status in PostgreSQL
```

---

## Stack

| Layer | Technology |
|---|---|
| API | [FastAPI](https://fastapi.tiangolo.com/) |
| Database | [PostgreSQL 15](https://www.postgresql.org/) + [SQLAlchemy 2.0](https://docs.sqlalchemy.org/) |
| Queue broker | [Redis 7](https://redis.io/) |
| Task queue | [Celery 5](https://docs.celeryq.dev/) |
| Templates | [Jinja2](https://jinja.palletsprojects.com/) |
| Containerization | [Docker](https://www.docker.com/) + Docker Compose |

---

## Project structure

```
app/
├── api/endpoints/
│   ├── notifications.py   # REST API routes
│   └── ui.py              # Jinja2 UI routes
├── core/
│   └── config.py          # Centralized config with startup validation
├── db/
│   ├── database.py        # SQLAlchemy engine and session
│   └── init_db.py         # DB initialization with retry logic
├── models/
│   └── notification.py    # Notification ORM model
├── schemas/
│   └── notification.py    # Pydantic schemas + Channel enum
├── services/
│   └── notification_service.py  # Business logic
└── tasks/
    ├── celery_app.py       # Celery configuration
    └── notification_tasks.py    # Async task with retry logic
templates/
└── index.html             # Live status UI
```

---

## Getting started

### Prerequisites

- [Docker](https://www.docker.com/) and Docker Compose

### 1. Clone and configure

```bash
git clone https://github.com/andriisyniuchenko/notification-service
cd notification-service
cp .env.example .env
```

### 2. Start all services

```bash
make up
```

This starts 4 containers: `web` (FastAPI), `worker` (Celery), `db` (PostgreSQL), `redis` (Redis).

### 3. Open the UI

```
http://localhost:8000
```

### 4. Open API docs

```
http://localhost:8000/docs
```

---

## Make commands

| Command | Description |
|---|---|
| `make up` | Build and start all containers in background |
| `make down` | Stop all containers |
| `make logs` | Follow logs from all containers |
| `make rebuild` | Full stop, volume wipe, and rebuild |
| `make reset` | Stop containers and remove volumes |
| `make run` | Run FastAPI locally without Docker |
| `make freeze` | Update requirements.txt from current venv |

---

## API

### `POST /notifications/`

Create a notification and queue it for delivery.

**Request body:**
```json
{
  "channel": "email",
  "recipient": "user@example.com",
  "content": "Hello!"
}
```

`channel` accepts: `email`, `sms`, `push`

**Response:**
```json
{
  "id": 1,
  "channel": "email",
  "recipient": "user@example.com",
  "content": "Hello!",
  "status": "pending",
  "created_at": "2026-04-07T22:00:00"
}
```

### `GET /notifications/`

Returns all notifications ordered by creation time descending.

---

## Retry logic

The Celery task retries up to **3 times** with a **5-second delay** between attempts.

| Status | Meaning |
|---|---|
| `pending` | Queued, not yet picked up |
| `retrying` | Failed, retrying |
| `sent` | Successfully delivered |
| `failed` | All retry attempts exhausted |

A 10% simulated failure rate is intentionally included to demonstrate the retry behavior live.

---

## Environment variables

| Variable | Example | Description |
|---|---|---|
| `DATABASE_URL` | `postgresql://postgres:postgres@db:5432/notifications` | PostgreSQL connection string |
| `REDIS_URL` | `redis://redis:6379/0` | Redis connection string |