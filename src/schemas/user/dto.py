import datetime as dt
from typing import Any
from uuid import UUID

from pydantic import BaseModel
from pydantic.class_validators import validator
from pydantic.fields import Field
from pydantic.networks import EmailStr


class UserRegisterSchema(BaseModel):
    email: EmailStr
    date_of_birth: dt.date
    password: str
    password_2: str = Field(..., min_length=8, max_length=35)

    @validator("password_2")
    def validate_passwords(cls, password_2: str, values: dict[str, Any]) -> str:
        if password_2 != values["password"]:
            raise ValueError("Passwords do not match")

        return password_2


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=35)


class UserResponseSchema(BaseModel):
    id: UUID
    email: EmailStr
    date_of_birth: dt.date
