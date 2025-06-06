from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import UserModel


class UsersRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_email(self, email: str) -> UserModel | None:
        user = await self.db.execute(select(UserModel).where(UserModel.email == email))

        return user.scalar_one_or_none()

    async def create(self, data: dict) -> UserModel:
        user = UserModel(**data)

        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)

        return user