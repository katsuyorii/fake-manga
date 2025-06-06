from pydantic import BaseModel, EmailStr, field_validator

from core.utils.validators import validate_password_strength


class AccessTokenResponseSchema(BaseModel):
    access_token: str
    type: str = 'bearer'

class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str

class UserRegistrationSchema(UserLoginSchema):
    @field_validator('password')
    @classmethod
    def validate_password(cls, value: str) -> str:
        return validate_password_strength(value)
