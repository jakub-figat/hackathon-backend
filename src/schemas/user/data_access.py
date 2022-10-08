import datetime as dt
from typing import (
    Any,
    Optional,
)
from uuid import UUID

from pydantic import EmailStr

from src.schemas.base import BaseModel
from src.utils.schemas import BaseInputSchema


class UserInputSchema(BaseInputSchema):
    email: EmailStr
    password: str
    date_of_birth: dt.date
    first_name: str
    last_name: str
    is_verified: bool

    def to_orm_kwargs(self) -> dict[str, Any]:
        return self.dict()


class UserUpdateSchema(BaseInputSchema):
    date_of_birth: dt.date
    first_name: str
    last_name: str
    phone_number: Optional[str]
    otp_code: Optional[int]
    otp_code_issued_at: Optional[dt.datetime]
    is_verified: bool

    def to_orm_kwargs(self) -> dict[str, Any]:
        return self.dict()


class UserSchema(BaseModel):
    id: UUID
    email: str
    password: str
    date_of_birth: dt.date
    first_name: str
    last_name: str
    is_verified: bool
    phone_number: Optional[str]
    otp_code: Optional[int]
    otp_code_issued_at: Optional[dt.datetime]
