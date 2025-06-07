from fastapi import Response, Request

from redis.asyncio import Redis

from datetime import datetime, timezone, timedelta

from core.utils.passwords import hashing_password
from core.utils.exceptions import EmailAlreadyRegistered

from users.repositories import UsersRepository
from core.utils.jwt import verify_jwt_token, create_jwt_token
from core.utils.exceptions import AccountMissing
from core.utils.passwords import verify_password
from src.settings import jwt_settings

from .schemas import UserRegistrationSchema, UserLoginSchema, AccessTokenResponseSchema
from .tasks import send_email_task
from .utils import create_verify_email_message
from .exceptions import AccountInactive, AccountNotVerify, IncorrectLoginOrPassword, TokenMissing, TokenInvalid


class TokenBlacklistService:
    def __init__(self, redis: Redis):
        self.redis = redis
    
    async def add_to_blacklist(self, payload: dict, token: str) -> None:
        key = f'blacklist:{token}'
        expire_token = payload.get('exp')
        datetime_now = int(datetime.now(timezone.utc).timestamp())
        ttl = expire_token - datetime_now
        
        await self.redis.set(key, 'true', ex=ttl)
    
    async def is_blacklisted(self, token: str) -> bool:
        return await self.redis.exists(f'blacklist:{token}')
    
class TokenService:
    def create_access_token(self, payload: dict, response: Response) -> str:
        access_token = create_jwt_token(payload, timedelta(minutes=jwt_settings.ACCESS_TOKEN_EXPIRE_MINUTES))
        self._set_jwt_cookies(response, 'access_token', access_token, jwt_settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60)

        return access_token

    def create_refresh_token(self, payload: dict, response: Response) -> str:
        refresh_token = create_jwt_token(payload, timedelta(days=jwt_settings.REFRESH_TOKEN_EXPIRE_DAYS))
        self._set_jwt_cookies(response, 'refresh_token', refresh_token, jwt_settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60)

        return refresh_token

    def _set_jwt_cookies(self, response: Response, key: str, value: str, max_age: int) -> None:
        response.set_cookie(
            key=key,
            value=value,
            max_age=max_age,
            secure=True,
            httponly=True,
            samesite='strict',
        )

class AuthService:
    def __init__(self, user_repository: UsersRepository, token_blacklist_service: TokenBlacklistService, token_service: TokenService):
        self.user_repository = user_repository
        self.token_blacklist_service = token_blacklist_service
        self.token_service = token_service

    async def registration(self, user_data: UserRegistrationSchema):
        user = await self.user_repository.get_by_email(user_data.email)

        if user is not None:
            raise EmailAlreadyRegistered()

        user_data_dict = user_data.model_dump()

        user_data_dict['password'] = hashing_password(user_data_dict.get('password'))

        new_user = await self.user_repository.create(user_data_dict)

        message = create_verify_email_message(new_user.id)

        send_email_task.delay(
        new_user.email,
        "Подтверждение учетной записи",
        message
        )

        return {'message': 'Письмо с подтверждением отправлено на почту!'}
    
    async def authentication(self, user_data: UserLoginSchema, response: Response) -> AccessTokenResponseSchema:
        user = await self.user_repository.get_by_email(user_data.email)

        if not user or not verify_password(user_data.password, user.password):
            raise IncorrectLoginOrPassword()
        
        if not user.is_active:
            raise AccountInactive()
        
        if not user.is_verified:
            raise AccountNotVerify()
        
        access_token = self.token_service.create_access_token({'sub': str(user.id), 'role': user.role}, response)
        self.token_service.create_refresh_token({'sub': str(user.id)}, response)

        return AccessTokenResponseSchema(access_token=access_token)

    async def logout(self, request: Request, response: Response):
        refresh_token = request.cookies.get('refresh_token')

        if not refresh_token:
            raise TokenMissing()
        
        payload = verify_jwt_token(token=refresh_token)

        await self.token_blacklist_service.add_to_blacklist(payload, refresh_token)

        response.delete_cookie(key='access_token')
        response.delete_cookie(key='refresh_token')

        return {'message': 'Вы успешно вышли из системы!'}
    
    async def refresh(self, request: Request, response: Response) -> AccessTokenResponseSchema:
        refresh_token = request.cookies.get('refresh_token')

        if not refresh_token:
            raise TokenMissing()
        
        if await self.token_blacklist_service.is_blacklisted(refresh_token):
            raise TokenInvalid()

        payload = verify_jwt_token(refresh_token)
        user_id = int(payload.get('sub'))

        user = await self.user_repository.get_by_id(user_id)

        if not user:
            raise AccountMissing()
        
        if not user.is_active:
            raise AccountInactive()

        access_token = self.token_service.create_access_token({'sub': str(user_id), 'role': user.role}, response)
        self.token_service.create_refresh_token({'sub': str(user_id)}, response)

        await self.token_blacklist_service.add_to_blacklist(payload, refresh_token)

        return AccessTokenResponseSchema(access_token=access_token)
    
    async def verify_email(self, token: str):
        payload = verify_jwt_token(token)
        user_id = int(payload.get('sub'))

        user = await self.user_repository.get_by_id(user_id)

        if not user:
            raise AccountMissing()

        if not user.is_active:
            raise AccountInactive()

        if user.is_verified:
            return {'message': 'Учетная запись уже активирована!'}
        
        await self.user_repository.verify_email(user)

        return {'message': 'Учетная запись успешно активирована!'}