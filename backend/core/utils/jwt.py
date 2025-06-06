import jwt

from fastapi import HTTPException, status

from datetime import timedelta, timezone, datetime

from src.settings import jwt_settings


def create_jwt_token(payload: dict, expire_delta: timedelta) -> str:
    to_encode = payload.copy()
    iat = datetime.now(timezone.utc)
    exp = iat + expire_delta
    to_encode.update({'exp': exp, 'iat': iat})

    jwt_token = jwt.encode(
        payload=to_encode,
        key=jwt_settings.SECRET_KEY,
        algorithm=jwt_settings.ALGORITHM
    )

    return jwt_token

def verify_jwt_token(token: str) -> dict:
    try:
        payload = jwt.decode(
            jwt=token,
            key=jwt_settings.SECRET_KEY,
            algorithms=[jwt_settings.ALGORITHM]
        )
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token expired')
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid token')
    
    return payload