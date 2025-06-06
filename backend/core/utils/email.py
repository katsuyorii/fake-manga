import aiosmtplib

from email.message import EmailMessage

from src.settings import smtp_settings


async def async_send_email(to_email: str, subject: str, body: str) -> None:
    message = EmailMessage()
    message["From"] = smtp_settings.SMTP_USER
    message["To"] = to_email
    message["Subject"] = subject
    message.add_alternative(body, subtype="html")

    await aiosmtplib.send(
        message,
        hostname=smtp_settings.SMTP_HOST,
        port=smtp_settings.SMTP_PORT,
        start_tls=True,
        username=smtp_settings.SMTP_USER,
        password=smtp_settings.SMTP_PASSWORD,
    )
