import datetime as dt
from uuid import UUID

from pydantic.fields import Field
from pydantic.networks import EmailStr

from src.schemas.base import BaseModel


class UserRegisterSchema(BaseModel):
    email: EmailStr
    date_of_birth: dt.date
    password: str = Field(..., min_length=8, max_length=35)


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=35)


class UserResponseSchema(BaseModel):
    id: UUID
    email: EmailStr
    date_of_birth: dt.date
