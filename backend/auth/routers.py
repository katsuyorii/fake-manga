from fastapi import APIRouter, Depends, status, Response

from .services import AuthService
from .schemas import UserRegistrationSchema, UserLoginSchema, AccessTokenResponseSchema
from .dependencies import get_auth_service


auth_router = APIRouter(
    prefix='/auth',
    tags=['Auth'],
)

@auth_router.post('/registration', status_code=status.HTTP_201_CREATED)
async def registration_user(user_data: UserRegistrationSchema, auth_service: AuthService = Depends(get_auth_service)):
    return await auth_service.registration(user_data)

@auth_router.post('/login', response_model=AccessTokenResponseSchema)
async def login_user(user_data: UserLoginSchema, response: Response, auth_service: AuthService = Depends(get_auth_service)):
    return await auth_service.authentication(user_data, response)

@auth_router.get('/email-verify')
async def verify_email_user(token: str, auth_service: AuthService = Depends(get_auth_service)):
    return await auth_service.verify_email(token)
