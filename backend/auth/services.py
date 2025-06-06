from fastapi import Response

from core.utils.passwords import hashing_password
from core.utils.exceptions import EmailAlreadyRegistered

from users.repositories import UsersRepository
from core.utils.jwt import verify_jwt_token
from core.utils.exceptions import AccountMissing
from core.utils.passwords import verify_password

from .schemas import UserRegistrationSchema, UserLoginSchema, AccessTokenResponseSchema
from .tasks import send_email_task
from .utils import create_verify_email_message, create_access_token, create_refresh_token
from .exceptions import AccountInactive, AccountNotVerify, IncorrectLoginOrPassword


class AuthService:
    def __init__(self, user_repository: UsersRepository):
        self.user_repository = user_repository

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
    
    async def authentication(self, user_data: UserLoginSchema, response: Response) -> AccessTokenResponseSchema:
        user = await self.user_repository.get_by_email(user_data.email)

        if not user or not verify_password(user_data.password, user.password):
            raise IncorrectLoginOrPassword()
        
        if not user.is_active:
            raise AccountInactive()
        
        if not user.is_verified:
            raise AccountNotVerify()
        
        access_token = create_access_token({'sub': str(user.id), 'role': user.role}, response)
        create_refresh_token({'sub': str(user.id)}, response)

        return AccessTokenResponseSchema(access_token=access_token)