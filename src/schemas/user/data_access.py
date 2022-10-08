import datetime as dt
from typing import Any
from uuid import UUID

from pydantic import (
    EmailStr,
    validator,
)

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

    def to_orm_kwargs(self) -> dict[str, Any]:
        return {"first_name": self.first_name, "last_name": self.last_name, "date_of_birth": self.date_of_birth}


class UserSchema(BaseModel):
    id: UUID
    email: str
    password: str
    date_of_birth: dt.date
    first_name: str
    last_name: str
    image: str | None = None
