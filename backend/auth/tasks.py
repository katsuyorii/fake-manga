import asyncio

from src.celery import celery_app
from core.utils.email import async_send_email


@celery_app.task
def send_email_task(to_email: str, subject: str, body: str) -> None:
    asyncio.run(async_send_email(to_email, subject, body))