from fastapi import Depends

from redis.asyncio import Redis

from users.repositories import UsersRepository
from users.dependencies import get_users_repository
from core.dependencies.redis import get_redis

from .services import AuthService, TokenBlacklistService, TokenService


async def get_token_service() -> TokenService:
    return TokenService()

async def get_token_blacklist_service(redis: Redis = Depends(get_redis)) -> TokenBlacklistService:
    return TokenBlacklistService(redis)

async def get_auth_service(user_repository: UsersRepository = Depends(get_users_repository), token_blacklist_service: TokenBlacklistService = Depends(get_token_blacklist_service), token_service: TokenService = Depends(get_token_service)) -> AuthService:
    return AuthService(user_repository, token_blacklist_service, token_service)