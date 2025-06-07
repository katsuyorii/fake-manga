from fastapi import Response

from core.utils.jwt import create_jwt_token
from core.utils.templates import env
from src.settings import jwt_settings

from datetime import timedelta


def create_verify_email_message(user_id: int) -> str:
    verify_token = create_jwt_token(payload={'sub': str(user_id)}, expire_delta=timedelta(minutes=30))
    message = render_verify_email_message_html(verify_token)

    return message

def render_verify_email_message_html(token: str) -> str:
    template = env.get_template("verify_email.html")
    verify_link = f"http://127.0.0.1:8000/auth/email-verify?token={token}"
    
    return template.render(verify_link=verify_link)