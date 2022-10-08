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

    def to_orm_kwargs(self) -> dict[str, Any]:
        return {
            "email": self.email,
            "password": self.password,
            "date_of_birth": self.date_of_birth,
            "first_name": self.first_name,
            "last_name": self.last_name,
        }


class UserUpdateSchema(BaseInputSchema):
    date_of_birth: dt.date
    first_name: str
    last_name: str
    phone_number: Optional[str]

    def to_orm_kwargs(self) -> dict[str, Any]:
        return self.dict()


class UserSchema(BaseModel):
    id: UUID
    email: str
    password: str
    date_of_birth: dt.date
    first_name: str
    last_name: str
    phone_number: Optional[str]
