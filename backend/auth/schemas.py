from pydantic import BaseModel, EmailStr, field_validator

from core.utils.validators import validate_password_strength


class UserRegistrationSchema(BaseModel):
    email: EmailStr
    password: str

    @field_validator('password')
    @classmethod
    def validate_password(cls, value: str) -> str:
        return validate_password_strength(value)