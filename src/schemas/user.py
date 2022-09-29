import datetime as dt
from typing import Any

from pydantic.class_validators import validator
from pydantic.fields import Field
from pydantic.main import BaseModel
from pydantic.networks import EmailStr


class UserRegisterSchema(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=35)
    password_2: str = Field(..., min_length=8, max_length=35)
    date_of_birth: dt.datetime

    def to_orm_kwargs(self) -> dict[str, Any]:
        kwargs = self.dict()
        kwargs.pop("password_2")

        return kwargs

    @validator("password_2")
    def validate_passwords(cls, password_2: str, values: dict[str, Any]) -> str:
        if password_2 != values["password"]:
            raise ValueError("Passwords do not match")

        return password_2

    @validator("date_of_birth")
    def validate_date_of_birth(cls, date_of_birth: dt.datetime) -> dt.datetime:
        if dt.datetime(1900, 1, 1) <= date_of_birth <= dt.datetime.now():
            raise ValueError("Invalid date of birth")

        return date_of_birth


class UserSchema(BaseModel):
    email: str
    date_of_birth: dt.datetime

    class Config:
        orm_mode = True
