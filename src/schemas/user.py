import datetime as dt
from typing import Any
from uuid import UUID

from pydantic.class_validators import validator
from pydantic.fields import Field
from pydantic.main import BaseModel
from pydantic.networks import EmailStr

from src.utils.schemas import BaseInputSchema


class UserInputSchema(BaseInputSchema):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=35)
    date_of_birth: dt.date

    @validator("date_of_birth")
    def validate_date_of_birth(cls, date_of_birth: dt.date) -> dt.date:
        if not dt.date(1900, 1, 1) <= date_of_birth <= dt.date.today():
            raise ValueError("Invalid date of birth")

        return date_of_birth

    def to_orm_kwargs(self) -> dict[str, Any]:
        return {"email": self.email, "password": self.password, "date_of_birth": self.date_of_birth}


class UserRegisterSchema(UserInputSchema):
    password_2: str = Field(..., min_length=8, max_length=35)

    @validator("password_2")
    def validate_passwords(cls, password_2: str, values: dict[str, Any]) -> str:
        if password_2 != values["password"]:
            raise ValueError("Passwords do not match")

        return password_2


class UserSchema(BaseModel):
    id: UUID
    email: str
    date_of_birth: dt.date

    class Config:
        orm_mode = True
