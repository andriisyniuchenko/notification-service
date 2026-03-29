from app.tasks.celery_app import celery


@celery.task(name="app.tasks.notification_tasks.send_notification_task")
def send_notification_task(notification_id: int):
    print(f"🔥 Sending notification {notification_id}")