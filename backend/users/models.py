from sqlalchemy import text, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from enum import Enum

from core.models.base import BaseModel


class UserRoleEnum(str, Enum):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'

class UserModel(BaseModel):
    __tablename__ = 'users'

    email: Mapped[str] = mapped_column(unique=True, index=True)
    password: Mapped[str]

    first_name: Mapped[str] = mapped_column(nullable=True)
    last_name: Mapped[str] = mapped_column(nullable=True)
    phone_number: Mapped[str] = mapped_column(String(20), unique=True, nullable=True)
    role: Mapped[UserRoleEnum] = mapped_column(default=UserRoleEnum.USER, index=True)

    is_active: Mapped[bool] = mapped_column(default=True)
    is_verified: Mapped[bool] = mapped_column(default=False)
    is_mailing: Mapped[bool] = mapped_column(default=True)

    addresses = relationship("UserAddress", back_populates="user", cascade="all, delete-orphan")

class UserAddress(BaseModel):
    __tablename__ = 'users_addresses'

    city: Mapped[str]
    street: Mapped[str]
    flat: Mapped[int]
    entrance: Mapped[int] = mapped_column(nullable=True)
    floot: Mapped[int] = mapped_column(nullable=True)
    intercom: Mapped[str] = mapped_column(nullable=True)

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    user = relationship('UserModel', back_populates='addresses')