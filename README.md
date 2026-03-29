# Notification Service

Simple backend service for *sending notifications* (email, SMS, push).

## Stack
- FastAPI
- PostgreSQL
- Redis
- Celery
- Docker

## Setup

```bash
git clone https://github.com/andriisyniuchenko/notification-service
cd notification-service
cp .env.example .env
```

## Run

### Local
```bash
uvicorn app.main:app --reload
```

### Docker
```bash
make up
```

## API Docs

http://localhost:8000/docs
