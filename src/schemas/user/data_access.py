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

    @validator("date_of_birth")
    def validate_date_of_birth(cls, date_of_birth: dt.date) -> dt.date:
        if not dt.date(1900, 1, 1) <= date_of_birth <= dt.date.today():
            raise ValueError("Invalid date of birth")

        return date_of_birth

    def to_orm_kwargs(self) -> dict[str, Any]:
        return {"email": self.email, "password": self.password, "date_of_birth": self.date_of_birth}


class UserSchema(BaseModel):
    id: UUID
    email: str
    password: str
    date_of_birth: dt.date
