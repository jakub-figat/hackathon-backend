import datetime as dt
import re
from typing import Optional
from uuid import UUID

from pydantic.class_validators import validator
from pydantic.fields import Field
from pydantic.networks import EmailStr

from src.schemas.base import BaseModel


class UserRegisterSchema(BaseModel):
    email: EmailStr
    date_of_birth: dt.date
    password: str = Field(..., min_length=8, max_length=35)
    first_name: str
    last_name: str

    @validator("date_of_birth")
    def validate_date_of_birth(cls, date_of_birth: dt.date) -> dt.date:
        if not dt.date(1900, 1, 1) <= date_of_birth <= dt.date.today():
            raise ValueError("Invalid date of birth")

        return date_of_birth


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=35)


class PasswordChangeSchema(BaseModel):
    password: str


class UserUpdateSchema(BaseModel):
    date_of_birth: dt.date
    first_name: str
    last_name: str
    phone_number: Optional[str]

    @validator("date_of_birth")
    def validate_date_of_birth(cls, date_of_birth: dt.date) -> dt.date:
        if not dt.date(1900, 1, 1) <= date_of_birth <= dt.date.today():
            raise ValueError("Invalid date of birth")

        return date_of_birth

    @validator("phone_number")
    def phone_validation(cls, v):
        if v is None:
            return v

        regex = r"^(\+)[1-9][0-9\-\(\)\.]{9,15}$"
        if not re.search(regex, v, re.I):
            raise ValueError("Phone Number Invalid.")
        return v


class UserResponseSchema(BaseModel):
    id: UUID
    email: EmailStr
    date_of_birth: dt.date
    first_name: str
    last_name: str
    phone_number: Optional[str]
