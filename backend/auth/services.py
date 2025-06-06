from core.utils.passwords import hashing_password
from core.utils.exceptions import EmailAlreadyRegistered

from users.repositories import UsersRepository

from .schemas import UserRegistrationSchema


class AuthService:
    def __init__(self, user_repository: UsersRepository):
        self.user_repository = user_repository

    async def registration(self, user_data: UserRegistrationSchema):
        user = await self.user_repository.get_by_email(user_data.email)

        if user is not None:
            raise EmailAlreadyRegistered()

        user_data_dict = user_data.model_dump()

        user_data_dict['password'] = hashing_password(user_data_dict.get('password'))

        await self.user_repository.create(user_data_dict)

        return {'message': 'Письмо с подтверждением отправлено на почту!'}