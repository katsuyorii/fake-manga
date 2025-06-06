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

def create_access_token(payload: dict, response: Response) -> str:
    access_token = create_jwt_token(payload, timedelta(minutes=jwt_settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    set_jwt_cookies(response, 'access_token', access_token, jwt_settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60)

    return access_token

def create_refresh_token(payload: dict, response: Response) -> str:
    refresh_token = create_jwt_token(payload, timedelta(days=jwt_settings.REFRESH_TOKEN_EXPIRE_DAYS))
    set_jwt_cookies(response, 'refresh_token', refresh_token, jwt_settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60)

    return refresh_token

def set_jwt_cookies(response: Response, key: str, value: str, max_age: int) -> None:
    response.set_cookie(
        key=key,
        value=value,
        max_age=max_age,
        secure=True,
        httponly=True,
        samesite='strict',
    )